from __future__ import annotations

import math
from typing import Any, Sequence

import numpy as np

from src.physics.defects import displace_and_boost_state
from src.physics.matter_gnls import MatterSplitStepSolver, MatterState
from src.physics.observables import mode_occupations


def nyquist_wave_number_limit(solver: MatterSplitStepSolver) -> float:
    return min(math.pi / dx for dx in solver.grid.dx)


def safe_launch_speed_limit(solver: MatterSplitStepSolver, nyquist_fraction: float) -> float:
    safe_k = max(float(nyquist_fraction), 1.0e-6) * nyquist_wave_number_limit(solver)
    return safe_k / max(float(solver.mass), 1.0e-12)


def calibration_velocity_scale_samples(
    configured_samples: Sequence[float] | None,
    *,
    target_velocity_scale: float | None = None,
    safe_scale_limit: float | None = None,
) -> list[float]:
    if configured_samples:
        samples = [float(value) for value in configured_samples if float(value) > 0.0]
    else:
        safe_limit = 1.25 if safe_scale_limit is None else float(safe_scale_limit)
        upper = max(min(1.25, safe_limit), 0.4)
        samples = np.linspace(0.5, upper, 6, dtype=np.float64).tolist()
    if target_velocity_scale is not None and float(target_velocity_scale) > 0.0:
        samples.append(float(target_velocity_scale))
    unique_samples = sorted({round(float(value), 12): float(value) for value in samples}.values())
    return unique_samples


def _measurement_window_bounds(num_samples: int, start_index: int, end_index: int | None) -> tuple[int, int]:
    upper = num_samples if end_index is None else min(int(end_index), num_samples)
    lower = max(int(start_index), 0)
    if upper - lower < 3:
        raise ValueError("Need at least three samples in the measurement window")
    return lower, upper


def estimate_tangential_velocity(
    time: np.ndarray,
    positions: np.ndarray,
    source_center: Sequence[float],
    start_index: int,
    end_index: int | None,
) -> dict[str, float]:
    times = np.asarray(time, dtype=np.float64)
    coords = np.asarray(positions, dtype=np.float64)
    if coords.ndim != 2 or coords.shape[1] < 2:
        raise ValueError("positions must have shape (num_samples, 2+)")
    if times.ndim != 1 or times.size != coords.shape[0]:
        raise ValueError("time must be one-dimensional and match positions")

    lower, upper = _measurement_window_bounds(coords.shape[0], start_index=start_index, end_index=end_index)
    window_pos = coords[lower:upper]
    window_time = times[lower:upper]
    delta_t = np.diff(window_time)
    velocity = np.diff(window_pos, axis=0) / delta_t[:, None]
    midpoint = 0.5 * (window_pos[1:] + window_pos[:-1])

    center = np.asarray(source_center, dtype=np.float64)
    radius_vec = midpoint[:, :2] - center[None, :2]
    radius = np.linalg.norm(radius_vec, axis=1)
    radius = np.maximum(radius, 1.0e-12)
    planar_velocity = velocity[:, :2]
    radial_speed = np.sum(radius_vec * planar_velocity, axis=1) / radius
    tangential_speed = (radius_vec[:, 0] * planar_velocity[:, 1] - radius_vec[:, 1] * planar_velocity[:, 0]) / radius

    return {
        "mean_tangential_speed": float(np.mean(tangential_speed)),
        "std_tangential_speed": float(np.std(tangential_speed)),
        "mean_radial_speed": float(np.mean(radial_speed)),
        "std_radial_speed": float(np.std(radial_speed)),
        "mean_radius": float(np.mean(radius)),
    }


def estimate_box_clearance(
    positions: np.ndarray,
    box_length: Sequence[float],
    start_index: int,
    end_index: int | None,
) -> dict[str, float]:
    coords = np.asarray(positions, dtype=np.float64)
    if coords.ndim != 2 or coords.shape[1] < 3:
        raise ValueError("positions must have shape (num_samples, 3+) for box-clearance estimation")

    lower, upper = _measurement_window_bounds(coords.shape[0], start_index=start_index, end_index=end_index)
    window_pos = coords[lower:upper, :3]
    half_length = 0.5 * np.asarray(box_length, dtype=np.float64)
    if half_length.shape != (3,):
        raise ValueError("box_length must provide exactly three dimensions")
    clearance = half_length[None, :] - np.abs(window_pos)
    radial_clearance = np.min(clearance, axis=1)
    return {
        "min_boundary_clearance": float(np.min(radial_clearance)),
        "mean_boundary_clearance": float(np.mean(radial_clearance)),
    }


