import numpy as np

from src.physics.background_sources import StaticCentralBackground
from src.physics.orbit_diagnostics import (
    effective_orbit_kinematics,
    finite_difference_velocity,
    summarize_box_density_audit,
    summarize_drag_like_residuals,
    summarize_planar_orbit_trace,
)
from src.physics.point_particle import run_point_particle_orbit


def test_finite_difference_velocity_recovers_uniform_motion() -> None:
    time = np.linspace(0.0, 10.0, 101)
    positions = np.stack([1.5 * time, -0.25 * time, np.zeros_like(time)], axis=1)

    velocity = finite_difference_velocity(positions, time)

    assert np.allclose(velocity[:, 0], 1.5, atol=1.0e-10)
    assert np.allclose(velocity[:, 1], -0.25, atol=1.0e-10)


def test_summarize_planar_orbit_trace_reports_small_newtonian_drift() -> None:
    background = StaticCentralBackground(
        profile="pure_kepler",
        mu=6.0,
        softening_length=0.0,
        core_radius=1.0e-6,
        center=(0.0, 0.0, 0.0),
        c_eff=24.0,
        rho_reference=1.0,
    )
    trajectory = run_point_particle_orbit(
        background=background,
        periapsis_radius=12.0,
        eccentricity=0.05,
        dt=0.02,
        steps=36000,
    )

    summary = summarize_planar_orbit_trace(
        time=trajectory["time"],
        positions=trajectory["position"],
        velocities=trajectory["velocity"],
        mu=background.mu,
        c_eff=background.c_eff,
        source_center=background.center,
        potential_fn=background.potential_at_position,
        fit_start_index=1000,
        turning_point_min_spacing=1,
        turning_point_smooth_window=9,
        turning_point_prominence_fraction=0.02,
    )

    assert abs(summary["beta_eff"]) < 0.05
    assert summary["periapse_count"] >= 4
    assert summary["orbital_energy_summary"]["max_rel_drift"] < 1.0e-4
    assert summary["angular_momentum_z_summary"]["max_rel_drift"] < 1.0e-10
    assert abs(summary["drag_audit_summary"]["mean_tangential_acceleration"]) < 1.0e-5
    assert abs(summary["drag_audit_summary"]["mean_specific_torque_z"]) < 1.0e-5
    assert abs(summary["drag_audit_summary"]["mean_power_residual"]) < 1.0e-5


def test_drag_like_residuals_detect_tangential_braking() -> None:
    radius = 2.0
    omega0 = 0.8
    alpha = 0.05
    time = np.linspace(0.0, 10.0, 1001)
    theta = omega0 * time - 0.5 * alpha * time**2
    positions = np.stack([radius * np.cos(theta), radius * np.sin(theta), np.zeros_like(theta)], axis=1)

    kinematics = effective_orbit_kinematics(
        time=time,
        positions=positions,
        source_center=(0.0, 0.0, 0.0),
        mu=1.0,
    )
    summary = summarize_drag_like_residuals(
        time=time,
        positions=positions,
        source_center=(0.0, 0.0, 0.0),
        mu=1.0,
    )

    assert np.mean(kinematics["tangential_acceleration"]) < -0.05
    assert summary["mean_tangential_acceleration"] < -0.05
    assert summary["mean_specific_torque_z"] < -0.1


def test_summarize_box_density_audit_reports_drop_and_correlation() -> None:
    sample_times = np.linspace(0.0, 4.0, 5)
    total_norm = np.array([1.0, 0.98, 0.95, 0.93, 0.90], dtype=np.float64)
    orbit_radius = np.array([16.0, 15.8, 15.3, 14.8, 14.2], dtype=np.float64)

    summary = summarize_box_density_audit(
        sample_times=sample_times,
        total_norm=total_norm,
        orbit_radius=orbit_radius,
        box_volume=8.0,
        start_time=0.0,
        end_time=4.0,
    )

    assert summary["window_sample_count"] == 5
    assert abs(summary["initial_total_norm"] - 1.0) < 1.0e-12
    assert abs(summary["final_total_norm"] - 0.9) < 1.0e-12
    assert abs(summary["max_rel_total_norm_drop"] - 0.1) < 1.0e-12
    assert abs(summary["initial_mean_box_density"] - 0.125) < 1.0e-12
    assert summary["radius_total_norm_correlation"] is not None
    assert summary["radius_total_norm_correlation"] > 0.99
