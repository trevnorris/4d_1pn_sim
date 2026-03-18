#!/usr/bin/env bash
set -euo pipefail

python -m src.scripts.check_cuda_runtime --require-cuda

RESTART=()
if [[ -f outputs/runs/exp01_single_heavy_source_inflow_320_cuda/checkpoint_relaxed.npz ]]; then
  RESTART=(
    --restart-relaxed
    outputs/runs/exp01_single_heavy_source_inflow_320_cuda/checkpoint_relaxed.npz
  )
fi

PYTHONUNBUFFERED=1 python -m src.experiments.exp01_single_heavy_source_inflow \
  --config configs/local/exp01_single_heavy_source_inflow_320_boundary_reservoir_cuda.json \
  "${RESTART[@]}"