def probe_launch_response(
    solver: MatterSplitStepSolver,
    state: MatterState,
    applied_speed: float,
    shift: Sequence[float],
    dt: float,
    steps: int,
    source_center: Sequence[float],
    rho_reference: float,
    external_potential=None,
    node_amplitude_mask=None,
    refill_controller_factory=None,
    ambient_density_fn=None,
    measure_start_step: int = 4,
    measure_end_step: int | None = None,
) -> dict[str, Any]:
    launched = displace_and_boost_state(
        solver=solver,
        state=state,
        shift=(float(shift[0]), float(shift[1]), float(shift[2])),
        momentum=(0.0, solver.mass * float(applied_speed), 0.0),
    )
    positions: list[list[float]] = []
    time: list[float] = []
    current = launched
    refill_controller = None if refill_controller_factory is None else refill_controller_factory()
    refill_metrics_last: dict[str, float] | None = None
    for _ in range(int(steps)):
        center = solver.estimate_defect_center(current.psi_modes)
        if ambient_density_fn is None:
            rho_ambient = float(rho_reference)
        else:
            rho_ambient = float(ambient_density_fn(center.detach().cpu().tolist()))
        current = solver.step(
            current,
            dt=dt,
            rho_ambient=rho_ambient,
            external_potential=external_potential,
            node_amplitude_mask=node_amplitude_mask,
        )
        if refill_controller is not None:
            current, refill_metrics_last = refill_controller.apply(solver=solver, state=current, dt=dt)
        center = solver.estimate_defect_center(current.psi_modes).detach().cpu().numpy()
        positions.append(center.tolist())
        time.append(float(current.time))

    occupations = mode_occupations(current.psi_modes, solver.grid.cell_volume).detach().cpu().numpy()
    occupation_total = float(max(np.sum(occupations), 1.0e-12))
    velocity_summary = estimate_tangential_velocity(
        time=np.asarray(time, dtype=np.float64),
        positions=np.asarray(positions, dtype=np.float64),
        source_center=source_center,
        start_index=measure_start_step,
        end_index=measure_end_step,
    )
    boundary_summary = estimate_box_clearance(
        positions=np.asarray(positions, dtype=np.float64),
        box_length=solver.grid.length,
        start_index=measure_start_step,
        end_index=measure_end_step,
    )
    launch_radius = float(
        np.linalg.norm(np.asarray(shift, dtype=np.float64)[:2] - np.asarray(source_center, dtype=np.float64)[:2])
    )
    return {
        "applied_speed": float(applied_speed),
        "requested_momentum": float(solver.mass * applied_speed),
        "positions": np.asarray(positions, dtype=np.float64),
        "time": np.asarray(time, dtype=np.float64),
        "velocity_summary": velocity_summary,
        "launch_radius": launch_radius,
        "radius_bias": float(velocity_summary["mean_radius"] - launch_radius),
        "window_summary": boundary_summary,
        "final_higher_mode_fraction": float(np.sum(occupations[1:]) / occupation_total),
        "final_norm": float(solver.total_norm(current.psi_modes)),
        "refill_metrics": refill_metrics_last,
    }


def choose_best_launch_probe(
    probes: Sequence[dict[str, Any]],
    target_speed: float,
) -> dict[str, Any]:
    if not probes:
        raise ValueError("Need at least one launch probe to choose a recommendation")

    best_score = None
    best_probe = None
    for probe in probes:
        tangential = float(probe["velocity_summary"]["mean_tangential_speed"])
        radial = float(probe["velocity_summary"]["mean_radial_speed"])
        score = abs(tangential - target_speed) + 0.25 * abs(radial)
        if best_score is None or score < best_score:
            best_score = score
            best_probe = probe
    assert best_probe is not None
    return best_probe


def _probe_window_usable(
    probe: dict[str, Any],
    *,
    boundary_clearance_floor: float | None,
    radius_bias_tolerance_fraction: float,
) -> bool:
    recommended_window = dict(probe.get("window_summary", {}))
    launch_radius = float(probe.get("launch_radius", 0.0))
    radius_bias = float(probe.get("radius_bias", 0.0))
    within_radius_tolerance = True
    if launch_radius > 0.0:
        within_radius_tolerance = abs(radius_bias) <= float(radius_bias_tolerance_fraction) * launch_radius
    has_boundary_check = boundary_clearance_floor is not None and "min_boundary_clearance" in recommended_window
    sufficient_boundary_clearance = True
    if has_boundary_check:
        sufficient_boundary_clearance = (
            float(recommended_window["min_boundary_clearance"]) >= float(boundary_clearance_floor)
        )
    return bool(within_radius_tolerance and sufficient_boundary_clearance)


