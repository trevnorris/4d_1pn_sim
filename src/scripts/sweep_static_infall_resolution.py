from __future__ import annotations

import argparse
import copy
import csv
import gc
import traceback
from pathlib import Path
from typing import Any

import numpy as np
import torch

from src.core.checkpoints import save_checkpoint
from src.core.config import load_json_config
from src.core.io import collect_runtime_info, dump_json, ensure_dir
from src.experiments.common import build_solver, prepare_relaxed_state, serializable_diag
from src.physics.background_sources import StaticCentralBackground
from src.physics.defects import displace_and_boost_state
from src.physics.diagnostics import snapshot_diagnostics
from src.physics.infall_analysis import summarize_static_infall_run


def _case_config(base_config: dict[str, Any], grid_shape: int, grid_length: float, scenario: str) -> dict[str, Any]:
    config = copy.deepcopy(base_config)
    config["run_name"] = f"{base_config['run_name']}_{scenario}_n{grid_shape}"
    config["output_dir"] = str(Path(base_config["output_dir"]) / f"{scenario}_n{grid_shape}")
    config["grid"]["shape"] = [int(grid_shape), int(grid_shape), int(grid_shape)]
    config["grid"]["length"] = [float(grid_length), float(grid_length), float(grid_length)]
    config["device"] = str(config.get("device", "cpu"))
    return config


