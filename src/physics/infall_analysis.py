from __future__ import annotations

import math
from typing import Any, Sequence

import numpy as np


def find_first_crossing_time(
    time: np.ndarray,
    radius: np.ndarray,
    target_radius: float,
) -> float | None:
    times = np.asarray(time, dtype=np.float64)
    values = np.asarray(radius, dtype=np.float64)
    if times.ndim != 1 or values.ndim != 1 or times.size != values.size:
        raise ValueError("time and radius must be one-dimensional arrays with matching length")
    if times.size == 0:
        return None

    target = float(target_radius)
    crossed = np.flatnonzero(values <= target)
    if crossed.size == 0:
        return None
    idx = int(crossed[0])
    if idx == 0:
        return float(times[0])

    t0 = float(times[idx - 1])
    t1 = float(times[idx])
    r0 = float(values[idx - 1])
    r1 = float(values[idx])
    denom = r0 - r1
    if abs(denom) < 1.0e-12:
        return t1
    fraction = (r0 - target) / denom
    fraction = min(max(fraction, 0.0), 1.0)
    return t0 + fraction * (t1 - t0)


def newtonian_radial_infall_time(
    mu: float,
    initial_radius: float,
    target_radius: float,
) -> float:
    mu_value = float(mu)
    radius_0 = float(initial_radius)
    radius_t = float(target_radius)
    if mu_value <= 0.0:
        raise ValueError("mu must be positive")
    if radius_0 <= 0.0:
        raise ValueError("initial_radius must be positive")
    if radius_t < 0.0 or radius_t > radius_0:
        raise ValueError("target_radius must satisfy 0 <= target_radius <= initial_radius")
    if abs(radius_t - radius_0) < 1.0e-12:
        return 0.0

    x = min(max(radius_t / radius_0, 0.0), 1.0)
    return math.sqrt(radius_0**3 / (2.0 * mu_value)) * (
        math.acos(math.sqrt(x)) + math.sqrt(x * (1.0 - x))
    )


def estimate_initial_radial_acceleration(
    time: np.ndarray,
    radius: np.ndarray,
    window_size: int = 33,
) -> dict[str, float]:
    times = np.asarray(time, dtype=np.float64)
    values = np.asarray(radius, dtype=np.float64)
    if times.ndim != 1 or values.ndim != 1 or times.size != values.size:
        raise ValueError("time and radius must be one-dimensional arrays with matching length")
    count = min(int(window_size), times.size)
    if count < 3:
        raise ValueError("Need at least three samples to estimate radial acceleration")

    fit_time = times[:count] - float(times[0])
    design = np.stack(
        [
            np.ones_like(fit_time),
            fit_time,
            0.5 * fit_time * fit_time,
        ],
        axis=1,
    )
    coeffs, _, _, _ = np.linalg.lstsq(design, values[:count], rcond=None)
    fitted = design @ coeffs
    residual = values[:count] - fitted
    return {
        "initial_radius": float(coeffs[0]),
        "initial_radial_speed": float(coeffs[1]),
        "initial_radial_acceleration": float(coeffs[2]),
        "fit_rms_residual": float(np.sqrt(np.mean(residual**2))),
        "window_size": float(count),
    }


def summarize_static_infall_run(
    time: np.ndarray,
    positions: np.ndarray,
    source_center: Sequence[float],
    mu: float,
    compactness: np.ndarray,
    coherence: np.ndarray,
    higher_mode_fraction: np.ndarray,
    leakage: np.ndarray,
    target_radius_fractions: Sequence[float],
) -> dict[str, Any]:
    times = np.asarray(time, dtype=np.float64)
    coords = np.asarray(positions, dtype=np.float64)
    if coords.ndim != 2 or coords.shape[1] < 3:
        raise ValueError("positions must have shape (num_samples, 3+)")
    center = np.asarray(source_center, dtype=np.float64)
    radius = np.linalg.norm(coords[:, :3] - center[None, :3], axis=1)
    initial_radius = float(radius[0])
    accel_fit = estimate_initial_radial_acceleration(times, radius)
    oracle_initial_acceleration = -float(mu) / max(initial_radius**2, 1.0e-12)
    accel_denom = (
        oracle_initial_acceleration
        if abs(oracle_initial_acceleration) > 1.0e-12
        else -1.0e-12
    )

    smallest_fraction = min(float(value) for value in target_radius_fractions)
    smallest_target_radius = smallest_fraction * initial_radius
    smallest_crossing_time = find_first_crossing_time(times, radius, smallest_target_radius)
    pre_target_end = times.size
    if smallest_crossing_time is not None:
        crossed = np.flatnonzero(radius <= smallest_target_radius)
        if crossed.size > 0:
            pre_target_end = int(crossed[0]) + 1

    crossings: dict[str, Any] = {}
    for fraction_value in target_radius_fractions:
        fraction = float(fraction_value)
        target_radius = fraction * initial_radius
        measured_time = find_first_crossing_time(times, radius, target_radius)
        oracle_time = newtonian_radial_infall_time(mu=float(mu), initial_radius=initial_radius, target_radius=target_radius)
        ratio = None if measured_time is None else float(measured_time / max(oracle_time, 1.0e-12))
        error = None if measured_time is None else float(measured_time - oracle_time)
        crossings[f"{fraction:.2f}"] = {
            "target_radius": float(target_radius),
            "measured_time": None if measured_time is None else float(measured_time),
            "oracle_time": float(oracle_time),
            "time_ratio": ratio,
            "time_error": error,
            "reached": bool(measured_time is not None),
        }

    prefix = slice(0, max(pre_target_end, 1))
    return {
        "initial_radius": initial_radius,
        "final_radius": float(radius[-1]),
        "min_radius": float(np.min(radius)),
        "max_radius": float(np.max(radius)),
        "mean_radius": float(np.mean(radius)),
        "initial_radial_fit": accel_fit,
        "oracle_initial_radial_acceleration": float(oracle_initial_acceleration),
        "initial_radial_acceleration_ratio": float(accel_fit["initial_radial_acceleration"] / accel_denom),
        "crossings": crossings,
        "pre_target_mean_coherence": float(np.mean(np.asarray(coherence, dtype=np.float64)[prefix])),
        "pre_target_mean_higher_mode_fraction": float(
            np.mean(np.asarray(higher_mode_fraction, dtype=np.float64)[prefix])
        ),
        "pre_target_mean_leakage": float(np.mean(np.asarray(leakage, dtype=np.float64)[prefix])),
        "initial_compactness": float(np.asarray(compactness, dtype=np.float64)[0]),
        "mean_compactness": float(np.mean(np.asarray(compactness, dtype=np.float64)[prefix])),
        "final_compactness": float(np.asarray(compactness, dtype=np.float64)[-1]),
        "pre_target_sample_count": int(pre_target_end),
    }
