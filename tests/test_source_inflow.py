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
    assert summary["reservoir_refill_mode"] == "disabled"

    timeseries = np.load(output_dir / "timeseries.npz")
    assert timeseries["shell_inflow_rates"].shape[1] == 2
    assert timeseries["shell_mean_densities"].shape[1] == 2


def test_exp01_single_heavy_source_inflow_boundary_reservoir_mode(tmp_path) -> None:
    output_dir = tmp_path / "run_boundary"
    config = {
        "run_name": "exp01_single_heavy_source_inflow_boundary_test",
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
        "boundary_reservoir": {
            "enabled": True,
            "inner_clearance": 1.0,
            "width": 2.0,
            "power": 2.0,
            "compensate_leakage": False,
            "restore_target_norm": True,
            "leakage_gain": 1.0,
            "max_delta_norm_fraction_per_step": 0.0,
        },
        "reservoir_refill": {
            "enabled": False,
        },
        "checkpoints": {
            "save_relaxed": False,
            "save_final": False,
        },
    }
    config_path = tmp_path / "config_boundary.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    run(config_path)

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["reservoir_refill_mode"] == "boundary"


def test_exp01_single_heavy_source_inflow_conditioning_writes_conditioned_outputs(tmp_path) -> None:
    output_dir = tmp_path / "run_conditioned"
    config = {
        "run_name": "exp01_single_heavy_source_inflow_conditioned_test",
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
            "conditioning_steps": 3,
            "conditioning_metric_stride": 1,
            "conditioning_progress_stride": 2,
            "conditioning_ramp_refill": True,
            "conditioning_ramp_fraction": 0.5,
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
        "boundary_reservoir": {
            "enabled": True,
            "inner_clearance": 1.0,
            "width": 2.0,
            "power": 2.0,
            "compensate_leakage": False,
            "restore_target_norm": True,
            "leakage_gain": 1.0,
            "max_delta_norm_fraction_per_step": 0.0,
        },
        "reservoir_refill": {
            "enabled": False,
        },
        "checkpoints": {
            "save_relaxed": False,
            "save_conditioned": True,
            "save_final": False,
        },
    }
    config_path = tmp_path / "config_conditioned.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    run(config_path)

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["conditioning_steps"] == 3
    assert summary["conditioning_completed_steps"] == 3
    assert summary["conditioning"]["sample_count"] >= 2
    assert (output_dir / "checkpoint_conditioned.npz").exists()

    timeseries = np.load(output_dir / "timeseries.npz")
    assert timeseries["conditioning_shell_inflow_rates"].shape[0] >= 2
    assert timeseries["conditioning_shell_inflow_rates"].shape[1] == 2


def test_exp01_single_heavy_source_inflow_boundary_relaxation_mode(tmp_path) -> None:
    output_dir = tmp_path / "run_relaxation"
    config = {
        "run_name": "exp01_single_heavy_source_inflow_boundary_relaxation_test",
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
            "conditioning_steps": 2,
            "conditioning_metric_stride": 1,
            "conditioning_progress_stride": 1,
            "conditioning_ramp_refill": True,
            "conditioning_ramp_fraction": 0.5,
            "conditioning_refill_scale": 2.0,
            "production_refill_scale": 0.5,
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
        "boundary_relaxation": {
            "enabled": True,
            "inner_clearance": 1.0,
            "width": 2.0,
            "power": 2.0,
            "target_density": 1.0e-3,
            "relaxation_fraction": 0.5,
            "max_delta_norm_fraction_per_step": 5.0e-2,
        },
        "reservoir_refill": {
            "enabled": False,
        },
        "checkpoints": {
            "save_relaxed": False,
            "save_conditioned": False,
            "save_final": False,
        },
    }
    config_path = tmp_path / "config_relaxation.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    run(config_path)

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["reservoir_refill_mode"] == "boundary_relaxation"
    assert summary["conditioning_refill_scale"] == 2.0
    assert summary["production_refill_scale"] == 0.5


def test_exp01_single_heavy_source_inflow_uniform_bath_initializer(tmp_path) -> None:
    output_dir = tmp_path / "run_uniform_bath"
    bath_density = 2.0 / 12.0**3
    config = {
        "run_name": "exp01_single_heavy_source_inflow_uniform_bath_test",
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
            "trap_strength_r": 0.0,
            "trap_strength_w": 0.0,
            "dt": 0.02,
        },
        "initializer": {
            "mode": "uniform_bath",
            "imaginary_dt": 0.01,
            "steps": 0,
            "apply_imaginary_relaxation": False,
            "target_norm": 2.0,
            "bath_density": bath_density,
            "gaussian_width": 1.0,
        },
        "experiment": {
            "conditioning_steps": 2,
            "conditioning_metric_stride": 1,
            "conditioning_progress_stride": 1,
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
        "boundary_relaxation": {
            "enabled": True,
            "inner_clearance": 1.0,
            "width": 2.0,
            "power": 2.0,
            "target_density": bath_density,
            "relaxation_fraction": 0.5,
            "max_delta_norm_fraction_per_step": 5.0e-2,
        },
        "reservoir_refill": {
            "enabled": False,
        },
        "checkpoints": {
            "save_relaxed": False,
            "save_conditioned": False,
            "save_final": False,
        },
    }
    config_path = tmp_path / "config_uniform_bath.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    run(config_path)

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["initializer_mode"] == "uniform_bath"
    assert summary["embedded_defect_enabled"] is False
    assert summary["prefilled_bath_density"] == pytest.approx(bath_density)

    timeseries = np.load(output_dir / "timeseries.npz")
    assert timeseries["conditioning_shell_inflow_rates"].shape[0] >= 2
    assert timeseries["shell_inflow_rates"].shape[0] >= 2


def test_exp01_single_heavy_source_inflow_bath_plus_gaussian_initializer(tmp_path) -> None:
    output_dir = tmp_path / "run_bath_plus_defect"
    bath_density = 2.0 / 12.0**3
    config = {
        "run_name": "exp01_single_heavy_source_inflow_bath_plus_gaussian_test",
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
            "mode": "bath_plus_gaussian_defect",
            "imaginary_dt": 0.01,
            "steps": 0,
            "apply_imaginary_relaxation": False,
            "target_norm": 4.0,
            "bath_density": bath_density,
            "defect_target_norm": 2.0,
            "gaussian_width": 1.0,
            "defect_phase_offset": 1.5707963267948966,
        },
        "experiment": {
            "conditioning_steps": 2,
            "conditioning_metric_stride": 1,
            "conditioning_progress_stride": 1,
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
        "boundary_relaxation": {
            "enabled": True,
            "inner_clearance": 1.0,
            "width": 2.0,
            "power": 2.0,
            "target_density": bath_density,
            "relaxation_fraction": 0.5,
            "max_delta_norm_fraction_per_step": 5.0e-2,
        },
        "reservoir_refill": {
            "enabled": False,
        },
        "checkpoints": {
            "save_relaxed": False,
            "save_conditioned": False,
            "save_final": False,
        },
    }
    config_path = tmp_path / "config_bath_plus_defect.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    run(config_path)

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["initializer_mode"] == "bath_plus_gaussian_defect"
    assert summary["embedded_defect_enabled"] is True
    assert summary["prefilled_bath_density"] == pytest.approx(bath_density)

    timeseries = np.load(output_dir / "timeseries.npz")
    assert timeseries["shell_inflow_rates"].shape[1] == 2
