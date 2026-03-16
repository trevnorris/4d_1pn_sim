#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export PYTHONUNBUFFERED=1

python -m src.scripts.check_cuda_runtime --require-cuda

python -m src.experiments.exp03_pde_newtonian_bound_orbit \
  --config configs/local/exp03_newtonian_bound_orbit_320_restart_cuda.json
