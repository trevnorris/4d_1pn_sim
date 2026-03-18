import torch
import pytest
import numpy as np

from src.core.grids import SpatialGrid3D
from src.core.hermite import HermiteBasis
from src.core.projection import ProjectionKernel
from src.physics.boundary_sponge import build_boundary_sponge_mask
from src.physics.eos import PolytropicEOS
from src.physics.geometry import AdiabaticGeometryClosure
from src.physics.matter_gnls import MatterSplitStepSolver, MatterState
from src.physics.open_system import (
    BoundaryDensityRelaxation,
    BoundaryReservoirRefill,
    UniformReservoirRefill,
    add_uniform_mode0_density,
    add_boundary_mode0_density,
    build_boundary_reservoir_shape,
    build_mode_leakage_matrix,
    projected_leakage_source_from_modes,
    relax_boundary_density_to_target,
)


def _build_solver() -> MatterSplitStepSolver:
    device = torch.device("cpu")
    real_dtype = torch.float64
    grid = SpatialGrid3D(shape=(4, 4, 4), length=(8.0, 8.0, 8.0), device=device, real_dtype=real_dtype)
    basis = HermiteBasis(num_modes=4, lambda_w=1.25, quadrature_order=10, device=device, real_dtype=real_dtype)
    eos = PolytropicEOS(K_eos=0.08, n=5.0)
    geometry = AdiabaticGeometryClosure(
        eos=eos,
        lambda_aspect=3.0,
        reference_rho=1.0,
        reference_a=1.1,
        reference_energy_scale=1.0,
    )
    return MatterSplitStepSolver(
        grid=grid,
        basis=basis,
        eos=eos,
        geometry=geometry,
        complex_dtype=torch.complex128,
        mass=1.0,
        kinetic_prefactor=0.5,
        transverse_prefactor=0.2,
        trap_strength_r=1.4,
        trap_strength_w=0.9,
    )


def test_mode_leakage_matrix_matches_node_evaluation() -> None:
    solver = _build_solver()
    kernel = ProjectionKernel.gaussian(nodes=solver.basis.nodes, quadrature_weights=solver.basis.weights, width=1.25)
    torch.manual_seed(1234)
    psi_modes = torch.randn((4, 4, 4, 4), dtype=torch.complex128)

    matrix = build_mode_leakage_matrix(solver.basis, kernel)
    s_mode = projected_leakage_source_from_modes(psi_modes, matrix, mass=solver.mass)

    psi_nodes = solver.reconstruct_nodes(psi_modes)
    derivative_nodes = solver.basis.derivative_in_w(psi_modes)
    current_w = (psi_nodes.conj() * derivative_nodes).imag / solver.mass
    s_node = kernel.leakage_source(current_w)

    assert torch.allclose(s_mode, s_node, atol=1.0e-10, rtol=1.0e-10)


def test_add_uniform_mode0_density_hits_requested_norm_increment() -> None:
    solver = _build_solver()
    psi_modes = torch.zeros((4, 4, 4, 4), dtype=torch.complex128)
    delta_norm = 0.25

    updated = add_uniform_mode0_density(solver, psi_modes, delta_norm=delta_norm)

    assert abs(float(solver.total_norm(updated)) - delta_norm) < 1.0e-12


def test_uniform_reservoir_refill_restores_target_norm() -> None:
    solver = _build_solver()
    kernel = ProjectionKernel.gaussian(nodes=solver.basis.nodes, quadrature_weights=solver.basis.weights, width=1.25)
    psi_modes = torch.zeros((4, 4, 4, 4), dtype=torch.complex128)
    psi_modes[0, 1, 1, 1] = 1.0 + 0.0j
    state = MatterState(psi_modes=psi_modes * 0.8, time=0.0, step=0, a=1.1, rho_ambient=1.0)
    target_norm = float(solver.total_norm(psi_modes))

    refill = UniformReservoirRefill.from_config(
        solver=solver,
        projection_kernel=kernel,
        target_norm=target_norm,
        config={
            "enabled": True,
            "compensate_leakage": False,
            "restore_target_norm": True,
            "leakage_gain": 1.0,
            "max_delta_norm_fraction_per_step": 0.0,
        },
    )

    updated_state, metrics = refill.apply(solver=solver, state=state, dt=0.1)

    assert abs(float(solver.total_norm(updated_state.psi_modes)) - target_norm) < 1.0e-12
    assert metrics["delta_norm_from_deficit"] > 0.0
    assert metrics["delta_norm_applied"] > 0.0


def test_boundary_mode0_density_hits_requested_norm_increment() -> None:
    solver = _build_solver()
    psi_modes = torch.zeros((4, 4, 4, 4), dtype=torch.complex128)
    boundary_shape = build_boundary_reservoir_shape(solver.grid, width=2.0, power=2.0)
    delta_norm = 0.25

    updated = add_boundary_mode0_density(
        solver,
        psi_modes,
        delta_norm=delta_norm,
        boundary_shape=boundary_shape,
    )

    assert abs(float(solver.total_norm(updated)) - delta_norm) < 1.0e-12


