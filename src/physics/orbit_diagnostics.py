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


def finite_difference_acceleration(
    velocities: np.ndarray,
    times: np.ndarray,
) -> np.ndarray:
    velocity = np.asarray(velocities, dtype=np.float64)
    time = np.asarray(times, dtype=np.float64)
    if velocity.ndim != 2 or velocity.shape[0] != time.size:
        raise ValueError("velocities must have shape (num_samples, dim) and match the time array")
    if time.size < 3:
        raise ValueError("Need at least three samples to estimate acceleration by finite differences")
    acceleration = np.empty_like(velocity, dtype=np.float64)
    for axis in range(velocity.shape[1]):
        acceleration[:, axis] = np.gradient(velocity[:, axis], time, edge_order=2)
    return acceleration


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


def effective_orbit_kinematics(
    time: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray | None = None,
    source_center: Sequence[float] = (0.0, 0.0, 0.0),
    mu: float | None = None,
) -> dict[str, np.ndarray]:
    time_array = np.asarray(time, dtype=np.float64)
    coords = np.asarray(positions, dtype=np.float64)
    if coords.ndim != 2 or coords.shape[0] != time_array.size or coords.shape[1] < 3:
        raise ValueError("positions must have shape (num_samples, 3+) and match the time array")

    if velocities is None:
        velocity_array = finite_difference_velocity(coords, time_array)
    else:
        velocity_array = np.asarray(velocities, dtype=np.float64)
        if velocity_array.shape != coords.shape:
            raise ValueError("velocities must match the shape of positions")
    acceleration_array = finite_difference_acceleration(velocity_array, time_array)

    relative = coords - np.asarray(source_center, dtype=np.float64)[None, :]
    radius_vec = relative[:, :2]
    planar_velocity = velocity_array[:, :2]
    planar_acceleration = acceleration_array[:, :2]
    radius = np.linalg.norm(radius_vec, axis=1)
    safe_radius = np.maximum(radius, 1.0e-12)
    radial_hat = radius_vec / safe_radius[:, None]
    tangential_hat = np.stack([-radial_hat[:, 1], radial_hat[:, 0]], axis=1)

    radial_speed = np.sum(planar_velocity * radial_hat, axis=1)
    tangential_speed = np.sum(planar_velocity * tangential_hat, axis=1)
    radial_acceleration = np.sum(planar_acceleration * radial_hat, axis=1)
    tangential_acceleration = np.sum(planar_acceleration * tangential_hat, axis=1)

    if mu is None:
        kepler_radial_acceleration = np.full_like(radius, np.nan, dtype=np.float64)
        radial_residual_acceleration = np.full_like(radius, np.nan, dtype=np.float64)
        power_residual = np.full_like(radius, np.nan, dtype=np.float64)
    else:
        kepler_radial_acceleration = -float(mu) / safe_radius**2
        radial_residual_acceleration = radial_acceleration - kepler_radial_acceleration
        kepler_acceleration = kepler_radial_acceleration[:, None] * radial_hat
        power_residual = np.sum(planar_velocity * (planar_acceleration - kepler_acceleration), axis=1)

    specific_torque_z = np.cross(relative, acceleration_array, axis=1)[:, 2]
    return {
        "velocity": velocity_array,
        "acceleration": acceleration_array,
        "radius": radius,
        "radial_speed": radial_speed,
        "tangential_speed": tangential_speed,
        "radial_acceleration": radial_acceleration,
        "tangential_acceleration": tangential_acceleration,
        "kepler_radial_acceleration": kepler_radial_acceleration,
        "radial_residual_acceleration": radial_residual_acceleration,
        "specific_torque_z": specific_torque_z,
        "power_residual": power_residual,
    }


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


