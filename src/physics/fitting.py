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


def estimate_characteristic_period_samples(values: np.ndarray) -> int:
    array = np.asarray(values, dtype=np.float64)
    if array.size < 16:
        return max(array.size, 1)
    centered = array - float(np.mean(array))
    if not np.any(centered):
        return max(array.size, 1)
    window = np.hanning(array.size)
    spectrum = np.fft.rfft(centered * window)
    power = np.abs(spectrum) ** 2
    if power.size <= 1 or not np.any(power[1:] > 0.0):
        return max(array.size, 1)
    dominant_mode = int(np.argmax(power[1:]) + 1)
    return max(int(round(array.size / dominant_mode)), 1)


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


def _extremum_prominence(values: np.ndarray, idx: int, kind: str, neighborhood: int) -> float:
    radius = np.asarray(values, dtype=np.float64)
    width = max(int(neighborhood), 1)
    left = radius[max(0, idx - width) : idx]
    right = radius[idx + 1 : min(radius.size, idx + width + 1)]
    if left.size == 0 or right.size == 0:
        return 0.0
    if kind == "min":
        return float(min(np.max(left), np.max(right)) - radius[idx])
    if kind == "max":
        return float(radius[idx] - max(np.min(left), np.min(right)))
    raise ValueError("kind must be 'min' or 'max'")


def _filter_by_prominence(
    indices: np.ndarray,
    values: np.ndarray,
    kind: str,
    neighborhood: int,
    min_prominence: float,
) -> np.ndarray:
    accepted = [
        int(idx)
        for idx in np.asarray(indices, dtype=np.int64)
        if _extremum_prominence(values, int(idx), kind=kind, neighborhood=neighborhood) >= min_prominence
    ]
    return np.asarray(accepted, dtype=np.int64)


def _select_stable_suffix(
    indices: np.ndarray,
    times: np.ndarray,
    expected_period_time: float,
    min_periapses: int,
    interval_tolerance: float,
) -> np.ndarray:
    extrema = np.asarray(indices, dtype=np.int64)
    times_array = np.asarray(times, dtype=np.float64)
    if extrema.size < min_periapses:
        return extrema

    best: tuple[int, float, int] | None = None
    best_suffix: np.ndarray | None = None
    min_interval = 0.5 * max(float(expected_period_time), 1.0e-12)
    for start in range(extrema.size - min_periapses + 1):
        suffix = extrema[start:]
        if suffix.size < min_periapses:
            continue
        intervals = np.diff(times_array[suffix])
        if intervals.size == 0:
            continue
        median_interval = float(np.median(intervals))
        if median_interval <= 0.0 or float(np.min(intervals)) < min_interval:
            continue
        max_fractional_deviation = float(np.max(np.abs(intervals - median_interval)) / median_interval)
        if max_fractional_deviation > interval_tolerance:
            continue
        score = (-suffix.size, max_fractional_deviation, -start)
        if best is None or score < best:
            best = score
            best_suffix = suffix

    if best_suffix is None:
        return np.asarray([], dtype=np.int64)
    return best_suffix


