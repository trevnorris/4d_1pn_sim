from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np

from src.physics.background_sources import StaticCentralBackground
from src.physics.orbit_diagnostics import summarize_planar_orbit_trace


@dataclass(frozen=True)
class PointParticleState:
    position: np.ndarray
    velocity: np.ndarray


def leapfrog_step(
    state: PointParticleState,
    dt: float,
    background: StaticCentralBackground,
) -> PointParticleState:
    acceleration = np.asarray(background.acceleration_at_position(state.position), dtype=np.float64)
    velocity_half = state.velocity + 0.5 * dt * acceleration
    position_next = state.position + dt * velocity_half
    acceleration_next = np.asarray(background.acceleration_at_position(position_next), dtype=np.float64)
    velocity_next = velocity_half + 0.5 * dt * acceleration_next
    return PointParticleState(position=position_next, velocity=velocity_next)


def initial_state_from_periapsis(
    periapsis_radius: float,
    eccentricity: float,
    background: StaticCentralBackground,
    velocity_scale: float = 1.0,
) -> PointParticleState:
    speed = background.periapsis_speed(periapsis_radius, eccentricity) * velocity_scale
    position = np.array([periapsis_radius, 0.0, 0.0], dtype=np.float64)
    velocity = np.array([0.0, speed, 0.0], dtype=np.float64)
    return PointParticleState(position=position, velocity=velocity)


def run_point_particle_trajectory(
    background: StaticCentralBackground,
    initial_position: np.ndarray,
    initial_velocity: np.ndarray,
    dt: float,
    steps: int,
) -> dict[str, np.ndarray]:
    state = PointParticleState(
        position=np.asarray(initial_position, dtype=np.float64).copy(),
        velocity=np.asarray(initial_velocity, dtype=np.float64).copy(),
    )
    time = np.empty(steps, dtype=np.float64)
    position = np.empty((steps, 3), dtype=np.float64)
    velocity = np.empty((steps, 3), dtype=np.float64)
    radius = np.empty(steps, dtype=np.float64)

    for idx in range(steps):
        state = leapfrog_step(state, dt=dt, background=background)
        time[idx] = (idx + 1) * dt
        position[idx] = state.position
        velocity[idx] = state.velocity
        radius[idx] = np.linalg.norm(state.position[:2])

    return {
        "time": time,
        "position": position,
        "velocity": velocity,
        "orbital_radius": radius,
    }


def run_point_particle_orbit(
    background: StaticCentralBackground,
    periapsis_radius: float,
    eccentricity: float,
    dt: float,
    steps: int,
    velocity_scale: float = 1.0,
) -> dict[str, np.ndarray]:
    state = initial_state_from_periapsis(
        periapsis_radius=periapsis_radius,
        eccentricity=eccentricity,
        background=background,
        velocity_scale=velocity_scale,
    )
    return run_point_particle_trajectory(
        background=background,
        initial_position=state.position,
        initial_velocity=state.velocity,
        dt=dt,
        steps=steps,
    )


def summarize_point_particle_orbit(
    trajectory: dict[str, np.ndarray],
    mu: float,
    c_eff: float,
    source_center: tuple[float, float, float] = (0.0, 0.0, 0.0),
    potential_fn=None,
    fit_start_index: int = 0,
    turning_point_min_spacing: int = 1,
    turning_point_smooth_window: int = 1,
    turning_point_min_spacing_fraction: float = 0.35,
    turning_point_prominence_fraction: float = 0.08,
) -> dict[str, Any]:
    return summarize_planar_orbit_trace(
        time=trajectory["time"],
        positions=trajectory["position"],
        velocities=trajectory["velocity"],
        mu=mu,
        c_eff=c_eff,
        source_center=source_center,
        potential_fn=potential_fn,
        fit_start_index=fit_start_index,
        turning_point_min_spacing=turning_point_min_spacing,
        turning_point_smooth_window=turning_point_smooth_window,
        turning_point_min_spacing_fraction=turning_point_min_spacing_fraction,
        turning_point_prominence_fraction=turning_point_prominence_fraction,
    )
