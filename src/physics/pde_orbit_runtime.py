from __future__ import annotations

from typing import Any

import numpy as np
import torch

from src.core.projection import projected_continuity_terms
from src.physics.background_sources import StaticCentralBackground
from src.physics.launch_calibration import probe_launch_response, safe_launch_speed_limit, summarize_launch_calibration
from src.physics.observables import mode_occupations, translation_aligned_coherence


def effective_radius_of_gyration(solver, psi_modes: torch.Tensor) -> float:
    rho = solver.effective_spatial_density(psi_modes)
    mass = rho.sum().clamp_min(1.0e-12) * solver.grid.cell_volume
    center = solver.estimate_defect_center(psi_modes)
    radius_sq = (
        (solver.x_grid - center[0]).square()
        + (solver.y_grid - center[1]).square()
        + (solver.z_grid - center[2]).square()
    )
    return float(torch.sqrt((radius_sq * rho).sum() * solver.grid.cell_volume / mass))


def sample_light_metrics(
    solver,
    state,
    reference_modes: torch.Tensor,
) -> dict[str, float]:
    occupations = mode_occupations(state.psi_modes, solver.grid.cell_volume)
    occupation_total = occupations.sum().clamp_min(1.0e-12)
    return {
        "mean_coherence": float(
            translation_aligned_coherence(solver, reference_modes, state.psi_modes, solver.grid.cell_volume)
        ),
        "mean_higher_mode_fraction": float(occupations[1:].sum() / occupation_total),
        "mean_compactness": effective_radius_of_gyration(solver, state.psi_modes),
    }


def sample_continuity_metrics(
    solver,
    state,
    projection_kernel,
    previous_snapshot: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, float]]:
    currents = solver.currents(state.psi_modes)
    rho_nodes = currents["psi_nodes"].abs().square()
    if previous_snapshot is None:
        metrics = {
            "mean_leakage": 0.0,
            "mean_continuity_residual": 0.0,
        }
    else:
        dt = max(float(state.time) - float(previous_snapshot["time"]), 1.0e-12)
        continuity = projected_continuity_terms(
            rho=rho_nodes,
            drho_dt=(rho_nodes - previous_snapshot["rho_nodes"]) / dt,
            current_xyz=currents["current_xyz"],
            current_w=currents["current_w"],
            kernel=projection_kernel,
            grid=solver.grid,
        )
        residual = continuity["continuity_residual"]
        metrics = {
            "mean_leakage": float(continuity["S_leak"].abs().mean()),
            "mean_continuity_residual": float(torch.sqrt((residual.square()).mean())),
        }
    next_snapshot = {
        "time": float(state.time),
        "rho_nodes": rho_nodes.detach().clone(),
    }
    del currents
    return next_snapshot, metrics


def window_mean(
    values: np.ndarray,
    sample_times: np.ndarray,
    start_time: float,
    end_time: float,
) -> float:
    if values.size == 0:
        return 0.0
    mask = (sample_times >= start_time) & (sample_times <= end_time)
    if not np.any(mask):
        nearest = int(np.argmin(np.abs(sample_times - 0.5 * (start_time + end_time))))
        return float(values[nearest])
    return float(np.mean(values[mask]))


def run_static_launch_calibration(
    solver,
    relaxed_state,
    config: dict[str, Any],
    background: StaticCentralBackground,
    background_potential,
    rho0: float,
    scenario: str,
) -> dict[str, Any] | None:
    calibration = dict(config.get("launch_calibration", {}))
    if not bool(calibration.get("enabled", False)):
        return None

    periapsis_radius = float(config["experiment"]["periapsis_radius"])
    eccentricity = float(config["experiment"]["eccentricity"])
    base_speed = background.periapsis_speed(periapsis_radius, eccentricity)
    target_speed = base_speed * float(config["experiment"].get("velocity_scale", 1.0))
    safe_fraction = float(calibration.get("safe_nyquist_fraction", 0.65))
    safe_speed = safe_launch_speed_limit(solver, nyquist_fraction=safe_fraction)
    boundary_clearance_floor = float(
        calibration.get("boundary_clearance_floor", 3.0 * max(float(dx) for dx in solver.grid.dx))
    )
    probe_steps = int(calibration.get("probe_steps", 160))
    measure_start_step = int(calibration.get("measure_start_step", 8))
    measure_end_step = calibration.get("measure_end_step")
    measure_end_step = int(measure_end_step) if measure_end_step is not None else None
    scales = [float(value) for value in calibration.get("velocity_scale_samples", [0.9, 0.95, 1.0, 1.05, 1.1])]
    probes = []
    for velocity_scale in scales:
        applied_speed = base_speed * velocity_scale
        if applied_speed > safe_speed:
            continue
        probe = probe_launch_response(
            solver=solver,
            state=relaxed_state,
            applied_speed=applied_speed,
            shift=(periapsis_radius, 0.0, 0.0),
            dt=float(config["solver"]["dt"]),
            steps=probe_steps,
            source_center=background.center,
            rho_reference=rho0,
            external_potential=background_potential,
            ambient_density_fn=background.ambient_density_at_position if scenario == "source_with_dressing" else None,
            measure_start_step=measure_start_step,
            measure_end_step=measure_end_step,
        )
        probe["velocity_scale"] = velocity_scale
        probes.append(probe)

    if not probes:
        return None
    summary = summarize_launch_calibration(
        probes=probes,
        target_speed=target_speed,
        safe_speed_limit=safe_speed,
        boundary_clearance_floor=boundary_clearance_floor,
    )
    summary.update(
        {
            "scenario": scenario,
            "base_periapsis_speed": float(base_speed),
            "target_velocity_scale": float(config["experiment"].get("velocity_scale", 1.0)),
            "safe_nyquist_fraction": safe_fraction,
            "probe_steps": probe_steps,
            "measure_start_step": measure_start_step,
            "measure_end_step": measure_end_step,
        }
    )
    return summary
