from __future__ import annotations

import json

import numpy as np
import pytest
import torch

from src.core.grids import SpatialGrid3D
from src.experiments.exp01_single_heavy_source_inflow import run
from src.physics.source_inflow import shell_flux_from_band_volume


def test_shell_flux_from_band_volume_scales_with_surface_area() -> None:
    grid = SpatialGrid3D.from_config(
        shape=(48, 48, 48),
        length=(12.0, 12.0, 12.0),
        device=torch.device("cpu"),
        real_dtype=torch.float32,
    )
    x_grid, y_grid, z_grid = grid.coordinates()
    radius = torch.sqrt(x_grid.square() + y_grid.square() + z_grid.square())
    rho = torch.ones_like(radius)
    radial_current = -torch.ones_like(radius)

    result = shell_flux_from_band_volume(
        grid=grid,
        radius=radius,
        radial_current=radial_current,
        rho=rho,
        shell_radii=[1.5, 3.0],
        band_width=float(grid.dx[0]),
    )

    inflow = result["shell_inflow_rates"]
    assert inflow[0] > 0.0
    assert inflow[1] > inflow[0]
    measured_ratio = inflow[1] / inflow[0]
    expected_ratio = (3.0 / 1.5) ** 2
    assert measured_ratio == pytest.approx(expected_ratio, rel=0.30)


def test_exp01_single_heavy_source_inflow_writes_summary(tmp_path) -> None:
    output_dir = tmp_path / "run"
    config = {
        "run_name": "exp01_single_heavy_source_inflow_test",
        "seed": 1234,
        "device": "cpu",
        "dtype": "float32",
        "complex_dtype": "complex64",
        "output_dir": str(output_dir),
        "overwrite_output": True,
        "grid": {
            "shape": [12, 12, 12],
            "length": [12.0, 12.0, 12.0],
        },
        "hermite": {
            "num_modes": 2,
            "lambda_w": 1.25,
            "quadrature_order": 8,
        },
        "eos": {
            "K_eos": 0.08,
            "n": 5.0,
        },
        "geometry": {
            "lambda_aspect": 3.0,
            "reference_rho": 1.0,
            "reference_a": 1.1,
            "reference_energy_scale": 1.0,
        },
        "solver": {
            "mass": 1.0,
            "kinetic_prefactor": 0.5,
            "transverse_prefactor": 0.2,
            "trap_strength_r": 0.4,
            "trap_strength_w": 0.9,
            "dt": 0.02,
        },
        "initializer": {
            "imaginary_dt": 0.01,
            "steps": 8,
            "target_norm": 2.0,
            "gaussian_width": 1.0,
        },
        "experiment": {
            "evolution_steps": 4,
            "metric_stride": 2,
            "progress_stride": 2,
            "shell_radii": [1.5, 2.5],
            "shell_band_width": 1.0,
            "core_radius": 1.5,
            "ambient_probe_radius": 3.0,
            "report_shell_index": 0,
        },
        "boundary_sponge": {
            "enabled": False,
        },
        "reservoir_refill": {
            "enabled": False,
        },
        "checkpoints": {
            "save_relaxed": False,
            "save_final": False,
        },
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    run(config_path)

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["completed_evolution_steps"] == 4
    assert len(summary["source_inflow"]["shell_radii"]) == 2
    assert len(summary["source_inflow"]["mean_shell_inflow_by_radius"]) == 2

    timeseries = np.load(output_dir / "timeseries.npz")
    assert timeseries["shell_inflow_rates"].shape[1] == 2
    assert timeseries["shell_mean_densities"].shape[1] == 2
