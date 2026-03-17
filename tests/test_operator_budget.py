import numpy as np

from src.physics.operator_budget import OperatorBudgetRecorder, summarize_operator_budget


def test_summarize_operator_budget_detects_sponge_norm_loss() -> None:
    recorder = OperatorBudgetRecorder()
    time = np.linspace(0.0, 4.0, 5)
    base_radius = 4.0
    angular_speed = 0.2

    for idx, t in enumerate(time):
        angle = angular_speed * t
        start_position = [base_radius * np.cos(angle), base_radius * np.sin(angle), 0.0]
        recorder.record(stage="start", time=t, position=start_position, total_norm=1.0)
        recorder.record(stage="linear1", time=t + 0.5, position=start_position, total_norm=1.0)
        recorder.record(stage="nonlinear", time=t + 0.5, position=start_position, total_norm=1.0)
        recorder.record(stage="sponge", time=t + 0.5, position=start_position, total_norm=0.99)
        recorder.record(stage="linear2", time=t + 1.0, position=start_position, total_norm=0.99)
        recorder.record(stage="refill", time=t + 1.0, position=start_position, total_norm=0.99)

    summary = summarize_operator_budget(
        recorder,
        source_center=(0.0, 0.0, 0.0),
        potential_fn=lambda position: -1.0 / max(float(np.linalg.norm(position)), 1.0e-12),
        mu=1.0,
        fit_start_index=0,
    )

    sponge_transition = summary["transitions"]["nonlinear_to_sponge"]
    assert sponge_transition["total_norm"]["mean_delta"] < 0.0
    assert sponge_transition["total_norm"]["mean_abs_delta"] > 0.0