def find_launch_probe_for_speed(
    probes: Sequence[dict[str, Any]],
    target_speed: float,
    *,
    rel_tol: float = 1.0e-9,
    abs_tol: float = 1.0e-12,
) -> dict[str, Any] | None:
    for probe in probes:
        if math.isclose(float(probe["applied_speed"]), float(target_speed), rel_tol=rel_tol, abs_tol=abs_tol):
            return probe
    return None


def summarize_launch_calibration(
    probes: Sequence[dict[str, Any]],
    target_speed: float,
    safe_speed_limit: float,
    boundary_clearance_floor: float | None = None,
    radius_bias_tolerance_fraction: float = 0.02,
) -> dict[str, Any]:
    recommended = choose_best_launch_probe(probes, target_speed=target_speed)
    target_probe = find_launch_probe_for_speed(probes, target_speed=target_speed)
    max_realized = max(float(probe["velocity_summary"]["mean_tangential_speed"]) for probe in probes)
    recommended_window = dict(recommended.get("window_summary", {}))
    launch_radius = float(recommended.get("launch_radius", 0.0))
    radius_bias = float(recommended.get("radius_bias", 0.0))
    recommended_window_usable = _probe_window_usable(
        recommended,
        boundary_clearance_floor=boundary_clearance_floor,
        radius_bias_tolerance_fraction=radius_bias_tolerance_fraction,
    )
    target_probe_window_usable = None
    target_probe_velocity_summary = None
    target_probe_window_summary = None
    if target_probe is not None:
        target_probe_window_usable = _probe_window_usable(
            target_probe,
            boundary_clearance_floor=boundary_clearance_floor,
            radius_bias_tolerance_fraction=radius_bias_tolerance_fraction,
        )
        target_probe_velocity_summary = dict(target_probe["velocity_summary"])
        target_probe_window_summary = dict(target_probe.get("window_summary", {}))
    return {
        "target_speed": float(target_speed),
        "safe_speed_limit": float(safe_speed_limit),
        "recommended_applied_speed": float(recommended["applied_speed"]),
        "recommended_realized_tangential_speed": float(recommended["velocity_summary"]["mean_tangential_speed"]),
        "recommended_velocity_summary": dict(recommended["velocity_summary"]),
        "recommended_launch_radius": launch_radius,
        "recommended_radius_bias": radius_bias,
        "recommended_window_summary": recommended_window,
        "max_realized_tangential_speed": float(max_realized),
        "target_reachable": bool(max_realized >= 0.98 * target_speed),
        "recommended_window_usable": recommended_window_usable,
        "target_probe_available": bool(target_probe is not None),
        "target_probe_window_usable": target_probe_window_usable,
        "target_probe_velocity_summary": target_probe_velocity_summary,
        "target_probe_window_summary": target_probe_window_summary,
        "boundary_clearance_floor": None if boundary_clearance_floor is None else float(boundary_clearance_floor),
        "radius_bias_tolerance_fraction": float(radius_bias_tolerance_fraction),
        "probes": [
            {
                "applied_speed": float(probe["applied_speed"]),
                "requested_momentum": float(probe["requested_momentum"]),
                "velocity_summary": dict(probe["velocity_summary"]),
                "launch_radius": float(probe.get("launch_radius", 0.0)),
                "radius_bias": float(probe.get("radius_bias", 0.0)),
                "window_summary": dict(probe.get("window_summary", {})),
                "final_higher_mode_fraction": float(probe["final_higher_mode_fraction"]),
                "final_norm": float(probe["final_norm"]),
            }
            for probe in probes
        ],
    }


def resolve_launch_speed(
    calibration_summary: dict[str, Any] | None,
    *,
    target_speed: float,
) -> dict[str, Any]:
    if calibration_summary is None:
        return {
            "applied_speed": float(target_speed),
            "selection": "target_without_calibration",
            "velocity_summary": None,
        }
    safe_speed_limit = float(calibration_summary["safe_speed_limit"])
    target_probe_available = bool(calibration_summary.get("target_probe_available", False))
    target_probe_window_usable = calibration_summary.get("target_probe_window_usable")
    target_safe = float(target_speed) <= safe_speed_limit + 1.0e-12
    if target_safe and target_probe_available and bool(target_probe_window_usable):
        return {
            "applied_speed": float(target_speed),
            "selection": "target_probe",
            "velocity_summary": calibration_summary.get("target_probe_velocity_summary"),
        }
    return {
        "applied_speed": float(calibration_summary["recommended_applied_speed"]),
        "selection": "recommended_probe",
        "velocity_summary": calibration_summary.get("recommended_velocity_summary"),
    }
