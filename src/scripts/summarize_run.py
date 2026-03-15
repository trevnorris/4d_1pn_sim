from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.core.targets import load_reference_targets


def compare_partition(measured: dict[str, float], target: dict[str, float]) -> dict[str, float]:
    total_target = sum(target.values())
    target_fraction = {key: value / total_target for key, value in target.items()}
    return {key: measured[key] - target_fraction[key] for key in measured}


def summarize(run_dir: str | Path) -> dict[str, object]:
    run_path = Path(run_dir)
    with (run_path / "summary.json").open("r", encoding="utf-8") as handle:
        summary = json.load(handle)
    targets = load_reference_targets()

    closure = summary["closure_scan"]
    partition_delta = compare_partition(closure["partition_fraction"], targets["energy_partition"])
    comparison = {
        "kappa_PV_error": closure["kappa_PV_estimate"] - targets["kappa_PV"],
        "dln_a_dln_rho_error": closure["a_fit"]["slope"] - targets["dln_a_dln_rho"],
        "partition_fraction_error": partition_delta,
        "mean_drive_coherence": summary["mean_drive_coherence"],
        "mean_drive_higher_mode_fraction": summary["mean_drive_higher_mode_fraction"],
        "mean_drive_leakage": summary["mean_drive_leakage"],
        "supports_target": (
            abs(closure["kappa_PV_estimate"] - targets["kappa_PV"]) < 0.2
            and abs(closure["a_fit"]["slope"] - targets["dln_a_dln_rho"]) < 0.15
        ),
    }
    with (run_path / "oracle_comparison.json").open("w", encoding="utf-8") as handle:
        json.dump(comparison, handle, indent=2, sort_keys=True)
    return comparison


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare an Experiment 1 run to the closure targets")
    parser.add_argument("--run-dir", required=True, help="Run directory produced by exp01_single_defect_response")
    args = parser.parse_args()

    run_path = Path(args.run_dir)
    with (run_path / "summary.json").open("r", encoding="utf-8") as handle:
        summary = json.load(handle)

    if "closure_scan" in summary:
        comparison = summarize(args.run_dir)
        print(f"supports_target: {comparison['supports_target']}")
        print(f"kappa_PV_error: {comparison['kappa_PV_error']:+.6f}")
        print(f"dln_a_dln_rho_error: {comparison['dln_a_dln_rho_error']:+.6f}")
        print(f"mean_drive_coherence: {comparison['mean_drive_coherence']:.6f}")
        print(f"mean_drive_higher_mode_fraction: {comparison['mean_drive_higher_mode_fraction']:.6e}")
        print(f"mean_drive_leakage: {comparison['mean_drive_leakage']:.6e}")
        partition_error = comparison["partition_fraction_error"]
        print(
            "partition_fraction_error: "
            f"E_w={partition_error['E_w']:+.6f}, "
            f"E_f={partition_error['E_f']:+.6f}, "
            f"E_PV={partition_error['E_PV']:+.6f}"
        )
        return

    if "orbit_summary" in summary:
        targets = load_reference_targets()
        orbit = summary["orbit_summary"]
        if "fit_error" in orbit:
            print(f"fit_error: {orbit['fit_error']}")
            print(f"mean_fit_coherence: {orbit['mean_fit_coherence']:.6f}")
            print(f"mean_fit_higher_mode_fraction: {orbit['mean_fit_higher_mode_fraction']:.6e}")
            print(f"mean_fit_leakage: {orbit['mean_fit_leakage']:.6e}")
            return
        beta_error = orbit["beta_eff"] - targets["beta_1PN"]
        print(f"beta_eff_error: {beta_error:+.6f}")
        print(f"delta_phi: {orbit['delta_phi']:.6f}")
        print(f"delta_phi_stderr: {orbit['delta_phi_stderr']:.6f}")
        print(f"semi_major_axis: {orbit['semi_major_axis']:.6f}")
        print(f"eccentricity: {orbit['eccentricity']:.6f}")
        print(f"mean_fit_coherence: {orbit['mean_fit_coherence']:.6f}")
        print(f"mean_fit_higher_mode_fraction: {orbit['mean_fit_higher_mode_fraction']:.6e}")
        print(f"mean_fit_leakage: {orbit['mean_fit_leakage']:.6e}")
        return

    raise ValueError("summary.json does not contain a known experiment summary shape")


if __name__ == "__main__":
    main()
