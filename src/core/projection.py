from __future__ import annotations

from dataclasses import dataclass

import torch

from src.core.grids import SpatialGrid3D


@dataclass
class ProjectionKernel:
    nodes: torch.Tensor
    quadrature_weights: torch.Tensor
    weight_values: torch.Tensor
    gradient_values: torch.Tensor

    @classmethod
    def gaussian(
        cls,
        nodes: torch.Tensor,
        quadrature_weights: torch.Tensor,
        width: float,
    ) -> "ProjectionKernel":
        raw = torch.exp(-(nodes / width).square())
        normalization = torch.sum(quadrature_weights * raw)
        weights = raw / normalization
        gradient = -2.0 * nodes / (width**2) * weights
        return cls(
            nodes=nodes,
            quadrature_weights=quadrature_weights,
            weight_values=weights,
            gradient_values=gradient,
        )

    def project(self, values: torch.Tensor) -> torch.Tensor:
        return torch.einsum("q,q,q...->...", self.quadrature_weights, self.weight_values, values)

    def leakage_source(self, current_w: torch.Tensor, boundary_flux: torch.Tensor | None = None) -> torch.Tensor:
        leakage = torch.einsum("q,q,q...->...", self.quadrature_weights, self.gradient_values, current_w)
        if boundary_flux is not None:
            leakage = leakage - boundary_flux
        return leakage


def projected_continuity_terms(
    rho: torch.Tensor,
    drho_dt: torch.Tensor,
    current_xyz: torch.Tensor,
    current_w: torch.Tensor,
    kernel: ProjectionKernel,
    grid: SpatialGrid3D,
) -> dict[str, torch.Tensor]:
    rho_brane = kernel.project(rho)
    drho_dt_brane = kernel.project(drho_dt)
    current_brane = torch.stack([kernel.project(component) for component in current_xyz], dim=0)
    s_leak = kernel.leakage_source(current_w)
    residual = drho_dt_brane + grid.divergence(current_brane) - s_leak
    return {
        "rho_brane": rho_brane,
        "current_brane": current_brane,
        "S_leak": s_leak,
        "continuity_residual": residual,
    }


def poisson_regime_ratios(
    rho_brane: torch.Tensor,
    drho_dt_brane: torch.Tensor,
    grad_rho_brane: torch.Tensor,
    grad_phi: torch.Tensor,
    v_transverse: torch.Tensor,
    source: torch.Tensor,
    eps: float = 1.0e-8,
) -> dict[str, torch.Tensor]:
    denom = source.abs().mean().clamp_min(eps)
    ratio_dt = drho_dt_brane.abs().mean() / denom
    advection = (grad_rho_brane * (grad_phi + v_transverse)).sum(dim=0)
    ratio_adv = advection.abs().mean() / denom
    return {
        "ratio_dt_over_source": ratio_dt,
        "ratio_adv_over_source": ratio_adv,
    }
