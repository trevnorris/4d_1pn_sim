from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import torch

from src.core.config import load_json_config
from src.core.io import collect_runtime_info, dump_json, ensure_dir
from src.experiments.common import build_solver, prepare_relaxed_state
from src.physics.background_sources import StaticCentralBackground
from src.physics.launch_calibration import (
    probe_launch_response,
    safe_launch_speed_limit,
    summarize_launch_calibration,
)


def _calibration_config(config: dict) -> dict:
    return dict(config.get("launch_calibration", {}))


def _velocity_scale_samples(calibration: dict, safe_scale_limit: float) -> list[float]:
    configured = calibration.get("velocity_scale_samples")
    if configured:
        return [float(value) for value in configured if float(value) > 0.0]
    upper = max(min(1.25, safe_scale_limit), 0.4)
    return np.linspace(0.5, upper, 6, dtype=np.float64).tolist()


def run(
    config_path: str | Path,
    output_dir: str | Path,
    scenario: str | None = None,
    periapsis_radius_override: float | None = None,
    target_velocity_scale_override: float | None = None,
) -> Path:
    config = load_json_config(config_path)
    seed = int(config["seed"])
    np.random.seed(seed)
    torch.manual_seed(seed)

    calibration = _calibration_config(config)
    output_path = ensure_dir(output_dir, overwrite=True)
    dump_json(output_path / "runtime.json", collect_runtime_info(seed))
    dump_json(output_path / "config.json", config)

    solver, _ = build_solver(config)
    rho0 = float(config["geometry"]["reference_rho"])
    relaxed = prepare_relaxed_state(solver=solver, config=config, rho_ambient=rho0)
    background = StaticCentralBackground.from_config(config["background"], rho_reference=rho0)
    background_potential = background.potential_field(solver.grid).to(solver.grid.real_dtype)
    scenario_name = scenario or str(calibration.get("scenario", "source_no_dressing"))
    dressing = scenario_name == "source_with_dressing"
    use_source = scenario_name in {"source_no_dressing", "source_with_dressing"}
    periapsis_radius = float(
        periapsis_radius_override if periapsis_radius_override is not None else config["experiment"]["periapsis_radius"]
    )
    eccentricity = float(config["experiment"]["eccentricity"])

    base_speed = background.periapsis_speed(
        periapsis_radius,
        eccentricity,
    )
    target_scale = float(
        target_velocity_scale_override
        if target_velocity_scale_override is not None
        else config["experiment"].get("velocity_scale", 1.0)
    )
    target_speed = base_speed * target_scale
    nyquist_fraction = float(calibration.get("safe_nyquist_fraction", 0.65))
    safe_speed = safe_launch_speed_limit(solver, nyquist_fraction=nyquist_fraction)
    safe_scale_limit = safe_speed / max(base_speed, 1.0e-12)
    boundary_clearance_floor = 3.0 * max(float(dx) for dx in solver.grid.dx)
    dt = float(config["solver"]["dt"])
    probe_steps = int(calibration.get("probe_steps", 160))
    measure_start_step = int(calibration.get("measure_start_step", 8))
    measure_end_step = calibration.get("measure_end_step")
    measure_end_step = int(measure_end_step) if measure_end_step is not None else None

    probes = []
    for velocity_scale in _velocity_scale_samples(calibration, safe_scale_limit=safe_scale_limit):
        applied_speed = base_speed * velocity_scale
        if applied_speed > safe_speed:
            continue
        probe = probe_launch_response(
            solver=solver,
            state=relaxed,
            applied_speed=applied_speed,
            shift=(periapsis_radius, 0.0, 0.0),
            dt=dt,
            steps=probe_steps,
            source_center=background.center,
            rho_reference=rho0,
            external_potential=background_potential if use_source else None,
            ambient_density_fn=background.ambient_density_at_position if dressing else None,
            measure_start_step=measure_start_step,
            measure_end_step=measure_end_step,
        )
        probe["velocity_scale"] = float(velocity_scale)
        probes.append(probe)

    summary = summarize_launch_calibration(
        probes=probes,
        target_speed=target_speed,
        safe_speed_limit=safe_speed,
        boundary_clearance_floor=boundary_clearance_floor,
    )
    summary.update(
        {
            "scenario": scenario_name,
            "base_periapsis_speed": float(base_speed),
            "target_velocity_scale": target_scale,
            "periapsis_radius": periapsis_radius,
            "eccentricity": eccentricity,
            "safe_scale_limit": float(safe_scale_limit),
            "safe_nyquist_fraction": nyquist_fraction,
            "boundary_clearance_floor": float(boundary_clearance_floor),
            "probe_steps": probe_steps,
            "measure_start_step": measure_start_step,
            "measure_end_step": measure_end_step,
        }
    )
    dump_json(output_path / "summary.json", summary)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Calibrate defect launch speed against realized COM tangential speed")
    parser.add_argument("--config", required=True, help="Experiment config path")
    parser.add_argument("--output-dir", required=True, help="Directory for calibration outputs")
    parser.add_argument(
        "--scenario",
        choices=["free_translation", "source_no_dressing", "source_with_dressing"],
        default=None,
        help="Optional scenario override",
    )
    parser.add_argument("--periapsis-radius", type=float, default=None, help="Optional periapsis-radius override")
    parser.add_argument("--target-velocity-scale", type=float, default=None, help="Optional target velocity-scale override")
    args = parser.parse_args()

    output_dir = run(
        config_path=args.config,
        output_dir=args.output_dir,
        scenario=args.scenario,
        periapsis_radius_override=args.periapsis_radius,
        target_velocity_scale_override=args.target_velocity_scale,
    )
    summary = load_json_config(Path(output_dir) / "summary.json")
    print(f"scenario: {summary['scenario']}")
    print(f"target_speed: {summary['target_speed']:.6f}")
    print(f"safe_speed_limit: {summary['safe_speed_limit']:.6f}")
    print(f"recommended_applied_speed: {summary['recommended_applied_speed']:.6f}")
    print(f"recommended_realized_tangential_speed: {summary['recommended_realized_tangential_speed']:.6f}")
    print(f"target_reachable: {summary['target_reachable']}")
    print(f"recommended_window_usable: {summary['recommended_window_usable']}")


if __name__ == "__main__":
    main()
