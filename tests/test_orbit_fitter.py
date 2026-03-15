import math

import numpy as np

from src.physics.fitting import fit_orbit_precession


def test_orbit_fitter_recovers_manufactured_precession() -> None:
    semi_major = 1.7
    eccentricity = 0.25
    precession = 0.035
    theta = np.linspace(0.0, 18.0 * 2.0 * math.pi, 12000, endpoint=False)
    reduced_angle = theta / (1.0 + precession / (2.0 * math.pi))
    radius = semi_major * (1.0 - eccentricity**2) / (1.0 + eccentricity * np.cos(reduced_angle))
    positions = np.stack([radius * np.cos(theta), radius * np.sin(theta)], axis=1)
    times = np.linspace(0.0, 18.0, theta.size, endpoint=False)

    fit = fit_orbit_precession(positions=positions, times=times)
    assert abs(fit["delta_phi"] - precession) < 3.0e-3
    assert fit["delta_phi_stderr"] < 1.0e-2
