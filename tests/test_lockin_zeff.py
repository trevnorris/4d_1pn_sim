import numpy as np

from src.physics.fitting import extract_effective_response


def test_lockin_extracts_manufactured_zeff_matrix() -> None:
    omega = 1.7
    time = np.linspace(0.0, 12.0 * np.pi / omega, 5000, endpoint=False)
    z_true = np.array([[2.0 + 0.3j, -0.2 + 0.1j], [0.4 - 0.5j, 1.5 + 0.2j]])
    effort_amp = np.array([[1.0 + 0.2j, 0.3 - 0.1j], [-0.4 + 0.3j, 0.8 + 0.6j]])
    flux_amp = z_true @ effort_amp

    effort_signal = np.real(effort_amp[:, :, None] * np.exp(1j * omega * time)[None, None, :])
    flux_signal = np.real(flux_amp[:, :, None] * np.exp(1j * omega * time)[None, None, :])

    result = extract_effective_response(
        effort_ports=effort_signal,
        flux_ports=flux_signal,
        time=time,
        omega=omega,
    )
    assert np.allclose(result["Z_eff"], z_true, atol=5.0e-3, rtol=5.0e-3)
