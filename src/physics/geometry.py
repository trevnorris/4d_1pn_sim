from __future__ import annotations

import math
from dataclasses import dataclass

from src.core.targets import load_reference_targets
from src.physics.eos import PolytropicEOS


@dataclass
class AdiabaticGeometryClosure:
    eos: PolytropicEOS
    lambda_aspect: float
    reference_rho: float
    reference_a: float
    reference_energy_scale: float

    def __post_init__(self) -> None:
        targets = load_reference_targets()["energy_partition"]
        e_w = self.reference_energy_scale * targets["E_w"]
        e_f = self.reference_energy_scale * targets["E_f"]
        e_pv = self.reference_energy_scale * targets["E_PV"]

        cs_ref = float(self.eos.sound_speed(self.reference_rho))
        pressure_ref = float(self.eos.pressure(self.reference_rho))
        volume_ref = math.pi * self.lambda_aspect * self.reference_a**3

        self.C_w = e_w * self.reference_a / cs_ref
        self.C_f = e_f * self.reference_rho * self.reference_a**2
        self.C_pv = e_pv / (pressure_ref * volume_ref)

    def equilibrium_energies(self, a_value: float, ambient_rho: float) -> dict[str, float]:
        c_s = float(self.eos.sound_speed(ambient_rho))
        pressure = float(self.eos.pressure(ambient_rho))
        e_w = self.C_w * c_s / a_value
        e_f = self.C_f / (ambient_rho * a_value**2)
        e_pv = self.C_pv * pressure * math.pi * self.lambda_aspect * a_value**3
        return {"E_w": e_w, "E_f": e_f, "E_PV": e_pv}

    def total_energy(self, a_value: float, ambient_rho: float) -> float:
        energies = self.equilibrium_energies(a_value, ambient_rho)
        return energies["E_w"] + energies["E_f"] + energies["E_PV"]

    def derivative(self, a_value: float, ambient_rho: float) -> float:
        c_s = float(self.eos.sound_speed(ambient_rho))
        pressure = float(self.eos.pressure(ambient_rho))
        return (
            -self.C_w * c_s / a_value**2
            - 2.0 * self.C_f / (ambient_rho * a_value**3)
            + 3.0 * self.C_pv * pressure * math.pi * self.lambda_aspect * a_value**2
        )

    def equilibrium_a(self, ambient_rho: float, initial_guess: float | None = None) -> float:
        a_low = max(0.05 * self.reference_a, 1.0e-4)
        a_high = max(initial_guess or self.reference_a, self.reference_a)

        derivative_low = self.derivative(a_low, ambient_rho)
        derivative_high = self.derivative(a_high, ambient_rho)
        while derivative_high <= 0.0:
            a_high *= 2.0
            derivative_high = self.derivative(a_high, ambient_rho)
            if a_high > 128.0 * self.reference_a:
                raise RuntimeError("Failed to bracket the adiabatic geometry equilibrium.")

        if derivative_low >= 0.0:
            a_low = 0.5 * self.reference_a
            derivative_low = self.derivative(a_low, ambient_rho)

        for _ in range(80):
            a_mid = 0.5 * (a_low + a_high)
            derivative_mid = self.derivative(a_mid, ambient_rho)
            if derivative_mid > 0.0:
                a_high = a_mid
            else:
                a_low = a_mid
            if abs(a_high - a_low) < 1.0e-8 * max(1.0, a_mid):
                break
        return 0.5 * (a_low + a_high)

    def closure_diagnostics(self, ambient_rho: float) -> dict[str, float]:
        a_eq = self.equilibrium_a(ambient_rho)
        energies = self.equilibrium_energies(a_eq, ambient_rho)
        total = sum(energies.values())
        x_ratio = energies["E_f"] / energies["E_w"]
        n_value = self.eos.n
        dln_f_dln_rho = (
            ((n_value - 1.0) / 2.0) * energies["E_w"]
            - energies["E_f"]
            + n_value * energies["E_PV"]
        ) / total
        dln_a_dln_rho = -(
            -(n_value - 1.0) / 2.0 + 2.0 * x_ratio + n_value * (1.0 + 2.0 * x_ratio)
        ) / (4.0 + 10.0 * x_ratio)
        return {
            "a_eq": a_eq,
            "L_eq": self.lambda_aspect * a_eq,
            "F_eq": total,
            "kappa_PV": dln_f_dln_rho - 1.0,
            "dln_F_dln_rho": dln_f_dln_rho,
            "dln_a_dln_rho": dln_a_dln_rho,
            "E_w": energies["E_w"],
            "E_f": energies["E_f"],
            "E_PV": energies["E_PV"],
        }
