#!/usr/bin/env bash
set -euo pipefail

python -m src.scripts.check_cuda_runtime --require-cuda

configs=(
  configs/local/exp01_prefilled_bath_source_relaxed_320_compactness_screen_d050.json
  configs/local/exp01_prefilled_bath_source_relaxed_320_compactness_screen_d055.json
  configs/local/exp01_prefilled_bath_source_relaxed_320_compactness_screen_d065.json
  configs/local/exp01_prefilled_bath_source_relaxed_320_compactness_screen_d070.json
)

for config in "${configs[@]}"; do
  echo "[exp01-compactness-screen] running ${config}"
  PYTHONUNBUFFERED=1 python -m src.experiments.exp01_single_heavy_source_inflow \
    --config "${config}"
done
