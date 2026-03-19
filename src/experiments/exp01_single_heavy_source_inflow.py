from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import torch

from src.core.checkpoints import save_checkpoint
from src.core.config import load_json_config
from src.core.io import collect_runtime_info, dump_json, ensure_dir
from src.experiments.common import build_solver, prepare_relaxed_state, state_from_checkpoint
from src.physics.boundary_sponge import BoundarySponge, build_boundary_sponge_mask
from src.physics.defects import uniform_mode0_initial_modes
from src.physics.open_system import (
    BoundaryDensityRelaxation,
    BoundaryReservoirRefill,
    UniformReservoirRefill,
    build_mode_leakage_matrix,
)
from src.physics.source_inflow import sample_source_inflow_metrics, summarize_source_inflow_series


def _empty_source_history() -> dict[str, list]:
    return {
        "time": [],
        "center": [],
        "total_norm": [],
        "box_mean_density": [],
        "compactness": [],
        "bound_mass_fraction": [],
        "core_mass": [],
        "core_mean_density": [],
        "ambient_mean_density": [],
        "coherence": [],
        "higher_mode_fraction": [],
        "mean_leakage": [],
        "signed_leakage_mean": [],
        "shell_inflow_rates": [],
        "shell_mean_densities": [],
        "refill_delta_norm": [],
        "refill_cumulative_norm": [],
    }


def _append_source_history(
    history: dict[str, list],
    metrics: dict[str, object],
    refill_metrics: dict[str, float],
    time_value: float,
) -> None:
    history["time"].append(float(time_value))
    history["center"].append(list(metrics["center"]))
    history["total_norm"].append(float(metrics["total_norm"]))
    history["box_mean_density"].append(float(metrics["box_mean_density"]))
    history["compactness"].append(float(metrics["radius_of_gyration"]))
    history["bound_mass_fraction"].append(float(metrics["bound_mass_fraction"]))
    history["core_mass"].append(float(metrics["core_mass"]))
    history["core_mean_density"].append(float(metrics["core_mean_density"]))
    history["ambient_mean_density"].append(float(metrics["ambient_mean_density"]))
    history["coherence"].append(float(metrics["coherence"]))
    history["higher_mode_fraction"].append(float(metrics["higher_mode_fraction"]))
    history["mean_leakage"].append(float(metrics["mean_leakage"]))
    history["signed_leakage_mean"].append(float(metrics["signed_leakage_mean"]))
    history["shell_inflow_rates"].append([float(value) for value in metrics["shell_inflow_rates"]])
    history["shell_mean_densities"].append([float(value) for value in metrics["shell_mean_densities"]])
    history["refill_delta_norm"].append(float(refill_metrics["delta_norm_applied"]))
    history["refill_cumulative_norm"].append(float(refill_metrics["cumulative_refill_norm"]))


def _history_to_summary(history: dict[str, list], shell_radii: list[float]) -> dict[str, object] | None:
    if not history["time"]:
        return None
    return summarize_source_inflow_series(
        shell_radii=shell_radii,
        shell_inflow_rates=np.asarray(history["shell_inflow_rates"], dtype=np.float64),
        shell_mean_densities=np.asarray(history["shell_mean_densities"], dtype=np.float64),
        total_norm=np.asarray(history["total_norm"], dtype=np.float64),
        box_mean_density=np.asarray(history["box_mean_density"], dtype=np.float64),
        ambient_mean_density=np.asarray(history["ambient_mean_density"], dtype=np.float64),
        core_mass=np.asarray(history["core_mass"], dtype=np.float64),
        core_mean_density=np.asarray(history["core_mean_density"], dtype=np.float64),
        coherence=np.asarray(history["coherence"], dtype=np.float64),
        higher_mode_fraction=np.asarray(history["higher_mode_fraction"], dtype=np.float64),
        compactness=np.asarray(history["compactness"], dtype=np.float64),
        bound_mass_fraction_series=np.asarray(history["bound_mass_fraction"], dtype=np.float64),
        mean_leakage=np.asarray(history["mean_leakage"], dtype=np.float64),
        signed_leakage_mean=np.asarray(history["signed_leakage_mean"], dtype=np.float64),
    )


