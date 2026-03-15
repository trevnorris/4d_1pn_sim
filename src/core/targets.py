from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any


REFERENCE_TARGETS_PATH = Path(__file__).resolve().parents[2] / "reference" / "symbolic_targets.json"


@lru_cache(maxsize=1)
def load_reference_targets() -> dict[str, Any]:
    with REFERENCE_TARGETS_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def energy_partition_fractions() -> dict[str, float]:
    targets = load_reference_targets()["energy_partition"]
    total = sum(targets.values())
    return {key: value / total for key, value in targets.items()}


def k_vec_target() -> float:
    return 2.0 / math.pi**2
