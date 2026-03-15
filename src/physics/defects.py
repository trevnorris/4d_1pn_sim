from __future__ import annotations

import torch

from src.physics.matter_gnls import MatterSplitStepSolver, MatterState


def gaussian_initial_modes(
    solver: MatterSplitStepSolver,
    gaussian_width: float,
    target_norm: float,
    rho_ambient: float,
) -> MatterState:
    radial_squared = solver.radial_squared
    num_modes = solver.basis.num_modes
    psi_modes = torch.zeros(
        (num_modes, *solver.grid.shape),
        device=solver.grid.device,
        dtype=solver.complex_dtype,
    )
    psi_modes[0] = torch.exp(-0.5 * radial_squared / (gaussian_width**2)).to(solver.complex_dtype)
    psi_modes = solver.normalize_modes(psi_modes, target_norm)
    return solver.build_state(psi_modes=psi_modes, time=0.0, step=0, rho_ambient=rho_ambient)


def imaginary_time_relax(
    solver: MatterSplitStepSolver,
    state: MatterState,
    dtau: float,
    steps: int,
    target_norm: float,
) -> MatterState:
    current = state
    for _ in range(steps):
        current = solver.step_imaginary(current, dtau=dtau, target_norm=target_norm)
    return current
