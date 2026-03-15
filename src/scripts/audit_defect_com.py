from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import torch

from src.core.checkpoints import save_checkpoint
from src.core.config import load_json_config
from src.core.io import collect_runtime_info, dump_json, ensure_dir
from src.experiments.common import build_solver, prepare_relaxed_state, serializable_diag
from src.physics.background_sources import StaticCentralBackground
from src.physics.com_audit import fit_ballistic_trajectory, fit_constant_acceleration_trajectory
from src.physics.defects import displace_and_boost_state
from src.physics.diagnostics import snapshot_diagnostics, summarize_orbit_run


def run_audit(
    config_path: str | Path,
    output_dir: str | Path,
    scenario: str,
    steps_override: int | None = None,
    velocity_scale_override: float | None = None,
) -> Path:
    config = load_json_config(config_path)
    seed = int(config["seed"])
    np.random.seed(seed)
    torch.manual_seed(seed)

    output_path = ensure_dir(output_dir, overwrite=True)
    dump_json(output_path / "config.json", config)
    dump_json(output_path / "runtime.json", collect_runtime_info(seed))
    solver, projection_kernel = build_solver(config)
    rho0 = float(config["geometry"]["reference_rho"])
    state = prepare_relaxed_state(solver=solver, config=config, rho_ambient=rho0)
    reference_modes = state.psi_modes.clone()

    background: StaticCentralBackground | None = None
    external_potential = None
    background_center = torch.zeros(3, device=solver.grid.device, dtype=solver.grid.real_dtype)
    if scenario in {"source_no_dressing", "source_with_dressing"}:
        background = StaticCentralBackground.from_config(config["background"], rho_reference=rho0)
        external_potential = background.potential_field(solver.grid).to(solver.grid.real_dtype)
        background_center = torch.tensor(background.center, device=solver.grid.device, dtype=solver.grid.real_dtype)

    dt = float(config["solver"]["dt"])
    steps = int(steps_override if steps_override is not None else config["experiment"]["orbit_steps"])
    total_time = steps * dt
    checkpoint_every = int(config["solver"].get("checkpoint_every", 0))

    displacement = (float(config["experiment"]["periapsis_radius"]), 0.0, 0.0)
    tangential_speed = 0.0
    velocity_scale = float(
        velocity_scale_override if velocity_scale_override is not None else config["experiment"].get("velocity_scale", 1.0)
    )
    if scenario in {"free_translation", "source_no_dressing", "source_with_dressing"}:
        if background is None:
            mu = float(config["background"]["mu"])
            periapsis_radius = float(config["experiment"]["periapsis_radius"])
            base_speed = np.sqrt(mu / periapsis_radius) * velocity_scale
            max_safe_speed = 0.15 * min(solver.grid.length) / max(total_time, 1.0e-12)
            tangential_speed = min(base_speed, max_safe_speed)
        else:
            tangential_speed = background.periapsis_speed(
                float(config["experiment"]["periapsis_radius"]),
                float(config["experiment"]["eccentricity"]),
            ) * velocity_scale
    state = displace_and_boost_state(
        solver=solver,
        state=state,
        shift=displacement,
        momentum=(0.0, solver.mass * tangential_speed, 0.0),
    )
    save_checkpoint(
        output_path / "checkpoint_inserted.npz",
        {
            "psi_modes": state.psi_modes,
            "time": state.time,
            "step": state.step,
            "a": state.a,
            "rho_ambient": state.rho_ambient,
        },
    )

    trajectory_time: list[float] = []
    trajectory_position: list[list[float]] = []
    a_history: list[float] = []
    ambient_density_history: list[float] = []
    leakage_history: list[float] = []
    higher_mode_history: list[float] = []
    coherence_history: list[float] = []
    compactness_history: list[float] = []
    continuity_history: list[float] = []
    orbit_log: list[dict[str, Any]] = []

    fit_start_index = int(config["experiment"].get("fit_start_index", 0))
    previous_diag: dict[str, Any] | None = None
    for _ in range(steps):
        center = solver.estimate_defect_center(state.psi_modes)
        if scenario == "source_with_dressing" and background is not None:
            rho_ambient = float(background.ambient_density_at_position(center.detach().cpu().tolist()))
        else:
            rho_ambient = rho0
        state = solver.step(
            state,
            dt=dt,
            rho_ambient=rho_ambient,
            external_potential=external_potential,
        )
        diag = snapshot_diagnostics(
            solver=solver,
            state=state,
            projection_kernel=projection_kernel,
            reference_modes=reference_modes,
            bound_radius_factor=float(config["experiment"]["bound_radius_factor"]),
            previous_snapshot=previous_diag,
        )
        previous_diag = diag
        orbit_log.append(serializable_diag(diag))
        trajectory_time.append(float(state.time))
        trajectory_position.append(list(diag["center_of_mass"]))
        a_history.append(float(state.a))
        ambient_density_history.append(float(rho_ambient))
        leakage_history.append(float(diag["mean_S_leak"]))
        higher_mode_history.append(float(diag["higher_mode_fraction"]))
        coherence_history.append(float(diag["coherence"]))
        compactness_history.append(float(diag["radius_of_gyration"]))
        continuity_history.append(float(diag["continuity_residual_l2"]))

        if checkpoint_every > 0 and state.step % checkpoint_every == 0:
            save_checkpoint(
                output_path / f"checkpoint_orbit_step_{state.step:05d}.npz",
                {
                    "psi_modes": state.psi_modes,
                    "time": state.time,
                    "step": state.step,
                    "a": state.a,
                    "rho_ambient": state.rho_ambient,
                },
            )

    time = np.asarray(trajectory_time, dtype=np.float64)
    positions = np.asarray(trajectory_position, dtype=np.float64)
    ballistic = fit_ballistic_trajectory(time, positions)
    accelerated = fit_constant_acceleration_trajectory(time, positions)

    orbit_summary = None
    orbit_fit_error = None
    if background is not None:
        try:
            orbit_summary = summarize_orbit_run(
                time=time,
                positions=positions,
                leakage=np.asarray(leakage_history, dtype=np.float64),
                higher_mode_fraction=np.asarray(higher_mode_history, dtype=np.float64),
                coherence_series=np.asarray(coherence_history, dtype=np.float64),
                compactness=np.asarray(compactness_history, dtype=np.float64),
                continuity_residual=np.asarray(continuity_history, dtype=np.float64),
                mu=background.mu,
                c_eff=background.c_eff,
                fit_start_index=fit_start_index,
                turning_point_min_spacing=int(config["experiment"].get("turning_point_min_spacing", 1)),
                turning_point_smooth_window=int(config["experiment"].get("turning_point_smooth_window", 1)),
            )
        except ValueError as exc:
            orbit_fit_error = str(exc)

    source_radius = np.linalg.norm(positions - background_center.detach().cpu().numpy()[None, :], axis=1)
    summary = {
        "scenario": scenario,
        "ballistic_fit": ballistic,
        "constant_acceleration_fit": accelerated,
        "mean_coherence": float(np.mean(coherence_history[fit_start_index:])),
        "mean_higher_mode_fraction": float(np.mean(higher_mode_history[fit_start_index:])),
        "mean_leakage": float(np.mean(leakage_history[fit_start_index:])),
        "mean_compactness": float(np.mean(compactness_history[fit_start_index:])),
        "mean_continuity_residual": float(np.mean(continuity_history[fit_start_index:])),
        "ambient_density_span": [
            float(np.min(ambient_density_history)),
            float(np.max(ambient_density_history)),
        ],
        "a_span": [
            float(np.min(a_history)),
            float(np.max(a_history)),
        ],
        "mean_source_radius": float(np.mean(source_radius)),
        "initial_tangential_speed": float(tangential_speed),
        "final_snapshot": orbit_log[-1],
    }
    if orbit_summary is not None:
        summary["orbit_summary"] = orbit_summary
    if orbit_fit_error is not None:
        summary["orbit_fit_error"] = orbit_fit_error

    dump_json(Path(output_path) / "summary.json", summary)
    save_checkpoint(
        output_path / "checkpoint_final.npz",
        {
            "psi_modes": state.psi_modes,
            "time": state.time,
            "step": state.step,
            "a": state.a,
            "rho_ambient": state.rho_ambient,
        },
    )
    np.savez_compressed(
        Path(output_path) / "timeseries.npz",
        time=time,
        position=positions,
        a=np.asarray(a_history, dtype=np.float64),
        rho_ambient=np.asarray(ambient_density_history, dtype=np.float64),
        coherence=np.asarray(coherence_history, dtype=np.float64),
        higher_mode_fraction=np.asarray(higher_mode_history, dtype=np.float64),
        mean_S_leak=np.asarray(leakage_history, dtype=np.float64),
        radius_of_gyration=np.asarray(compactness_history, dtype=np.float64),
        continuity_residual_l2=np.asarray(continuity_history, dtype=np.float64),
    )
    plain_language = [
        f"COM audit summary for scenario '{scenario}':",
        f"- ballistic RMS residual = {summary['ballistic_fit']['rms_residual']:.6e}",
        f"- fitted acceleration norm = {summary['constant_acceleration_fit']['acceleration_norm']:.6e}",
        f"- mean coherence = {summary['mean_coherence']:.6f}",
        f"- mean higher-mode fraction = {summary['mean_higher_mode_fraction']:.6e}",
        f"- mean leakage = {summary['mean_leakage']:.6e}",
    ]
    if orbit_summary is not None:
        plain_language.append(f"- beta_eff = {orbit_summary['beta_eff']:.6f}")
        plain_language.append(f"- Delta phi = {orbit_summary['delta_phi']:.6f}")
    elif orbit_fit_error is not None:
        plain_language.append(f"- orbit fit failed: {orbit_fit_error}")
    (output_path / "plain_language_summary.txt").write_text("\n".join(plain_language) + "\n", encoding="utf-8")
    assumptions = [
        "The defect is represented by the reduced matter-only split-step solver with co-moving internal confinement.",
        "The audit omits live Maxwell, free-heavy recoil, and isolated Poisson boundary handling.",
        "Source-present audits use the imposed static background from the supplied experiment config.",
    ]
    (output_path / "unresolved_assumptions.txt").write_text("\n".join(assumptions) + "\n", encoding="utf-8")
    return Path(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit defect COM motion for null-force and source-only scenarios")
    parser.add_argument("--config", required=True, help="Experiment config path")
    parser.add_argument("--output-dir", required=True, help="Directory for audit outputs")
    parser.add_argument(
        "--scenario",
        required=True,
        choices=["free_translation", "displaced_rest", "source_no_dressing", "source_with_dressing"],
        help="Audit scenario to execute",
    )
    parser.add_argument("--steps", type=int, default=None, help="Optional override for the audit step count")
    parser.add_argument("--velocity-scale", type=float, default=None, help="Optional override for the launch velocity scale")
    args = parser.parse_args()

    output_dir = run_audit(
        config_path=args.config,
        output_dir=args.output_dir,
        scenario=args.scenario,
        steps_override=args.steps,
        velocity_scale_override=args.velocity_scale,
    )
    summary = load_json_config(output_dir / "summary.json")
    print(f"scenario: {summary['scenario']}")
    print(f"ballistic_rms: {summary['ballistic_fit']['rms_residual']:.6e}")
    print(f"acceleration_norm: {summary['constant_acceleration_fit']['acceleration_norm']:.6e}")
    print(f"mean_coherence: {summary['mean_coherence']:.6f}")
    if "orbit_summary" in summary:
        print(f"beta_eff: {summary['orbit_summary']['beta_eff']:.6f}")
        print(f"delta_phi: {summary['orbit_summary']['delta_phi']:.6f}")
    elif "orbit_fit_error" in summary:
        print(f"orbit_fit_error: {summary['orbit_fit_error']}")


if __name__ == "__main__":
    main()
