from __future__ import annotations

import torch


def fft3(field: torch.Tensor) -> torch.Tensor:
    return torch.fft.fftn(field, dim=(-3, -2, -1))


def ifft3(field_fft: torch.Tensor) -> torch.Tensor:
    return torch.fft.ifftn(field_fft, dim=(-3, -2, -1))


def apply_diagonal_phase(field: torch.Tensor, phase: torch.Tensor) -> torch.Tensor:
    return field * phase
