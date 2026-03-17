from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

import numpy as np

from src.physics.orbit_diagnostics import (
    effective_orbit_kinematics,
    specific_orbital_energy,
    angular_momentum_z,
    summarize_effective_orbit_conservation,
)


STAGE_ORDER = ("start", "linear1", "nonlinear", "sponge", "linear2", "refill")
TRANSITION_ORDER = (
    ("linear1", "start"),
    ("nonlinear", "linear1"),
    ("sponge", "nonlinear"),
    ("linear2", "sponge"),
    ("refill", "linear2"),
)


@dataclass
class OperatorBudgetRecorder:
    stage_time: dict[str, list[float]] = field(default_factory=lambda: {stage: [] for stage in STAGE_ORDER})
    stage_position: dict[str, list[list[float]]] = field(default_factory=lambda: {stage: [] for stage in STAGE_ORDER})
    stage_total_norm: dict[str, list[float]] = field(default_factory=lambda: {stage: [] for stage in STAGE_ORDER})

    def record(
        self,
        *,
        stage: str,
        time: float,
        position: Sequence[float],
        total_norm: float,
    ) -> None:
        if stage not in self.stage_time:
            raise ValueError(f"Unknown operator-budget stage: {stage}")
        self.stage_time[stage].append(float(time))
        self.stage_position[stage].append([float(value) for value in position])
        self.stage_total_norm[stage].append(float(total_norm))

    def arrays(self) -> dict[str, dict[str, np.ndarray]]:
        return {
            stage: {
                "time": np.asarray(self.stage_time[stage], dtype=np.float64),
                "position": np.asarray(self.stage_position[stage], dtype=np.float64),
                "total_norm": np.asarray(self.stage_total_norm[stage], dtype=np.float64),
            }
            for stage in STAGE_ORDER
        }


def summarize_delta(values_before: np.ndarray, values_after: np.ndarray) -> dict[str, float]:
    before = np.asarray(values_before, dtype=np.float64)
    after = np.asarray(values_after, dtype=np.float64)
    if before.shape != after.shape:
        raise ValueError("values_before and values_after must have matching shapes")
    if before.ndim != 1:
        raise ValueError("delta summaries expect one-dimensional arrays")
    if before.size == 0:
        raise ValueError("Need at least one sample to summarize operator deltas")
    delta = after - before
    cumulative = np.cumsum(delta)
    return {
        "mean_delta": float(np.mean(delta)),
        "mean_abs_delta": float(np.mean(np.abs(delta))),
        "max_abs_delta": float(np.max(np.abs(delta))),
        "cumulative_delta": float(np.sum(delta)),
        "max_abs_cumulative_delta": float(np.max(np.abs(cumulative))),
    }


def summarize_operator_budget(
    recorder: OperatorBudgetRecorder,
    *,
    source_center: Sequence[float],
    potential_fn,
    mu: float,
    fit_start_index: int = 0,
) -> dict[str, Any]:
    stage_arrays = recorder.arrays()
    per_stage: dict[str, dict[str, Any]] = {}
    stage_scalars: dict[str, dict[str, np.ndarray]] = {}

    for stage in STAGE_ORDER:
        times = stage_arrays[stage]["time"]
        positions = stage_arrays[stage]["position"]
        total_norm = stage_arrays[stage]["total_norm"]
        if times.size == 0:
            continue
        if positions.ndim != 2 or positions.shape[0] != times.size:
            raise ValueError(f"Operator-budget stage {stage} has inconsistent position samples")
        conservation = summarize_effective_orbit_conservation(
            time=times,
            positions=positions,
            source_center=source_center,
            potential_fn=potential_fn,
            mu=mu,
            fit_start_index=min(int(fit_start_index), max(times.size - 1, 0)),
        )
        kinematics = effective_orbit_kinematics(
            time=times,
            positions=positions,
            source_center=source_center,
            mu=mu,
        )
        energy_series = specific_orbital_energy(positions, kinematics["velocity"], potential_fn=potential_fn)
        angular_momentum_series = angular_momentum_z(
            positions,
            kinematics["velocity"],
            source_center=source_center,
        )
        per_stage[stage] = {
            "sample_count": int(times.size),
            "orbital_energy_summary": conservation["orbital_energy_summary"],
            "angular_momentum_z_summary": conservation["angular_momentum_z_summary"],
            "drag_audit_summary": conservation["drag_audit_summary"],
            "total_norm_summary": {
                "initial": float(total_norm[0]),
                "final": float(total_norm[-1]),
                "min": float(np.min(total_norm)),
                "max": float(np.max(total_norm)),
                "max_abs_drift": float(np.max(np.abs(total_norm - total_norm[0]))),
                "max_rel_drift": float(
                    np.max(np.abs(total_norm - total_norm[0])) / max(abs(float(total_norm[0])), 1.0e-12)
                ),
            },
        }
        stage_scalars[stage] = {
            "orbital_energy": energy_series,
            "angular_momentum_z": angular_momentum_series,
            "total_norm": total_norm,
            "mean_tangential_speed": np.asarray(kinematics["tangential_speed"], dtype=np.float64),
        }

    transitions: dict[str, dict[str, Any]] = {}
    for after, before in TRANSITION_ORDER:
        if before not in stage_scalars or after not in stage_scalars:
            continue
        transition_key = f"{before}_to_{after}"
        transitions[transition_key] = {
            "orbital_energy": summarize_delta(
                stage_scalars[before]["orbital_energy"],
                stage_scalars[after]["orbital_energy"],
            ),
            "angular_momentum_z": summarize_delta(
                stage_scalars[before]["angular_momentum_z"],
                stage_scalars[after]["angular_momentum_z"],
            ),
            "total_norm": summarize_delta(
                stage_scalars[before]["total_norm"],
                stage_scalars[after]["total_norm"],
            ),
            "mean_tangential_speed": summarize_delta(
                stage_scalars[before]["mean_tangential_speed"],
                stage_scalars[after]["mean_tangential_speed"],
            ),
        }

    return {
        "stages": per_stage,
        "transitions": transitions,
    }
