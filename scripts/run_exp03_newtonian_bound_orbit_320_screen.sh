#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export PYTHONUNBUFFERED=1

python -m src.scripts.check_cuda_runtime --require-cuda

if [[ ! -f outputs/runs/exp03_newtonian_bound_orbit_320_cuda_smoke/checkpoint_relaxed.npz ]]; then
  echo "Missing outputs/runs/exp03_newtonian_bound_orbit_320_cuda_smoke/checkpoint_relaxed.npz" >&2
  echo "Run ./scripts/run_exp03_newtonian_bound_orbit_320_cuda_smoke.sh first." >&2
  exit 1
fi

configs=(
  "configs/local/exp03_newtonian_bound_orbit_320_screen_sponge_only.json"
  "configs/local/exp03_newtonian_bound_orbit_320_screen_refill_leakonly.json"
  "configs/local/exp03_newtonian_bound_orbit_320_screen_sponge_refill_leakonly.json"
  "configs/local/exp03_newtonian_bound_orbit_320_screen_weak_sponge_refill_leakonly.json"
)

for config in "${configs[@]}"; do
  echo "[screen] running $config"
  python -m src.experiments.exp03_pde_newtonian_bound_orbit --config "$config"
done
