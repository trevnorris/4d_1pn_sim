from src.physics.background_sources import StaticCentralBackground
from src.physics.point_particle import run_point_particle_orbit, summarize_point_particle_orbit


def test_point_particle_pure_kepler_has_small_precession() -> None:
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
        periapsis_radius=3.2,
        eccentricity=0.2,
        dt=0.01,
        steps=16000,
    )
    summary = summarize_point_particle_orbit(
        trajectory=trajectory,
        mu=background.mu,
        c_eff=background.c_eff,
        fit_start_index=500,
        turning_point_min_spacing=500,
        turning_point_smooth_window=9,
    )
    assert abs(summary["beta_eff"]) < 0.2