def run_infall_case(
    config: dict[str, Any],
    scenario: str,
    output_dir: str | Path,
    steps: int,
    target_radius_fractions: list[float],
    stop_at_smallest_target: bool,
) -> dict[str, Any]:
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

    background = StaticCentralBackground.from_config(config["background"], rho_reference=rho0)
    background_potential = background.potential_field(solver.grid).to(solver.grid.real_dtype)
    source_center = torch.tensor(background.center, device=solver.grid.device, dtype=solver.grid.real_dtype)

    start_radius = float(config["experiment"]["periapsis_radius"])
    velocity_scale = float(config["experiment"].get("velocity_scale", 0.0))
    tangential_speed = background.periapsis_speed(start_radius, float(config["experiment"].get("eccentricity", 0.0)))
    tangential_speed *= velocity_scale

    state = displace_and_boost_state(
        solver=solver,
        state=state,
        shift=(start_radius, 0.0, 0.0),
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

    checkpoint_every = int(config["solver"].get("checkpoint_every", 0))
    dt = float(config["solver"]["dt"])
    min_target_radius = min(float(value) for value in target_radius_fractions) * start_radius

    trajectory_time: list[float] = []
    trajectory_position: list[list[float]] = []
    ambient_density_history: list[float] = []
    a_history: list[float] = []
    coherence_history: list[float] = []
    higher_mode_history: list[float] = []
    leakage_history: list[float] = []
    compactness_history: list[float] = []
    continuity_history: list[float] = []
    orbit_log: list[dict[str, Any]] = []

    stop_reason = "max_steps"
    previous_diag: dict[str, Any] | None = None
    for _ in range(int(steps)):
        center = solver.estimate_defect_center(state.psi_modes)
        if scenario == "source_with_dressing":
            rho_ambient = float(background.ambient_density_at_position(center.detach().cpu().tolist()))
        else:
            rho_ambient = rho0
        state = solver.step(
            state,
            dt=dt,
            rho_ambient=rho_ambient,
            external_potential=background_potential,
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
        ambient_density_history.append(float(rho_ambient))
        a_history.append(float(state.a))
        coherence_history.append(float(diag["coherence"]))
        higher_mode_history.append(float(diag["higher_mode_fraction"]))
        leakage_history.append(float(diag["mean_S_leak"]))
        compactness_history.append(float(diag["radius_of_gyration"]))
        continuity_history.append(float(diag["continuity_residual_l2"]))

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

        current_radius = float(
            np.linalg.norm(
                np.asarray(diag["center_of_mass"], dtype=np.float64)
                - np.asarray(background.center, dtype=np.float64)
            )
        )
        if stop_at_smallest_target and current_radius <= min_target_radius:
            stop_reason = "reached_min_target_radius"
            break

    time = np.asarray(trajectory_time, dtype=np.float64)
    positions = np.asarray(trajectory_position, dtype=np.float64)
    compactness = np.asarray(compactness_history, dtype=np.float64)
    coherence = np.asarray(coherence_history, dtype=np.float64)
    higher_mode = np.asarray(higher_mode_history, dtype=np.float64)
    leakage = np.asarray(leakage_history, dtype=np.float64)
    continuity = np.asarray(continuity_history, dtype=np.float64)
    ambient_density = np.asarray(ambient_density_history, dtype=np.float64)
    a_history_array = np.asarray(a_history, dtype=np.float64)

    infall_summary = summarize_static_infall_run(
        time=time,
        positions=positions,
        source_center=background.center,
        mu=background.mu,
        compactness=compactness,
        coherence=coherence,
        higher_mode_fraction=higher_mode,
        leakage=leakage,
        target_radius_fractions=target_radius_fractions,
    )
    dx = float(solver.grid.dx[0])
    infall_summary.update(
        {
            "scenario": scenario,
            "grid_shape": list(solver.grid.shape),
            "grid_length": list(solver.grid.length),
            "dx": dx,
            "initial_compactness_cells": float(infall_summary["initial_compactness"] / dx),
            "mean_compactness_cells": float(infall_summary["mean_compactness"] / dx),
            "initial_radius_over_initial_compactness": float(
                infall_summary["initial_radius"] / max(infall_summary["initial_compactness"], 1.0e-12)
            ),
            "mean_continuity_residual": float(np.mean(continuity)),
            "ambient_density_span": [float(np.min(ambient_density)), float(np.max(ambient_density))],
            "a_span": [float(np.min(a_history_array)), float(np.max(a_history_array))],
            "stop_reason": stop_reason,
            "step_count": int(time.size),
            "initial_tangential_speed": float(tangential_speed),
            "final_snapshot": orbit_log[-1],
        }
    )

    dump_json(output_path / "summary.json", infall_summary)
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
        time=time,
        position=positions,
        rho_ambient=ambient_density,
        a=a_history_array,
        coherence=coherence,
        higher_mode_fraction=higher_mode,
        mean_S_leak=leakage,
        radius_of_gyration=compactness,
        continuity_residual_l2=continuity,
    )
    plain_language = [
        f"Static-background infall summary for scenario '{scenario}' on grid {solver.grid.shape[0]}^3:",
        f"- initial radius = {infall_summary['initial_radius']:.6f}",
        f"- final radius = {infall_summary['final_radius']:.6f}",
        f"- initial compactness = {infall_summary['initial_compactness']:.6f} ({infall_summary['initial_compactness_cells']:.3f} cells)",
        f"- initial radial acceleration = {infall_summary['initial_radial_fit']['initial_radial_acceleration']:.6e}",
        f"- oracle radial acceleration = {infall_summary['oracle_initial_radial_acceleration']:.6e}",
        f"- pre-target coherence = {infall_summary['pre_target_mean_coherence']:.6f}",
        f"- pre-target higher-mode fraction = {infall_summary['pre_target_mean_higher_mode_fraction']:.6e}",
        f"- pre-target leakage = {infall_summary['pre_target_mean_leakage']:.6e}",
        f"- stop reason = {stop_reason}",
    ]
    for key, crossing in infall_summary["crossings"].items():
        if crossing["reached"]:
            plain_language.append(
                f"- crossing {key} r0: measured t = {crossing['measured_time']:.6f}, "
                f"oracle t = {crossing['oracle_time']:.6f}, ratio = {crossing['time_ratio']:.6f}"
            )
        else:
            plain_language.append(f"- crossing {key} r0: not reached within run window")
    (output_path / "plain_language_summary.txt").write_text("\n".join(plain_language) + "\n", encoding="utf-8")
    assumptions = [
        "The source is an imposed static analytic background, not a live second defect.",
        "The defect is prepared by imaginary-time relaxation and then released from rest for radial infall.",
        "The run omits live Maxwell, free-heavy recoil, and isolated Poisson boundary handling.",
    ]
    (output_path / "unresolved_assumptions.txt").write_text("\n".join(assumptions) + "\n", encoding="utf-8")
    return infall_summary


def _write_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    fieldnames = [
        "scenario",
        "grid_n",
        "dx",
        "status",
        "initial_compactness",
        "initial_compactness_cells",
        "initial_radius_over_initial_compactness",
        "initial_radial_acceleration",
        "oracle_initial_radial_acceleration",
        "initial_radial_acceleration_ratio",
        "crossing_0.75_time_ratio",
        "crossing_0.50_time_ratio",
        "pre_target_mean_coherence",
        "pre_target_mean_higher_mode_fraction",
        "pre_target_mean_leakage",
        "stop_reason",
        "error",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def run(config_path: str | Path) -> Path:
    config = load_json_config(config_path)
    sweep = dict(config["resolution_sweep"])
    output_path = ensure_dir(config["output_dir"], overwrite=bool(config.get("overwrite_output", False)))
    dump_json(output_path / "config.json", config)
    dump_json(output_path / "runtime.json", collect_runtime_info(int(config["seed"])))

    grid_sizes = [int(value) for value in sweep["grid_sizes"]]
    scenarios = [str(value) for value in sweep.get("scenarios", ["source_no_dressing"])]
    grid_length = float(sweep.get("grid_length", config["grid"]["length"][0]))
    steps = int(sweep.get("steps", config["experiment"]["orbit_steps"]))
    target_radius_fractions = [float(value) for value in sweep.get("target_radius_fractions", [0.75, 0.5])]
    stop_at_smallest_target = bool(sweep.get("stop_at_smallest_target", True))

    cases: list[dict[str, Any]] = []
    csv_rows: list[dict[str, Any]] = []
    for scenario in scenarios:
        for grid_size in grid_sizes:
            case = {
                "scenario": scenario,
                "grid_n": grid_size,
            }
            case_output = output_path / f"{scenario}_n{grid_size}"
            case_config = _case_config(config, grid_shape=grid_size, grid_length=grid_length, scenario=scenario)
            try:
                summary = run_infall_case(
                    config=case_config,
                    scenario=scenario,
                    output_dir=case_output,
                    steps=steps,
                    target_radius_fractions=target_radius_fractions,
                    stop_at_smallest_target=stop_at_smallest_target,
                )
                case.update({"status": "completed", "summary": summary})
                csv_rows.append(
                    {
                        "scenario": scenario,
                        "grid_n": grid_size,
                        "dx": summary["dx"],
                        "status": "completed",
                        "initial_compactness": summary["initial_compactness"],
                        "initial_compactness_cells": summary["initial_compactness_cells"],
                        "initial_radius_over_initial_compactness": summary["initial_radius_over_initial_compactness"],
                        "initial_radial_acceleration": summary["initial_radial_fit"]["initial_radial_acceleration"],
                        "oracle_initial_radial_acceleration": summary["oracle_initial_radial_acceleration"],
                        "initial_radial_acceleration_ratio": summary["initial_radial_acceleration_ratio"],
                        "crossing_0.75_time_ratio": summary["crossings"].get("0.75", {}).get("time_ratio"),
                        "crossing_0.50_time_ratio": summary["crossings"].get("0.50", {}).get("time_ratio"),
                        "pre_target_mean_coherence": summary["pre_target_mean_coherence"],
                        "pre_target_mean_higher_mode_fraction": summary["pre_target_mean_higher_mode_fraction"],
                        "pre_target_mean_leakage": summary["pre_target_mean_leakage"],
                        "stop_reason": summary["stop_reason"],
                        "error": "",
                    }
                )
            except (RuntimeError, MemoryError) as exc:
                error_text = "".join(traceback.format_exception_only(type(exc), exc)).strip()
                failure = {
                    "scenario": scenario,
                    "grid_n": grid_size,
                    "status": "failed",
                    "error": error_text,
                }
                dump_json(case_output / "summary.json", failure)
                cases.append(failure)
                csv_rows.append(
                    {
                        "scenario": scenario,
                        "grid_n": grid_size,
                        "dx": "",
                        "status": "failed",
                        "initial_compactness": "",
                        "initial_compactness_cells": "",
                        "initial_radius_over_initial_compactness": "",
                        "initial_radial_acceleration": "",
                        "oracle_initial_radial_acceleration": "",
                        "initial_radial_acceleration_ratio": "",
                        "crossing_0.75_time_ratio": "",
                        "crossing_0.50_time_ratio": "",
                        "pre_target_mean_coherence": "",
                        "pre_target_mean_higher_mode_fraction": "",
                        "pre_target_mean_leakage": "",
                        "stop_reason": "failed",
                        "error": error_text,
                    }
                )
            else:
                cases.append(case)
            finally:
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

    aggregate = {
        "run_name": config["run_name"],
        "grid_sizes": grid_sizes,
        "grid_length": grid_length,
        "scenarios": scenarios,
        "target_radius_fractions": target_radius_fractions,
        "cases": cases,
    }
    dump_json(output_path / "summary.json", aggregate)
    _write_csv(csv_rows, output_path / "summary.csv")

    lines = ["Static-background infall resolution sweep summary:"]
    for scenario in scenarios:
        lines.append(f"Scenario: {scenario}")
        for case in [entry for entry in cases if entry["scenario"] == scenario]:
            if case["status"] != "completed":
                lines.append(f"- N = {case['grid_n']}: failed with {case['error']}")
                continue
            summary = case["summary"]
            ratio_075 = summary["crossings"].get("0.75", {}).get("time_ratio")
            ratio_050 = summary["crossings"].get("0.50", {}).get("time_ratio")
            lines.append(
                f"- N = {case['grid_n']}: dx = {summary['dx']:.4f}, "
                f"Rg/dx = {summary['initial_compactness_cells']:.3f}, "
                f"r0/Rg = {summary['initial_radius_over_initial_compactness']:.3f}, "
                f"t(0.75r0)/toracle = {ratio_075 if ratio_075 is not None else 'n/a'}, "
                f"t(0.50r0)/toracle = {ratio_050 if ratio_050 is not None else 'n/a'}"
            )
    (output_path / "plain_language_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Sweep radial infall behavior across grid resolutions")
    parser.add_argument("--config", required=True, help="Sweep config path")
    args = parser.parse_args()

    output_path = run(args.config)
    summary = load_json_config(output_path / "summary.json")
    print(f"run_name: {summary['run_name']}")
    for case in summary["cases"]:
        if case["status"] == "completed":
            crossing = case["summary"]["crossings"].get("0.50", {})
            ratio = crossing.get("time_ratio")
            print(
                f"{case['scenario']} N={case['grid_n']}: "
                f"Rg/dx={case['summary']['initial_compactness_cells']:.3f}, "
                f"t(0.50r0)/toracle={ratio if ratio is not None else 'n/a'}"
            )
        else:
            print(f"{case['scenario']} N={case['grid_n']}: failed ({case['error']})")


if __name__ == "__main__":
    main()
