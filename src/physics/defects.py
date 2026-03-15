from __future__ import annotations

import torch

from src.core.fft_ops import fft3, ifft3
from src.physics.matter_gnls import MatterSplitStepSolver, MatterState


def gaussian_initial_modes(
    solver: MatterSplitStepSolver,
    gaussian_width: float,
    target_norm: float,
    rho_ambient: float,
    center: tuple[float, float, float] = (0.0, 0.0, 0.0),
    momentum: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> MatterState:
    cx, cy, cz = center
    radial_squared = (solver.x_grid - cx).square() + (solver.y_grid - cy).square() + (solver.z_grid - cz).square()
    phase = torch.exp(
        1j
        * (
            momentum[0] * solver.x_grid
            + momentum[1] * solver.y_grid
            + momentum[2] * solver.z_grid
        )
    ).to(solver.complex_dtype)
    num_modes = solver.basis.num_modes
    psi_modes = torch.zeros(
        (num_modes, *solver.grid.shape),
        device=solver.grid.device,
        dtype=solver.complex_dtype,
    )
    psi_modes[0] = torch.exp(-0.5 * radial_squared / (gaussian_width**2)).to(solver.complex_dtype) * phase
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


def translate_modes(
    solver: MatterSplitStepSolver,
    psi_modes: torch.Tensor,
    shift: tuple[float, float, float],
) -> torch.Tensor:
    kx, ky, kz = solver.grid.wave_numbers()
    phase = torch.exp(
        -1j
        * (
            kx * shift[0]
            + ky * shift[1]
            + kz * shift[2]
        )
    ).to(solver.complex_dtype)
    shifted_fft = fft3(psi_modes) * phase.unsqueeze(0)
    return ifft3(shifted_fft)


def boost_modes(
    solver: MatterSplitStepSolver,
    psi_modes: torch.Tensor,
    momentum: tuple[float, float, float],
) -> torch.Tensor:
    phase = torch.exp(
        1j
        * (
            momentum[0] * solver.x_grid
            + momentum[1] * solver.y_grid
            + momentum[2] * solver.z_grid
        )
    ).to(solver.complex_dtype)
    return psi_modes * phase.unsqueeze(0)


def displace_and_boost_state(
    solver: MatterSplitStepSolver,
    state: MatterState,
    shift: tuple[float, float, float],
    momentum: tuple[float, float, float],
) -> MatterState:
    psi_modes = translate_modes(solver, state.psi_modes, shift=shift)
    psi_modes = boost_modes(solver, psi_modes, momentum=momentum)
    psi_modes = solver.normalize_modes(psi_modes, float(solver.total_norm(state.psi_modes)))
    return MatterState(
        psi_modes=psi_modes,
        time=float(state.time),
        step=int(state.step),
        a=float(state.a),
        rho_ambient=float(state.rho_ambient),
    )
