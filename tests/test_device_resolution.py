import torch

from src.core.grids import resolve_device


def test_resolve_device_cpu() -> None:
    device = resolve_device("cpu")
    assert device.type == "cpu"


def test_resolve_device_cuda_if_available_falls_back_or_uses_cuda() -> None:
    device = resolve_device("cuda_if_available")
    assert device.type in {"cpu", "cuda"}


def test_resolve_device_explicit_cuda_raises_without_cuda() -> None:
    if torch.cuda.is_available():
        device = resolve_device("cuda")
        assert device.type == "cuda"
    else:
        try:
            resolve_device("cuda")
        except RuntimeError as exc:
            assert "CUDA device requested" in str(exc)
        else:
            raise AssertionError("Expected explicit CUDA request to fail when CUDA is unavailable")
