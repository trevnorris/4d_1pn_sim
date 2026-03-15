from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class PolytropicEOS:
    K_eos: float
    n: float

    def pressure(self, rho: torch.Tensor | float) -> torch.Tensor:
        rho_tensor = torch.as_tensor(rho)
        return self.K_eos * rho_tensor.pow(self.n)

    def sound_speed(self, rho: torch.Tensor | float) -> torch.Tensor:
        rho_tensor = torch.as_tensor(rho)
        return torch.sqrt(self.n * self.K_eos * rho_tensor.pow(self.n - 1.0))

    def internal_energy_density(self, rho: torch.Tensor | float) -> torch.Tensor:
        rho_tensor = torch.as_tensor(rho)
        return self.K_eos * rho_tensor.pow(self.n) / (self.n - 1.0)

    def enthalpy(self, rho: torch.Tensor | float) -> torch.Tensor:
        rho_tensor = torch.as_tensor(rho)
        return self.n * self.K_eos * rho_tensor.pow(self.n - 1.0) / (self.n - 1.0)

    def relative_enthalpy(self, local_density: torch.Tensor, ambient_density: float) -> torch.Tensor:
        ambient = torch.as_tensor(ambient_density, device=local_density.device, dtype=local_density.dtype)
        total = local_density + ambient
        return self.enthalpy(total) - self.enthalpy(ambient)
