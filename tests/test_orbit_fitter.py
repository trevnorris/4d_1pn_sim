import math

import numpy as np

from src.physics.fitting import estimate_beta_eff, estimate_planar_orbit_shape, fit_orbit_precession


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


def test_planar_orbit_shape_and_beta_eff_helpers() -> None:
    semi_major = 2.9
    eccentricity = 0.2
    theta = np.linspace(0.0, 10.0 * 2.0 * math.pi, 6000, endpoint=False)
    radius = semi_major * (1.0 - eccentricity**2) / (1.0 + eccentricity * np.cos(theta))
    positions = np.stack([radius * np.cos(theta), radius * np.sin(theta)], axis=1)

    shape = estimate_planar_orbit_shape(positions)
    assert abs(shape["semi_major_axis"] - semi_major) < 5.0e-3
    assert abs(shape["eccentricity"] - eccentricity) < 5.0e-3

    beta_eff = estimate_beta_eff(
        delta_phi=0.06,
        semi_major_axis=shape["semi_major_axis"],
        eccentricity=shape["eccentricity"],
        mu=6.0,
        c_eff=24.0,
    )
    expected = 0.06 * 24.0**2 * semi_major / (2.0 * math.pi * 6.0) * (1.0 - eccentricity**2)
    assert abs(beta_eff - expected) < 1.0e-12
