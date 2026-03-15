from __future__ import annotations

from typing import Any

import numpy as np


def _design_matrix(time: np.ndarray, degree: int) -> np.ndarray:
    columns = [np.ones_like(time)]
    if degree >= 1:
        columns.append(time)
    if degree >= 2:
        columns.append(0.5 * time * time)
    return np.stack(columns, axis=1)


def _fit_polynomial_trajectory(time: np.ndarray, positions: np.ndarray, degree: int) -> dict[str, Any]:
    fit_time = np.asarray(time, dtype=np.float64)
    fit_positions = np.asarray(positions, dtype=np.float64)
    if fit_time.ndim != 1:
        raise ValueError("time must be one-dimensional")
    if fit_positions.ndim != 2 or fit_positions.shape[1] != 3:
        raise ValueError("positions must have shape (samples, 3)")
    if fit_positions.shape[0] != fit_time.size:
        raise ValueError("time and positions must have matching sample counts")

    shifted_time = fit_time - fit_time[0]
    design = _design_matrix(shifted_time, degree=degree)
    coeffs, _, _, _ = np.linalg.lstsq(design, fit_positions, rcond=None)
    fitted = design @ coeffs
    residual = fit_positions - fitted
    residual_norm = np.linalg.norm(residual, axis=1)
    summary = {
        "rms_residual": float(np.sqrt(np.mean(residual_norm**2))),
        "max_residual": float(np.max(residual_norm)),
        "initial_position": coeffs[0].tolist(),
        "initial_velocity": coeffs[1].tolist() if degree >= 1 else [0.0, 0.0, 0.0],
    }
    if degree >= 2:
        summary["acceleration"] = coeffs[2].tolist()
        summary["acceleration_norm"] = float(np.linalg.norm(coeffs[2]))
    return summary


def fit_ballistic_trajectory(time: np.ndarray, positions: np.ndarray) -> dict[str, Any]:
    return _fit_polynomial_trajectory(time, positions, degree=1)


def fit_constant_acceleration_trajectory(time: np.ndarray, positions: np.ndarray) -> dict[str, Any]:
    return _fit_polynomial_trajectory(time, positions, degree=2)
