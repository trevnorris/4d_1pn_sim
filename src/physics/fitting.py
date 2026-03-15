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


def _moving_average(values: np.ndarray, window: int) -> np.ndarray:
    if window <= 1:
        return values
    kernel = np.ones(window, dtype=np.float64) / float(window)
    return np.convolve(values, kernel, mode="same")


def _cluster_extrema(
    raw_indices: np.ndarray,
    values: np.ndarray,
    kind: str,
    min_spacing: int,
) -> np.ndarray:
    if raw_indices.size == 0:
        return raw_indices

    clusters: list[list[int]] = [[int(raw_indices[0])]]
    for idx in raw_indices[1:]:
        if int(idx) - clusters[-1][-1] < min_spacing:
            clusters[-1].append(int(idx))
        else:
            clusters.append([int(idx)])

    selected = []
    for cluster in clusters:
        if kind == "min":
            chosen = min(cluster, key=lambda i: values[i])
        else:
            chosen = max(cluster, key=lambda i: values[i])
        selected.append(chosen)
    return np.asarray(selected, dtype=np.int64)


def find_turning_points(
    radius: np.ndarray,
    kind: str,
    min_spacing: int = 1,
    smooth_window: int = 1,
) -> np.ndarray:
    radius_array = np.asarray(radius, dtype=np.float64)
    working = _moving_average(radius_array, smooth_window)
    if kind == "min":
        mask = (working[1:-1] < working[:-2]) & (working[1:-1] <= working[2:])
    elif kind == "max":
        mask = (working[1:-1] > working[:-2]) & (working[1:-1] >= working[2:])
    else:
        raise ValueError("kind must be 'min' or 'max'")
    raw_indices = np.where(mask)[0] + 1
    return _cluster_extrema(raw_indices, radius_array, kind=kind, min_spacing=max(int(min_spacing), 1))


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


def fit_orbit_precession(
    positions: np.ndarray,
    times: np.ndarray,
    min_spacing: int = 1,
    smooth_window: int = 1,
) -> dict[str, Any]:
    coords = np.asarray(positions, dtype=np.float64)
    times_array = np.asarray(times, dtype=np.float64)
    if coords.ndim != 2 or coords.shape[1] < 2:
        raise ValueError("positions must have shape (num_samples, 2+) for periapsis fitting")

    x = coords[:, 0]
    y = coords[:, 1]
    radius = np.sqrt(x**2 + y**2)
    candidate_indices = find_turning_points(radius, kind="min", min_spacing=min_spacing, smooth_window=smooth_window)
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


def estimate_planar_orbit_shape(
    positions: np.ndarray,
    min_spacing: int = 1,
    smooth_window: int = 1,
) -> dict[str, float]:
    coords = np.asarray(positions, dtype=np.float64)
    radius = np.sqrt(coords[:, 0] ** 2 + coords[:, 1] ** 2)
    peri_indices = find_turning_points(radius, kind="min", min_spacing=min_spacing, smooth_window=smooth_window)
    apo_indices = find_turning_points(radius, kind="max", min_spacing=min_spacing, smooth_window=smooth_window)
    if peri_indices.size == 0:
        raise ValueError("Need at least one periapsis to estimate orbit shape")

    peri_radius = float(np.median(radius[peri_indices]))
    apo_radius = float(np.median(radius[apo_indices])) if apo_indices.size else float(np.max(radius))
    semi_major_axis = 0.5 * (peri_radius + apo_radius)
    eccentricity = (apo_radius - peri_radius) / max(apo_radius + peri_radius, 1.0e-12)
    return {
        "periapsis_radius": peri_radius,
        "apoapsis_radius": apo_radius,
        "semi_major_axis": float(semi_major_axis),
        "eccentricity": float(eccentricity),
    }


def estimate_beta_eff(
    delta_phi: float,
    semi_major_axis: float,
    eccentricity: float,
    mu: float,
    c_eff: float,
) -> float:
    return float(delta_phi * c_eff**2 * semi_major_axis * (1.0 - eccentricity**2) / (2.0 * math.pi * mu))
