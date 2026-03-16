from __future__ import annotations

import argparse
from pathlib import Path
import time
from typing import Any

import numpy as np
import torch

from src.core.checkpoints import save_checkpoint
from src.core.config import load_json_config
from src.core.io import collect_runtime_info, dump_json, ensure_dir
from src.experiments.common import build_solver, prepare_relaxed_state, state_from_checkpoint
from src.physics.background_sources import StaticCentralBackground
from src.physics.defects import displace_and_boost_state
from src.physics.newtonian_orbit_gate import evaluate_newtonian_orbit_gate
from src.physics.orbit_diagnostics import summarize_effective_orbit_conservation, summarize_planar_orbit_trace
from src.physics.pde_orbit_runtime import (
    run_static_launch_calibration,
    sample_continuity_metrics,
    sample_light_metrics,
    window_mean,
)


def run(config_path: str | Path, restart_relaxed: str | Path | None = None) -> Path:
    config = load_json_config(config_path)
    seed = int(config["seed"])
    np.random.seed(seed)
    torch.manual_seed(seed)

    output_path = ensure_dir(config["output_dir"], overwrite=bool(config.get("overwrite_output", False)))
    dump_json(output_path / "config.json", config)
    dump_json(output_path / "runtime.json", collect_runtime_info(seed))
    print(f"[exp03] output_dir={output_path}", flush=True)

    solver, projection_kernel = build_solver(config)
    rho0 = float(config["geometry"]["reference_rho"])
    background = StaticCentralBackground.from_config(config["background"], rho_reference=rho0)
    background_potential = background.potential_field(solver.grid).to(solver.grid.real_dtype)

    relaxed_restart_path = restart_relaxed or config.get("restart_relaxed")
    if relaxed_restart_path is None:
        print("[exp03] stage=relax start", flush=True)
        relax_start = time.monotonic()
        relaxed_state = prepare_relaxed_state(solver=solver, config=config, rho_ambient=rho0)
        print(f"[exp03] stage=relax done elapsed_s={time.monotonic() - relax_start:.2f}", flush=True)
    else:
        print(f"[exp03] stage=load_relaxed checkpoint={relaxed_restart_path}", flush=True)
        relaxed_state = state_from_checkpoint(relaxed_restart_path, solver=solver)
    save_checkpoint(
        output_path / "checkpoint_relaxed.npz",
        {
            "psi_modes": relaxed_state.psi_modes,
            "time": relaxed_state.time,
            "step": relaxed_state.step,
            "a": relaxed_state.a,
            "rho_ambient": relaxed_state.rho_ambient,
        },
    )

    print("[exp03] stage=launch_calibration start", flush=True)
    calibration_start = time.monotonic()
    calibration_summary = run_static_launch_calibration(
        solver=solver,
        relaxed_state=relaxed_state,
        config=config,
        background=background,
        background_potential=background_potential,
        rho0=rho0,
        scenario="source_no_dressing",
    )
    print(f"[exp03] stage=launch_calibration done elapsed_s={time.monotonic() - calibration_start:.2f}", flush=True)
    if calibration_summary is None:
        base_speed = background.periapsis_speed(
            float(config["experiment"]["periapsis_radius"]),
            float(config["experiment"]["eccentricity"]),
        )
        applied_speed = base_speed * float(config["experiment"].get("velocity_scale", 1.0))
    else:
        applied_speed = float(calibration_summary["recommended_applied_speed"])
        dump_json(output_path / "launch_calibration.json", calibration_summary)

    start_radius = float(config["experiment"]["periapsis_radius"])
    state = displace_and_boost_state(
        solver=solver,
        state=relaxed_state,
        shift=(start_radius, 0.0, 0.0),
        momentum=(0.0, solver.mass * applied_speed, 0.0),
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

    reference_modes = state.psi_modes.clone()
    checkpoint_every = int(config["solver"].get("checkpoint_every", 0))
    progress_every = int(config["solver"].get("progress_every", max(checkpoint_every, 256) if checkpoint_every > 0 else 256))
    metric_stride = int(config["experiment"].get("metric_stride", 16))
    continuity_stride = int(config["experiment"].get("continuity_stride", 64))
    dt = float(config["solver"]["dt"])
    steps = int(config["experiment"]["orbit_steps"])

    defect_positions: list[list[float]] = []
    defect_time: list[float] = []
    metric_sample_times: list[float] = []
    coherence_history: list[float] = []
    higher_mode_history: list[float] = []
    compactness_history: list[float] = []
    continuity_sample_times: list[float] = []
    leakage_history: list[float] = []
    continuity_history: list[float] = []
    final_snapshot: dict[str, Any] | None = None

    previous_continuity_snapshot: dict[str, Any] | None = None
    print("[exp03] stage=evolve start", flush=True)
    evolve_start = time.monotonic()
    for idx in range(steps):
        state = solver.step(
            state,
            dt=dt,
            rho_ambient=rho0,
            external_potential=background_potential,
        )
        defect_time.append(float(state.time))
        current_center = solver.estimate_defect_center(state.psi_modes).detach().cpu().numpy()
        defect_positions.append(current_center.tolist())

        if metric_stride > 0 and ((idx + 1) % metric_stride == 0 or idx == steps - 1):
            light_metrics = sample_light_metrics(
                solver=solver,
                state=state,
                reference_modes=reference_modes,
            )
            metric_sample_times.append(float(state.time))
            coherence_history.append(float(light_metrics["mean_coherence"]))
            higher_mode_history.append(float(light_metrics["mean_higher_mode_fraction"]))
            compactness_history.append(float(light_metrics["mean_compactness"]))
            final_snapshot = {
                "time": float(state.time),
                "step": int(state.step),
                "rho_ambient": float(state.rho_ambient),
                "a": float(state.a),
                "center_of_mass": current_center.tolist(),
                **light_metrics,
            }

        if continuity_stride > 0 and ((idx + 1) % continuity_stride == 0 or idx == steps - 1):
            previous_continuity_snapshot, continuity_metrics = sample_continuity_metrics(
                solver=solver,
                state=state,
                projection_kernel=projection_kernel,
                previous_snapshot=previous_continuity_snapshot,
            )
            continuity_sample_times.append(float(state.time))
            leakage_history.append(float(continuity_metrics["mean_leakage"]))
            continuity_history.append(float(continuity_metrics["mean_continuity_residual"]))

        if checkpoint_every > 0 and state.step % checkpoint_every == 0:
            save_checkpoint(
                output_path / f"checkpoint_step_{state.step:05d}.npz",
                {
                    "psi_modes": state.psi_modes,
                    "time": state.time,
                    "step": state.step,
                    "a": state.a,
                    "rho_ambient": state.rho_ambient,
                },
            )
        if progress_every > 0 and state.step % progress_every == 0:
            radius = float(np.linalg.norm(np.asarray(current_center, dtype=np.float64)[:2]))
            coherence_value = coherence_history[-1] if coherence_history else float("nan")
            print(
                f"[exp03] stage=evolve step={state.step} time={state.time:.3f} "
                f"radius={radius:.6f} coherence={coherence_value:.6f}",
                flush=True,
            )
    print(f"[exp03] stage=evolve done elapsed_s={time.monotonic() - evolve_start:.2f}", flush=True)

    defect_time_array = np.asarray(defect_time, dtype=np.float64)
    defect_positions_array = np.asarray(defect_positions, dtype=np.float64)
    metric_sample_times_array = np.asarray(metric_sample_times, dtype=np.float64)
    continuity_sample_times_array = np.asarray(continuity_sample_times, dtype=np.float64)
    fit_start_index = int(config["experiment"].get("fit_start_index", 0))
    fit_start_index = min(max(fit_start_index, 0), max(defect_time_array.size - 1, 0))
    window_start_time = float(defect_time_array[fit_start_index]) if defect_time_array.size else 0.0
    window_end_time = float(defect_time_array[-1]) if defect_time_array.size else 0.0

    conservation_summary = summarize_effective_orbit_conservation(
        time=defect_time_array,
        positions=defect_positions_array,
        source_center=background.center,
        potential_fn=background.potential_at_position,
        mu=background.mu,
        fit_start_index=fit_start_index,
    )
    try:
        orbit_summary = summarize_planar_orbit_trace(
            time=defect_time_array,
            positions=defect_positions_array,
            mu=background.mu,
            c_eff=background.c_eff,
            source_center=background.center,
            potential_fn=background.potential_at_position,
            fit_start_index=fit_start_index,
            turning_point_min_spacing=int(config["experiment"].get("turning_point_min_spacing", 1)),
            turning_point_smooth_window=int(config["experiment"].get("turning_point_smooth_window", 1)),
            turning_point_min_spacing_fraction=float(config["experiment"].get("turning_point_min_spacing_fraction", 0.35)),
            turning_point_prominence_fraction=float(config["experiment"].get("turning_point_prominence_fraction", 0.08)),
        )
        fit_error = None
    except ValueError as exc:
        orbit_summary = {
            "fit_error": str(exc),
            "fit_start_index": int(fit_start_index),
            **conservation_summary,
        }
        fit_error = str(exc)

    defect_metrics = {
        "mean_coherence": window_mean(
            np.asarray(coherence_history, dtype=np.float64),
            metric_sample_times_array,
            window_start_time,
            window_end_time,
        ),
        "mean_higher_mode_fraction": window_mean(
            np.asarray(higher_mode_history, dtype=np.float64),
            metric_sample_times_array,
            window_start_time,
            window_end_time,
        ),
        "mean_leakage": window_mean(
            np.asarray(leakage_history, dtype=np.float64),
            continuity_sample_times_array,
            window_start_time,
            window_end_time,
        ),
        "mean_compactness": window_mean(
            np.asarray(compactness_history, dtype=np.float64),
            metric_sample_times_array,
            window_start_time,
            window_end_time,
        ),
        "mean_continuity_residual": window_mean(
            np.asarray(continuity_history, dtype=np.float64),
            continuity_sample_times_array,
            window_start_time,
            window_end_time,
        ),
        "metric_stride": int(metric_stride),
        "continuity_stride": int(continuity_stride),
        "metric_sample_count": int(metric_sample_times_array.size),
        "continuity_sample_count": int(continuity_sample_times_array.size),
    }
    newtonian_gate = evaluate_newtonian_orbit_gate(
        orbit_summary=orbit_summary,
        defect_metrics=defect_metrics,
        thresholds={key: float(value) for key, value in config["newtonian_gate"].items()},
        fit_error=fit_error,
    )

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
        output_path / "timeseries.npz",
        time=defect_time_array,
        defect_position=defect_positions_array,
        metric_sample_time=metric_sample_times_array,
        coherence=np.asarray(coherence_history, dtype=np.float64),
        higher_mode_fraction=np.asarray(higher_mode_history, dtype=np.float64),
        continuity_sample_time=continuity_sample_times_array,
        mean_S_leak=np.asarray(leakage_history, dtype=np.float64),
        radius_of_gyration=np.asarray(compactness_history, dtype=np.float64),
        continuity_residual_l2=np.asarray(continuity_history, dtype=np.float64),
    )

    summary = {
        "run_name": str(config["run_name"]),
        "background": {
            "profile": background.profile,
            "mu": float(background.mu),
            "c_eff": float(background.c_eff),
            "center": list(background.center),
        },
        "restart_relaxed": None if relaxed_restart_path is None else str(relaxed_restart_path),
        "defect_applied_speed": float(applied_speed),
        "launch_calibration": calibration_summary,
        "orbit_summary": orbit_summary,
        "defect_metrics": defect_metrics,
        "newtonian_gate": newtonian_gate,
        "final_snapshot": final_snapshot,
        "assumptions": [
            "This run uses the imposed static analytic background with fixed ambient density rho0 and no dressing response.",
            "The defect confinement remains centered on the instantaneous defect COM as a reduced COM/internal split surrogate.",
            "The orbit_summary energy and angular-momentum drifts are effective COM point-particle diagnostics, not exact full-field invariants.",
            "This is a Newtonian-gate run, not a 1PN measurement run.",
        ],
    }
    dump_json(output_path / "summary.json", summary)

    lines = [
        "Experiment 3 PDE Newtonian bound-orbit summary:",
        f"- defect applied speed = {applied_speed:.6f}",
        f"- newtonian gate pass = {newtonian_gate['passes']}",
        f"- fit error = {fit_error}" if fit_error is not None else f"- beta_eff = {orbit_summary['beta_eff']:.6e}",
        f"- periapse count = {orbit_summary.get('periapse_count', 0)}",
        f"- max relative orbital-energy drift = {orbit_summary['orbital_energy_summary']['max_rel_drift']:.6e}",
        f"- max relative angular-momentum drift = {orbit_summary['angular_momentum_z_summary']['max_rel_drift']:.6e}",
        f"- mean coherence = {defect_metrics['mean_coherence']:.6f}",
        f"- mean higher-mode fraction = {defect_metrics['mean_higher_mode_fraction']:.6e}",
        f"- mean leakage = {defect_metrics['mean_leakage']:.6e}",
    ]
    (output_path / "plain_language_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (output_path / "unresolved_assumptions.txt").write_text("\n".join(summary["assumptions"]) + "\n", encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Experiment 3: PDE Newtonian bound orbit")
    parser.add_argument("--config", required=True, help="Path to the JSON config file")
    parser.add_argument("--restart-relaxed", default=None, help="Optional pre-relaxed checkpoint path")
    args = parser.parse_args()

    output_path = run(config_path=args.config, restart_relaxed=args.restart_relaxed)
    summary = load_json_config(Path(output_path) / "summary.json")
    print(f"newtonian_gate_pass: {summary['newtonian_gate']['passes']}")
    print(f"fit_error: {summary['orbit_summary'].get('fit_error')}")
    print(f"max_rel_energy_drift: {summary['orbit_summary']['orbital_energy_summary']['max_rel_drift']:.6e}")
    print(f"max_rel_angular_momentum_drift: {summary['orbit_summary']['angular_momentum_z_summary']['max_rel_drift']:.6e}")
    print(f"mean_coherence: {summary['defect_metrics']['mean_coherence']:.6f}")


if __name__ == "__main__":
    main()
