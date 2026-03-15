from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import torch


def save_checkpoint(path: str | Path, state: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {}
    for key, value in state.items():
        if isinstance(value, torch.Tensor):
            payload[key] = value.detach().cpu().numpy()
        elif isinstance(value, (float, int, np.ndarray)):
            payload[key] = value
        else:
            payload[key] = np.array(value)
    np.savez_compressed(target, **payload)


def load_checkpoint(path: str | Path, device: torch.device, complex_dtype: torch.dtype) -> dict[str, Any]:
    data = np.load(Path(path), allow_pickle=False)
    state: dict[str, Any] = {}
    for key in data.files:
        value = data[key]
        if np.iscomplexobj(value):
            state[key] = torch.as_tensor(value, device=device, dtype=complex_dtype)
        elif value.ndim > 0:
            state[key] = torch.as_tensor(value, device=device)
        else:
            scalar = value.item()
            state[key] = scalar
    return state
