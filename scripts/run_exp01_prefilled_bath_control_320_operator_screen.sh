#!/usr/bin/env bash
set -euo pipefail

python -m src.scripts.check_cuda_runtime --require-cuda

for cfg in \
  configs/local/exp01_prefilled_bath_control_320_bare.json \
  configs/local/exp01_prefilled_bath_control_320_sponge_only.json \
  configs/local/exp01_prefilled_bath_control_320_boundary_relaxation_only.json \
  configs/local/exp01_prefilled_bath_control_320_sponge_boundary_relaxation.json
do
  echo "[bath-screen] running $cfg"
  PYTHONUNBUFFERED=1 python -m src.experiments.exp01_single_heavy_source_inflow --config "$cfg"
done
