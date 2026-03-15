from __future__ import annotations

from typing import Any

import numpy as np
import torch

from src.core.projection import ProjectionKernel, projected_continuity_terms
from src.physics.fitting import extract_effective_response, fit_loglog_slope
from src.physics.matter_gnls import MatterSplitStepSolver, MatterState
from src.physics.observables import (
    bound_mass_fraction,
    center_of_mass,
    coherence,
    mode_occupations,
    radius_of_gyration,
)


def snapshot_diagnostics(
    solver: MatterSplitStepSolver,
    state: MatterState,
    projection_kernel: ProjectionKernel,
    reference_modes: torch.Tensor,
    bound_radius_factor: float,
    previous_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    snapshot = solver.snapshot(state)
    psi_nodes = snapshot["psi_nodes"]
    rho_nodes = psi_nodes.abs().square()
    rho_brane = projection_kernel.project(rho_nodes)
    occupations = mode_occupations(state.psi_modes, solver.grid.cell_volume)
    higher_mode_fraction = float(occupations[1:].sum() / occupations.sum().clamp_min(1.0e-12))
    diag: dict[str, Any] = {
        "time": float(state.time),
        "step": int(state.step),
        "rho_ambient": float(state.rho_ambient),
        "a": float(state.a),
        "L": float(solver.geometry.lambda_aspect * state.a),
        "norm": float(solver.total_norm(state.psi_modes)),
        "center_of_mass": center_of_mass(rho_brane, solver.grid).detach().cpu().numpy().tolist(),
        "radius_of_gyration": float(radius_of_gyration(rho_brane, solver.grid)),
        "bound_mass_fraction": float(
            bound_mass_fraction(rho_brane, solver.grid, bound_radius_factor * state.a)
        ),
        "mode_occupations": occupations.detach().cpu().numpy().tolist(),
        "higher_mode_fraction": higher_mode_fraction,
        "coherence": float(coherence(reference_modes, state.psi_modes, solver.grid.cell_volume)),
    }

    closure = solver.geometry.closure_diagnostics(state.rho_ambient)
    for key, value in closure.items():
        diag[key] = float(value)

    if previous_snapshot is not None:
        dt = max(state.time - previous_snapshot["time"], 1.0e-12)
        drho_dt = (rho_nodes - previous_snapshot["rho_nodes"]) / dt
        continuity = projected_continuity_terms(
            rho=rho_nodes,
            drho_dt=drho_dt,
            current_xyz=snapshot["current_xyz"],
            current_w=snapshot["current_w"],
            kernel=projection_kernel,
            grid=solver.grid,
        )
        residual = continuity["continuity_residual"]
        diag["continuity_residual_l2"] = float(torch.sqrt((residual.square()).mean()))
        diag["mean_S_leak"] = float(continuity["S_leak"].abs().mean())
    else:
        diag["continuity_residual_l2"] = 0.0
        diag["mean_S_leak"] = 0.0

    diag["rho_nodes"] = rho_nodes
    return diag


def summarize_closure_scan(scan_rows: list[dict[str, Any]]) -> dict[str, Any]:
    rho_values = np.array([row["rho_ambient"] for row in scan_rows], dtype=np.float64)
    a_values = np.array([row["a_eq"] for row in scan_rows], dtype=np.float64)
    f_values = np.array([row["F_eq"] for row in scan_rows], dtype=np.float64)
    a_fit = fit_loglog_slope(rho_values, a_values)
    f_fit = fit_loglog_slope(rho_values, f_values)
    mean_partition = {
        key: float(np.mean([row[key] for row in scan_rows]))
        for key in ("E_w", "E_f", "E_PV")
    }
    total_partition = sum(mean_partition.values())
    partition_fraction = {key: value / total_partition for key, value in mean_partition.items()}
    return {
        "rho_values": rho_values.tolist(),
        "a_fit": a_fit,
        "F_fit": f_fit,
        "kappa_PV_estimate": f_fit["slope"] - 1.0,
        "partition_mean": mean_partition,
        "partition_fraction": partition_fraction,
    }


def summarize_drive_response(
    time: np.ndarray,
    effort_signal: np.ndarray,
    flux_signal: np.ndarray,
    omega: float,
    cycles_to_skip: int,
) -> dict[str, Any]:
    response = extract_effective_response(
        effort_ports=np.asarray(effort_signal)[None, :],
        flux_ports=np.asarray(flux_signal)[None, :],
        time=time,
        omega=omega,
        cycles_to_skip=cycles_to_skip,
    )
    z_eff = response["Z_eff"][0, 0]
    return {
        "effort_amplitude_real": float(np.real(response["effort_amplitude"][0, 0])),
        "effort_amplitude_imag": float(np.imag(response["effort_amplitude"][0, 0])),
        "flux_amplitude_real": float(np.real(response["flux_amplitude"][0, 0])),
        "flux_amplitude_imag": float(np.imag(response["flux_amplitude"][0, 0])),
        "Z_eff_real": float(np.real(z_eff)),
        "Z_eff_imag": float(np.imag(z_eff)),
        "Z_eff_abs": float(np.abs(z_eff)),
    }
