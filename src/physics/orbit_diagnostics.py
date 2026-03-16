from __future__ import annotations

from typing import Any, Callable, Sequence

import numpy as np

from src.physics.fitting import estimate_beta_eff, estimate_planar_orbit_shape, fit_orbit_precession


def finite_difference_velocity(
    positions: np.ndarray,
    times: np.ndarray,
) -> np.ndarray:
    coords = np.asarray(positions, dtype=np.float64)
    time = np.asarray(times, dtype=np.float64)
    if coords.ndim != 2 or coords.shape[0] != time.size:
        raise ValueError("positions must have shape (num_samples, dim) and match the time array")
    if time.size < 3:
        raise ValueError("Need at least three samples to estimate velocity by finite differences")
    velocity = np.empty_like(coords, dtype=np.float64)
    for axis in range(coords.shape[1]):
        velocity[:, axis] = np.gradient(coords[:, axis], time, edge_order=2)
    return velocity


def specific_orbital_energy(
    positions: np.ndarray,
    velocities: np.ndarray,
    potential_fn: Callable[[np.ndarray], float],
) -> np.ndarray:
    coords = np.asarray(positions, dtype=np.float64)
    speed_sq = np.sum(np.asarray(velocities, dtype=np.float64) ** 2, axis=1)
    potential = np.asarray([float(potential_fn(position)) for position in coords], dtype=np.float64)
    return 0.5 * speed_sq + potential


def angular_momentum_z(
    positions: np.ndarray,
    velocities: np.ndarray,
    source_center: Sequence[float] = (0.0, 0.0, 0.0),
) -> np.ndarray:
    coords = np.asarray(positions, dtype=np.float64) - np.asarray(source_center, dtype=np.float64)[None, :]
    velocity = np.asarray(velocities, dtype=np.float64)
    if coords.shape[1] < 3 or velocity.shape[1] < 3:
        raise ValueError("positions and velocities must provide three spatial components")
    return np.cross(coords, velocity, axis=1)[:, 2]


def summarize_scalar_drift(
    values: np.ndarray,
    fit_start_index: int = 0,
) -> dict[str, float]:
    series = np.asarray(values, dtype=np.float64)[int(fit_start_index) :]
    if series.size == 0:
        raise ValueError("Need at least one sample to summarize drift")
    initial = float(series[0])
    delta = series - initial
    scale = max(abs(initial), 1.0e-12)
    return {
        "initial": initial,
        "mean": float(np.mean(series)),
        "min": float(np.min(series)),
        "max": float(np.max(series)),
        "max_abs_drift": float(np.max(np.abs(delta))),
        "rms_drift": float(np.sqrt(np.mean(delta**2))),
        "max_rel_drift": float(np.max(np.abs(delta)) / scale),
        "rms_rel_drift": float(np.sqrt(np.mean(delta**2)) / scale),
    }


def summarize_effective_orbit_conservation(
    time: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray | None = None,
    source_center: Sequence[float] = (0.0, 0.0, 0.0),
    potential_fn: Callable[[np.ndarray], float] | None = None,
    mu: float | None = None,
    fit_start_index: int = 0,
) -> dict[str, Any]:
    time_array = np.asarray(time, dtype=np.float64)
    coords = np.asarray(positions, dtype=np.float64)
    if coords.ndim != 2 or coords.shape[0] != time_array.size:
        raise ValueError("positions must have shape (num_samples, dim) and match the time array")

    if velocities is None:
        velocity_array = finite_difference_velocity(coords, time_array)
        velocity_source = "finite_difference"
    else:
        velocity_array = np.asarray(velocities, dtype=np.float64)
        if velocity_array.shape != coords.shape:
            raise ValueError("velocities must match the shape of positions")
        velocity_source = "provided"

    if potential_fn is None:
        if mu is None:
            raise ValueError("mu must be provided when potential_fn is omitted")

        def kepler_potential(position: np.ndarray) -> float:
            relative = np.asarray(position, dtype=np.float64) - np.asarray(source_center, dtype=np.float64)
            radius_value = max(float(np.linalg.norm(relative)), 1.0e-12)
            return -float(mu) / radius_value

        potential = kepler_potential
        potential_source = "point_kepler"
    else:
        potential = potential_fn
        potential_source = "custom"

    energy = specific_orbital_energy(coords, velocity_array, potential_fn=potential)
    angular_momentum = angular_momentum_z(coords, velocity_array, source_center=source_center)
    return {
        "velocity_source": velocity_source,
        "potential_source": potential_source,
        "orbital_energy_summary": summarize_scalar_drift(energy, fit_start_index=fit_start_index),
        "angular_momentum_z_summary": summarize_scalar_drift(angular_momentum, fit_start_index=fit_start_index),
    }


