from __future__ import annotations

import torch

from src.core.grids import SpatialGrid3D


def center_of_mass(rho: torch.Tensor, grid: SpatialGrid3D) -> torch.Tensor:
    x, y, z = grid.coordinates()
    mass = rho.sum().clamp_min(1.0e-12) * grid.cell_volume
    coords = torch.stack([x, y, z], dim=0)
    return (coords * rho.unsqueeze(0)).sum(dim=(-3, -2, -1)) * grid.cell_volume / mass


def radius_of_gyration(rho: torch.Tensor, grid: SpatialGrid3D) -> torch.Tensor:
    x, y, z = grid.coordinates()
    radius_sq = x.square() + y.square() + z.square()
    mass = rho.sum().clamp_min(1.0e-12) * grid.cell_volume
    return torch.sqrt((radius_sq * rho).sum() * grid.cell_volume / mass)


def bound_mass_fraction(rho: torch.Tensor, grid: SpatialGrid3D, bound_radius: float) -> torch.Tensor:
    x, y, z = grid.coordinates()
    mask = (x.square() + y.square() + z.square()) <= bound_radius**2
    bound_mass = rho[mask].sum() * grid.cell_volume
    total_mass = rho.sum().clamp_min(1.0e-12) * grid.cell_volume
    return bound_mass / total_mass


def mode_occupations(psi_modes: torch.Tensor, cell_volume: float) -> torch.Tensor:
    return psi_modes.abs().square().sum(dim=(-3, -2, -1)) * cell_volume


def coherence(reference: torch.Tensor, current: torch.Tensor, cell_volume: float) -> torch.Tensor:
    numerator = (reference.conj() * current).sum() * cell_volume
    denom = torch.sqrt(
        (reference.abs().square().sum() * cell_volume).clamp_min(1.0e-12)
        * (current.abs().square().sum() * cell_volume).clamp_min(1.0e-12)
    )
    return numerator.abs() / denom
