from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import torch


def physicists_hermite_values(num_modes: int, points: torch.Tensor) -> torch.Tensor:
    values = [torch.ones_like(points)]
    if num_modes == 1:
        return torch.stack(values, dim=0)

    values.append(2.0 * points)
    for n in range(1, num_modes - 1):
        values.append(2.0 * points * values[n] - 2.0 * n * values[n - 1])
    return torch.stack(values[:num_modes], dim=0)


@dataclass
class HermiteBasis:
    num_modes: int
    lambda_w: float
    quadrature_order: int
    device: torch.device
    real_dtype: torch.dtype

    def __post_init__(self) -> None:
        gh_nodes, gh_weights = np.polynomial.hermite.hermgauss(self.quadrature_order)
        nodes = torch.as_tensor(gh_nodes * self.lambda_w, dtype=self.real_dtype, device=self.device)
        weights = torch.as_tensor(gh_weights * self.lambda_w, dtype=self.real_dtype, device=self.device)
        y = nodes / self.lambda_w
        hermite_values = physicists_hermite_values(self.num_modes, y)

        norms = [
            math.sqrt(self.lambda_w * math.sqrt(math.pi) * (2.0**n) * math.factorial(n))
            for n in range(self.num_modes)
        ]
        basis = hermite_values / torch.as_tensor(norms, dtype=self.real_dtype, device=self.device).unsqueeze(1)

        derivative = torch.zeros_like(basis)
        for n in range(1, self.num_modes):
            derivative[n] = math.sqrt(2.0 * n) / self.lambda_w * basis[n - 1]

        self.nodes = nodes
        self.weights = weights
        self.basis_values = basis
        self.basis_derivative_values = derivative
        self.mode_masses_sq = (
            2.0
            * torch.arange(self.num_modes, device=self.device, dtype=self.real_dtype)
            / (self.lambda_w**2)
        )
        self.basis_at_zero = self.evaluate_at(torch.zeros(1, device=self.device, dtype=self.real_dtype)).squeeze(1)

    def evaluate_at(self, points: torch.Tensor) -> torch.Tensor:
        y = points / self.lambda_w
        hermite_values = physicists_hermite_values(self.num_modes, y)
        norms = [
            math.sqrt(self.lambda_w * math.sqrt(math.pi) * (2.0**n) * math.factorial(n))
            for n in range(self.num_modes)
        ]
        return hermite_values / torch.as_tensor(norms, dtype=self.real_dtype, device=self.device).unsqueeze(1)

    def reconstruct(self, coefficients: torch.Tensor) -> torch.Tensor:
        basis_values = self.basis_values.to(coefficients.dtype)
        return torch.einsum("mq,m...->q...", basis_values, coefficients)

    def project(self, values: torch.Tensor) -> torch.Tensor:
        weights = self.weights.to(values.real.dtype)
        basis_values = self.basis_values.to(values.dtype)
        return torch.einsum("q,mq,q...->m...", weights, basis_values, values)

    def derivative_in_w(self, coefficients: torch.Tensor) -> torch.Tensor:
        derivative_values = self.basis_derivative_values.to(coefficients.dtype)
        return torch.einsum("mq,m...->q...", derivative_values, coefficients)

    def brane_coupling_weights(self) -> torch.Tensor:
        return self.basis_at_zero.square()
