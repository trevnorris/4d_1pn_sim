#!/usr/bin/env bash
set -euo pipefail

python -m src.scripts.check_cuda_runtime --require-cuda

configs=(
  configs/local/exp01_prefilled_bath_source_relaxed_320_refill_screen_p075.json
  configs/local/exp01_prefilled_bath_source_relaxed_320_refill_screen_p100.json
  configs/local/exp01_prefilled_bath_source_relaxed_320_refill_screen_p125.json
  configs/local/exp01_prefilled_bath_source_relaxed_320_refill_screen_p150.json
)

for config in "${configs[@]}"; do
  echo "[exp01-refill-screen] running ${config}"
  PYTHONUNBUFFERED=1 python -m src.experiments.exp01_single_heavy_source_inflow \
    --config "${config}"
done
