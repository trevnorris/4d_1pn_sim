import math

from src.physics.orbit_oracles import evaluate_orbit_oracle


def test_orbit_oracle_newtonian_beta_zero() -> None:
    result = evaluate_orbit_oracle(
        beta_eff=0.0,
        mu=6.0,
        c_eff=24.0,
        semi_major_axis=1.8,
        eccentricity=0.25,
    )
    assert abs(result["fit_beta_eff"]) < 0.2
    assert abs(result["fit_delta_phi"]) < 5.0e-3


def test_orbit_oracle_positive_beta_sign_and_magnitude() -> None:
    result = evaluate_orbit_oracle(
        beta_eff=3.0,
        mu=6.0,
        c_eff=24.0,
        semi_major_axis=1.8,
        eccentricity=0.25,
    )
    assert result["fit_beta_eff"] > 0.0
    assert abs(result["fit_beta_eff"] - 3.0) / 3.0 < 0.15
    assert result["fit_delta_phi_stderr"] < 0.25 * abs(result["fit_delta_phi"])


def test_orbit_oracle_negative_beta_sign_and_magnitude() -> None:
    target = -2.0
    result = evaluate_orbit_oracle(
        beta_eff=target,
        mu=6.0,
        c_eff=24.0,
        semi_major_axis=1.8,
        eccentricity=0.25,
    )
    assert result["fit_beta_eff"] < 0.0
    assert abs(result["fit_beta_eff"] - target) / abs(target) < 0.15
    assert result["fit_delta_phi_stderr"] < 0.25 * abs(result["fit_delta_phi"])
