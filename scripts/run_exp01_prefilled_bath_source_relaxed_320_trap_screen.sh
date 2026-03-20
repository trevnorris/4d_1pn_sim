#!/usr/bin/env bash
set -euo pipefail

python -m src.scripts.check_cuda_runtime --require-cuda

configs=(
  configs/local/exp01_prefilled_bath_source_relaxed_320_trap_screen_r030.json
  configs/local/exp01_prefilled_bath_source_relaxed_320_trap_screen_r035.json
  configs/local/exp01_prefilled_bath_source_relaxed_320_trap_screen_r045.json
  configs/local/exp01_prefilled_bath_source_relaxed_320_trap_screen_r050.json
)

for config in "${configs[@]}"; do
  echo "[exp01-trap-screen] running ${config}"
  PYTHONUNBUFFERED=1 python -m src.experiments.exp01_single_heavy_source_inflow \
    --config "${config}"
done