def summarize_drag_like_residuals(
    time: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray | None = None,
    source_center: Sequence[float] = (0.0, 0.0, 0.0),
    mu: float | None = None,
    fit_start_index: int = 0,
) -> dict[str, float]:
    kinematics = effective_orbit_kinematics(
        time=time,
        positions=positions,
        velocities=velocities,
        source_center=source_center,
        mu=mu,
    )

    start = int(fit_start_index)

    def _summary(name: str) -> tuple[float, float]:
        values = np.asarray(kinematics[name], dtype=np.float64)[start:]
        values = values[np.isfinite(values)]
        if values.size == 0:
            return float("nan"), float("nan")
        return float(np.mean(values)), float(np.max(np.abs(values)))

    mean_tangential_acceleration, max_abs_tangential_acceleration = _summary("tangential_acceleration")
    mean_specific_torque_z, max_abs_specific_torque_z = _summary("specific_torque_z")
    mean_power_residual, max_abs_power_residual = _summary("power_residual")
    mean_radial_residual_acceleration, max_abs_radial_residual_acceleration = _summary("radial_residual_acceleration")
    mean_radial_speed, _ = _summary("radial_speed")
    mean_tangential_speed, _ = _summary("tangential_speed")
    return {
        "mean_tangential_acceleration": mean_tangential_acceleration,
        "max_abs_tangential_acceleration": max_abs_tangential_acceleration,
        "mean_specific_torque_z": mean_specific_torque_z,
        "max_abs_specific_torque_z": max_abs_specific_torque_z,
        "mean_power_residual": mean_power_residual,
        "max_abs_power_residual": max_abs_power_residual,
        "mean_radial_residual_acceleration": mean_radial_residual_acceleration,
        "max_abs_radial_residual_acceleration": max_abs_radial_residual_acceleration,
        "mean_radial_speed": mean_radial_speed,
        "mean_tangential_speed": mean_tangential_speed,
    }


def summarize_box_density_audit(
    sample_times: np.ndarray,
    total_norm: np.ndarray,
    orbit_radius: np.ndarray,
    *,
    box_volume: float,
    start_time: float = 0.0,
    end_time: float | None = None,
) -> dict[str, float | int | None]:
    times = np.asarray(sample_times, dtype=np.float64)
    norm = np.asarray(total_norm, dtype=np.float64)
    radius = np.asarray(orbit_radius, dtype=np.float64)
    if times.ndim != 1 or norm.ndim != 1 or radius.ndim != 1:
        raise ValueError("sample_times, total_norm, and orbit_radius must be one-dimensional")
    if not (times.size == norm.size == radius.size):
        raise ValueError("sample_times, total_norm, and orbit_radius must have the same length")
    if times.size == 0:
        raise ValueError("Need at least one density sample")

    if end_time is None:
        end_time = float(times[-1])
    mask = (times >= float(start_time)) & (times <= float(end_time))
    if not np.any(mask):
        nearest = int(np.argmin(np.abs(times - 0.5 * (float(start_time) + float(end_time)))))
        mask[nearest] = True

    window_norm = norm[mask]
    window_radius = radius[mask]
    density = window_norm / max(float(box_volume), 1.0e-12)
    initial_norm = float(window_norm[0])
    initial_density = float(density[0])
    norm_drop = initial_norm - window_norm
    density_drop = initial_density - density

    radius_density_correlation: float | None
    if window_norm.size < 2 or np.std(window_norm) < 1.0e-12 or np.std(window_radius) < 1.0e-12:
        radius_density_correlation = None
    else:
        radius_density_correlation = float(np.corrcoef(window_norm, window_radius)[0, 1])

    return {
        "window_sample_count": int(window_norm.size),
        "initial_total_norm": initial_norm,
        "final_total_norm": float(window_norm[-1]),
        "min_total_norm": float(np.min(window_norm)),
        "mean_total_norm": float(np.mean(window_norm)),
        "max_abs_total_norm_drop": float(np.max(norm_drop)),
        "max_rel_total_norm_drop": float(np.max(norm_drop) / max(abs(initial_norm), 1.0e-12)),
        "initial_mean_box_density": initial_density,
        "final_mean_box_density": float(density[-1]),
        "min_mean_box_density": float(np.min(density)),
        "mean_mean_box_density": float(np.mean(density)),
        "max_abs_mean_box_density_drop": float(np.max(density_drop)),
        "max_rel_mean_box_density_drop": float(np.max(density_drop) / max(abs(initial_density), 1.0e-12)),
        "radius_total_norm_correlation": radius_density_correlation,
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
        "drag_audit_summary": summarize_drag_like_residuals(
            time=time_array,
            positions=coords,
            velocities=velocity_array,
            source_center=source_center,
            mu=mu,
            fit_start_index=fit_start_index,
        ),
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
        "drag_audit_summary": conservation["drag_audit_summary"],
    }
