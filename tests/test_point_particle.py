import numpy as np

from src.physics.background_sources import StaticCentralBackground
from src.physics.point_particle import (
    initial_state_from_periapsis,
    run_point_particle_orbit,
    run_point_particle_trajectory,
    summarize_point_particle_orbit,
)


def test_point_particle_pure_kepler_has_small_precession() -> None:
    background = StaticCentralBackground(
        profile="pure_kepler",
        mu=6.0,
        softening_length=0.0,
        core_radius=1.0e-6,
        center=(0.0, 0.0, 0.0),
        c_eff=24.0,
        rho_reference=1.0,
    )
    trajectory = run_point_particle_orbit(
        background=background,
        periapsis_radius=3.2,
        eccentricity=0.2,
        dt=0.01,
        steps=16000,
    )
    summary = summarize_point_particle_orbit(
        trajectory=trajectory,
        mu=background.mu,
        c_eff=background.c_eff,
        fit_start_index=500,
        turning_point_min_spacing=500,
        turning_point_smooth_window=9,
    )
    assert abs(summary["beta_eff"]) < 0.2


def test_run_point_particle_trajectory_matches_periapsis_constructor() -> None:
    background = StaticCentralBackground(
        profile="pure_kepler",
        mu=6.0,
        softening_length=0.0,
        core_radius=1.0e-6,
        center=(0.0, 0.0, 0.0),
        c_eff=24.0,
        rho_reference=1.0,
    )
    periapsis_radius = 5.0
    eccentricity = 0.1
    dt = 0.02
    steps = 256
    initial_state = initial_state_from_periapsis(
        periapsis_radius=periapsis_radius,
        eccentricity=eccentricity,
        background=background,
    )

    from_constructor = run_point_particle_orbit(
        background=background,
        periapsis_radius=periapsis_radius,
        eccentricity=eccentricity,
        dt=dt,
        steps=steps,
    )
    from_trajectory = run_point_particle_trajectory(
        background=background,
        initial_position=initial_state.position,
        initial_velocity=initial_state.velocity,
        dt=dt,
        steps=steps,
    )

    for key in ("time", "position", "velocity", "orbital_radius"):
        assert np.allclose(from_constructor[key], from_trajectory[key])
