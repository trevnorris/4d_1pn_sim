from __future__ import annotations

from typing import Any

import numpy as np
import torch

from src.core.grids import SpatialGrid3D
from src.physics.observables import (
    bound_mass_fraction,
    mode_occupations,
    radius_of_gyration,
    translation_aligned_coherence,
)
from src.physics.open_system import projected_leakage_source_from_modes


def shell_flux_from_band_volume(
    grid: SpatialGrid3D,
    radius: torch.Tensor,
    radial_current: torch.Tensor,
    rho: torch.Tensor,
    shell_radii: list[float],
    band_width: float,
) -> dict[str, list[float]]:
    if band_width <= 0.0:
        raise ValueError("shell band width must be positive")

    half_width = 0.5 * float(band_width)
    shell_inflow_rates: list[float] = []
    shell_mean_densities: list[float] = []
    shell_cell_counts: list[int] = []
    for shell_radius in shell_radii:
        mask = (radius - float(shell_radius)).abs() <= half_width
        count = int(mask.sum().item())
        if count == 0:
            raise ValueError(
                f"shell radius {shell_radius} with band width {band_width} contains no grid cells"
            )
        outward_flux = float(radial_current[mask].sum() * grid.cell_volume / float(band_width))
        shell_inflow_rates.append(-outward_flux)
        shell_mean_densities.append(float(rho[mask].mean()))
        shell_cell_counts.append(count)
    return {
        "shell_inflow_rates": shell_inflow_rates,
        "shell_mean_densities": shell_mean_densities,
        "shell_cell_counts": shell_cell_counts,
    }


def sample_source_inflow_metrics(
    solver,
    psi_modes: torch.Tensor,
    reference_modes: torch.Tensor,
    leakage_matrix: torch.Tensor,
    shell_radii: list[float],
    shell_band_width: float,
    core_radius: float,
    ambient_probe_radius: float,
) -> dict[str, Any]:
    rho = solver.effective_spatial_density(psi_modes)
    center = solver.estimate_defect_center(psi_modes)
    x_grid, y_grid, z_grid = solver.grid.coordinates()
    dx = x_grid - center[0]
    dy = y_grid - center[1]
    dz = z_grid - center[2]
    radius = torch.sqrt(dx.square() + dy.square() + dz.square())
    min_radius = max(max(solver.grid.dx), 1.0e-12)
    safe_radius = radius.clamp_min(min_radius)

    psi_fft = torch.fft.fftn(psi_modes, dim=(-3, -2, -1))
    radial_current = torch.zeros_like(rho)
    for offset, k_component in zip((dx, dy, dz), solver.grid.wave_numbers()):
        grad_modes = torch.fft.ifftn(1j * k_component.unsqueeze(0) * psi_fft, dim=(-3, -2, -1))
        current_component = (psi_modes.conj() * grad_modes).imag.sum(dim=0) / max(float(solver.mass), 1.0e-12)
        radial_current = radial_current + current_component.real * offset / safe_radius

    shell_profile = shell_flux_from_band_volume(
        grid=solver.grid,
        radius=radius,
        radial_current=radial_current,
        rho=rho,
        shell_radii=shell_radii,
        band_width=shell_band_width,
    )

    core_mask = radius <= float(core_radius)
    if not bool(core_mask.any()):
        raise ValueError("core radius contains no grid cells")
    ambient_mask = radius >= float(ambient_probe_radius)
    if not bool(ambient_mask.any()):
        raise ValueError("ambient probe radius excludes all grid cells")

    occupations = mode_occupations(psi_modes, solver.grid.cell_volume)
    leakage_source = projected_leakage_source_from_modes(
        psi_modes=psi_modes,
        leakage_matrix=leakage_matrix,
        mass=solver.mass,
    )
    total_norm = float(solver.total_norm(psi_modes))
    volume = float(np.prod(np.asarray(solver.grid.length, dtype=np.float64)))
    return {
        "center": center.detach().cpu().numpy().tolist(),
        "total_norm": total_norm,
        "box_mean_density": total_norm / max(volume, 1.0e-12),
        "radius_of_gyration": float(radius_of_gyration(rho, solver.grid)),
        "bound_mass_fraction": float(bound_mass_fraction(rho, solver.grid, float(core_radius))),
        "core_mass": float(rho[core_mask].sum() * solver.grid.cell_volume),
        "core_mean_density": float(rho[core_mask].mean()),
        "ambient_mean_density": float(rho[ambient_mask].mean()),
        "higher_mode_fraction": float(occupations[1:].sum() / occupations.sum().clamp_min(1.0e-12)),
        "coherence": float(
            translation_aligned_coherence(solver, reference_modes, psi_modes, solver.grid.cell_volume)
        ),
        "signed_leakage_mean": float(leakage_source.mean()),
        "mean_leakage": float(leakage_source.abs().mean()),
        "shell_inflow_rates": shell_profile["shell_inflow_rates"],
        "shell_mean_densities": shell_profile["shell_mean_densities"],
        "shell_cell_counts": shell_profile["shell_cell_counts"],
    }


