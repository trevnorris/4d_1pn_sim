from __future__ import annotations

from typing import Any


def evaluate_newtonian_orbit_gate(
    orbit_summary: dict[str, Any],
    defect_metrics: dict[str, float],
    thresholds: dict[str, float],
    fit_error: str | None = None,
) -> dict[str, Any]:
    fit_available = fit_error is None
    periapse_count = int(orbit_summary.get("periapse_count", 0)) if fit_available else 0
    beta_eff = float(orbit_summary.get("beta_eff", 0.0)) if fit_available else float("inf")
    energy_drift = (
        float(orbit_summary["orbital_energy_summary"]["max_rel_drift"])
        if "orbital_energy_summary" in orbit_summary
        else float("inf")
    )
    angular_momentum_drift = (
        float(orbit_summary["angular_momentum_z_summary"]["max_rel_drift"])
        if "angular_momentum_z_summary" in orbit_summary
        else float("inf")
    )
    gates = {
        "orbit_fit_available": fit_available,
        "min_periapse_count": periapse_count >= int(thresholds["min_periapse_count"]),
        "max_abs_beta_eff": abs(beta_eff) <= float(thresholds["max_abs_beta_eff"]),
        "max_rel_energy_drift": energy_drift <= float(thresholds["max_rel_energy_drift"]),
        "max_rel_angular_momentum_drift": angular_momentum_drift
        <= float(thresholds["max_rel_angular_momentum_drift"]),
        "min_coherence": float(defect_metrics["mean_coherence"]) >= float(thresholds["min_coherence"]),
        "max_higher_mode_fraction": float(defect_metrics["mean_higher_mode_fraction"])
        <= float(thresholds["max_higher_mode_fraction"]),
        "max_leakage": float(defect_metrics["mean_leakage"]) <= float(thresholds["max_leakage"]),
    }
    return {
        "passes": bool(all(gates.values())),
        "gates": gates,
    }
