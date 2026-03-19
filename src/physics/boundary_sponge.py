from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch

from src.core.grids import SpatialGrid3D


@dataclass
class BoundarySponge:
    mask: torch.Tensor
    target_nodes: torch.Tensor | None = None


def build_boundary_sponge_mask(
    grid: SpatialGrid3D,
    dt: float,
    config: dict[str, Any],
) -> torch.Tensor:
    if not bool(config.get("enabled", False)):
        raise ValueError("boundary sponge config must be enabled before building a mask")

    width = float(config["width"])
    strength = float(config["strength"])
    power = float(config.get("power", 2.0))
    if width <= 0.0:
        raise ValueError("boundary sponge width must be positive")
    if strength < 0.0:
        raise ValueError("boundary sponge strength must be non-negative")
    if power <= 0.0:
        raise ValueError("boundary sponge power must be positive")

    x_grid, y_grid, z_grid = grid.coordinates()
    half_lengths = [0.5 * float(length) for length in grid.length]
    clearance = torch.minimum(
        torch.minimum(half_lengths[0] - x_grid.abs(), half_lengths[1] - y_grid.abs()),
        half_lengths[2] - z_grid.abs(),
    ).to(grid.real_dtype)
    normalized = (width - clearance).clamp_min(0.0) / width
    damping_rate = strength * normalized.pow(power)
    mask = torch.exp(-float(dt) * damping_rate)
    return mask.to(grid.real_dtype)


def apply_boundary_sponge_to_nodes(
    psi_nodes: torch.Tensor,
    sponge: torch.Tensor | BoundarySponge | None,
) -> torch.Tensor:
    if sponge is None:
        return psi_nodes
    if isinstance(sponge, torch.Tensor):
        mask = sponge
        target_nodes = None
    else:
        mask = sponge.mask
        target_nodes = sponge.target_nodes
    mask_tensor = mask.unsqueeze(0) if mask.ndim == 3 else mask
    mask_tensor = mask_tensor.to(psi_nodes.dtype)
    if target_nodes is None:
        return psi_nodes * mask_tensor
    target = target_nodes.to(psi_nodes.dtype)
    return target + (psi_nodes - target) * mask_tensor
