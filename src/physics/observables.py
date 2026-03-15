from __future__ import annotations

import torch

from src.core.grids import SpatialGrid3D
from src.physics.defects import translate_modes


def center_of_mass(rho: torch.Tensor, grid: SpatialGrid3D) -> torch.Tensor:
    x, y, z = grid.coordinates()
    mass = rho.sum().clamp_min(1.0e-12) * grid.cell_volume
    coords = torch.stack([x, y, z], dim=0)
    return (coords * rho.unsqueeze(0)).sum(dim=(-3, -2, -1)) * grid.cell_volume / mass


def radius_of_gyration(rho: torch.Tensor, grid: SpatialGrid3D) -> torch.Tensor:
    x, y, z = grid.coordinates()
    com = center_of_mass(rho, grid)
    radius_sq = (x - com[0]).square() + (y - com[1]).square() + (z - com[2]).square()
    mass = rho.sum().clamp_min(1.0e-12) * grid.cell_volume
    return torch.sqrt((radius_sq * rho).sum() * grid.cell_volume / mass)


def bound_mass_fraction(rho: torch.Tensor, grid: SpatialGrid3D, bound_radius: float) -> torch.Tensor:
    x, y, z = grid.coordinates()
    com = center_of_mass(rho, grid)
    mask = ((x - com[0]).square() + (y - com[1]).square() + (z - com[2]).square()) <= bound_radius**2
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


def translation_aligned_coherence(
    solver,
    reference: torch.Tensor,
    current: torch.Tensor,
    cell_volume: float,
) -> torch.Tensor:
    reference_center = solver.estimate_defect_center(reference)
    current_center = solver.estimate_defect_center(current)
    shift = tuple(float(reference_center[i] - current_center[i]) for i in range(3))
    aligned_current = translate_modes(solver, current, shift=shift)
    reference_density = solver.effective_spatial_density(reference)
    current_density = solver.effective_spatial_density(aligned_current)
    return coherence(reference_density, current_density, cell_volume)


def orbital_radius(center: torch.Tensor, source_center: torch.Tensor) -> torch.Tensor:
    return torch.sqrt(((center - source_center) ** 2).sum())
