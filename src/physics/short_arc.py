from __future__ import annotations

from typing import Any, Sequence

import numpy as np

from src.physics.launch_calibration import estimate_box_clearance


def summarize_short_arc_match(
    time: np.ndarray,
    tracer_positions: np.ndarray,
    defect_positions: np.ndarray,
    source_center: Sequence[float],
    box_length: Sequence[float],
    start_index: int = 0,
    end_index: int | None = None,
) -> dict[str, Any]:
    times = np.asarray(time, dtype=np.float64)
    tracer = np.asarray(tracer_positions, dtype=np.float64)
    defect = np.asarray(defect_positions, dtype=np.float64)
    if tracer.shape != defect.shape or tracer.ndim != 2 or tracer.shape[1] < 2:
        raise ValueError("tracer_positions and defect_positions must have matching shape (num_samples, 2+)")
    if times.ndim != 1 or times.size != tracer.shape[0]:
        raise ValueError("time must be one-dimensional and match the trajectory length")

    lower = max(int(start_index), 0)
    upper = tracer.shape[0] if end_index is None else min(int(end_index), tracer.shape[0])
    if upper - lower < 3:
        raise ValueError("Need at least three samples in the short-arc comparison window")

    center = np.asarray(source_center, dtype=np.float64)
    tracer_window = tracer[lower:upper]
    defect_window = defect[lower:upper]
    tracer_vec = tracer_window[:, :2] - center[None, :2]
    defect_vec = defect_window[:, :2] - center[None, :2]
    tracer_radius = np.linalg.norm(tracer_vec, axis=1)
    defect_radius = np.linalg.norm(defect_vec, axis=1)
    tracer_angle = np.unwrap(np.arctan2(tracer_vec[:, 1], tracer_vec[:, 0]))
    defect_angle = np.unwrap(np.arctan2(defect_vec[:, 1], defect_vec[:, 0]))

    position_error = np.linalg.norm(defect_window[:, :3] - tracer_window[:, :3], axis=1)
    radius_error = defect_radius - tracer_radius
    phase_error = defect_angle - tracer_angle
    initial_radius = float(max(tracer_radius[0], 1.0e-12))
    boundary_summary = estimate_box_clearance(
        positions=defect,
        box_length=box_length,
        start_index=lower,
        end_index=upper,
    )

    return {
        "compare_start_index": int(lower),
        "compare_end_index": int(upper),
        "window_duration": float(times[upper - 1] - times[lower]),
        "tracer_angular_sweep": float(tracer_angle[-1] - tracer_angle[0]),
        "defect_angular_sweep": float(defect_angle[-1] - defect_angle[0]),
        "angular_sweep_error": float((defect_angle[-1] - defect_angle[0]) - (tracer_angle[-1] - tracer_angle[0])),
        "position_rms": float(np.sqrt(np.mean(position_error**2))),
        "position_max": float(np.max(position_error)),
        "normalized_position_rms": float(np.sqrt(np.mean(position_error**2)) / initial_radius),
        "radius_rms": float(np.sqrt(np.mean(radius_error**2))),
        "radius_max_abs": float(np.max(np.abs(radius_error))),
        "normalized_radius_rms": float(np.sqrt(np.mean(radius_error**2)) / initial_radius),
        "phase_rms": float(np.sqrt(np.mean(phase_error**2))),
        "phase_max_abs": float(np.max(np.abs(phase_error))),
        "boundary_summary": boundary_summary,
        "initial_radius": initial_radius,
    }


def evaluate_short_arc_acceptance(
    short_arc_summary: dict[str, Any],
    defect_metrics: dict[str, float],
    thresholds: dict[str, float],
) -> dict[str, Any]:
    gates = {
        "min_angular_sweep": float(short_arc_summary["defect_angular_sweep"]) >= float(thresholds["min_angular_sweep"]),
        "max_angular_sweep_error": abs(float(short_arc_summary["angular_sweep_error"]))
        <= float(thresholds["max_angular_sweep_error"]),
        "max_normalized_position_rms": float(short_arc_summary["normalized_position_rms"])
        <= float(thresholds["max_normalized_position_rms"]),
        "max_normalized_radius_rms": float(short_arc_summary["normalized_radius_rms"])
        <= float(thresholds["max_normalized_radius_rms"]),
        "max_phase_rms": float(short_arc_summary["phase_rms"]) <= float(thresholds["max_phase_rms"]),
        "min_boundary_clearance": float(short_arc_summary["boundary_summary"]["min_boundary_clearance"])
        >= float(thresholds["min_boundary_clearance"]),
        "min_coherence": float(defect_metrics["mean_coherence"]) >= float(thresholds["min_coherence"]),
        "max_higher_mode_fraction": float(defect_metrics["mean_higher_mode_fraction"])
        <= float(thresholds["max_higher_mode_fraction"]),
        "max_leakage": float(defect_metrics["mean_leakage"]) <= float(thresholds["max_leakage"]),
    }
    return {
        "passes": bool(all(gates.values())),
        "gates": gates,
    }
