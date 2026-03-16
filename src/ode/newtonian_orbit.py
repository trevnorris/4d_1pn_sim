from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from src.core.config import load_json_config
from src.core.io import collect_runtime_info, dump_json, ensure_dir
from src.ode.common_orbit_diagnostics import summarize_planar_orbit_trace
from src.physics.background_sources import StaticCentralBackground
from src.physics.point_particle import run_point_particle_orbit


def run(config_path: str | Path) -> Path:
    config = load_json_config(config_path)
    seed = int(config["seed"])
    np.random.seed(seed)

    output_dir = ensure_dir(config["output_dir"], overwrite=bool(config.get("overwrite_output", False)))
    dump_json(output_dir / "config.json", config)
    dump_json(output_dir / "runtime.json", collect_runtime_info(seed))

    background = StaticCentralBackground.from_config(
        config["background"],
        rho_reference=float(config["geometry"]["reference_rho"]),
    )
    trajectory = run_point_particle_orbit(
        background=background,
        periapsis_radius=float(config["experiment"]["periapsis_radius"]),
        eccentricity=float(config["experiment"]["eccentricity"]),
        dt=float(config["solver"]["dt"]),
        steps=int(config["experiment"]["orbit_steps"]),
        velocity_scale=float(config["experiment"].get("velocity_scale", 1.0)),
    )
    summary = summarize_planar_orbit_trace(
        time=trajectory["time"],
        positions=trajectory["position"],
        velocities=trajectory["velocity"],
        mu=background.mu,
        c_eff=background.c_eff,
        source_center=background.center,
        potential_fn=background.potential_at_position,
        fit_start_index=int(config["experiment"].get("fit_start_index", 0)),
        turning_point_min_spacing=int(config["experiment"].get("turning_point_min_spacing", 1)),
        turning_point_smooth_window=int(config["experiment"].get("turning_point_smooth_window", 1)),
        turning_point_min_spacing_fraction=float(config["experiment"].get("turning_point_min_spacing_fraction", 0.35)),
        turning_point_prominence_fraction=float(config["experiment"].get("turning_point_prominence_fraction", 0.08)),
    )
    summary.update(
        {
            "run_name": str(config["run_name"]),
            "background": {
                "profile": background.profile,
                "mu": float(background.mu),
                "c_eff": float(background.c_eff),
                "center": list(background.center),
            },
        }
    )
    dump_json(output_dir / "summary.json", summary)
    np.savez_compressed(
        output_dir / "timeseries.npz",
        time=trajectory["time"],
        position=trajectory["position"],
        velocity=trajectory["velocity"],
        orbital_radius=trajectory["orbital_radius"],
    )
    lines = [
        "ODE Newtonian orbit reference summary:",
        f"- delta_phi = {summary['delta_phi']:.6e}",
        f"- beta_eff = {summary['beta_eff']:.6e}",
        f"- periapse_count = {summary['periapse_count']}",
        f"- max relative orbital-energy drift = {summary['orbital_energy_summary']['max_rel_drift']:.6e}",
        f"- max relative angular-momentum drift = {summary['angular_momentum_z_summary']['max_rel_drift']:.6e}",
    ]
    (output_dir / "plain_language_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    assumptions = [
        "This is a point-particle Newtonian reference, not a PDE run.",
        "The same orbit fitter and orbital-element extraction are used as the PDE-side reference.",
        "The background uses the configured static central potential exactly and omits any dressing response.",
    ]
    (output_dir / "unresolved_assumptions.txt").write_text("\n".join(assumptions) + "\n", encoding="utf-8")
    return output_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ODE Newtonian orbit reference")
    parser.add_argument("--config", required=True, help="ODE Newtonian orbit config path")
    args = parser.parse_args()

    output_dir = run(args.config)
    summary = load_json_config(output_dir / "summary.json")
    print(f"delta_phi: {summary['delta_phi']:.6e}")
    print(f"beta_eff: {summary['beta_eff']:.6e}")
    print(f"periapse_count: {summary['periapse_count']}")
    print(f"max_rel_energy_drift: {summary['orbital_energy_summary']['max_rel_drift']:.6e}")
    print(f"max_rel_angular_momentum_drift: {summary['angular_momentum_z_summary']['max_rel_drift']:.6e}")


if __name__ == "__main__":
    main()