def _summary_triplet(values: np.ndarray) -> dict[str, float]:
    data = np.asarray(values, dtype=np.float64)
    return {
        "initial": float(data[0]),
        "mean": float(np.mean(data)),
        "final": float(data[-1]),
        "min": float(np.min(data)),
        "max": float(np.max(data)),
    }


def summarize_source_inflow_series(
    shell_radii: list[float],
    shell_inflow_rates: np.ndarray,
    shell_mean_densities: np.ndarray,
    total_norm: np.ndarray,
    box_mean_density: np.ndarray,
    ambient_mean_density: np.ndarray,
    core_mass: np.ndarray,
    core_mean_density: np.ndarray,
    coherence: np.ndarray,
    higher_mode_fraction: np.ndarray,
    compactness: np.ndarray,
    bound_mass_fraction_series: np.ndarray,
    mean_leakage: np.ndarray,
    signed_leakage_mean: np.ndarray,
) -> dict[str, Any]:
    shell_inflow = np.asarray(shell_inflow_rates, dtype=np.float64)
    shell_density = np.asarray(shell_mean_densities, dtype=np.float64)
    total_norm_arr = np.asarray(total_norm, dtype=np.float64)
    box_density_arr = np.asarray(box_mean_density, dtype=np.float64)
    ambient_density_arr = np.asarray(ambient_mean_density, dtype=np.float64)
    core_mass_arr = np.asarray(core_mass, dtype=np.float64)
    core_density_arr = np.asarray(core_mean_density, dtype=np.float64)
    coherence_arr = np.asarray(coherence, dtype=np.float64)
    higher_modes_arr = np.asarray(higher_mode_fraction, dtype=np.float64)
    compactness_arr = np.asarray(compactness, dtype=np.float64)
    bound_mass_arr = np.asarray(bound_mass_fraction_series, dtype=np.float64)
    leakage_arr = np.asarray(mean_leakage, dtype=np.float64)
    signed_leakage_arr = np.asarray(signed_leakage_mean, dtype=np.float64)

    initial_norm = max(float(total_norm_arr[0]), 1.0e-12)
    initial_box_density = max(float(box_density_arr[0]), 1.0e-12)
    initial_ambient_density = max(float(ambient_density_arr[0]), 1.0e-12)

    return {
        "sample_count": int(total_norm_arr.shape[0]),
        "shell_radii": [float(value) for value in shell_radii],
        "mean_shell_inflow_by_radius": shell_inflow.mean(axis=0).tolist(),
        "std_shell_inflow_by_radius": shell_inflow.std(axis=0).tolist(),
        "final_shell_inflow_by_radius": shell_inflow[-1].tolist(),
        "max_abs_shell_inflow_by_radius": np.abs(shell_inflow).max(axis=0).tolist(),
        "mean_shell_density_by_radius": shell_density.mean(axis=0).tolist(),
        "final_shell_density_by_radius": shell_density[-1].tolist(),
        "total_norm": {
            **_summary_triplet(total_norm_arr),
            "max_rel_drop": float(np.max((total_norm_arr[0] - total_norm_arr) / initial_norm)),
        },
        "box_mean_density": {
            **_summary_triplet(box_density_arr),
            "max_rel_drop": float(np.max((box_density_arr[0] - box_density_arr) / initial_box_density)),
        },
        "ambient_mean_density": {
            **_summary_triplet(ambient_density_arr),
            "max_rel_drop": float(np.max((ambient_density_arr[0] - ambient_density_arr) / initial_ambient_density)),
        },
        "core_mass": _summary_triplet(core_mass_arr),
        "core_mean_density": _summary_triplet(core_density_arr),
        "coherence": _summary_triplet(coherence_arr),
        "higher_mode_fraction": _summary_triplet(higher_modes_arr),
        "compactness": _summary_triplet(compactness_arr),
        "bound_mass_fraction": _summary_triplet(bound_mass_arr),
        "mean_leakage": _summary_triplet(leakage_arr),
        "signed_leakage_mean": _summary_triplet(signed_leakage_arr),
    }
