from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import torch

from src.core.checkpoints import load_checkpoint, save_checkpoint
from src.core.config import load_json_config
from src.core.io import collect_runtime_info, dump_json, ensure_dir
from src.core.targets import load_reference_targets
from src.experiments.common import build_solver, clone_state, serializable_diag
from src.physics.background_sources import StaticCentralBackground
from src.physics.defects import displace_and_boost_state, gaussian_initial_modes, imaginary_time_relax
from src.physics.diagnostics import snapshot_diagnostics, summarize_orbit_run
from src.physics.observables import orbital_radius
from src.physics.matter_gnls import MatterState


def run(config_path: str | Path, restart: str | None = None) -> Path:
    config = load_json_config(config_path)
    seed = int(config["seed"])
    np.random.seed(seed)
    torch.manual_seed(seed)

    output_dir = ensure_dir(config["output_dir"], overwrite=bool(config.get("overwrite_output", False)))
    dump_json(output_dir / "config.json", config)
    dump_json(output_dir / "runtime.json", collect_runtime_info(seed))

    solver, projection_kernel = build_solver(config)
    rho0 = float(config["geometry"]["reference_rho"])
    background = StaticCentralBackground.from_config(config["background"], rho_reference=rho0)
    background_potential = background.potential_field(solver.grid).to(solver.grid.real_dtype)
    source_center = torch.tensor(background.center, device=solver.grid.device, dtype=solver.grid.real_dtype)

    if restart is not None:
        checkpoint_state = load_checkpoint(restart, device=solver.grid.device, complex_dtype=solver.complex_dtype)
        state = MatterState(
            psi_modes=checkpoint_state["psi_modes"],
            time=float(checkpoint_state["time"]),
            step=int(checkpoint_state["step"]),
            a=float(checkpoint_state["a"]),
            rho_ambient=float(checkpoint_state["rho_ambient"]),
        )
    else:
        state = gaussian_initial_modes(
            solver=solver,
            gaussian_width=config["initializer"]["gaussian_width"],
            target_norm=config["initializer"]["target_norm"],
            rho_ambient=rho0,
        )
        state = imaginary_time_relax(
            solver=solver,
            state=state,
            dtau=config["initializer"]["imaginary_dt"],
            steps=config["initializer"]["steps"],
            target_norm=config["initializer"]["target_norm"],
        )
        save_checkpoint(
            output_dir / "checkpoint_relaxed.npz",
            {
                "psi_modes": state.psi_modes,
                "time": state.time,
                "step": state.step,
                "a": state.a,
                "rho_ambient": state.rho_ambient,
            },
        )
        periapsis_radius = float(config["experiment"]["periapsis_radius"])
        eccentricity = float(config["experiment"]["eccentricity"])
        initial_speed = background.periapsis_speed(periapsis_radius, eccentricity) * float(
            config["experiment"].get("velocity_scale", 1.0)
        )
        initial_momentum = (
            0.0,
            solver.mass * initial_speed,
            0.0,
        )
        state = displace_and_boost_state(
            solver,
            state,
            shift=(periapsis_radius, 0.0, 0.0),
            momentum=initial_momentum,
        )
        save_checkpoint(
            output_dir / "checkpoint_inserted.npz",
            {
                "psi_modes": state.psi_modes,
                "time": state.time,
                "step": state.step,
                "a": state.a,
                "rho_ambient": state.rho_ambient,
            },
        )

    reference_modes = state.psi_modes.clone()
    dt = float(config["solver"]["dt"])
    checkpoint_every = int(config["solver"]["checkpoint_every"])
    bound_radius_factor = float(config["experiment"]["bound_radius_factor"])
    fit_start_index = int(config["experiment"].get("fit_start_index", 0))

    trajectory_time: list[float] = []
    trajectory_position: list[list[float]] = []
    ambient_density_history: list[float] = []
    a_history: list[float] = []
    radius_history: list[float] = []
    leakage_history: list[float] = []
    higher_mode_history: list[float] = []
    coherence_history: list[float] = []
    compactness_history: list[float] = []
    continuity_history: list[float] = []
    orbit_log: list[dict[str, Any]] = []

    previous_diag: dict[str, Any] | None = None
    for _ in range(int(config["experiment"]["orbit_steps"])):
        center = solver.estimate_defect_center(state.psi_modes)
        current_rho = background.ambient_density_at_position(center.detach().cpu().tolist())
        state = solver.step(
            state,
            dt=dt,
            rho_ambient=float(current_rho),
            external_potential=background_potential,
        )
        diag = snapshot_diagnostics(
            solver=solver,
            state=state,
            projection_kernel=projection_kernel,
            reference_modes=reference_modes,
            bound_radius_factor=bound_radius_factor,
            previous_snapshot=previous_diag,
        )
        previous_diag = diag
        orbit_log.append(serializable_diag(diag))

        center_tensor = torch.tensor(diag["center_of_mass"], device=solver.grid.device, dtype=solver.grid.real_dtype)
        trajectory_time.append(float(state.time))
        trajectory_position.append(list(diag["center_of_mass"]))
        ambient_density_history.append(float(current_rho))
        a_history.append(float(state.a))
        radius_history.append(float(orbital_radius(center_tensor, source_center)))
        leakage_history.append(float(diag["mean_S_leak"]))
        higher_mode_history.append(float(diag["higher_mode_fraction"]))
        coherence_history.append(float(diag["coherence"]))
        compactness_history.append(float(diag["radius_of_gyration"]))
        continuity_history.append(float(diag["continuity_residual_l2"]))

        if state.step % checkpoint_every == 0:
            save_checkpoint(
                output_dir / f"checkpoint_orbit_step_{state.step:05d}.npz",
                {
                    "psi_modes": state.psi_modes,
                    "time": state.time,
                    "step": state.step,
                    "a": state.a,
                    "rho_ambient": state.rho_ambient,
                },
            )

    save_checkpoint(
        output_dir / "checkpoint_final.npz",
        {
            "psi_modes": state.psi_modes,
            "time": state.time,
            "step": state.step,
            "a": state.a,
            "rho_ambient": state.rho_ambient,
        },
    )

    try:
        orbit_summary = summarize_orbit_run(
            time=np.asarray(trajectory_time, dtype=np.float64),
            positions=np.asarray(trajectory_position, dtype=np.float64),
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
        fit_error = None
    except ValueError as exc:
        orbit_summary = {
            "fit_error": str(exc),
            "fit_start_index": fit_start_index,
            "mean_fit_leakage": float(np.mean(leakage_history[fit_start_index:])),
            "mean_fit_higher_mode_fraction": float(np.mean(higher_mode_history[fit_start_index:])),
            "mean_fit_coherence": float(np.mean(coherence_history[fit_start_index:])),
            "mean_fit_compactness": float(np.mean(compactness_history[fit_start_index:])),
            "mean_fit_continuity_residual": float(np.mean(continuity_history[fit_start_index:])),
        }
        fit_error = str(exc)

    np.savez_compressed(
        output_dir / "timeseries.npz",
        time=np.asarray(trajectory_time, dtype=np.float64),
        position=np.asarray(trajectory_position, dtype=np.float64),
        rho_ambient=np.asarray(ambient_density_history, dtype=np.float64),
        a=np.asarray(a_history, dtype=np.float64),
        orbital_radius=np.asarray(radius_history, dtype=np.float64),
        mean_S_leak=np.asarray(leakage_history, dtype=np.float64),
        higher_mode_fraction=np.asarray(higher_mode_history, dtype=np.float64),
        coherence=np.asarray(coherence_history, dtype=np.float64),
        radius_of_gyration=np.asarray(compactness_history, dtype=np.float64),
        continuity_residual_l2=np.asarray(continuity_history, dtype=np.float64),
    )

    targets = load_reference_targets()
    summary = {
        "run_name": config["run_name"],
        "targets": targets,
        "background": {
            "profile": background.profile,
            "mu": background.mu,
            "softening_length": background.softening_length,
            "core_radius": background.core_radius,
            "c_eff": background.c_eff,
            "center": list(background.center),
        },
        "orbit_summary": orbit_summary,
        "final_snapshot": orbit_log[-1],
        "assumptions": [
            "The heavy source is represented by an imposed static background potential.",
            "The defect internal confinement is carried with the instantaneous defect center as a reduced COM/internal split surrogate.",
            "Ambient density for the adiabatic geometry closure is sampled from the imposed background via the weak-field rho-coupling rule.",
            "The run omits live Maxwell, free-heavy recoil, clamped-source controls, and isolated Poisson solves.",
        ],
    }
    dump_json(output_dir / "summary.json", summary)

    supports_target = (
        fit_error is None
        and abs(orbit_summary["beta_eff"] - targets["beta_1PN"]) < float(config["experiment"].get("beta_tolerance", 0.75))
        and orbit_summary["mean_fit_higher_mode_fraction"] < float(config["experiment"].get("higher_mode_threshold", 0.05))
        and orbit_summary["mean_fit_coherence"] > float(config["experiment"].get("coherence_threshold", 0.97))
    )

    if fit_error is None:
        plain_language = [
            "Experiment 2 static-background orbit summary:",
            f"- Fitted Delta phi = {orbit_summary['delta_phi']:.6f} +/- {orbit_summary['delta_phi_stderr']:.6f}.",
            f"- Fitted beta_eff = {orbit_summary['beta_eff']:.4f} against the target beta_1PN = {targets['beta_1PN']:.1f}.",
            f"- Orbit shape over the fit window: a = {orbit_summary['semi_major_axis']:.4f}, e = {orbit_summary['eccentricity']:.4f}.",
            f"- Fit-window diagnostics: coherence = {orbit_summary['mean_fit_coherence']:.4f}, higher-mode fraction = {orbit_summary['mean_fit_higher_mode_fraction']:.4e}, leakage = {orbit_summary['mean_fit_leakage']:.4e}.",
            f"- Target support on this run: {supports_target}.",
        ]
    else:
        plain_language = [
            "Experiment 2 static-background orbit summary:",
            f"- Orbit fit failed: {fit_error}.",
            f"- Available fit-window diagnostics: coherence = {orbit_summary['mean_fit_coherence']:.4f}, higher-mode fraction = {orbit_summary['mean_fit_higher_mode_fraction']:.4e}, leakage = {orbit_summary['mean_fit_leakage']:.4e}.",
            "- This run did not produce a usable periapsis sequence for beta_eff extraction.",
        ]
    (output_dir / "plain_language_summary.txt").write_text("\n".join(plain_language) + "\n", encoding="utf-8")
    (output_dir / "unresolved_assumptions.txt").write_text("\n".join(summary["assumptions"]) + "\n", encoding="utf-8")
    return output_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Experiment 2: static-background orbit")
    parser.add_argument("--config", required=True, help="Path to the JSON config file")
    parser.add_argument("--restart", default=None, help="Optional checkpoint .npz path")
    args = parser.parse_args()
    run(args.config, restart=args.restart)


if __name__ == "__main__":
    main()
