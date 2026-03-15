import math

from src.core.targets import k_vec_target, load_reference_targets


def test_symbolic_targets_match_required_regression_values() -> None:
    targets = load_reference_targets()
    assert targets["n"] == 5.0
    assert targets["kappa_add"] == 0.5
    assert targets["alpha_sq"] == 0.75
    assert math.isclose(targets["K_vec"], 2.0 / math.pi**2, rel_tol=1.0e-15)
    assert targets["kappa_PV"] == 1.5
    assert targets["energy_partition"] == {"E_w": 11.0, "E_f": 2.0, "E_PV": 5.0}
    assert targets["dln_a_dln_rho"] == -57.0 / 64.0
    assert targets["beta_1PN"] == 3.0
    assert targets["eih_cross_coefficients"] == {"v_dot_v": -3.5, "v_n_v_n": -0.5}
    assert math.isclose(k_vec_target(), targets["K_vec"], rel_tol=1.0e-15)
