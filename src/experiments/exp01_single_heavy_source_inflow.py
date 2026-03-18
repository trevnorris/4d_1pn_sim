from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import torch

from src.core.checkpoints import save_checkpoint
from src.core.config import load_json_config
from src.core.io import collect_runtime_info, dump_json, ensure_dir
from src.experiments.common import build_solver, prepare_relaxed_state, state_from_checkpoint
from src.physics.boundary_sponge import build_boundary_sponge_mask
from src.physics.open_system import (
    BoundaryReservoirRefill,
    UniformReservoirRefill,
    build_mode_leakage_matrix,
)
from src.physics.source_inflow import sample_source_inflow_metrics, summarize_source_inflow_series


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
    experiment_config = dict(config["experiment"])
    evolution_steps = int(experiment_config["evolution_steps"])
    metric_stride = max(1, int(experiment_config.get("metric_stride", 64)))
    progress_stride = max(1, int(experiment_config.get("progress_stride", 512)))
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
    save_final = bool(checkpoint_config.get("save_final", False))

    boundary_sponge_config = dict(config.get("boundary_sponge", {}))
    node_amplitude_mask = None
    if bool(boundary_sponge_config.get("enabled", False)):
        node_amplitude_mask = build_boundary_sponge_mask(
            grid=solver.grid,
            dt=dt,
            config=boundary_sponge_config,
        )

    refill_config = dict(config.get("reservoir_refill", {}))
    boundary_reservoir_config = dict(config.get("boundary_reservoir", {}))
    refill_controller = None
    refill_mode = "disabled"
    if bool(boundary_reservoir_config.get("enabled", False)):
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

    reference_modes = state.psi_modes.clone()

    time_history: list[float] = []
    center_history: list[list[float]] = []
    total_norm_history: list[float] = []
    box_density_history: list[float] = []
    compactness_history: list[float] = []
    bound_mass_history: list[float] = []
    core_mass_history: list[float] = []
    core_density_history: list[float] = []
    ambient_density_history: list[float] = []
    coherence_history: list[float] = []
    higher_mode_history: list[float] = []
    mean_leakage_history: list[float] = []
    signed_leakage_history: list[float] = []
    shell_inflow_history: list[list[float]] = []
    shell_density_history: list[list[float]] = []
    refill_delta_norm_history: list[float] = []
    refill_cumulative_history: list[float] = []

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
            time_history.append(float(state.time))
            center_history.append(list(metrics["center"]))
            total_norm_history.append(float(metrics["total_norm"]))
            box_density_history.append(float(metrics["box_mean_density"]))
            compactness_history.append(float(metrics["radius_of_gyration"]))
            bound_mass_history.append(float(metrics["bound_mass_fraction"]))
            core_mass_history.append(float(metrics["core_mass"]))
            core_density_history.append(float(metrics["core_mean_density"]))
            ambient_density_history.append(float(metrics["ambient_mean_density"]))
            coherence_history.append(float(metrics["coherence"]))
            higher_mode_history.append(float(metrics["higher_mode_fraction"]))
            mean_leakage_history.append(float(metrics["mean_leakage"]))
            signed_leakage_history.append(float(metrics["signed_leakage_mean"]))
            shell_inflow_history.append([float(value) for value in metrics["shell_inflow_rates"]])
            shell_density_history.append([float(value) for value in metrics["shell_mean_densities"]])
            refill_delta_norm_history.append(float(refill_metrics["delta_norm_applied"]))
            refill_cumulative_history.append(float(refill_metrics["cumulative_refill_norm"]))

        if (idx + 1) % progress_stride == 0 or idx == evolution_steps - 1:
            report_inflow = float(shell_inflow_history[-1][report_shell_index]) if shell_inflow_history else 0.0
            report_coherence = float(coherence_history[-1]) if coherence_history else 0.0
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

    source_inflow_summary = summarize_source_inflow_series(
        shell_radii=shell_radii,
        shell_inflow_rates=np.asarray(shell_inflow_history, dtype=np.float64),
        shell_mean_densities=np.asarray(shell_density_history, dtype=np.float64),
        total_norm=np.asarray(total_norm_history, dtype=np.float64),
        box_mean_density=np.asarray(box_density_history, dtype=np.float64),
        ambient_mean_density=np.asarray(ambient_density_history, dtype=np.float64),
        core_mass=np.asarray(core_mass_history, dtype=np.float64),
        core_mean_density=np.asarray(core_density_history, dtype=np.float64),
        coherence=np.asarray(coherence_history, dtype=np.float64),
        higher_mode_fraction=np.asarray(higher_mode_history, dtype=np.float64),
        compactness=np.asarray(compactness_history, dtype=np.float64),
        bound_mass_fraction_series=np.asarray(bound_mass_history, dtype=np.float64),
        mean_leakage=np.asarray(mean_leakage_history, dtype=np.float64),
        signed_leakage_mean=np.asarray(signed_leakage_history, dtype=np.float64),
    )

    np.savez_compressed(
        output_dir / "timeseries.npz",
        shell_radii=np.asarray(shell_radii, dtype=np.float64),
        time=np.asarray(time_history, dtype=np.float64),
        source_center=np.asarray(center_history, dtype=np.float64),
        total_norm=np.asarray(total_norm_history, dtype=np.float64),
        box_mean_density=np.asarray(box_density_history, dtype=np.float64),
        radius_of_gyration=np.asarray(compactness_history, dtype=np.float64),
        bound_mass_fraction=np.asarray(bound_mass_history, dtype=np.float64),
        core_mass=np.asarray(core_mass_history, dtype=np.float64),
        core_mean_density=np.asarray(core_density_history, dtype=np.float64),
        ambient_mean_density=np.asarray(ambient_density_history, dtype=np.float64),
        coherence=np.asarray(coherence_history, dtype=np.float64),
        higher_mode_fraction=np.asarray(higher_mode_history, dtype=np.float64),
        mean_leakage=np.asarray(mean_leakage_history, dtype=np.float64),
        signed_leakage_mean=np.asarray(signed_leakage_history, dtype=np.float64),
        shell_inflow_rates=np.asarray(shell_inflow_history, dtype=np.float64),
        shell_mean_densities=np.asarray(shell_density_history, dtype=np.float64),
        refill_delta_norm=np.asarray(refill_delta_norm_history, dtype=np.float64),
        refill_cumulative_norm=np.asarray(refill_cumulative_history, dtype=np.float64),
    )

    completed_evolution_steps = evolution_steps
    summary = {
        "run_name": config["run_name"],
        "completed_evolution_steps": int(completed_evolution_steps),
        "final_state_step": int(state.step),
        "requested_steps": evolution_steps,
        "source_inflow": source_inflow_summary,
        "boundary_sponge_enabled": bool(boundary_sponge_config.get("enabled", False)),
        "reservoir_refill_enabled": refill_controller is not None,
        "reservoir_refill_mode": refill_mode,
        "assumptions": [
            "This is a single-defect source-calibration run, not a two-body gravity test.",
            "The heavy source proxy is created by the chosen relaxed defect norm and confinement, not a separate throat microphysics model.",
            "Shell inflow rates are estimated from a mode-summed 3D current on thin spherical bands rather than a full 4D control-volume flux.",
            "Ambient density locking is only represented if the optional refill controller is enabled and does not by itself validate momentum neutrality.",
        ],
    }
    dump_json(output_dir / "summary.json", summary)

    mean_shell_inflow = np.asarray(source_inflow_summary["mean_shell_inflow_by_radius"], dtype=np.float64)
    best_shell = report_shell_index
    plain_language = [
        "Single heavy-source inflow calibration summary:",
        f"- The run completed {completed_evolution_steps} fixed-background steps after source relaxation.",
        f"- Reservoir mode = {refill_mode}.",
        f"- Mean coherence = {source_inflow_summary['coherence']['mean']:.6f} and mean higher-mode fraction = {source_inflow_summary['higher_mode_fraction']['mean']:.6e}.",
        f"- Maximum relative total-norm drop = {source_inflow_summary['total_norm']['max_rel_drop']:.6e}.",
        f"- Mean shell inflow at r = {shell_radii[best_shell]:.3f} is {mean_shell_inflow[best_shell]:.6e}.",
        f"- Final ambient mean density outside r >= {ambient_probe_radius:.3f} is {source_inflow_summary['ambient_mean_density']['final']:.6e}.",
        "- This run calibrates whether a single live heavy defect settles into a stable inflow/source state before introducing a second body.",
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
