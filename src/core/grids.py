from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import torch


def resolve_device(device_name: str) -> torch.device:
    if device_name == "cuda_if_available":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(device_name)


@dataclass(frozen=True)
class SpatialGrid3D:
    shape: tuple[int, int, int]
    length: tuple[float, float, float]
    device: torch.device
    real_dtype: torch.dtype

    @classmethod
    def from_config(
        cls,
        shape: Sequence[int],
        length: Sequence[float],
        device: torch.device,
        real_dtype: torch.dtype,
    ) -> "SpatialGrid3D":
        return cls(tuple(int(v) for v in shape), tuple(float(v) for v in length), device, real_dtype)

    @property
    def dx(self) -> tuple[float, float, float]:
        return tuple(L / N for L, N in zip(self.length, self.shape))

    @property
    def cell_volume(self) -> float:
        dx, dy, dz = self.dx
        return dx * dy * dz

    def coordinates(self) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        coords = []
        for N, L in zip(self.shape, self.length):
            dx = L / N
            axis = torch.arange(N, device=self.device, dtype=self.real_dtype) * dx - 0.5 * L
            coords.append(axis)
        return tuple(torch.meshgrid(*coords, indexing="ij"))

    def radial_squared(self) -> torch.Tensor:
        x, y, z = self.coordinates()
        return x.square() + y.square() + z.square()

    def wave_numbers(self) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        k_axes = []
        for N, L in zip(self.shape, self.length):
            dx = L / N
            axis = 2.0 * math.pi * torch.fft.fftfreq(N, d=dx, device=self.device)
            k_axes.append(axis.to(self.real_dtype))
        return tuple(torch.meshgrid(*k_axes, indexing="ij"))

    def k_squared(self) -> torch.Tensor:
        kx, ky, kz = self.wave_numbers()
        return kx.square() + ky.square() + kz.square()

    def divergence(self, vector_field: torch.Tensor) -> torch.Tensor:
        kx, ky, kz = self.wave_numbers()
        field_fft = torch.fft.fftn(vector_field, dim=(-3, -2, -1))
        div_fft = 1j * (kx * field_fft[0] + ky * field_fft[1] + kz * field_fft[2])
        return torch.fft.ifftn(div_fft, dim=(-3, -2, -1)).real

    def gradient(self, scalar_field: torch.Tensor) -> torch.Tensor:
        kx, ky, kz = self.wave_numbers()
        field_fft = torch.fft.fftn(scalar_field, dim=(-3, -2, -1))
        components = [
            torch.fft.ifftn(1j * component * field_fft, dim=(-3, -2, -1)).real
            for component in (kx, ky, kz)
        ]
        return torch.stack(components, dim=0)
