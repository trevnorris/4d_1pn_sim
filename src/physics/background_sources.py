from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import torch

from src.core.grids import SpatialGrid3D


@dataclass(frozen=True)
class StaticCentralBackground:
    profile: str
    mu: float
    softening_length: float
    core_radius: float
    center: tuple[float, float, float]
    c_eff: float
    rho_reference: float
    density_coupling: float = 1.0

    @classmethod
    def from_config(cls, config: dict[str, object], rho_reference: float) -> "StaticCentralBackground":
        center = tuple(float(v) for v in config.get("center", (0.0, 0.0, 0.0)))
        profile = str(config.get("profile", "softened_kepler"))
        return cls(
            profile=profile,
            mu=float(config["mu"]),
            softening_length=float(config.get("softening_length", 0.0)),
            core_radius=float(config.get("core_radius", 1.0e-3)),
            center=center,
            c_eff=float(config["c_eff"]),
            rho_reference=rho_reference,
            density_coupling=float(config.get("density_coupling", 1.0)),
        )

    def radius_squared_field(self, grid: SpatialGrid3D) -> torch.Tensor:
        x, y, z = grid.coordinates()
        cx, cy, cz = self.center
        return (x - cx).square() + (y - cy).square() + (z - cz).square()

    def potential_field(self, grid: SpatialGrid3D) -> torch.Tensor:
        radius_sq = self.radius_squared_field(grid)
        if self.profile == "softened_kepler":
            return -self.mu / torch.sqrt(radius_sq + self.softening_length**2)
        if self.profile == "pure_kepler":
            radius = torch.sqrt(radius_sq).clamp_min(self.core_radius)
            return -self.mu / radius
        raise ValueError(f"Unsupported background profile: {self.profile}")

    def potential_at_position(self, position: Sequence[float]) -> float:
        dx = float(position[0]) - self.center[0]
        dy = float(position[1]) - self.center[1]
        dz = float(position[2]) - self.center[2]
        radius_sq = dx * dx + dy * dy + dz * dz
        if self.profile == "softened_kepler":
            radius = math.sqrt(radius_sq + self.softening_length**2)
            return -self.mu / radius
        if self.profile == "pure_kepler":
            radius = max(math.sqrt(radius_sq), self.core_radius)
            return -self.mu / radius
        raise ValueError(f"Unsupported background profile: {self.profile}")

    def acceleration_at_position(self, position: Sequence[float]) -> tuple[float, float, float]:
        dx = float(position[0]) - self.center[0]
        dy = float(position[1]) - self.center[1]
        dz = float(position[2]) - self.center[2]
        radius_sq = dx * dx + dy * dy + dz * dz
        if self.profile == "softened_kepler":
            denom = (radius_sq + self.softening_length**2) ** 1.5
            scale = -self.mu / max(denom, 1.0e-12)
        elif self.profile == "pure_kepler":
            radius = max(math.sqrt(radius_sq), self.core_radius)
            scale = -self.mu / max(radius**3, 1.0e-12)
        else:
            raise ValueError(f"Unsupported background profile: {self.profile}")
        return (scale * dx, scale * dy, scale * dz)

    def ambient_density_at_position(self, position: Sequence[float]) -> float:
        phi = self.potential_at_position(position)
        correction = -self.density_coupling * phi / (self.c_eff**2)
        return max(1.0e-6, self.rho_reference * (1.0 + correction))

    def circular_speed(self, radius: float) -> float:
        if self.profile == "softened_kepler":
            denom = (radius * radius + self.softening_length**2) ** 1.5
            return math.sqrt(self.mu * radius * radius / max(denom, 1.0e-12))
        return math.sqrt(self.mu / max(radius, self.core_radius))

    def periapsis_speed(self, periapsis_radius: float, eccentricity: float) -> float:
        semi_major_axis = periapsis_radius / (1.0 - eccentricity)
        return math.sqrt(self.mu * (2.0 / periapsis_radius - 1.0 / semi_major_axis))

    def beta_eff(self, delta_phi: float, semi_major_axis: float, eccentricity: float) -> float:
        denom = 2.0 * math.pi * self.mu
        numer = delta_phi * (self.c_eff**2) * semi_major_axis * (1.0 - eccentricity**2)
        return numer / denom
