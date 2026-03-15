from __future__ import annotations

import math
from typing import Any

import numpy as np

from src.physics.fitting import estimate_beta_eff, estimate_planar_orbit_shape, fit_orbit_precession


def generate_precessing_orbit(
    semi_major_axis: float,
    eccentricity: float,
    delta_phi_per_orbit: float,
    num_orbits: int,
    num_samples: int,
) -> dict[str, np.ndarray]:
    theta = np.linspace(0.0, num_orbits * 2.0 * math.pi, num_samples, endpoint=False, dtype=np.float64)
    reduced_angle = theta / (1.0 + delta_phi_per_orbit / (2.0 * math.pi))
    radius = semi_major_axis * (1.0 - eccentricity**2) / (1.0 + eccentricity * np.cos(reduced_angle))
    positions = np.stack([radius * np.cos(theta), radius * np.sin(theta)], axis=1)
    time = np.linspace(0.0, float(num_orbits), num_samples, endpoint=False, dtype=np.float64)
    return {
        "time": time,
        "positions": positions,
        "radius": radius,
    }


def orbit_oracle_delta_phi(beta_eff: float, mu: float, c_eff: float, semi_major_axis: float, eccentricity: float) -> float:
    return 2.0 * math.pi * beta_eff * mu / (c_eff**2 * semi_major_axis * (1.0 - eccentricity**2))


def evaluate_orbit_oracle(
    beta_eff: float,
    mu: float,
    c_eff: float,
    semi_major_axis: float,
    eccentricity: float,
    num_orbits: int = 8,
    num_samples: int = 12000,
    min_spacing: int = 300,
    smooth_window: int = 11,
) -> dict[str, Any]:
    delta_phi = orbit_oracle_delta_phi(
        beta_eff=beta_eff,
        mu=mu,
        c_eff=c_eff,
        semi_major_axis=semi_major_axis,
        eccentricity=eccentricity,
    )
    oracle = generate_precessing_orbit(
        semi_major_axis=semi_major_axis,
        eccentricity=eccentricity,
        delta_phi_per_orbit=delta_phi,
        num_orbits=num_orbits,
        num_samples=num_samples,
    )
    fit = fit_orbit_precession(
        positions=oracle["positions"],
        times=oracle["time"],
        min_spacing=min_spacing,
        smooth_window=smooth_window,
    )
    shape = estimate_planar_orbit_shape(
        positions=oracle["positions"],
        min_spacing=min_spacing,
        smooth_window=smooth_window,
    )
    beta_fit = estimate_beta_eff(
        delta_phi=fit["delta_phi"],
        semi_major_axis=shape["semi_major_axis"],
        eccentricity=shape["eccentricity"],
        mu=mu,
        c_eff=c_eff,
    )
    return {
        "target_beta_eff": beta_eff,
        "target_delta_phi": delta_phi,
        "fit_delta_phi": fit["delta_phi"],
        "fit_delta_phi_stderr": fit["delta_phi_stderr"],
        "fit_beta_eff": beta_fit,
        "shape": shape,
        "num_periapses": len(fit["periapse_times"]),
    }
