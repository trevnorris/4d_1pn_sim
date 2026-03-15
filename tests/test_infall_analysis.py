import math

import numpy as np

from src.physics.infall_analysis import (
    estimate_initial_radial_acceleration,
    find_first_crossing_time,
    newtonian_radial_infall_time,
)


def test_find_first_crossing_time_interpolates_linearly() -> None:
    time = np.array([0.0, 1.0, 2.0], dtype=np.float64)
    radius = np.array([10.0, 8.0, 6.0], dtype=np.float64)

    crossing = find_first_crossing_time(time, radius, target_radius=7.0)

    assert crossing is not None
    assert abs(crossing - 1.5) < 1.0e-12


def test_newtonian_radial_infall_time_matches_full_collapse_limit() -> None:
    mu = 6.0
    radius = 16.0

    collapse_time = newtonian_radial_infall_time(mu=mu, initial_radius=radius, target_radius=0.0)
    expected = 0.5 * math.pi * math.sqrt(radius**3 / (2.0 * mu))

    assert abs(collapse_time - expected) < 1.0e-12


def test_estimate_initial_radial_acceleration_recovers_quadratic_motion() -> None:
    initial_radius = 16.0
    initial_speed = -0.1
    acceleration = -0.35
    time = np.linspace(0.0, 1.0, 64, dtype=np.float64)
    radius = initial_radius + initial_speed * time + 0.5 * acceleration * time * time

    summary = estimate_initial_radial_acceleration(time, radius, window_size=40)

    assert abs(summary["initial_radius"] - initial_radius) < 1.0e-10
    assert abs(summary["initial_radial_speed"] - initial_speed) < 1.0e-10
    assert abs(summary["initial_radial_acceleration"] - acceleration) < 1.0e-10
    assert summary["fit_rms_residual"] < 1.0e-12
