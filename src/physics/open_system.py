from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch

from src.core.grids import SpatialGrid3D
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


def build_boundary_reservoir_shape(
    grid: SpatialGrid3D,
    width: float,
    power: float = 2.0,
    inner_clearance: float = 0.0,
    normalize: bool = True,
) -> torch.Tensor:
    if width <= 0.0:
        raise ValueError("boundary reservoir width must be positive")
    if power <= 0.0:
        raise ValueError("boundary reservoir power must be positive")
    if inner_clearance < 0.0:
        raise ValueError("boundary reservoir inner_clearance must be non-negative")

    x_grid, y_grid, z_grid = grid.coordinates()
    half_lengths = [0.5 * float(length) for length in grid.length]
    clearance = torch.minimum(
        torch.minimum(half_lengths[0] - x_grid.abs(), half_lengths[1] - y_grid.abs()),
        half_lengths[2] - z_grid.abs(),
    ).to(grid.real_dtype)
    if inner_clearance > 0.0:
        shell_position = ((clearance - float(inner_clearance)) / float(width)).clamp(0.0, 1.0)
        raw = (4.0 * shell_position * (1.0 - shell_position)).clamp_min(0.0).pow(float(power))
    else:
        raw = ((float(width) - clearance).clamp_min(0.0) / float(width)).pow(float(power))
    if float(raw.max()) <= 0.0:
        raise ValueError(
            "boundary reservoir support is empty; adjust width/inner_clearance for the current grid"
        )
    if not normalize:
        return raw
    norm_sq = (raw.square().sum() * float(grid.cell_volume)).clamp_min(1.0e-12)
    return raw / torch.sqrt(norm_sq)


def add_boundary_mode0_density(
    solver: MatterSplitStepSolver,
    psi_modes: torch.Tensor,
    delta_norm: float,
    boundary_shape: torch.Tensor,
) -> torch.Tensor:
    if delta_norm <= 0.0:
        return psi_modes
    shape = boundary_shape.to(psi_modes.dtype)
    overlap = (psi_modes[0].conj() * shape).sum() * float(solver.grid.cell_volume)
    if torch.abs(overlap) > 1.0e-12:
        phase = 1j * overlap / torch.abs(overlap)
    else:
        phase = torch.ones((), device=psi_modes.device, dtype=psi_modes.dtype)
    amplitude = float(delta_norm) ** 0.5
    updated = psi_modes.clone()
    updated[0] = updated[0] + amplitude * phase.to(psi_modes.dtype) * shape
    return updated


def relax_boundary_density_to_target(
    solver: MatterSplitStepSolver,
    psi_modes: torch.Tensor,
    boundary_profile: torch.Tensor,
    target_density: float,
    relaxation_fraction: float,
    max_delta_norm: float = 0.0,
) -> tuple[torch.Tensor, float]:
    if relaxation_fraction <= 0.0 or target_density < 0.0:
        return psi_modes, 0.0

    rho = solver.effective_spatial_density(psi_modes)
    profile = boundary_profile.to(rho.dtype).clamp_min(0.0)
    blend = (float(relaxation_fraction) * profile).clamp(0.0, 1.0)
    target = torch.full_like(rho, float(target_density))
    desired_rho = rho + blend * (target - rho)
    delta_rho = desired_rho - rho
    delta_norm = float(delta_rho.sum() * float(solver.grid.cell_volume))

    if max_delta_norm > 0.0 and abs(delta_norm) > float(max_delta_norm):
        scale = float(max_delta_norm) / max(abs(delta_norm), 1.0e-12)
        desired_rho = rho + delta_rho * scale
        delta_rho = desired_rho - rho
        delta_norm = float(delta_rho.sum() * float(solver.grid.cell_volume))

    rho_eps = 1.0e-16
    updated = psi_modes.clone()
    nonzero_mask = rho > rho_eps
    if bool(nonzero_mask.any()):
        scale = torch.ones_like(rho)
        scale[nonzero_mask] = torch.sqrt((desired_rho[nonzero_mask] / rho[nonzero_mask]).clamp_min(0.0))
        updated = updated * scale.unsqueeze(0).to(psi_modes.dtype)

    zero_fill_mask = (~nonzero_mask) & (desired_rho > rho_eps) & (profile > 0.0)
    if bool(zero_fill_mask.any()):
        psi0 = updated[0]
        phase_anchor = torch.ones_like(psi0)
        nonzero_mode0 = psi0.abs() > 1.0e-12
        phase_anchor[nonzero_mode0] = psi0[nonzero_mode0] / psi0[nonzero_mode0].abs()
        psi0[zero_fill_mask] = torch.sqrt(desired_rho[zero_fill_mask]).to(psi_modes.dtype) * phase_anchor[zero_fill_mask]
        updated[0] = psi0

    return updated, delta_norm


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


