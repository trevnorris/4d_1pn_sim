from types import SimpleNamespace

import numpy as np

from src.physics.launch_calibration import (
    calibration_velocity_scale_samples,
    estimate_box_clearance,
    estimate_tangential_velocity,
    resolve_launch_speed,
    safe_launch_speed_limit,
    summarize_launch_calibration,
)


def test_estimate_tangential_velocity_recovers_circular_motion() -> None:
    radius = 2.0
    speed = 0.75
    omega = speed / radius
    time = np.linspace(0.0, 10.0, 2001)
    theta = omega * time
    positions = np.stack([radius * np.cos(theta), radius * np.sin(theta), np.zeros_like(theta)], axis=1)

    summary = estimate_tangential_velocity(
        time=time,
        positions=positions,
        source_center=(0.0, 0.0, 0.0),
        start_index=50,
        end_index=400,
    )

    assert abs(summary["mean_tangential_speed"] - speed) < 5.0e-4
    assert abs(summary["mean_radial_speed"]) < 5.0e-4


def test_safe_launch_speed_limit_uses_nyquist_fraction() -> None:
    solver = SimpleNamespace(
        mass=2.0,
        grid=SimpleNamespace(dx=(0.5, 0.25, 0.4)),
    )

    limit = safe_launch_speed_limit(solver, nyquist_fraction=0.5)

    assert abs(limit - (0.5 * np.pi / 0.5) / 2.0) < 1.0e-12


def test_estimate_box_clearance_tracks_nearest_boundary() -> None:
    positions = np.array(
        [
            [1.0, 0.0, 0.0],
            [2.5, 0.5, 0.0],
            [3.0, -1.0, 0.0],
            [3.5, 0.0, 0.0],
        ],
        dtype=np.float64,
    )

    summary = estimate_box_clearance(
        positions=positions,
        box_length=(10.0, 10.0, 10.0),
        start_index=0,
        end_index=None,
    )

    assert abs(summary["min_boundary_clearance"] - 1.5) < 1.0e-12
    assert summary["mean_boundary_clearance"] > summary["min_boundary_clearance"]


def test_summarize_launch_calibration_picks_closest_probe() -> None:
    probes = [
        {
            "applied_speed": 0.8,
            "requested_momentum": 0.8,
            "velocity_summary": {"mean_tangential_speed": 0.55, "mean_radial_speed": -0.08},
            "launch_radius": 4.0,
            "radius_bias": 0.02,
            "window_summary": {"min_boundary_clearance": 4.5, "mean_boundary_clearance": 4.8},
            "final_higher_mode_fraction": 0.01,
            "final_norm": 1.0,
        },
        {
            "applied_speed": 1.0,
            "requested_momentum": 1.0,
            "velocity_summary": {"mean_tangential_speed": 0.72, "mean_radial_speed": -0.02},
            "launch_radius": 4.0,
            "radius_bias": 0.03,
            "window_summary": {"min_boundary_clearance": 4.2, "mean_boundary_clearance": 4.6},
            "final_higher_mode_fraction": 0.02,
            "final_norm": 1.0,
        },
        {
            "applied_speed": 1.2,
            "requested_momentum": 1.2,
            "velocity_summary": {"mean_tangential_speed": 0.93, "mean_radial_speed": -0.06},
            "launch_radius": 4.0,
            "radius_bias": -0.35,
            "window_summary": {"min_boundary_clearance": 1.0, "mean_boundary_clearance": 1.4},
            "final_higher_mode_fraction": 0.03,
            "final_norm": 1.0,
        },
    ]

    summary = summarize_launch_calibration(
        probes=probes,
        target_speed=0.74,
        safe_speed_limit=1.3,
        boundary_clearance_floor=3.0,
    )

    assert abs(summary["recommended_applied_speed"] - 1.0) < 1.0e-12
    assert abs(summary["recommended_realized_tangential_speed"] - 0.72) < 1.0e-12
    assert summary["target_reachable"]
    assert summary["recommended_window_usable"]


def test_calibration_velocity_scale_samples_includes_exact_target_scale() -> None:
    samples = calibration_velocity_scale_samples(
        [0.9, 0.95, 1.0, 1.05, 1.1],
        target_velocity_scale=0.978,
        safe_scale_limit=1.1,
    )

    assert 0.978 in samples
    assert samples == sorted(samples)


def test_resolve_launch_speed_prefers_usable_target_probe() -> None:
    probes = [
        {
            "applied_speed": 0.978,
            "requested_momentum": 0.978,
            "velocity_summary": {"mean_tangential_speed": 0.701, "mean_radial_speed": -0.003},
            "launch_radius": 4.0,
            "radius_bias": 0.02,
            "window_summary": {"min_boundary_clearance": 4.2, "mean_boundary_clearance": 4.5},
            "final_higher_mode_fraction": 0.01,
            "final_norm": 1.0,
        },
        {
            "applied_speed": 1.0,
            "requested_momentum": 1.0,
            "velocity_summary": {"mean_tangential_speed": 0.702, "mean_radial_speed": -0.001},
            "launch_radius": 4.0,
            "radius_bias": 0.01,
            "window_summary": {"min_boundary_clearance": 4.4, "mean_boundary_clearance": 4.7},
            "final_higher_mode_fraction": 0.01,
            "final_norm": 1.0,
        },
    ]

    summary = summarize_launch_calibration(
        probes=probes,
        target_speed=0.978,
        safe_speed_limit=1.2,
        boundary_clearance_floor=3.0,
    )

    launch_choice = resolve_launch_speed(summary, target_speed=0.978)

    assert summary["target_probe_available"]
    assert summary["target_probe_window_usable"]
    assert launch_choice["selection"] == "target_probe"
    assert abs(launch_choice["applied_speed"] - 0.978) < 1.0e-12


def test_resolve_launch_speed_falls_back_when_target_probe_not_usable() -> None:
    probes = [
        {
            "applied_speed": 0.978,
            "requested_momentum": 0.978,
            "velocity_summary": {"mean_tangential_speed": 0.701, "mean_radial_speed": -0.003},
            "launch_radius": 4.0,
            "radius_bias": 0.20,
            "window_summary": {"min_boundary_clearance": 1.5, "mean_boundary_clearance": 2.0},
            "final_higher_mode_fraction": 0.01,
            "final_norm": 1.0,
        },
        {
            "applied_speed": 1.0,
            "requested_momentum": 1.0,
            "velocity_summary": {"mean_tangential_speed": 0.74, "mean_radial_speed": -0.001},
            "launch_radius": 4.0,
            "radius_bias": 0.01,
            "window_summary": {"min_boundary_clearance": 4.4, "mean_boundary_clearance": 4.7},
            "final_higher_mode_fraction": 0.01,
            "final_norm": 1.0,
        },
    ]

    summary = summarize_launch_calibration(
        probes=probes,
        target_speed=0.978,
        safe_speed_limit=1.2,
        boundary_clearance_floor=3.0,
    )

    launch_choice = resolve_launch_speed(summary, target_speed=0.978)

    assert summary["target_probe_available"]
    assert summary["target_probe_window_usable"] is False
    assert launch_choice["selection"] == "recommended_probe"
    assert abs(launch_choice["applied_speed"] - 1.0) < 1.0e-12
