from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch

from src.core.fft_ops import fft3, ifft3
from src.core.grids import SpatialGrid3D
from src.core.hermite import HermiteBasis
from src.physics.boundary_sponge import apply_boundary_sponge_to_nodes
from src.physics.eos import PolytropicEOS
from src.physics.geometry import AdiabaticGeometryClosure


@dataclass
class MatterState:
    psi_modes: torch.Tensor
    time: float
    step: int
    a: float
    rho_ambient: float


class MatterSplitStepSolver:
    def __init__(
        self,
        grid: SpatialGrid3D,
        basis: HermiteBasis,
        eos: PolytropicEOS,
        geometry: AdiabaticGeometryClosure,
        complex_dtype: torch.dtype,
        mass: float,
        kinetic_prefactor: float,
        transverse_prefactor: float,
        trap_strength_r: float,
        trap_strength_w: float,
    ) -> None:
        self.grid = grid
        self.basis = basis
        self.eos = eos
        self.geometry = geometry
        self.complex_dtype = complex_dtype
        self.mass = mass
        self.kinetic_prefactor = kinetic_prefactor
        self.transverse_prefactor = transverse_prefactor
        self.trap_strength_r = trap_strength_r
        self.trap_strength_w = trap_strength_w
        self.k_squared = self.grid.k_squared().to(self.grid.real_dtype)
        self.x_grid, self.y_grid, self.z_grid = self.grid.coordinates()
        self.radial_squared = (self.x_grid.square() + self.y_grid.square() + self.z_grid.square()).to(self.grid.real_dtype)
        self.w_squared = self.basis.nodes.square().view(-1, 1, 1, 1).to(self.grid.real_dtype)
        self.mode_masses_sq = self.basis.mode_masses_sq.view(-1, 1, 1, 1).to(self.grid.real_dtype)

    def normalize_modes(self, psi_modes: torch.Tensor, target_norm: float) -> torch.Tensor:
        current_norm = self.total_norm(psi_modes).clamp_min(1.0e-12)
        return psi_modes * (target_norm / current_norm).sqrt().to(psi_modes.dtype)

    def total_norm(self, psi_modes: torch.Tensor) -> torch.Tensor:
        density = psi_modes.abs().square().sum(dim=0)
        return density.sum() * self.grid.cell_volume

    def build_state(self, psi_modes: torch.Tensor, time: float, step: int, rho_ambient: float) -> MatterState:
        a_value = self.geometry.equilibrium_a(rho_ambient)
        return MatterState(psi_modes=psi_modes, time=time, step=step, a=a_value, rho_ambient=rho_ambient)

    def reconstruct_nodes(self, psi_modes: torch.Tensor) -> torch.Tensor:
        return self.basis.reconstruct(psi_modes)

    def project_nodes(self, psi_nodes: torch.Tensor) -> torch.Tensor:
        return self.basis.project(psi_nodes)

    def effective_spatial_density(self, psi_modes: torch.Tensor) -> torch.Tensor:
        return psi_modes.abs().square().sum(dim=0)

    def estimate_defect_center(self, psi_modes: torch.Tensor) -> torch.Tensor:
        rho = self.effective_spatial_density(psi_modes)
        mass = rho.sum().clamp_min(1.0e-12) * self.grid.cell_volume
        center = torch.stack(
            [
                (self.x_grid * rho).sum() * self.grid.cell_volume / mass,
                (self.y_grid * rho).sum() * self.grid.cell_volume / mass,
                (self.z_grid * rho).sum() * self.grid.cell_volume / mass,
            ],
            dim=0,
        )
        return center

    def confinement_potential(self, a_value: float, center: torch.Tensor | None = None) -> torch.Tensor:
        L_value = self.geometry.lambda_aspect * a_value
        if center is None:
            radial_squared = self.radial_squared
        else:
            cx, cy, cz = center.to(self.grid.real_dtype)
            radial_squared = (self.x_grid - cx).square() + (self.y_grid - cy).square() + (self.z_grid - cz).square()
        radial_term = 0.5 * self.trap_strength_r * radial_squared / (a_value**2)
        transverse_term = 0.5 * self.trap_strength_w * self.w_squared / (L_value**2)
        return radial_term.unsqueeze(0) + transverse_term

    def nonlinear_potential(
        self,
        psi_nodes: torch.Tensor,
        a_value: float,
        rho_ambient: float,
        external_potential: torch.Tensor | None = None,
        confinement_center: torch.Tensor | None = None,
    ) -> torch.Tensor:
        local_density = psi_nodes.abs().square()
        potential = self.confinement_potential(a_value, center=confinement_center)
        if external_potential is not None:
            potential = potential + (external_potential.unsqueeze(0) if external_potential.ndim == 3 else external_potential)
        return potential + self.eos.relative_enthalpy(local_density, rho_ambient)

    def linear_half_step(self, psi_modes: torch.Tensor, delta: complex | float) -> torch.Tensor:
        linear_operator = self.kinetic_prefactor * self.k_squared.unsqueeze(0) + self.transverse_prefactor * self.mode_masses_sq
        phase = torch.exp(torch.as_tensor(delta, device=psi_modes.device) * linear_operator.to(self.complex_dtype))
        psi_fft = fft3(psi_modes)
        psi_fft = psi_fft * phase
        return ifft3(psi_fft)

    def nonlinear_full_step(
        self,
        psi_modes: torch.Tensor,
        delta: complex | float,
        a_value: float,
        rho_ambient: float,
        external_potential: torch.Tensor | None = None,
        confinement_center: torch.Tensor | None = None,
        node_amplitude_mask: torch.Tensor | None = None,
    ) -> torch.Tensor:
        psi_nodes = self.nonlinear_full_step_nodes(
            psi_modes,
            delta,
            a_value,
            rho_ambient,
            external_potential=external_potential,
            confinement_center=confinement_center,
        )
        psi_nodes = self.apply_node_amplitude_mask_to_nodes(psi_nodes, node_amplitude_mask=node_amplitude_mask)
        return self.project_nodes(psi_nodes)

    def nonlinear_full_step_nodes(
        self,
        psi_modes: torch.Tensor,
        delta: complex | float,
        a_value: float,
        rho_ambient: float,
        external_potential: torch.Tensor | None = None,
        confinement_center: torch.Tensor | None = None,
    ) -> torch.Tensor:
        psi_nodes = self.reconstruct_nodes(psi_modes)
        potential = self.nonlinear_potential(
            psi_nodes,
            a_value,
            rho_ambient,
            external_potential=external_potential,
            confinement_center=confinement_center,
        )
        phase = torch.exp(torch.as_tensor(delta, device=psi_modes.device) * potential.to(self.complex_dtype))
        psi_nodes = psi_nodes * phase
        return psi_nodes

    def apply_node_amplitude_mask_to_nodes(
        self,
        psi_nodes: torch.Tensor,
        node_amplitude_mask: torch.Tensor | None = None,
    ) -> torch.Tensor:
        return apply_boundary_sponge_to_nodes(psi_nodes, node_amplitude_mask)

    def step_components(
        self,
        state: MatterState,
        dt: float,
        rho_ambient: float,
        external_potential: torch.Tensor | None = None,
        node_amplitude_mask: torch.Tensor | None = None,
    ) -> dict[str, MatterState]:
        a_value = self.geometry.equilibrium_a(rho_ambient, initial_guess=state.a)
        confinement_center = self.estimate_defect_center(state.psi_modes)
        psi_half = self.linear_half_step(state.psi_modes, -0.5j * dt)
        linear1_state = MatterState(
            psi_modes=psi_half,
            time=state.time + 0.5 * dt,
            step=state.step,
            a=a_value,
            rho_ambient=rho_ambient,
        )
        nonlinear_nodes = self.nonlinear_full_step_nodes(
            psi_half,
            -1.0j * dt,
            a_value,
            rho_ambient,
            external_potential=external_potential,
            confinement_center=confinement_center,
        )
        psi_nonlinear = self.project_nodes(nonlinear_nodes)
        nonlinear_state = MatterState(
            psi_modes=psi_nonlinear,
            time=state.time + 0.5 * dt,
            step=state.step,
            a=a_value,
            rho_ambient=rho_ambient,
        )
        sponge_nodes = self.apply_node_amplitude_mask_to_nodes(nonlinear_nodes, node_amplitude_mask=node_amplitude_mask)
        psi_sponge = self.project_nodes(sponge_nodes)
        sponge_state = MatterState(
            psi_modes=psi_sponge,
            time=state.time + 0.5 * dt,
            step=state.step,
            a=a_value,
            rho_ambient=rho_ambient,
        )
        psi_next = self.linear_half_step(psi_sponge, -0.5j * dt)
        linear2_state = MatterState(
            psi_modes=psi_next,
            time=state.time + dt,
            step=state.step + 1,
            a=a_value,
            rho_ambient=rho_ambient,
        )
        return {
            "start": state,
            "linear1": linear1_state,
            "nonlinear": nonlinear_state,
            "sponge": sponge_state,
            "linear2": linear2_state,
        }

    def step(
        self,
        state: MatterState,
        dt: float,
        rho_ambient: float,
        external_potential: torch.Tensor | None = None,
        node_amplitude_mask: torch.Tensor | None = None,
    ) -> MatterState:
        return self.step_components(
            state,
            dt,
            rho_ambient,
            external_potential=external_potential,
            node_amplitude_mask=node_amplitude_mask,
        )["linear2"]

    def step_imaginary(
        self,
        state: MatterState,
        dtau: float,
        target_norm: float,
        external_potential: torch.Tensor | None = None,
        node_amplitude_mask: torch.Tensor | None = None,
    ) -> MatterState:
        a_value = self.geometry.equilibrium_a(state.rho_ambient, initial_guess=state.a)
        confinement_center = self.estimate_defect_center(state.psi_modes)
        psi_half = self.linear_half_step(state.psi_modes, -0.5 * dtau)
        psi_full = self.nonlinear_full_step(
            psi_half,
            -dtau,
            a_value,
            state.rho_ambient,
            external_potential=external_potential,
            confinement_center=confinement_center,
            node_amplitude_mask=node_amplitude_mask,
        )
        psi_next = self.linear_half_step(psi_full, -0.5 * dtau)
        psi_next = self.normalize_modes(psi_next, target_norm)
        return MatterState(psi_modes=psi_next, time=state.time, step=state.step + 1, a=a_value, rho_ambient=state.rho_ambient)

    def gradients_xyz_nodes(self, psi_nodes: torch.Tensor) -> torch.Tensor:
        kx, ky, kz = self.grid.wave_numbers()
        psi_fft = torch.fft.fftn(psi_nodes, dim=(-3, -2, -1))
        gradients = [
            torch.fft.ifftn(1j * component.unsqueeze(0) * psi_fft, dim=(-3, -2, -1))
            for component in (kx, ky, kz)
        ]
        return torch.stack(gradients, dim=0)

    def currents(self, psi_modes: torch.Tensor) -> dict[str, torch.Tensor]:
        psi_nodes = self.reconstruct_nodes(psi_modes)
        gradients_xyz = self.gradients_xyz_nodes(psi_nodes)
        derivative_w = self.basis.derivative_in_w(psi_modes)
        current_xyz = (psi_nodes.conj().unsqueeze(0) * gradients_xyz).imag / self.mass
        current_w = (psi_nodes.conj() * derivative_w).imag / self.mass
        return {
            "psi_nodes": psi_nodes,
            "current_xyz": current_xyz,
            "current_w": current_w,
        }

    def snapshot(self, state: MatterState) -> dict[str, Any]:
        currents = self.currents(state.psi_modes)
        return {
            "psi_modes": state.psi_modes,
            "psi_nodes": currents["psi_nodes"],
            "current_xyz": currents["current_xyz"],
            "current_w": currents["current_w"],
            "defect_center": self.estimate_defect_center(state.psi_modes),
            "time": state.time,
            "step": state.step,
            "a": state.a,
            "rho_ambient": state.rho_ambient,
        }
