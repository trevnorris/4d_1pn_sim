import torch

from src.core.grids import SpatialGrid3D
from src.core.hermite import HermiteBasis
from src.core.projection import ProjectionKernel, projected_continuity_terms


def test_projected_continuity_identity_on_manufactured_data() -> None:
    grid = SpatialGrid3D.from_config(
        shape=(8, 8, 8),
        length=(4.0, 4.0, 4.0),
        device=torch.device("cpu"),
        real_dtype=torch.float64,
    )
    basis = HermiteBasis(
        num_modes=4,
        lambda_w=1.1,
        quadrature_order=18,
        device=torch.device("cpu"),
        real_dtype=torch.float64,
    )
    kernel = ProjectionKernel.gaussian(basis.nodes, basis.weights, width=1.1)

    x, y, z = grid.coordinates()
    spatial = 1.0 + 0.1 * torch.cos(x) * torch.cos(y) * torch.cos(z)
    t0 = 0.37

    w = basis.nodes.view(-1, 1, 1, 1)
    rho = torch.sin(torch.tensor(t0, dtype=torch.float64)) * w * spatial
    drho_dt = torch.cos(torch.tensor(t0, dtype=torch.float64)) * w * spatial
    current_w = -0.5 * torch.cos(torch.tensor(t0, dtype=torch.float64)) * w.square() * spatial
    current_xyz = torch.zeros((3, *rho.shape), dtype=torch.float64)

    continuity = projected_continuity_terms(
        rho=rho,
        drho_dt=drho_dt,
        current_xyz=current_xyz,
        current_w=current_w,
        kernel=kernel,
        grid=grid,
    )
    residual = continuity["continuity_residual"]
    assert torch.max(torch.abs(residual)).item() < 5.0e-11
