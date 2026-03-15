import math

import torch

from src.core.hermite import HermiteBasis


def test_hermite_basis_orthonormality_and_spectrum() -> None:
    basis = HermiteBasis(
        num_modes=6,
        lambda_w=1.7,
        quadrature_order=24,
        device=torch.device("cpu"),
        real_dtype=torch.float64,
    )
    gram = torch.einsum("q,mq,nq->mn", basis.weights, basis.basis_values, basis.basis_values)
    identity = torch.eye(basis.num_modes, dtype=torch.float64)
    assert torch.allclose(gram, identity, atol=1.0e-12, rtol=1.0e-12)

    expected_masses = torch.tensor(
        [2.0 * n / basis.lambda_w**2 for n in range(basis.num_modes)],
        dtype=torch.float64,
    )
    assert torch.allclose(basis.mode_masses_sq.cpu(), expected_masses, atol=1.0e-12, rtol=1.0e-12)


def test_hermite_brane_coupling_parity_rule() -> None:
    basis = HermiteBasis(
        num_modes=7,
        lambda_w=1.3,
        quadrature_order=20,
        device=torch.device("cpu"),
        real_dtype=torch.float64,
    )
    weights = basis.brane_coupling_weights().cpu()
    for index in range(1, basis.num_modes, 2):
        assert abs(float(weights[index])) < 1.0e-12
    assert math.isclose(float(weights[0]), 1.0 / (basis.lambda_w * math.sqrt(math.pi)), rel_tol=1.0e-12)
