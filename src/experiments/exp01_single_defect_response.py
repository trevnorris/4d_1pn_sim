from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import torch

from src.core.checkpoints import load_checkpoint, save_checkpoint
from src.core.config import load_json_config
from src.core.io import collect_runtime_info, dump_json, ensure_dir
from src.core.targets import energy_partition_fractions, load_reference_targets
from src.experiments.common import build_solver, clone_state, serializable_diag
from src.physics.defects import gaussian_initial_modes, imaginary_time_relax
from src.physics.diagnostics import snapshot_diagnostics, summarize_closure_scan, summarize_drive_response
from src.physics.matter_gnls import MatterSplitStepSolver, MatterState


def run(config_path: str | Path, restart: str | None = None) -> Path:
    config = load_json_config(config_path)
    seed = int(config["seed"])
    np.random.seed(seed)
    torch.manual_seed(seed)

    output_dir = ensure_dir(config["output_dir"], overwrite=bool(config.get("overwrite_output", False)))
    dump_json(output_dir / "config.json", config)
    dump_json(output_dir / "runtime.json", collect_runtime_info(seed))

    solver, projection_kernel = build_solver(config)
    rho0 = float(config["geometry"]["reference_rho"])

    if restart is not None:
        checkpoint_state = load_checkpoint(restart, device=solver.grid.device, complex_dtype=solver.complex_dtype)
        initial_state = MatterState(
            psi_modes=checkpoint_state["psi_modes"],
            time=float(checkpoint_state["time"]),
            step=int(checkpoint_state["step"]),
            a=float(checkpoint_state["a"]),
            rho_ambient=float(checkpoint_state["rho_ambient"]),
        )
    else:
        initial_state = gaussian_initial_modes(
            solver=solver,
            gaussian_width=config["initializer"]["gaussian_width"],
            target_norm=config["initializer"]["target_norm"],
            rho_ambient=rho0,
        )
        initial_state = imaginary_time_relax(
            solver=solver,
            state=initial_state,
            dtau=config["initializer"]["imaginary_dt"],
            steps=config["initializer"]["steps"],
            target_norm=config["initializer"]["target_norm"],
        )
        save_checkpoint(
            output_dir / "checkpoint_relaxed.npz",
            {
                "psi_modes": initial_state.psi_modes,
                "time": initial_state.time,
                "step": initial_state.step,
                "a": initial_state.a,
                "rho_ambient": initial_state.rho_ambient,
            },
        )

    reference_modes = initial_state.psi_modes.clone()

    dt = float(config["solver"]["dt"])
    checkpoint_every = int(config["solver"]["checkpoint_every"])
    bound_radius_factor = float(config["experiment"]["bound_radius_factor"])

    state = clone_state(initial_state)
    previous_diag: dict[str, Any] | None = None
    stabilization_log: list[dict[str, Any]] = []
    for _ in range(int(config["experiment"]["stabilization_steps"])):
        state = solver.step(state, dt=dt, rho_ambient=rho0)
        diag = snapshot_diagnostics(
            solver=solver,
            state=state,
            projection_kernel=projection_kernel,
            reference_modes=reference_modes,
            bound_radius_factor=bound_radius_factor,
            previous_snapshot=previous_diag,
        )
        previous_diag = diag
        stabilization_log.append(serializable_diag(diag))
        if state.step % checkpoint_every == 0:
            save_checkpoint(
                output_dir / f"checkpoint_stability_step_{state.step:05d}.npz",
                {
                    "psi_modes": state.psi_modes,
                    "time": state.time,
                    "step": state.step,
                    "a": state.a,
                    "rho_ambient": state.rho_ambient,
                },
            )

    stabilized_state = clone_state(state)

    scan_rows: list[dict[str, Any]] = []
    for scan_rho in config["experiment"]["sweep_rho_values"]:
        scan_state = clone_state(stabilized_state)
        previous_scan_diag = previous_diag
        for _ in range(int(config["experiment"]["sweep_relax_steps"])):
            scan_state = solver.step(scan_state, dt=dt, rho_ambient=float(scan_rho))
            previous_scan_diag = snapshot_diagnostics(
                solver=solver,
                state=scan_state,
                projection_kernel=projection_kernel,
                reference_modes=reference_modes,
                bound_radius_factor=bound_radius_factor,
                previous_snapshot=previous_scan_diag,
            )
        scan_rows.append(serializable_diag(previous_scan_diag))

    drive_state = clone_state(stabilized_state)
    drive_times: list[float] = []
    drive_rho: list[float] = []
    drive_a: list[float] = []
    drive_radius: list[float] = []
    drive_leakage: list[float] = []
    drive_modes: list[float] = []
    drive_coherence: list[float] = []
    drive_residual: list[float] = []
    effort_signal: list[float] = []
    flux_signal: list[float] = []
    previous_drive_diag = previous_diag
    for local_step in range(int(config["experiment"]["drive_steps"])):
        local_time = local_step * dt
        current_rho = rho0 * (1.0 + config["experiment"]["drive_amplitude"] * np.sin(config["experiment"]["drive_omega"] * local_time))
        drive_state = solver.step(drive_state, dt=dt, rho_ambient=float(current_rho))
        drive_diag = snapshot_diagnostics(
            solver=solver,
            state=drive_state,
            projection_kernel=projection_kernel,
            reference_modes=reference_modes,
            bound_radius_factor=bound_radius_factor,
            previous_snapshot=previous_drive_diag,
        )
        previous_drive_diag = drive_diag
        drive_times.append(float(drive_state.time))
        drive_rho.append(float(current_rho))
        drive_a.append(float(drive_state.a))
        drive_radius.append(float(drive_diag["radius_of_gyration"]))
        drive_leakage.append(float(drive_diag["mean_S_leak"]))
        drive_modes.append(float(drive_diag["higher_mode_fraction"]))
        drive_coherence.append(float(drive_diag["coherence"]))
        drive_residual.append(float(drive_diag["continuity_residual_l2"]))
        effort_signal.append(float(current_rho - rho0))
        flux_signal.append(float(drive_state.a - stabilized_state.a))
        if drive_state.step % checkpoint_every == 0:
            save_checkpoint(
                output_dir / f"checkpoint_drive_step_{drive_state.step:05d}.npz",
                {
                    "psi_modes": drive_state.psi_modes,
                    "time": drive_state.time,
                    "step": drive_state.step,
                    "a": drive_state.a,
                    "rho_ambient": drive_state.rho_ambient,
                },
            )

    closure_summary = summarize_closure_scan(scan_rows)
    drive_summary = summarize_drive_response(
        time=np.asarray(drive_times),
        effort_signal=np.asarray(effort_signal),
        flux_signal=np.asarray(flux_signal),
        omega=float(config["experiment"]["drive_omega"]),
        cycles_to_skip=int(config["experiment"]["lockin_cycles_to_skip"]),
    )

    save_checkpoint(
        output_dir / "checkpoint_final.npz",
        {
            "psi_modes": drive_state.psi_modes,
            "time": drive_state.time,
            "step": drive_state.step,
            "a": drive_state.a,
            "rho_ambient": drive_state.rho_ambient,
        },
    )

    np.savez_compressed(
        output_dir / "timeseries.npz",
        time=np.asarray(drive_times, dtype=np.float64),
        rho_ambient=np.asarray(drive_rho, dtype=np.float64),
        a=np.asarray(drive_a, dtype=np.float64),
        radius_of_gyration=np.asarray(drive_radius, dtype=np.float64),
        mean_S_leak=np.asarray(drive_leakage, dtype=np.float64),
        higher_mode_fraction=np.asarray(drive_modes, dtype=np.float64),
        coherence=np.asarray(drive_coherence, dtype=np.float64),
        continuity_residual_l2=np.asarray(drive_residual, dtype=np.float64),
    )

    targets = load_reference_targets()
    target_partition = energy_partition_fractions()
    summary = {
        "run_name": config["run_name"],
        "targets": targets,
        "stability": stabilization_log[-1],
        "closure_scan": closure_summary,
        "drive_response": drive_summary,
        "target_partition_fraction": target_partition,
        "mean_drive_leakage": float(np.mean(drive_leakage)),
        "mean_drive_higher_mode_fraction": float(np.mean(drive_modes)),
        "mean_drive_coherence": float(np.mean(drive_coherence)),
        "assumptions": [
            "a(t) is updated by the declared adiabatic one-DOF closure rather than an independent wall dynamics model.",
            "The matter confinement is a phenomenological harmonic throat potential used for Sprint 1 defect preparation.",
            "Z_eff is extracted from a scalar density-drive to breathing-response port, not a full mouth operator basis.",
            "The Maxwell, free-heavy, and two-live-defect sectors remain out of scope for this sprint.",
        ],
    }
    dump_json(output_dir / "summary.json", summary)

    plain_language = [
        "Sprint 1 run summary:",
        f"- The reduced geometry closure fit gives kappa_PV = {closure_summary['kappa_PV_estimate']:.4f} and dln a / dln rho = {closure_summary['a_fit']['slope']:.4f}.",
        f"- The mean closure partition fractions are Ew={closure_summary['partition_fraction']['E_w']:.4f}, Ef={closure_summary['partition_fraction']['E_f']:.4f}, EPV={closure_summary['partition_fraction']['E_PV']:.4f}.",
        f"- During the driven segment, mean coherence = {summary['mean_drive_coherence']:.4f}, mean higher-mode fraction = {summary['mean_drive_higher_mode_fraction']:.4e}, mean leakage proxy = {summary['mean_drive_leakage']:.4e}.",
        "- This supports internal consistency of the reduced matter+adiabatic-geometry prototype only; it does not yet validate the full PDE closure claim beyond the declared closure model.",
    ]
    (output_dir / "plain_language_summary.txt").write_text("\n".join(plain_language) + "\n", encoding="utf-8")
    (output_dir / "unresolved_assumptions.txt").write_text("\n".join(summary["assumptions"]) + "\n", encoding="utf-8")
    return output_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Sprint 1 Experiment 1: single-defect response")
    parser.add_argument("--config", required=True, help="Path to the JSON config file")
    parser.add_argument("--restart", default=None, help="Optional checkpoint .npz path")
    args = parser.parse_args()
    run(args.config, restart=args.restart)


if __name__ == "__main__":
    main()
