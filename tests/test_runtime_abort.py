from src.physics.runtime_abort import boundary_clearance, evaluate_runtime_abort_check


def test_boundary_clearance_tracks_nearest_box_face() -> None:
    clearance = boundary_clearance(position=(10.0, -4.0, 0.5), box_lengths=(48.0, 48.0, 48.0))
    assert clearance == 14.0


def test_runtime_abort_check_stays_clear_for_good_metrics() -> None:
    check = evaluate_runtime_abort_check(
        conservation_summary={
            "orbital_energy_summary": {"max_rel_drift": 0.03},
            "angular_momentum_z_summary": {"max_rel_drift": 0.02},
        },
        light_metrics={
            "mean_coherence": 0.999,
            "mean_higher_mode_fraction": 0.004,
        },
        continuity_metrics={
            "mean_leakage": 2.0e-8,
        },
        min_boundary_clearance=11.5,
        thresholds={
            "max_rel_energy_drift": 0.12,
            "max_rel_angular_momentum_drift": 0.08,
            "min_coherence": 0.99,
            "max_higher_mode_fraction": 0.02,
            "max_leakage": 5.0e-6,
            "min_boundary_clearance": 8.0,
        },
    )

    assert not check["triggered"]
    assert all(check["gates"].values())


def test_runtime_abort_check_triggers_on_large_effective_drift() -> None:
    check = evaluate_runtime_abort_check(
        conservation_summary={
            "orbital_energy_summary": {"max_rel_drift": 0.15},
            "angular_momentum_z_summary": {"max_rel_drift": 0.03},
        },
        light_metrics={
            "mean_coherence": 0.999,
            "mean_higher_mode_fraction": 0.004,
        },
        continuity_metrics={
            "mean_leakage": 2.0e-8,
        },
        min_boundary_clearance=11.5,
        thresholds={
            "max_rel_energy_drift": 0.12,
            "max_rel_angular_momentum_drift": 0.08,
            "min_coherence": 0.99,
            "max_higher_mode_fraction": 0.02,
            "max_leakage": 5.0e-6,
            "min_boundary_clearance": 8.0,
        },
    )

    assert check["triggered"]
    assert "max_rel_energy_drift" in check["failed_gates"]
    assert check["gates"]["max_rel_energy_drift"] is False


def test_runtime_abort_check_triggers_on_nonfinite_metrics() -> None:
    check = evaluate_runtime_abort_check(
        conservation_summary={
            "orbital_energy_summary": {"max_rel_drift": float("nan")},
            "angular_momentum_z_summary": {"max_rel_drift": 0.03},
        },
        light_metrics={
            "mean_coherence": 0.999,
            "mean_higher_mode_fraction": 0.004,
        },
        continuity_metrics={
            "mean_leakage": 2.0e-8,
        },
        min_boundary_clearance=11.5,
        thresholds={
            "max_rel_energy_drift": 0.12,
            "max_rel_angular_momentum_drift": 0.08,
            "min_coherence": 0.99,
            "max_higher_mode_fraction": 0.02,
            "max_leakage": 5.0e-6,
            "min_boundary_clearance": 8.0,
        },
    )

    assert check["triggered"]
    assert "finite_metrics" in check["failed_gates"]
