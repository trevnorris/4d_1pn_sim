#!/usr/bin/env bash
set -euo pipefail

python -m src.scripts.check_cuda_runtime --require-cuda

RELAXED=outputs/runs/exp01_single_heavy_source_inflow_320_cuda/checkpoint_relaxed.npz
if [[ ! -f "$RELAXED" ]]; then
  echo "missing relaxed checkpoint: $RELAXED" >&2
  echo "run ./scripts/run_exp01_single_heavy_source_inflow_320_cuda.sh first" >&2
  exit 1
fi

PYTHONUNBUFFERED=1 python -m src.experiments.exp01_single_heavy_source_inflow \
  --config configs/local/exp01_single_heavy_source_inflow_320_boundary_relaxation_conditioned_long.json \
  --restart-relaxed "$RELAXED"
