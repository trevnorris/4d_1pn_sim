from src.physics.newtonian_orbit_gate import evaluate_newtonian_orbit_gate


def test_evaluate_newtonian_orbit_gate_passes_clean_case() -> None:
    orbit_summary = {
        "periapse_count": 4,
        "beta_eff": 0.03,
        "orbital_energy_summary": {"max_rel_drift": 1.0e-3},
        "angular_momentum_z_summary": {"max_rel_drift": 5.0e-4},
    }
    defect_metrics = {
        "mean_coherence": 0.999,
        "mean_higher_mode_fraction": 0.004,
        "mean_leakage": 2.0e-8,
    }
    thresholds = {
        "min_periapse_count": 3,
        "max_abs_beta_eff": 0.2,
        "max_rel_energy_drift": 0.05,
        "max_rel_angular_momentum_drift": 0.05,
        "min_coherence": 0.995,
        "max_higher_mode_fraction": 0.01,
        "max_leakage": 1.0e-6,
    }

    gate = evaluate_newtonian_orbit_gate(orbit_summary, defect_metrics, thresholds)

    assert gate["passes"]
    assert all(gate["gates"].values())


def test_evaluate_newtonian_orbit_gate_fails_without_fit() -> None:
    orbit_summary = {
        "orbital_energy_summary": {"max_rel_drift": 1.0e-3},
        "angular_momentum_z_summary": {"max_rel_drift": 5.0e-4},
    }
    defect_metrics = {
        "mean_coherence": 0.999,
        "mean_higher_mode_fraction": 0.004,
        "mean_leakage": 2.0e-8,
    }
    thresholds = {
        "min_periapse_count": 3,
        "max_abs_beta_eff": 0.2,
        "max_rel_energy_drift": 0.05,
        "max_rel_angular_momentum_drift": 0.05,
        "min_coherence": 0.995,
        "max_higher_mode_fraction": 0.01,
        "max_leakage": 1.0e-6,
    }

    gate = evaluate_newtonian_orbit_gate(orbit_summary, defect_metrics, thresholds, fit_error="no periapses")

    assert not gate["passes"]
    assert not gate["gates"]["orbit_fit_available"]
