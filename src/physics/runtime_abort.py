from __future__ import annotations

import math
from typing import Any, Sequence

import numpy as np


def boundary_clearance(position: Sequence[float], box_lengths: Sequence[float]) -> float:
    coords = np.asarray(position, dtype=np.float64)
    lengths = np.asarray(box_lengths, dtype=np.float64)
    if coords.ndim != 1 or lengths.ndim != 1 or coords.size < lengths.size:
        raise ValueError("position must be one-dimensional and provide at least one value per box axis")
    half_lengths = 0.5 * lengths
    return float(np.min(half_lengths - np.abs(coords[: lengths.size])))


def evaluate_runtime_abort_check(
    conservation_summary: dict[str, Any],
    light_metrics: dict[str, float],
    continuity_metrics: dict[str, float],
    min_boundary_clearance: float,
    thresholds: dict[str, float],
) -> dict[str, Any]:
    observed = {
        "max_rel_energy_drift": float(conservation_summary["orbital_energy_summary"]["max_rel_drift"]),
        "max_rel_angular_momentum_drift": float(
            conservation_summary["angular_momentum_z_summary"]["max_rel_drift"]
        ),
        "mean_coherence": float(light_metrics["mean_coherence"]),
        "mean_higher_mode_fraction": float(light_metrics["mean_higher_mode_fraction"]),
        "mean_leakage": float(continuity_metrics["mean_leakage"]),
        "min_boundary_clearance": float(min_boundary_clearance),
    }
    finite_metrics = all(math.isfinite(value) for value in observed.values())
    gates = {
        "finite_metrics": finite_metrics,
        "max_rel_energy_drift": finite_metrics
        and observed["max_rel_energy_drift"] <= float(thresholds["max_rel_energy_drift"]),
        "max_rel_angular_momentum_drift": finite_metrics
        and observed["max_rel_angular_momentum_drift"] <= float(thresholds["max_rel_angular_momentum_drift"]),
        "min_coherence": finite_metrics and observed["mean_coherence"] >= float(thresholds["min_coherence"]),
        "max_higher_mode_fraction": finite_metrics
        and observed["mean_higher_mode_fraction"] <= float(thresholds["max_higher_mode_fraction"]),
        "max_leakage": finite_metrics and observed["mean_leakage"] <= float(thresholds["max_leakage"]),
        "min_boundary_clearance": finite_metrics
        and observed["min_boundary_clearance"] >= float(thresholds["min_boundary_clearance"]),
    }
    failed_gates = [name for name, passed in gates.items() if not passed]
    return {
        "triggered": bool(failed_gates),
        "failed_gates": failed_gates,
        "gates": gates,
        "observed": observed,
    }
