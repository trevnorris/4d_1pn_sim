from __future__ import annotations

from pathlib import Path
from typing import Any

import torch

from src.core.checkpoints import load_checkpoint
from src.core.grids import SpatialGrid3D, resolve_device
from src.core.hermite import HermiteBasis
from src.core.projection import ProjectionKernel
from src.physics.defects import (
    bath_plus_gaussian_initial_modes,
    gaussian_initial_modes,
    imaginary_time_relax,
    uniform_mode0_initial_modes,
)
from src.physics.eos import PolytropicEOS
from src.physics.geometry import AdiabaticGeometryClosure
from src.physics.matter_gnls import MatterSplitStepSolver, MatterState


DTYPE_MAP = {
    "float32": torch.float32,
    "float64": torch.float64,
    "complex64": torch.complex64,
    "complex128": torch.complex128,
}


def build_solver(config: dict[str, Any]) -> tuple[MatterSplitStepSolver, ProjectionKernel]:
    device = resolve_device(config["device"])
    real_dtype = DTYPE_MAP[config["dtype"]]
    complex_dtype = DTYPE_MAP[config["complex_dtype"]]

    grid = SpatialGrid3D.from_config(
        shape=config["grid"]["shape"],
        length=config["grid"]["length"],
        device=device,
        real_dtype=real_dtype,
    )
    basis = HermiteBasis(
        num_modes=config["hermite"]["num_modes"],
        lambda_w=config["hermite"]["lambda_w"],
        quadrature_order=config["hermite"]["quadrature_order"],
        device=device,
        real_dtype=real_dtype,
    )
    eos = PolytropicEOS(K_eos=config["eos"]["K_eos"], n=config["eos"]["n"])
    geometry = AdiabaticGeometryClosure(
        eos=eos,
        lambda_aspect=config["geometry"]["lambda_aspect"],
        reference_rho=config["geometry"]["reference_rho"],
        reference_a=config["geometry"]["reference_a"],
        reference_energy_scale=config["geometry"]["reference_energy_scale"],
    )
    solver = MatterSplitStepSolver(
        grid=grid,
        basis=basis,
        eos=eos,
        geometry=geometry,
        complex_dtype=complex_dtype,
        mass=config["solver"]["mass"],
        kinetic_prefactor=config["solver"]["kinetic_prefactor"],
        transverse_prefactor=config["solver"]["transverse_prefactor"],
        trap_strength_r=config["solver"]["trap_strength_r"],
        trap_strength_w=config["solver"]["trap_strength_w"],
    )
    projection = ProjectionKernel.gaussian(
        nodes=basis.nodes,
        quadrature_weights=basis.weights,
        width=basis.lambda_w,
    )
    return solver, projection


def serializable_diag(diag: dict[str, Any]) -> dict[str, Any]:
    payload = {}
    for key, value in diag.items():
        if isinstance(value, torch.Tensor):
            continue
        payload[key] = value
    return payload


def clone_state(state: MatterState) -> MatterState:
    return MatterState(
        psi_modes=state.psi_modes.clone(),
        time=float(state.time),
        step=int(state.step),
        a=float(state.a),
        rho_ambient=float(state.rho_ambient),
    )


def state_from_checkpoint(
    path: str | Path,
    solver: MatterSplitStepSolver,
) -> MatterState:
    checkpoint_state = load_checkpoint(path, device=solver.grid.device, complex_dtype=solver.complex_dtype)
    return MatterState(
        psi_modes=checkpoint_state["psi_modes"],
        time=float(checkpoint_state["time"]),
        step=int(checkpoint_state["step"]),
        a=float(checkpoint_state["a"]),
        rho_ambient=float(checkpoint_state["rho_ambient"]),
    )


def prepare_relaxed_state(
    solver: MatterSplitStepSolver,
    config: dict[str, Any],
    rho_ambient: float,
) -> MatterState:
    initializer = dict(config["initializer"])
    mode = str(initializer.get("mode", "gaussian_defect"))

    if mode == "gaussian_defect":
        state = gaussian_initial_modes(
            solver=solver,
            gaussian_width=float(initializer["gaussian_width"]),
            target_norm=float(initializer["target_norm"]),
            rho_ambient=rho_ambient,
            center=tuple(float(v) for v in initializer.get("center", (0.0, 0.0, 0.0))),
            momentum=tuple(float(v) for v in initializer.get("momentum", (0.0, 0.0, 0.0))),
        )
        relax_enabled = bool(initializer.get("apply_imaginary_relaxation", True))
    elif mode == "uniform_bath":
        state = uniform_mode0_initial_modes(
            solver=solver,
            bath_density=float(initializer["bath_density"]),
            rho_ambient=rho_ambient,
            phase_offset=float(initializer.get("bath_phase_offset", 0.0)),
        )
        relax_enabled = bool(initializer.get("apply_imaginary_relaxation", False))
    elif mode == "bath_plus_gaussian_defect":
        state = bath_plus_gaussian_initial_modes(
            solver=solver,
            bath_density=float(initializer["bath_density"]),
            defect_target_norm=float(initializer.get("defect_target_norm", initializer["target_norm"])),
            gaussian_width=float(initializer["gaussian_width"]),
            rho_ambient=rho_ambient,
            center=tuple(float(v) for v in initializer.get("center", (0.0, 0.0, 0.0))),
            momentum=tuple(float(v) for v in initializer.get("momentum", (0.0, 0.0, 0.0))),
            bath_phase_offset=float(initializer.get("bath_phase_offset", 0.0)),
            defect_phase_offset=float(initializer.get("defect_phase_offset", 0.5 * 3.141592653589793)),
        )
        relax_enabled = bool(initializer.get("apply_imaginary_relaxation", False))
    else:
        raise ValueError(f"unsupported initializer mode: {mode}")

    relax_steps = int(initializer.get("steps", 0))
    if not relax_enabled or relax_steps <= 0:
        return state
    return imaginary_time_relax(
        solver=solver,
        state=state,
        dtau=float(initializer["imaginary_dt"]),
        steps=relax_steps,
        target_norm=float(initializer["target_norm"]),
    )
