#!/usr/bin/env bash
set -euo pipefail

python -m src.scripts.check_cuda_runtime --require-cuda

RELAXED=outputs/runs/exp01_single_heavy_source_inflow_320_cuda/checkpoint_relaxed.npz
if [[ ! -f "$RELAXED" ]]; then
  echo "missing relaxed checkpoint: $RELAXED" >&2
  echo "run ./scripts/run_exp01_single_heavy_source_inflow_320_cuda.sh first" >&2
  exit 1
fi

CONFIGS=(
  configs/local/exp01_single_heavy_source_inflow_320_boundary_shell_refine_inner6_w1p5_cap5em6.json
  configs/local/exp01_single_heavy_source_inflow_320_boundary_shell_refine_inner6_w2_cap25em7.json
  configs/local/exp01_single_heavy_source_inflow_320_boundary_shell_refine_inner6p5_w2_cap5em6.json
  configs/local/exp01_single_heavy_source_inflow_320_boundary_shell_refine_inner7_w2_cap5em6.json
)

for config in "${CONFIGS[@]}"; do
  echo "[boundary-shell-refine] running $config"
  PYTHONUNBUFFERED=1 python -m src.experiments.exp01_single_heavy_source_inflow \
    --config "$config" \
    --restart-relaxed "$RELAXED"
done
