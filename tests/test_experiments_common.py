from types import SimpleNamespace

import torch

from src.core.checkpoints import save_checkpoint
from src.experiments.common import state_from_checkpoint


def test_state_from_checkpoint_restores_matter_state(tmp_path) -> None:
    checkpoint_path = tmp_path / "state.npz"
    psi_modes = torch.ones((2, 4, 4, 4), dtype=torch.complex64)
    save_checkpoint(
        checkpoint_path,
        {
            "psi_modes": psi_modes,
            "time": 1.25,
            "step": 12,
            "a": 1.1,
            "rho_ambient": 0.95,
        },
    )
    solver = SimpleNamespace(
        grid=SimpleNamespace(device=torch.device("cpu")),
        complex_dtype=torch.complex64,
    )

    state = state_from_checkpoint(checkpoint_path, solver=solver)

    assert torch.allclose(state.psi_modes, psi_modes)
    assert state.time == 1.25
    assert state.step == 12
    assert state.a == 1.1
    assert state.rho_ambient == 0.95