def summarize_planar_orbit_trace(
    time: np.ndarray,
    positions: np.ndarray,
    mu: float,
    c_eff: float,
    velocities: np.ndarray | None = None,
    source_center: Sequence[float] = (0.0, 0.0, 0.0),
    potential_fn: Callable[[np.ndarray], float] | None = None,
    fit_start_index: int = 0,
    turning_point_min_spacing: int = 1,
    turning_point_smooth_window: int = 1,
    turning_point_min_spacing_fraction: float = 0.35,
    turning_point_prominence_fraction: float = 0.08,
) -> dict[str, Any]:
    time_array = np.asarray(time, dtype=np.float64)
    coords = np.asarray(positions, dtype=np.float64)
    if coords.ndim != 2 or coords.shape[0] != time_array.size or coords.shape[1] < 2:
        raise ValueError("positions must have shape (num_samples, 2+) and match the time array")

    relative_positions = coords - np.asarray(source_center, dtype=np.float64)[None, :]
    fit_slice = slice(int(fit_start_index), None)
    fit_positions = relative_positions[fit_slice]
    fit_time = time_array[fit_slice]
    if fit_positions.shape[0] < 16:
        raise ValueError("Need at least 16 samples in the orbit fit window")

    precession = fit_orbit_precession(
        positions=fit_positions,
        times=fit_time,
        min_spacing=turning_point_min_spacing,
        smooth_window=turning_point_smooth_window,
        min_spacing_fraction=turning_point_min_spacing_fraction,
        prominence_fraction=turning_point_prominence_fraction,
    )
    shape = estimate_planar_orbit_shape(
        positions=fit_positions,
        min_spacing=turning_point_min_spacing,
        smooth_window=turning_point_smooth_window,
        min_spacing_fraction=turning_point_min_spacing_fraction,
        prominence_fraction=turning_point_prominence_fraction,
    )
    beta_eff = estimate_beta_eff(
        delta_phi=precession["delta_phi"],
        semi_major_axis=shape["semi_major_axis"],
        eccentricity=shape["eccentricity"],
        mu=mu,
        c_eff=c_eff,
    )
    radius = np.sqrt(fit_positions[:, 0] ** 2 + fit_positions[:, 1] ** 2)

    conservation = summarize_effective_orbit_conservation(
        time=time_array,
        positions=coords,
        velocities=velocities,
        source_center=source_center,
        potential_fn=potential_fn,
        mu=mu,
        fit_start_index=fit_start_index,
    )

    return {
        "fit_start_index": int(fit_start_index),
        "turning_point_min_spacing": int(turning_point_min_spacing),
        "turning_point_smooth_window": int(turning_point_smooth_window),
        "turning_point_min_spacing_fraction": float(turning_point_min_spacing_fraction),
        "turning_point_prominence_fraction": float(turning_point_prominence_fraction),
        "velocity_source": conservation["velocity_source"],
        "potential_source": conservation["potential_source"],
        "characteristic_period_samples": int(precession["characteristic_period_samples"]),
        "candidate_periapse_count": int(len(precession["candidate_periapse_times"])),
        "periapse_count": int(len(precession["periapse_times"])),
        "candidate_periapse_times": precession["candidate_periapse_times"].tolist(),
        "delta_phi": float(precession["delta_phi"]),
        "delta_phi_stderr": float(precession["delta_phi_stderr"]),
        "phase_increment": float(precession["phase_increment"]),
        "periapse_times": precession["periapse_times"].tolist(),
        "periapse_angles": precession["periapse_angles"].tolist(),
        "beta_eff": float(beta_eff),
        "semi_major_axis": float(shape["semi_major_axis"]),
        "eccentricity": float(shape["eccentricity"]),
        "periapsis_radius": float(shape["periapsis_radius"]),
        "apoapsis_radius": float(shape["apoapsis_radius"]),
        "mean_fit_radius": float(np.mean(radius)),
        "orbital_energy_summary": conservation["orbital_energy_summary"],
        "angular_momentum_z_summary": conservation["angular_momentum_z_summary"],
    }