def find_turning_points(
    radius: np.ndarray,
    kind: str,
    min_spacing: int = 1,
    smooth_window: int = 1,
    min_spacing_fraction: float = 0.35,
    prominence_fraction: float = 0.08,
) -> np.ndarray:
    radius_array = np.asarray(radius, dtype=np.float64)
    working = _moving_average(radius_array, smooth_window)
    characteristic_period = estimate_characteristic_period_samples(working)
    dynamic_spacing = max(int(min_spacing), int(math.ceil(min_spacing_fraction * characteristic_period)), 1)
    neighborhood = max(dynamic_spacing // 2, 1)
    min_prominence = max(prominence_fraction * float(np.ptp(working)), 1.0e-9)
    if kind == "min":
        mask = (working[1:-1] < working[:-2]) & (working[1:-1] <= working[2:])
    elif kind == "max":
        mask = (working[1:-1] > working[:-2]) & (working[1:-1] >= working[2:])
    else:
        raise ValueError("kind must be 'min' or 'max'")
    raw_indices = np.where(mask)[0] + 1
    clustered = _cluster_extrema(raw_indices, working, kind=kind, min_spacing=dynamic_spacing)
    return _filter_by_prominence(
        clustered,
        working,
        kind=kind,
        neighborhood=neighborhood,
        min_prominence=min_prominence,
    )


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
    min_spacing_fraction: float = 0.35,
    prominence_fraction: float = 0.08,
    min_periapses: int = 3,
    interval_tolerance: float = 0.35,
) -> dict[str, Any]:
    coords = np.asarray(positions, dtype=np.float64)
    times_array = np.asarray(times, dtype=np.float64)
    if coords.ndim != 2 or coords.shape[1] < 2:
        raise ValueError("positions must have shape (num_samples, 2+) for periapsis fitting")

    x = coords[:, 0]
    y = coords[:, 1]
    radius = np.sqrt(x**2 + y**2)
    characteristic_period_samples = estimate_characteristic_period_samples(_moving_average(radius, smooth_window))
    candidate_indices = find_turning_points(
        radius,
        kind="min",
        min_spacing=min_spacing,
        smooth_window=smooth_window,
        min_spacing_fraction=min_spacing_fraction,
        prominence_fraction=prominence_fraction,
    )
    if candidate_indices.size < min_periapses:
        raise ValueError("Need at least three periapses to fit precession")
    median_dt = float(np.median(np.diff(times_array))) if times_array.size > 1 else 1.0
    stable_indices = _select_stable_suffix(
        candidate_indices,
        times_array,
        expected_period_time=characteristic_period_samples * median_dt,
        min_periapses=min_periapses,
        interval_tolerance=interval_tolerance,
    )
    if stable_indices.size < min_periapses:
        raise ValueError("Need at least three well-separated periapses to fit precession")

    periapse_angles = np.unwrap(np.arctan2(y[stable_indices], x[stable_indices]))
    orbit_index = np.arange(stable_indices.size, dtype=np.float64)
    design = np.stack([orbit_index, np.ones_like(orbit_index)], axis=1)
    coeffs, _, _, _ = np.linalg.lstsq(design, periapse_angles, rcond=None)
    slope, intercept = coeffs
    residual = periapse_angles - design @ coeffs
    variance = float(np.sum(residual**2) / max(stable_indices.size - 2, 1))
    covariance = variance * np.linalg.pinv(design.T @ design)
    slope_stderr = float(np.sqrt(max(covariance[0, 0], 0.0)))
    delta_phi = float(slope)
    return {
        "candidate_periapse_indices": candidate_indices,
        "candidate_periapse_times": times_array[candidate_indices],
        "periapse_indices": stable_indices,
        "periapse_times": times_array[stable_indices],
        "periapse_angles": periapse_angles,
        "phase_increment": float(slope),
        "delta_phi": delta_phi,
        "delta_phi_stderr": slope_stderr,
        "intercept": float(intercept),
        "characteristic_period_samples": int(characteristic_period_samples),
    }


def estimate_planar_orbit_shape(
    positions: np.ndarray,
    min_spacing: int = 1,
    smooth_window: int = 1,
    min_spacing_fraction: float = 0.35,
    prominence_fraction: float = 0.08,
) -> dict[str, float]:
    coords = np.asarray(positions, dtype=np.float64)
    radius = np.sqrt(coords[:, 0] ** 2 + coords[:, 1] ** 2)
    peri_indices = find_turning_points(
        radius,
        kind="min",
        min_spacing=min_spacing,
        smooth_window=smooth_window,
        min_spacing_fraction=min_spacing_fraction,
        prominence_fraction=prominence_fraction,
    )
    apo_indices = find_turning_points(
        radius,
        kind="max",
        min_spacing=min_spacing,
        smooth_window=smooth_window,
        min_spacing_fraction=min_spacing_fraction,
        prominence_fraction=prominence_fraction,
    )
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
