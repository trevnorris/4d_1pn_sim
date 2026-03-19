#!/usr/bin/env bash
set -euo pipefail

python -m src.scripts.check_cuda_runtime --require-cuda

PYTHONUNBUFFERED=1 python -m src.experiments.exp01_single_heavy_source_inflow \
  --config configs/local/exp01_prefilled_bath_source_320_boundary_relaxation.json
