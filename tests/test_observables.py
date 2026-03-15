import torch

from src.core.grids import SpatialGrid3D
from src.physics.observables import bound_mass_fraction, radius_of_gyration


def _gaussian_density(grid: SpatialGrid3D, center: tuple[float, float, float], sigma: float) -> torch.Tensor:
    x, y, z = grid.coordinates()
    cx, cy, cz = center
    radius_sq = (x - cx).square() + (y - cy).square() + (z - cz).square()
    return torch.exp(-0.5 * radius_sq / (sigma * sigma))


def test_radius_of_gyration_is_translation_invariant() -> None:
    grid = SpatialGrid3D.from_config(shape=(32, 32, 32), length=(16.0, 16.0, 16.0), device=torch.device("cpu"), real_dtype=torch.float32)
    sigma = 0.9
    rho_centered = _gaussian_density(grid, center=(0.0, 0.0, 0.0), sigma=sigma)
    rho_shifted = _gaussian_density(grid, center=(3.0, -2.0, 1.5), sigma=sigma)

    rg_centered = float(radius_of_gyration(rho_centered, grid))
    rg_shifted = float(radius_of_gyration(rho_shifted, grid))

    assert abs(rg_centered - rg_shifted) < 5.0e-3


def test_bound_mass_fraction_is_translation_invariant() -> None:
    grid = SpatialGrid3D.from_config(shape=(32, 32, 32), length=(16.0, 16.0, 16.0), device=torch.device("cpu"), real_dtype=torch.float32)
    sigma = 0.9
    bound_radius = 1.8
    rho_centered = _gaussian_density(grid, center=(0.0, 0.0, 0.0), sigma=sigma)
    rho_shifted = _gaussian_density(grid, center=(-2.5, 2.0, -1.0), sigma=sigma)

    frac_centered = float(bound_mass_fraction(rho_centered, grid, bound_radius=bound_radius))
    frac_shifted = float(bound_mass_fraction(rho_shifted, grid, bound_radius=bound_radius))

    assert abs(frac_centered - frac_shifted) < 5.0e-3
