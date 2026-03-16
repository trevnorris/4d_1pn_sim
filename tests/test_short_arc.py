import numpy as np

from src.physics.short_arc import evaluate_short_arc_acceptance, summarize_short_arc_match


def test_summarize_short_arc_match_recovers_small_tracking_errors() -> None:
    time = np.linspace(0.0, 10.0, 1001)
    theta = 0.15 * time
    radius = 12.0
    tracer = np.stack(
        [
            radius * np.cos(theta),
            radius * np.sin(theta),
            np.zeros_like(theta),
        ],
        axis=1,
    )
    defect = np.stack(
        [
            (radius + 0.18) * np.cos(theta + 0.01),
            (radius + 0.18) * np.sin(theta + 0.01),
            np.zeros_like(theta),
        ],
        axis=1,
    )

    summary = summarize_short_arc_match(
        time=time,
        tracer_positions=tracer,
        defect_positions=defect,
        source_center=(0.0, 0.0, 0.0),
        box_length=(48.0, 48.0, 48.0),
        start_index=50,
        end_index=950,
    )

    assert summary["tracer_angular_sweep"] > 1.3
    assert abs(summary["angular_sweep_error"]) < 5.0e-3
    assert summary["normalized_position_rms"] < 0.03
    assert summary["normalized_radius_rms"] < 0.02
    assert abs(summary["phase_rms"] - 0.01) < 5.0e-4
    assert summary["boundary_summary"]["min_boundary_clearance"] > 11.5


def test_evaluate_short_arc_acceptance_flags_failed_gate() -> None:
    short_arc_summary = {
        "defect_angular_sweep": 1.25,
        "angular_sweep_error": 0.02,
        "normalized_position_rms": 0.03,
        "normalized_radius_rms": 0.01,
        "phase_rms": 0.02,
        "boundary_summary": {"min_boundary_clearance": 9.0},
    }
    defect_metrics = {
        "mean_coherence": 0.997,
        "mean_higher_mode_fraction": 0.004,
        "mean_leakage": 2.0e-7,
    }
    thresholds = {
        "min_angular_sweep": 1.0,
        "max_angular_sweep_error": 0.05,
        "max_normalized_position_rms": 0.08,
        "max_normalized_radius_rms": 0.04,
        "max_phase_rms": 0.05,
        "min_boundary_clearance": 8.0,
        "min_coherence": 0.995,
        "max_higher_mode_fraction": 0.01,
        "max_leakage": 1.0e-6,
    }

    acceptance = evaluate_short_arc_acceptance(
        short_arc_summary=short_arc_summary,
        defect_metrics=defect_metrics,
        thresholds=thresholds,
    )

    assert acceptance["passes"]
    assert all(acceptance["gates"].values())

    failed = evaluate_short_arc_acceptance(
        short_arc_summary=short_arc_summary,
        defect_metrics={**defect_metrics, "mean_coherence": 0.97},
        thresholds=thresholds,
    )

    assert not failed["passes"]
    assert not failed["gates"]["min_coherence"]
