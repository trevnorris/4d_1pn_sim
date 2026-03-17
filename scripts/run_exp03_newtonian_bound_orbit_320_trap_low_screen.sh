#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export PYTHONUNBUFFERED=1

python -m src.scripts.check_cuda_runtime --require-cuda

configs=(
  "configs/local/exp03_newtonian_bound_orbit_320_screen_trap_low_r020.json"
  "configs/local/exp03_newtonian_bound_orbit_320_screen_trap_low_r040.json"
  "configs/local/exp03_newtonian_bound_orbit_320_screen_trap_low_r060.json"
  "configs/local/exp03_newtonian_bound_orbit_320_screen_trap_r080.json"
)

for config in "${configs[@]}"; do
  echo "[trap-low-screen] running $config"
  python -m src.experiments.exp03_pde_newtonian_bound_orbit --config "$config"
done