@dataclass
class BoundaryReservoirRefill:
    leakage_matrix: torch.Tensor
    boundary_shape: torch.Tensor
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
    ) -> "BoundaryReservoirRefill":
        return cls(
            leakage_matrix=build_mode_leakage_matrix(solver.basis, projection_kernel).to(solver.grid.device),
            boundary_shape=build_boundary_reservoir_shape(
                solver.grid,
                width=float(config["width"]),
                power=float(config.get("power", 2.0)),
                inner_clearance=float(config.get("inner_clearance", 0.0)),
            ).to(solver.grid.device),
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
        psi_modes = add_boundary_mode0_density(
            solver,
            state.psi_modes,
            delta_norm=delta_norm,
            boundary_shape=self.boundary_shape,
        )
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


@dataclass
class BoundaryDensityRelaxation:
    boundary_profile: torch.Tensor
    target_density: float
    target_norm: float
    relaxation_fraction: float
    max_delta_norm_fraction_per_step: float
    stage_scale: float = 1.0
    cumulative_refill_norm: float = 0.0

    @classmethod
    def from_config(
        cls,
        solver: MatterSplitStepSolver,
        target_norm: float,
        config: dict[str, Any],
    ) -> "BoundaryDensityRelaxation":
        volume = float(solver.grid.length[0] * solver.grid.length[1] * solver.grid.length[2])
        target_density = float(config.get("target_density", float(target_norm) / max(volume, 1.0e-12)))
        return cls(
            boundary_profile=build_boundary_reservoir_shape(
                solver.grid,
                width=float(config["width"]),
                power=float(config.get("power", 2.0)),
                inner_clearance=float(config.get("inner_clearance", 0.0)),
                normalize=False,
            ).to(solver.grid.device),
            target_density=target_density,
            target_norm=float(target_norm),
            relaxation_fraction=float(config.get("relaxation_fraction", 0.2)),
            max_delta_norm_fraction_per_step=float(config.get("max_delta_norm_fraction_per_step", 0.0)),
        )

    def apply(
        self,
        solver: MatterSplitStepSolver,
        state: MatterState,
        dt: float,
    ) -> tuple[MatterState, dict[str, float]]:
        del dt
        max_delta_norm = 0.0
        if self.max_delta_norm_fraction_per_step > 0.0:
            max_delta_norm = self.max_delta_norm_fraction_per_step * self.target_norm
        psi_modes, delta_norm = relax_boundary_density_to_target(
            solver=solver,
            psi_modes=state.psi_modes,
            boundary_profile=self.boundary_profile,
            target_density=self.target_density,
            relaxation_fraction=self.relaxation_fraction * self.stage_scale,
            max_delta_norm=max_delta_norm,
        )
        self.cumulative_refill_norm += float(delta_norm)
        updated_state = MatterState(
            psi_modes=psi_modes,
            time=float(state.time),
            step=int(state.step),
            a=float(state.a),
            rho_ambient=float(state.rho_ambient),
        )
        return updated_state, {
            "signed_leakage_mean": 0.0,
            "mean_leakage": 0.0,
            "delta_norm_from_leakage": 0.0,
            "delta_norm_from_deficit": float(delta_norm),
            "delta_norm_applied": float(delta_norm),
            "cumulative_refill_norm": float(self.cumulative_refill_norm),
        }
