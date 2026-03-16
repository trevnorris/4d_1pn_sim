import numpy as np

from src.physics.background_sources import StaticCentralBackground
from src.physics.orbit_diagnostics import finite_difference_velocity, summarize_planar_orbit_trace
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
