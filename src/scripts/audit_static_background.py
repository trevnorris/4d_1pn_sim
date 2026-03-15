from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.core.config import load_json_config
from src.core.io import dump_json, ensure_dir
from src.physics.background_sources import StaticCentralBackground
from src.physics.point_particle import run_point_particle_orbit, summarize_point_particle_orbit


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit apsidal drift from the imposed static background alone")
    parser.add_argument("--config", required=True, help="Experiment 2 config path")
    parser.add_argument("--output-dir", required=True, help="Directory for audit outputs")
    parser.add_argument(
        "--mode",
        choices=["configured", "pure_kepler"],
        default="configured",
        help="Use the configured softened background or a pure -mu/r background",
    )
    args = parser.parse_args()

    config = load_json_config(args.config)
    output_dir = ensure_dir(args.output_dir, overwrite=True)
    rho0 = float(config["geometry"]["reference_rho"])
    background = StaticCentralBackground.from_config(config["background"], rho_reference=rho0)
    if args.mode == "pure_kepler":
        background = StaticCentralBackground(
            profile="pure_kepler",
            mu=background.mu,
            softening_length=0.0,
            core_radius=1.0e-6,
            center=background.center,
            c_eff=background.c_eff,
            rho_reference=background.rho_reference,
            density_coupling=background.density_coupling,
        )

    trajectory = run_point_particle_orbit(
        background=background,
        periapsis_radius=float(config["experiment"]["periapsis_radius"]),
        eccentricity=float(config["experiment"]["eccentricity"]),
        dt=float(config["solver"]["dt"]),
        steps=int(config["experiment"]["orbit_steps"]),
        velocity_scale=float(config["experiment"].get("velocity_scale", 1.0)),
    )
    summary = summarize_point_particle_orbit(
        trajectory=trajectory,
        mu=background.mu,
        c_eff=background.c_eff,
        fit_start_index=int(config["experiment"].get("fit_start_index", 0)),
        turning_point_min_spacing=int(config["experiment"].get("turning_point_min_spacing", 1)),
        turning_point_smooth_window=int(config["experiment"].get("turning_point_smooth_window", 1)),
    )
    dump_json(
        Path(output_dir) / "summary.json",
        {
            "mode": args.mode,
            "background": {
                "mu": background.mu,
                "softening_length": background.softening_length,
                "c_eff": background.c_eff,
            },
            "summary": summary,
        },
    )
    np.savez_compressed(
        Path(output_dir) / "timeseries.npz",
        time=trajectory["time"],
        position=trajectory["position"],
        velocity=trajectory["velocity"],
        orbital_radius=trajectory["orbital_radius"],
    )
    print(f"mode: {args.mode}")
    print(f"beta_eff: {summary['beta_eff']:.6f}")
    print(f"delta_phi: {summary['delta_phi']:.6f}")
    print(f"semi_major_axis: {summary['semi_major_axis']:.6f}")
    print(f"eccentricity: {summary['eccentricity']:.6f}")


if __name__ == "__main__":
    main()
