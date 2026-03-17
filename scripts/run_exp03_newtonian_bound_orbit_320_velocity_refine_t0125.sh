#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export PYTHONUNBUFFERED=1

python -m src.scripts.check_cuda_runtime --require-cuda

configs=(
  "configs/local/exp03_newtonian_bound_orbit_320_screen_velocity_refine_t0125_v0975.json"
  "configs/local/exp03_newtonian_bound_orbit_320_screen_velocity_refine_t0125_v0978.json"
  "configs/local/exp03_newtonian_bound_orbit_320_screen_velocity_refine_t0125_v0981.json"
  "configs/local/exp03_newtonian_bound_orbit_320_screen_velocity_refine_t0125_v0983.json"
)

for config in "${configs[@]}"; do
  echo "[velocity-refine] running $config"
  python -m src.experiments.exp03_pde_newtonian_bound_orbit --config "$config"
done
