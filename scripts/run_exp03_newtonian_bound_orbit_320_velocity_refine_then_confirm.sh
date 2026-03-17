#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export PYTHONUNBUFFERED=1

python -m src.scripts.check_cuda_runtime --require-cuda

required_summaries=(
  "outputs/runs/exp03_newtonian_bound_orbit_320_screen_velocity_refine_t0125_v0975/summary.json"
  "outputs/runs/exp03_newtonian_bound_orbit_320_screen_velocity_refine_t0125_v0978/summary.json"
  "outputs/runs/exp03_newtonian_bound_orbit_320_screen_velocity_refine_t0125_v0981/summary.json"
  "outputs/runs/exp03_newtonian_bound_orbit_320_screen_velocity_refine_t0125_v0983/summary.json"
)

missing=0
for summary in "${required_summaries[@]}"; do
  if [[ ! -f "$summary" ]]; then
    missing=1
    break
  fi
done

if [[ "$missing" -eq 1 ]]; then
  echo "[overnight] refine summaries missing; running the refine batch first"
  ./scripts/run_exp03_newtonian_bound_orbit_320_velocity_refine_t0125.sh
else
  echo "[overnight] refine summaries already present; skipping directly to confirmations"
fi

echo "[overnight] refine batch complete; launching longer confirmations"
configs=(
  "configs/local/exp03_newtonian_bound_orbit_320_confirm_t0125_v0978_long.json"
  "configs/local/exp03_newtonian_bound_orbit_320_confirm_t0125_v0981_long.json"
)

for config in "${configs[@]}"; do
  echo "[overnight] running $config"
  python -m src.experiments.exp03_pde_newtonian_bound_orbit --config "$config"
done