def test_boundary_reservoir_shape_can_target_interior_shell() -> None:
    grid = SpatialGrid3D(shape=(16, 16, 16), length=(16.0, 16.0, 16.0), device=torch.device("cpu"), real_dtype=torch.float64)
    boundary_shape = build_boundary_reservoir_shape(grid, width=2.0, power=2.0, inner_clearance=2.0)

    x_grid, y_grid, z_grid = grid.coordinates()
    clearance = torch.minimum(
        torch.minimum(8.0 - x_grid.abs(), 8.0 - y_grid.abs()),
        8.0 - z_grid.abs(),
    )
    max_index = int(boundary_shape.argmax())
    max_clearance = float(clearance.reshape(-1)[max_index])

    assert float(boundary_shape[0, 0, 0]) == pytest.approx(0.0)
    assert float(boundary_shape[grid.shape[0] // 2, grid.shape[1] // 2, grid.shape[2] // 2]) == pytest.approx(0.0)
    assert max_clearance == pytest.approx(3.0, abs=float(grid.dx[0]))


def test_boundary_reservoir_refill_restores_target_norm() -> None:
    solver = _build_solver()
    kernel = ProjectionKernel.gaussian(nodes=solver.basis.nodes, quadrature_weights=solver.basis.weights, width=1.25)
    psi_modes = torch.zeros((4, 4, 4, 4), dtype=torch.complex128)
    psi_modes[0, 1, 1, 1] = 1.0 + 0.0j
    state = MatterState(psi_modes=psi_modes * 0.8, time=0.0, step=0, a=1.1, rho_ambient=1.0)
    target_norm = float(solver.total_norm(psi_modes))

    refill = BoundaryReservoirRefill.from_config(
        solver=solver,
        projection_kernel=kernel,
        target_norm=target_norm,
        config={
            "enabled": True,
            "width": 2.0,
            "power": 2.0,
            "inner_clearance": 1.0,
            "compensate_leakage": False,
            "restore_target_norm": True,
            "leakage_gain": 1.0,
            "max_delta_norm_fraction_per_step": 0.0,
        },
    )

    updated_state, metrics = refill.apply(solver=solver, state=state, dt=0.1)

    assert abs(float(solver.total_norm(updated_state.psi_modes)) - target_norm) < 1.0e-12
    assert metrics["delta_norm_from_deficit"] > 0.0
    assert metrics["delta_norm_applied"] > 0.0


def test_relax_boundary_density_to_target_populates_edge_collar() -> None:
    solver = _build_solver()
    psi_modes = torch.zeros((4, 4, 4, 4), dtype=torch.complex128)
    profile = build_boundary_reservoir_shape(
        solver.grid,
        width=2.0,
        power=2.0,
        inner_clearance=1.0,
        normalize=False,
    )

    updated, delta_norm = relax_boundary_density_to_target(
        solver=solver,
        psi_modes=psi_modes,
        boundary_profile=profile,
        target_density=1.0e-3,
        relaxation_fraction=0.5,
        max_delta_norm=0.0,
    )

    rho = solver.effective_spatial_density(updated)
    peak_index = np.unravel_index(int(profile.argmax().item()), tuple(profile.shape))
    assert delta_norm > 0.0
    assert float(rho.max()) > 0.0
    assert float(rho[peak_index]) > float(
        rho[solver.grid.shape[0] // 2, solver.grid.shape[1] // 2, solver.grid.shape[2] // 2]
    )


def test_boundary_density_relaxation_caps_net_norm_adjustment() -> None:
    solver = _build_solver()
    state = MatterState(
        psi_modes=torch.zeros((4, 4, 4, 4), dtype=torch.complex128),
        time=0.0,
        step=0,
        a=1.1,
        rho_ambient=1.0,
    )
    controller = BoundaryDensityRelaxation.from_config(
        solver=solver,
        target_norm=1.0,
        config={
            "enabled": True,
            "inner_clearance": 1.0,
            "width": 2.0,
            "power": 2.0,
            "target_density": 1.0e-2,
            "relaxation_fraction": 1.0,
            "max_delta_norm_fraction_per_step": 5.0e-2,
        },
    )

    updated_state, metrics = controller.apply(solver=solver, state=state, dt=0.1)

    assert float(solver.total_norm(updated_state.psi_modes)) <= 5.0e-2 + 1.0e-12
    assert metrics["delta_norm_applied"] <= 5.0e-2 + 1.0e-12


def test_step_components_matches_step() -> None:
    solver = _build_solver()
    torch.manual_seed(1234)
    psi_modes = torch.randn((4, 4, 4, 4), dtype=torch.complex128)
    state = MatterState(psi_modes=psi_modes, time=0.0, step=0, a=1.1, rho_ambient=1.0)
    mask = build_boundary_sponge_mask(
        grid=solver.grid,
        dt=0.015,
        config={"enabled": True, "width": 2.0, "strength": 8.0, "power": 2.0},
    )

    direct = solver.step(
        state,
        dt=0.015,
        rho_ambient=1.0,
        external_potential=None,
        node_amplitude_mask=mask,
    )
    components = solver.step_components(
        state,
        dt=0.015,
        rho_ambient=1.0,
        external_potential=None,
        node_amplitude_mask=mask,
    )

    assert torch.allclose(direct.psi_modes, components["linear2"].psi_modes, atol=1.0e-12, rtol=1.0e-12)
    assert direct.time == components["linear2"].time
    assert direct.step == components["linear2"].step


def test_boundary_sponge_mask_damps_edges_more_than_center() -> None:
    solver = _build_solver()
    mask = build_boundary_sponge_mask(
        grid=solver.grid,
        dt=0.015,
        config={"enabled": True, "width": 2.0, "strength": 8.0, "power": 2.0},
    )

    center_value = float(mask[solver.grid.shape[0] // 2, solver.grid.shape[1] // 2, solver.grid.shape[2] // 2])
    edge_value = float(mask[0, 0, 0])

    assert abs(center_value - 1.0) < 1.0e-12
    assert edge_value < center_value
