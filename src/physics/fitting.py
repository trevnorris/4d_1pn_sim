from __future__ import annotations

import math
from typing import Any

import numpy as np


def fit_loglog_slope(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    log_x = np.log(np.asarray(x, dtype=np.float64))
    log_y = np.log(np.asarray(y, dtype=np.float64))
    design = np.stack([log_x, np.ones_like(log_x)], axis=1)
    coeffs, _, _, _ = np.linalg.lstsq(design, log_y, rcond=None)
    slope, intercept = coeffs
    residual = log_y - design @ coeffs
    variance = float(np.sum(residual**2) / max(len(log_x) - 2, 1))
    covariance = variance * np.linalg.pinv(design.T @ design)
    slope_stderr = float(np.sqrt(max(covariance[0, 0], 0.0)))
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "slope_stderr": slope_stderr,
    }


def lockin_amplitude(
    signal: np.ndarray,
    time: np.ndarray,
    omega: float,
    cycles_to_skip: int = 0,
) -> np.ndarray:
    signal_array = np.asarray(signal)
    time_array = np.asarray(time, dtype=np.float64)
    start_time = 0.0
    if cycles_to_skip > 0:
        start_time = 2.0 * math.pi * cycles_to_skip / omega
    mask = time_array >= start_time
    if np.count_nonzero(mask) < 8:
        mask = np.ones_like(time_array, dtype=bool)
    phase = np.exp(-1j * omega * time_array[mask])
    return np.mean(signal_array[..., mask] * phase, axis=-1)


def extract_effective_response(
    effort_ports: np.ndarray,
    flux_ports: np.ndarray,
    time: np.ndarray,
    omega: float,
    cycles_to_skip: int = 0,
) -> dict[str, Any]:
    effort_amp = lockin_amplitude(effort_ports, time, omega, cycles_to_skip=cycles_to_skip)
    flux_amp = lockin_amplitude(flux_ports, time, omega, cycles_to_skip=cycles_to_skip)
    effort_amp = np.atleast_2d(effort_amp)
    flux_amp = np.atleast_2d(flux_amp)
    try:
        z_eff = flux_amp @ np.linalg.inv(effort_amp)
    except np.linalg.LinAlgError:
        z_eff = flux_amp @ np.linalg.pinv(effort_amp)
    return {
        "effort_amplitude": effort_amp,
        "flux_amplitude": flux_amp,
        "Z_eff": z_eff,
    }


def fit_orbit_precession(positions: np.ndarray, times: np.ndarray) -> dict[str, Any]:
    coords = np.asarray(positions, dtype=np.float64)
    times_array = np.asarray(times, dtype=np.float64)
    if coords.ndim != 2 or coords.shape[1] < 2:
        raise ValueError("positions must have shape (num_samples, 2+) for periapsis fitting")

    x = coords[:, 0]
    y = coords[:, 1]
    radius = np.sqrt(x**2 + y**2)
    candidate_indices = np.where((radius[1:-1] < radius[:-2]) & (radius[1:-1] <= radius[2:]))[0] + 1
    if candidate_indices.size < 3:
        raise ValueError("Need at least three periapses to fit precession")

    periapse_angles = np.unwrap(np.arctan2(y[candidate_indices], x[candidate_indices]))
    orbit_index = np.arange(candidate_indices.size, dtype=np.float64)
    design = np.stack([orbit_index, np.ones_like(orbit_index)], axis=1)
    coeffs, _, _, _ = np.linalg.lstsq(design, periapse_angles, rcond=None)
    slope, intercept = coeffs
    residual = periapse_angles - design @ coeffs
    variance = float(np.sum(residual**2) / max(candidate_indices.size - 2, 1))
    covariance = variance * np.linalg.pinv(design.T @ design)
    slope_stderr = float(np.sqrt(max(covariance[0, 0], 0.0)))
    delta_phi = float(slope)
    return {
        "periapse_indices": candidate_indices,
        "periapse_times": times_array[candidate_indices],
        "periapse_angles": periapse_angles,
        "phase_increment": float(slope),
        "delta_phi": delta_phi,
        "delta_phi_stderr": slope_stderr,
        "intercept": float(intercept),
    }