def run(config_path: str | Path, restart_relaxed: str | None = None) -> Path:
    config = load_json_config(config_path)
    seed = int(config["seed"])
    np.random.seed(seed)
    torch.manual_seed(seed)

    output_dir = ensure_dir(config["output_dir"], overwrite=bool(config.get("overwrite_output", False)))
    dump_json(output_dir / "config.json", config)
    dump_json(output_dir / "runtime.json", collect_runtime_info(seed))

    solver, projection_kernel = build_solver(config)
    rho0 = float(config["geometry"]["reference_rho"])
    dt = float(config["solver"]["dt"])
    initializer_config = dict(config["initializer"])
    initializer_mode = str(initializer_config.get("mode", "gaussian_defect"))
    prefilled_bath_density = (
        float(initializer_config["bath_density"])
        if "bath_density" in initializer_config
        else None
    )
    embedded_defect_enabled = initializer_mode in {"gaussian_defect", "bath_plus_gaussian_defect"}
    experiment_config = dict(config["experiment"])
    conditioning_steps = max(0, int(experiment_config.get("conditioning_steps", 0)))
    evolution_steps = int(experiment_config["evolution_steps"])
    metric_stride = max(1, int(experiment_config.get("metric_stride", 64)))
    progress_stride = max(1, int(experiment_config.get("progress_stride", 512)))
    conditioning_metric_stride = max(1, int(experiment_config.get("conditioning_metric_stride", metric_stride)))
    conditioning_progress_stride = max(1, int(experiment_config.get("conditioning_progress_stride", progress_stride)))
    conditioning_ramp_refill = bool(experiment_config.get("conditioning_ramp_refill", conditioning_steps > 0))
    conditioning_ramp_fraction = float(experiment_config.get("conditioning_ramp_fraction", 0.5))
    conditioning_ramp_fraction = min(max(conditioning_ramp_fraction, 1.0e-6), 1.0)
    conditioning_refill_scale = float(experiment_config.get("conditioning_refill_scale", 1.0))
    production_refill_scale = float(experiment_config.get("production_refill_scale", 1.0))
    shell_radii = [float(value) for value in experiment_config["shell_radii"]]
    shell_band_width = float(experiment_config["shell_band_width"])
    core_radius = float(experiment_config["core_radius"])
    ambient_probe_radius = float(experiment_config["ambient_probe_radius"])
    report_shell_index = min(
        max(0, int(experiment_config.get("report_shell_index", len(shell_radii) // 2))),
        len(shell_radii) - 1,
    )

    checkpoint_config = dict(config.get("checkpoints", {}))
    save_relaxed = bool(checkpoint_config.get("save_relaxed", True))
    save_conditioned = bool(checkpoint_config.get("save_conditioned", False))
    save_final = bool(checkpoint_config.get("save_final", False))

    boundary_sponge_config = dict(config.get("boundary_sponge", {}))
    node_amplitude_mask = None
    if bool(boundary_sponge_config.get("enabled", False)):
        sponge_mask = build_boundary_sponge_mask(
            grid=solver.grid,
            dt=dt,
            config=boundary_sponge_config,
        )
        preserve_bath_perturbations = bool(boundary_sponge_config.get("preserve_bath_perturbations", False))
        if preserve_bath_perturbations and prefilled_bath_density is not None:
            bath_reference_state = uniform_mode0_initial_modes(
                solver=solver,
                bath_density=prefilled_bath_density,
                rho_ambient=rho0,
                phase_offset=float(initializer_config.get("bath_phase_offset", 0.0)),
            )
            node_amplitude_mask = BoundarySponge(
                mask=sponge_mask,
                target_nodes=solver.reconstruct_nodes(bath_reference_state.psi_modes),
            )
        else:
            node_amplitude_mask = sponge_mask

    refill_config = dict(config.get("reservoir_refill", {}))
    boundary_reservoir_config = dict(config.get("boundary_reservoir", {}))
    boundary_relaxation_config = dict(config.get("boundary_relaxation", {}))
    refill_controller = None
    refill_mode = "disabled"
    if bool(boundary_relaxation_config.get("enabled", False)):
        refill_controller = BoundaryDensityRelaxation.from_config(
            solver=solver,
            target_norm=float(config["initializer"]["target_norm"]),
            config=boundary_relaxation_config,
        )
        refill_mode = "boundary_relaxation"
    elif bool(boundary_reservoir_config.get("enabled", False)):
        refill_controller = BoundaryReservoirRefill.from_config(
            solver=solver,
            projection_kernel=projection_kernel,
            target_norm=float(config["initializer"]["target_norm"]),
            config=boundary_reservoir_config,
        )
        refill_mode = "boundary"
    elif bool(refill_config.get("enabled", False)):
        refill_controller = UniformReservoirRefill.from_config(
            solver=solver,
            projection_kernel=projection_kernel,
            target_norm=float(config["initializer"]["target_norm"]),
            config=refill_config,
        )
        refill_mode = "uniform"

    leakage_matrix = build_mode_leakage_matrix(solver.basis, projection_kernel).to(solver.grid.device)
    base_refill_cap = (
        float(refill_controller.max_delta_norm_fraction_per_step)
        if refill_controller is not None and hasattr(refill_controller, "max_delta_norm_fraction_per_step")
        else 0.0
    )
    if refill_controller is not None and hasattr(refill_controller, "stage_scale"):
        refill_controller.stage_scale = float(production_refill_scale)

    print(f"[exp01-heavy] output_dir={output_dir}")
    if restart_relaxed is not None:
        print(f"[exp01-heavy] stage=load_relaxed checkpoint={restart_relaxed}")
        state = state_from_checkpoint(restart_relaxed, solver=solver)
    else:
        print("[exp01-heavy] stage=relax start")
        state = prepare_relaxed_state(solver=solver, config=config, rho_ambient=rho0)
        if save_relaxed:
            save_checkpoint(
                output_dir / "checkpoint_relaxed.npz",
                {
                    "psi_modes": state.psi_modes,
                    "time": state.time,
                    "step": state.step,
                    "a": state.a,
                    "rho_ambient": state.rho_ambient,
                },
            )
        print("[exp01-heavy] stage=relax done")

    relaxed_reference_modes = state.psi_modes.clone()
    conditioning_history = _empty_source_history()
    production_history = _empty_source_history()

    if conditioning_steps > 0:
        print(f"[exp01-heavy] stage=condition start steps={conditioning_steps}")
        ramp_steps = max(1, int(np.ceil(conditioning_steps * conditioning_ramp_fraction)))
        for idx in range(conditioning_steps):
            state = solver.step(
                state,
                dt=dt,
                rho_ambient=rho0,
                node_amplitude_mask=node_amplitude_mask,
            )
            refill_metrics = {
                "delta_norm_applied": 0.0,
                "cumulative_refill_norm": 0.0,
            }
            if refill_controller is not None:
                if hasattr(refill_controller, "stage_scale"):
                    if conditioning_ramp_refill:
                        ramp_scale = min(float(idx + 1) / float(ramp_steps), 1.0)
                    else:
                        ramp_scale = 1.0
                    refill_controller.stage_scale = conditioning_refill_scale * ramp_scale
                if base_refill_cap > 0.0:
                    if conditioning_ramp_refill:
                        cap_scale = min(float(idx + 1) / float(ramp_steps), 1.0)
                        refill_controller.max_delta_norm_fraction_per_step = base_refill_cap * cap_scale
                    else:
                        refill_controller.max_delta_norm_fraction_per_step = base_refill_cap * conditioning_refill_scale
                state, refill_metrics = refill_controller.apply(solver=solver, state=state, dt=dt)

            should_sample = idx == 0 or idx == conditioning_steps - 1 or (idx + 1) % conditioning_metric_stride == 0
            if should_sample:
                metrics = sample_source_inflow_metrics(
                    solver=solver,
                    psi_modes=state.psi_modes,
                    reference_modes=relaxed_reference_modes,
                    leakage_matrix=leakage_matrix,
                    shell_radii=shell_radii,
                    shell_band_width=shell_band_width,
                    core_radius=core_radius,
                    ambient_probe_radius=ambient_probe_radius,
                )
                _append_source_history(
                    conditioning_history,
                    metrics=metrics,
                    refill_metrics=refill_metrics,
                    time_value=float(state.time),
                )

            if (idx + 1) % conditioning_progress_stride == 0 or idx == conditioning_steps - 1:
                report_inflow = (
                    float(conditioning_history["shell_inflow_rates"][-1][report_shell_index])
                    if conditioning_history["shell_inflow_rates"]
                    else 0.0
                )
                report_coherence = float(conditioning_history["coherence"][-1]) if conditioning_history["coherence"] else 0.0
                print(
                    f"[exp01-heavy] stage=condition step={state.step} time={state.time:.3f} "
                    f"inflow_r{shell_radii[report_shell_index]:.2f}={report_inflow:.6e} "
                    f"coherence={report_coherence:.6f}"
                )

        if refill_controller is not None:
            if hasattr(refill_controller, "max_delta_norm_fraction_per_step"):
                refill_controller.max_delta_norm_fraction_per_step = base_refill_cap * production_refill_scale
            if hasattr(refill_controller, "stage_scale"):
                refill_controller.stage_scale = float(production_refill_scale)
        if save_conditioned:
            save_checkpoint(
                output_dir / "checkpoint_conditioned.npz",
                {
                    "psi_modes": state.psi_modes,
                    "time": state.time,
                    "step": state.step,
                    "a": state.a,
                    "rho_ambient": state.rho_ambient,
                },
            )
        print("[exp01-heavy] stage=condition done")

    reference_modes = state.psi_modes.clone()

    if refill_controller is not None:
        if hasattr(refill_controller, "max_delta_norm_fraction_per_step"):
            refill_controller.max_delta_norm_fraction_per_step = base_refill_cap * production_refill_scale
        if hasattr(refill_controller, "stage_scale"):
            refill_controller.stage_scale = float(production_refill_scale)

    print("[exp01-heavy] stage=evolve start")
    for idx in range(evolution_steps):
        state = solver.step(
            state,
            dt=dt,
            rho_ambient=rho0,
            node_amplitude_mask=node_amplitude_mask,
        )
        refill_metrics = {
            "delta_norm_applied": 0.0,
            "cumulative_refill_norm": 0.0,
        }
        if refill_controller is not None:
            state, refill_metrics = refill_controller.apply(solver=solver, state=state, dt=dt)

        should_sample = idx == 0 or idx == evolution_steps - 1 or (idx + 1) % metric_stride == 0
        if should_sample:
            metrics = sample_source_inflow_metrics(
                solver=solver,
                psi_modes=state.psi_modes,
                reference_modes=reference_modes,
                leakage_matrix=leakage_matrix,
                shell_radii=shell_radii,
                shell_band_width=shell_band_width,
                core_radius=core_radius,
                ambient_probe_radius=ambient_probe_radius,
            )
            _append_source_history(
                production_history,
                metrics=metrics,
                refill_metrics=refill_metrics,
                time_value=float(state.time),
            )

        if (idx + 1) % progress_stride == 0 or idx == evolution_steps - 1:
            report_inflow = (
                float(production_history["shell_inflow_rates"][-1][report_shell_index])
                if production_history["shell_inflow_rates"]
                else 0.0
            )
            report_coherence = float(production_history["coherence"][-1]) if production_history["coherence"] else 0.0
            print(
                f"[exp01-heavy] stage=evolve step={state.step} time={state.time:.3f} "
                f"inflow_r{shell_radii[report_shell_index]:.2f}={report_inflow:.6e} "
                f"coherence={report_coherence:.6f}"
            )

    print("[exp01-heavy] stage=evolve done")

    if save_final:
        save_checkpoint(
            output_dir / "checkpoint_final.npz",
            {
                "psi_modes": state.psi_modes,
                "time": state.time,
                "step": state.step,
                "a": state.a,
                "rho_ambient": state.rho_ambient,
            },
        )

    source_inflow_summary = _history_to_summary(production_history, shell_radii)
    if source_inflow_summary is None:
        raise RuntimeError("production history is empty; increase evolution_steps or lower metric_stride")
    conditioning_summary = _history_to_summary(conditioning_history, shell_radii)

    np.savez_compressed(
        output_dir / "timeseries.npz",
        shell_radii=np.asarray(shell_radii, dtype=np.float64),
        time=np.asarray(production_history["time"], dtype=np.float64),
        source_center=np.asarray(production_history["center"], dtype=np.float64),
        total_norm=np.asarray(production_history["total_norm"], dtype=np.float64),
        box_mean_density=np.asarray(production_history["box_mean_density"], dtype=np.float64),
        radius_of_gyration=np.asarray(production_history["compactness"], dtype=np.float64),
        bound_mass_fraction=np.asarray(production_history["bound_mass_fraction"], dtype=np.float64),
        core_mass=np.asarray(production_history["core_mass"], dtype=np.float64),
        core_mean_density=np.asarray(production_history["core_mean_density"], dtype=np.float64),
        ambient_mean_density=np.asarray(production_history["ambient_mean_density"], dtype=np.float64),
        coherence=np.asarray(production_history["coherence"], dtype=np.float64),
        higher_mode_fraction=np.asarray(production_history["higher_mode_fraction"], dtype=np.float64),
        mean_leakage=np.asarray(production_history["mean_leakage"], dtype=np.float64),
        signed_leakage_mean=np.asarray(production_history["signed_leakage_mean"], dtype=np.float64),
        shell_inflow_rates=np.asarray(production_history["shell_inflow_rates"], dtype=np.float64),
        shell_mean_densities=np.asarray(production_history["shell_mean_densities"], dtype=np.float64),
        refill_delta_norm=np.asarray(production_history["refill_delta_norm"], dtype=np.float64),
        refill_cumulative_norm=np.asarray(production_history["refill_cumulative_norm"], dtype=np.float64),
        conditioning_time=np.asarray(conditioning_history["time"], dtype=np.float64),
        conditioning_source_center=np.asarray(conditioning_history["center"], dtype=np.float64),
        conditioning_total_norm=np.asarray(conditioning_history["total_norm"], dtype=np.float64),
        conditioning_box_mean_density=np.asarray(conditioning_history["box_mean_density"], dtype=np.float64),
        conditioning_radius_of_gyration=np.asarray(conditioning_history["compactness"], dtype=np.float64),
        conditioning_bound_mass_fraction=np.asarray(conditioning_history["bound_mass_fraction"], dtype=np.float64),
        conditioning_core_mass=np.asarray(conditioning_history["core_mass"], dtype=np.float64),
        conditioning_core_mean_density=np.asarray(conditioning_history["core_mean_density"], dtype=np.float64),
        conditioning_ambient_mean_density=np.asarray(conditioning_history["ambient_mean_density"], dtype=np.float64),
        conditioning_coherence=np.asarray(conditioning_history["coherence"], dtype=np.float64),
        conditioning_higher_mode_fraction=np.asarray(conditioning_history["higher_mode_fraction"], dtype=np.float64),
        conditioning_mean_leakage=np.asarray(conditioning_history["mean_leakage"], dtype=np.float64),
        conditioning_signed_leakage_mean=np.asarray(conditioning_history["signed_leakage_mean"], dtype=np.float64),
        conditioning_shell_inflow_rates=np.asarray(conditioning_history["shell_inflow_rates"], dtype=np.float64),
        conditioning_shell_mean_densities=np.asarray(conditioning_history["shell_mean_densities"], dtype=np.float64),
        conditioning_refill_delta_norm=np.asarray(conditioning_history["refill_delta_norm"], dtype=np.float64),
        conditioning_refill_cumulative_norm=np.asarray(conditioning_history["refill_cumulative_norm"], dtype=np.float64),
    )

    completed_evolution_steps = evolution_steps
    summary = {
        "run_name": config["run_name"],
        "initializer_mode": initializer_mode,
        "embedded_defect_enabled": bool(embedded_defect_enabled),
        "prefilled_bath_density": prefilled_bath_density,
        "conditioning_steps": int(conditioning_steps),
        "conditioning_completed_steps": int(conditioning_steps),
        "conditioning_ramp_refill": bool(
            conditioning_ramp_refill
            and refill_controller is not None
            and (base_refill_cap > 0.0 or hasattr(refill_controller, "stage_scale"))
        ),
        "conditioning_ramp_fraction": float(conditioning_ramp_fraction),
        "conditioning_refill_scale": float(conditioning_refill_scale),
        "production_refill_scale": float(production_refill_scale),
        "completed_evolution_steps": int(completed_evolution_steps),
        "final_state_step": int(state.step),
        "requested_steps": evolution_steps,
        "conditioning": conditioning_summary,
        "source_inflow": source_inflow_summary,
        "boundary_sponge_enabled": bool(boundary_sponge_config.get("enabled", False)),
        "reservoir_refill_enabled": refill_controller is not None,
        "reservoir_refill_mode": refill_mode,
        "assumptions": [
            (
                "This is a single-defect source-calibration run, not a two-body gravity test."
                if embedded_defect_enabled
                else "This is a prefilled-bath boundary-control run with no embedded defect."
            ),
            (
                "The heavy source proxy is created by the chosen relaxed defect norm and confinement, not a separate throat microphysics model."
                if embedded_defect_enabled
                else "Any measured shell flux should stay near zero; persistent flow in this run would implicate the bath/boundary protocol rather than source physics."
            ),
            "Shell inflow rates are estimated from a mode-summed 3D current on thin spherical bands rather than a full 4D control-volume flux.",
            "Ambient density locking is only represented if the optional refill controller is enabled and does not by itself validate momentum neutrality.",
        ],
    }
    dump_json(output_dir / "summary.json", summary)

    mean_shell_inflow = np.asarray(source_inflow_summary["mean_shell_inflow_by_radius"], dtype=np.float64)
    best_shell = report_shell_index
    plain_language = [
        "Single heavy-source inflow calibration summary:",
        f"- Initializer mode = {initializer_mode}.",
        (
            f"- The run completed {conditioning_steps} conditioning steps and {completed_evolution_steps} measured fixed-background steps after source relaxation."
            if embedded_defect_enabled
            else f"- The run completed {conditioning_steps} conditioning steps and {completed_evolution_steps} measured fixed-background steps from a prefilled bath state."
        ),
        f"- Reservoir mode = {refill_mode}.",
        (
            f"- Prefilled bath density = {prefilled_bath_density:.6e}."
            if prefilled_bath_density is not None
            else "- No prefilled bath was used."
        ),
        f"- Mean coherence = {source_inflow_summary['coherence']['mean']:.6f} and mean higher-mode fraction = {source_inflow_summary['higher_mode_fraction']['mean']:.6e}.",
        f"- Maximum relative total-norm drop = {source_inflow_summary['total_norm']['max_rel_drop']:.6e}.",
        f"- Mean shell inflow at r = {shell_radii[best_shell]:.3f} is {mean_shell_inflow[best_shell]:.6e}.",
        f"- Final ambient mean density outside r >= {ambient_probe_radius:.3f} is {source_inflow_summary['ambient_mean_density']['final']:.6e}.",
        (
            "- This run calibrates whether a single live heavy defect in the chosen bath protocol settles into a stable inflow/source state before introducing a second body."
            if embedded_defect_enabled
            else "- This run checks whether the prefilled bath and boundary protocol can stay quiet before introducing a defect."
        ),
    ]
    (output_dir / "plain_language_summary.txt").write_text("\n".join(plain_language) + "\n", encoding="utf-8")
    (output_dir / "unresolved_assumptions.txt").write_text("\n".join(summary["assumptions"]) + "\n", encoding="utf-8")
    return output_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Run single heavy-source inflow calibration")
    parser.add_argument("--config", required=True, help="Path to the JSON config file")
    parser.add_argument("--restart-relaxed", default=None, help="Optional relaxed checkpoint .npz path")
    args = parser.parse_args()
    output_path = run(config_path=args.config, restart_relaxed=args.restart_relaxed)
    summary_path = output_path / "summary.json"
    summary = load_json_config(summary_path)
    source_inflow = summary["source_inflow"]
    print(f"completed_evolution_steps: {summary['completed_evolution_steps']}")
    print(f"mean_coherence: {source_inflow['coherence']['mean']:.6e}")
    print(f"max_rel_total_norm_drop: {source_inflow['total_norm']['max_rel_drop']:.6e}")
    print(f"mean_shell_inflow_r0: {source_inflow['mean_shell_inflow_by_radius'][0]:.6e}")


if __name__ == "__main__":
    main()
