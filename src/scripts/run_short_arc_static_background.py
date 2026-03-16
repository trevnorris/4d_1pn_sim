from __future__ import annotations

import argparse
import copy
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
from src.physics.pde_orbit_runtime import (
    run_static_launch_calibration,
    sample_continuity_metrics,
    sample_light_metrics,
    window_mean,
)
from src.physics.point_particle import run_point_particle_trajectory
from src.physics.short_arc import evaluate_short_arc_acceptance, summarize_short_arc_match


def run(
    config_path: str | Path,
    scenario: str | None = None,
    restart_relaxed: str | Path | None = None,
) -> Path:
    config = load_json_config(config_path)
    seed = int(config["seed"])
    np.random.seed(seed)
    torch.manual_seed(seed)

    short_arc = dict(config["short_arc"])
    scenario_name = scenario or str(short_arc.get("scenario", "source_no_dressing"))
    effective_config = copy.deepcopy(config)
    effective_config["short_arc"]["scenario"] = scenario_name
    effective_run_name = str(config["run_name"])
    if not effective_run_name.endswith(scenario_name):
        effective_run_name = f"{effective_run_name}_{scenario_name}"
    output_root = Path(str(config["output_dir"]))
    effective_output_dir = output_root
    if not output_root.name.endswith(scenario_name):
        effective_output_dir = output_root.parent / f"{output_root.name}_{scenario_name}"
    effective_config["run_name"] = effective_run_name
    effective_config["output_dir"] = str(effective_output_dir)

    output_path = ensure_dir(effective_output_dir, overwrite=bool(config.get("overwrite_output", False)))
    dump_json(output_path / "config.json", effective_config)
    dump_json(output_path / "runtime.json", collect_runtime_info(seed))
    print(f"[short-arc] output_dir={output_path}", flush=True)
    print(f"[short-arc] scenario={scenario_name}", flush=True)

    solver, projection_kernel = build_solver(config)
    rho0 = float(config["geometry"]["reference_rho"])
    background = StaticCentralBackground.from_config(config["background"], rho_reference=rho0)
    background_potential = background.potential_field(solver.grid).to(solver.grid.real_dtype)

    relaxed_restart_path = restart_relaxed or config.get("restart_relaxed")
    if relaxed_restart_path is None:
        print("[short-arc] stage=relax start", flush=True)
        relax_start = time.monotonic()
        relaxed_state = prepare_relaxed_state(solver=solver, config=config, rho_ambient=rho0)
        print(f"[short-arc] stage=relax done elapsed_s={time.monotonic() - relax_start:.2f}", flush=True)
    else:
        print(f"[short-arc] stage=load_relaxed checkpoint={relaxed_restart_path}", flush=True)
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

    print("[short-arc] stage=launch_calibration start", flush=True)
    calibration_start = time.monotonic()
    calibration_summary = run_static_launch_calibration(
        solver=solver,
        relaxed_state=relaxed_state,
        config=config,
        background=background,
        background_potential=background_potential,
        rho0=rho0,
        scenario=scenario_name,
    )
    print(f"[short-arc] stage=launch_calibration done elapsed_s={time.monotonic() - calibration_start:.2f}", flush=True)
    if calibration_summary is None:
        base_speed = background.periapsis_speed(
            float(config["experiment"]["periapsis_radius"]),
            float(config["experiment"]["eccentricity"]),
        )
        target_speed = base_speed * float(config["experiment"].get("velocity_scale", 1.0))
        applied_speed = target_speed
        tracer_velocity = np.array([0.0, target_speed, 0.0], dtype=np.float64)
    else:
        applied_speed = float(calibration_summary["recommended_applied_speed"])
        velocity_summary = calibration_summary["recommended_velocity_summary"]
        tracer_velocity = np.array(
            [
                float(velocity_summary["mean_radial_speed"]),
                float(velocity_summary["mean_tangential_speed"]),
                0.0,
            ],
            dtype=np.float64,
        )
        dump_json(output_path / "launch_calibration.json", calibration_summary)

    start_radius = float(config["experiment"]["periapsis_radius"])
    initial_position = np.array([start_radius, 0.0, 0.0], dtype=np.float64)
    print("[short-arc] stage=tracer start", flush=True)
    tracer_start = time.monotonic()
    tracer = run_point_particle_trajectory(
        background=background,
        initial_position=initial_position,
        initial_velocity=tracer_velocity,
        dt=float(config["solver"]["dt"]),
        steps=int(config["experiment"]["orbit_steps"]),
    )
    print(f"[short-arc] stage=tracer done elapsed_s={time.monotonic() - tracer_start:.2f}", flush=True)

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
    progress_every = int(config["solver"].get("progress_every", max(checkpoint_every, 128) if checkpoint_every > 0 else 128))
    metric_stride = int(short_arc.get("metric_stride", 16))
    continuity_stride = int(short_arc.get("continuity_stride", 64))
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
    print("[short-arc] stage=evolve start", flush=True)
    evolve_start = time.monotonic()
    for idx in range(steps):
        center = solver.estimate_defect_center(state.psi_modes)
        if scenario_name == "source_with_dressing":
            rho_ambient = float(background.ambient_density_at_position(center.detach().cpu().tolist()))
        else:
            rho_ambient = rho0
        state = solver.step(
            state,
            dt=dt,
            rho_ambient=rho_ambient,
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
                f"[short-arc] stage=evolve step={state.step} time={state.time:.3f} "
                f"radius={radius:.6f} coherence={coherence_value:.6f}",
                flush=True,
            )

    print(f"[short-arc] stage=evolve done elapsed_s={time.monotonic() - evolve_start:.2f}", flush=True)

    defect_time_array = np.asarray(defect_time, dtype=np.float64)
    defect_positions_array = np.asarray(defect_positions, dtype=np.float64)
    compare_start = int(short_arc.get("compare_start_step", 0))
    compare_end = short_arc.get("compare_end_step")
    compare_end = int(compare_end) if compare_end is not None else None

    short_arc_summary = summarize_short_arc_match(
        time=defect_time_array,
        tracer_positions=tracer["position"],
        defect_positions=defect_positions_array,
        source_center=background.center,
        box_length=solver.grid.length,
        start_index=compare_start,
        end_index=compare_end,
    )
    lower = short_arc_summary["compare_start_index"]
    upper = short_arc_summary["compare_end_index"]
    window_start_time = float(defect_time_array[lower])
    window_end_time = float(defect_time_array[upper - 1])
    metric_sample_times_array = np.asarray(metric_sample_times, dtype=np.float64)
    continuity_sample_times_array = np.asarray(continuity_sample_times, dtype=np.float64)
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
    acceptance = evaluate_short_arc_acceptance(
        short_arc_summary=short_arc_summary,
        defect_metrics=defect_metrics,
        thresholds={
            key: float(value)
            for key, value in short_arc.items()
            if key
            in {
                "min_angular_sweep",
                "max_angular_sweep_error",
                "max_normalized_position_rms",
                "max_normalized_radius_rms",
                "max_phase_rms",
                "min_boundary_clearance",
                "min_coherence",
                "max_higher_mode_fraction",
                "max_leakage",
            }
        },
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
        tracer_position=tracer["position"],
        tracer_velocity=tracer["velocity"],
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
        "run_name": effective_run_name,
        "scenario": scenario_name,
        "background": {
            "profile": background.profile,
            "mu": background.mu,
            "c_eff": background.c_eff,
            "center": list(background.center),
        },
        "launch_calibration": calibration_summary,
        "restart_relaxed": None if relaxed_restart_path is None else str(relaxed_restart_path),
        "tracer_initial_velocity": tracer_velocity.tolist(),
        "defect_applied_speed": float(applied_speed),
        "short_arc_summary": short_arc_summary,
        "defect_metrics": defect_metrics,
        "acceptance": acceptance,
        "final_snapshot": final_snapshot,
    }
    dump_json(output_path / "summary.json", summary)

    lines = [
        f"Short-arc static-background summary for scenario '{scenario_name}':",
        f"- defect applied speed = {applied_speed:.6f}",
        f"- tracer angular sweep = {short_arc_summary['tracer_angular_sweep']:.6f}",
        f"- defect angular sweep = {short_arc_summary['defect_angular_sweep']:.6f}",
        f"- normalized position RMS = {short_arc_summary['normalized_position_rms']:.6e}",
        f"- normalized radius RMS = {short_arc_summary['normalized_radius_rms']:.6e}",
        f"- phase RMS = {short_arc_summary['phase_rms']:.6e}",
        f"- min boundary clearance = {short_arc_summary['boundary_summary']['min_boundary_clearance']:.6f}",
        f"- mean coherence = {defect_metrics['mean_coherence']:.6f}",
        f"- mean higher-mode fraction = {defect_metrics['mean_higher_mode_fraction']:.6e}",
        f"- mean leakage = {defect_metrics['mean_leakage']:.6e}",
        f"- acceptance pass = {acceptance['passes']}",
    ]
    (output_path / "plain_language_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    assumptions = [
        "The source is an imposed static analytic background, not a live second defect.",
        "The point tracer is matched to the defect using the launch-calibration velocity summary.",
        "This is a short-arc tuning run, not a full perihelion extraction.",
    ]
    (output_path / "unresolved_assumptions.txt").write_text("\n".join(assumptions) + "\n", encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a tracer-matched short-arc defect orbit against a static background")
    parser.add_argument("--config", required=True, help="Short-arc config path")
    parser.add_argument(
        "--scenario",
        choices=["source_no_dressing", "source_with_dressing"],
        default=None,
        help="Optional scenario override",
    )
    parser.add_argument(
        "--restart-relaxed",
        default=None,
        help="Optional checkpoint for a pre-relaxed defect state before insertion",
    )
    args = parser.parse_args()

    output_path = run(
        config_path=args.config,
        scenario=args.scenario,
        restart_relaxed=args.restart_relaxed,
    )
    summary = load_json_config(Path(output_path) / "summary.json")
    print(f"scenario: {summary['scenario']}")
    print(f"acceptance_pass: {summary['acceptance']['passes']}")
    print(f"normalized_position_rms: {summary['short_arc_summary']['normalized_position_rms']:.6e}")
    print(f"phase_rms: {summary['short_arc_summary']['phase_rms']:.6e}")
    print(f"mean_coherence: {summary['defect_metrics']['mean_coherence']:.6f}")


if __name__ == "__main__":
    main()
