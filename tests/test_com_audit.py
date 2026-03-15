import numpy as np

from src.physics.com_audit import fit_ballistic_trajectory, fit_constant_acceleration_trajectory


def test_ballistic_fit_recovers_uniform_translation() -> None:
    time = np.linspace(0.0, 4.0, 201)
    velocity = np.array([0.5, -0.25, 0.1])
    origin = np.array([1.0, 2.0, -3.0])
    positions = origin[None, :] + time[:, None] * velocity[None, :]

    fit = fit_ballistic_trajectory(time, positions)

    assert fit["rms_residual"] < 1.0e-12
    assert np.allclose(fit["initial_position"], origin)
    assert np.allclose(fit["initial_velocity"], velocity)


def test_constant_acceleration_fit_recovers_quadratic_motion() -> None:
    time = np.linspace(0.0, 3.0, 151)
    origin = np.array([0.3, -0.2, 0.5])
    velocity = np.array([0.8, 0.1, -0.4])
    acceleration = np.array([-0.25, 0.5, 0.0])
    positions = origin[None, :] + time[:, None] * velocity[None, :] + 0.5 * (time[:, None] ** 2) * acceleration[None, :]

    fit = fit_constant_acceleration_trajectory(time, positions)

    assert fit["rms_residual"] < 1.0e-12
    assert np.allclose(fit["initial_position"], origin)
    assert np.allclose(fit["initial_velocity"], velocity)
    assert np.allclose(fit["acceleration"], acceleration)
    assert abs(fit["acceleration_norm"] - np.linalg.norm(acceleration)) < 1.0e-12
