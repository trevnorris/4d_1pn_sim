from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch

from src.core.hermite import HermiteBasis
from src.core.projection import ProjectionKernel
from src.physics.matter_gnls import MatterSplitStepSolver, MatterState


def build_mode_leakage_matrix(
    basis: HermiteBasis,
    projection_kernel: ProjectionKernel,
) -> torch.Tensor:
    coefficients = (projection_kernel.quadrature_weights * projection_kernel.gradient_values).to(basis.real_dtype)
    return torch.einsum(
        "q,mq,nq->mn",
        coefficients,
        basis.basis_values,
        basis.basis_derivative_values,
    ).to(basis.real_dtype)


def projected_leakage_source_from_modes(
    psi_modes: torch.Tensor,
    leakage_matrix: torch.Tensor,
    mass: float,
) -> torch.Tensor:
    mixed_modes = torch.einsum("mn,n...->m...", leakage_matrix.to(psi_modes.dtype), psi_modes)
    return (psi_modes.conj() * mixed_modes).sum(dim=0).imag / max(float(mass), 1.0e-12)


def add_uniform_mode0_density(
    solver: MatterSplitStepSolver,
    psi_modes: torch.Tensor,
    delta_norm: float,
) -> torch.Tensor:
    if delta_norm <= 0.0:
        return psi_modes
    volume = float(solver.grid.length[0] * solver.grid.length[1] * solver.grid.length[2])
    amplitude = (float(delta_norm) / max(volume, 1.0e-12)) ** 0.5
    mean_overlap = psi_modes[0].sum() * float(solver.grid.cell_volume)
    if torch.abs(mean_overlap) > 1.0e-12:
        phase = 1j * mean_overlap / torch.abs(mean_overlap)
    else:
        phase = torch.ones((), device=psi_modes.device, dtype=psi_modes.dtype)
    updated = psi_modes.clone()
    updated[0] = updated[0] + amplitude * phase.to(psi_modes.dtype)
    return updated


@dataclass
class UniformReservoirRefill:
    leakage_matrix: torch.Tensor
    target_norm: float
    leakage_gain: float
    compensate_leakage: bool
    restore_target_norm: bool
    max_delta_norm_fraction_per_step: float
    cumulative_refill_norm: float = 0.0

    @classmethod
    def from_config(
        cls,
        solver: MatterSplitStepSolver,
        projection_kernel: ProjectionKernel,
        target_norm: float,
        config: dict[str, Any],
    ) -> "UniformReservoirRefill":
        return cls(
            leakage_matrix=build_mode_leakage_matrix(solver.basis, projection_kernel).to(solver.grid.device),
            target_norm=float(target_norm),
            leakage_gain=float(config.get("leakage_gain", 1.0)),
            compensate_leakage=bool(config.get("compensate_leakage", True)),
            restore_target_norm=bool(config.get("restore_target_norm", True)),
            max_delta_norm_fraction_per_step=float(config.get("max_delta_norm_fraction_per_step", 0.0)),
        )

    def apply(
        self,
        solver: MatterSplitStepSolver,
        state: MatterState,
        dt: float,
    ) -> tuple[MatterState, dict[str, float]]:
        leakage_source = projected_leakage_source_from_modes(
            psi_modes=state.psi_modes,
            leakage_matrix=self.leakage_matrix,
            mass=solver.mass,
        )
        signed_leakage_mean = float(leakage_source.mean())
        abs_leakage_mean = float(leakage_source.abs().mean())
        volume = float(solver.grid.length[0] * solver.grid.length[1] * solver.grid.length[2])
        delta_norm_from_leakage = 0.0
        if self.compensate_leakage:
            delta_norm_from_leakage = max(0.0, -self.leakage_gain * signed_leakage_mean * volume * float(dt))
        current_norm = float(solver.total_norm(state.psi_modes))
        delta_norm_from_deficit = 0.0
        if self.restore_target_norm:
            delta_norm_from_deficit = max(0.0, self.target_norm - current_norm)
        delta_norm = delta_norm_from_leakage + delta_norm_from_deficit
        if self.max_delta_norm_fraction_per_step > 0.0:
            delta_norm = min(delta_norm, self.max_delta_norm_fraction_per_step * self.target_norm)
        psi_modes = add_uniform_mode0_density(solver, state.psi_modes, delta_norm)
        self.cumulative_refill_norm += delta_norm
        updated_state = MatterState(
            psi_modes=psi_modes,
            time=float(state.time),
            step=int(state.step),
            a=float(state.a),
            rho_ambient=float(state.rho_ambient),
        )
        return updated_state, {
            "signed_leakage_mean": signed_leakage_mean,
            "mean_leakage": abs_leakage_mean,
            "delta_norm_from_leakage": float(delta_norm_from_leakage),
            "delta_norm_from_deficit": float(delta_norm_from_deficit),
            "delta_norm_applied": float(delta_norm),
            "cumulative_refill_norm": float(self.cumulative_refill_norm),
        }
