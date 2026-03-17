#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export PYTHONUNBUFFERED=1

python -m src.scripts.check_cuda_runtime --require-cuda

configs=(
  "configs/local/exp03_newtonian_bound_orbit_320_screen_trap_narrow_r015.json"
  "configs/local/exp03_newtonian_bound_orbit_320_screen_trap_low_r020.json"
  "configs/local/exp03_newtonian_bound_orbit_320_screen_trap_narrow_r025.json"
  "configs/local/exp03_newtonian_bound_orbit_320_screen_trap_narrow_r030.json"
)

for config in "${configs[@]}"; do
  echo "[trap-narrow-screen] running $config"
  python -m src.experiments.exp03_pde_newtonian_bound_orbit --config "$config"
done
