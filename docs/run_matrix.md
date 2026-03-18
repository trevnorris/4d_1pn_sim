# Run Matrix

This file tracks the experiment ladder status at a glance.

## Status legend

- `complete`: finished and interpretable
- `active`: current next-step branch
- `blocked`: conceptually chosen but waiting on prerequisites
- `retired`: no longer worth spending compute on

## Experiment ladder

| Experiment | Status | Current read |
| --- | --- | --- |
| PDE static force / infall regression | `complete` | Static `1/r^2` force law validated; converged by `64^3`; `256^3` chosen for orbit-quality defect resolution |
| PDE Newtonian short-arc control (`256^3`, no dressing) | `complete` | Passed tracer-matched short-arc acceptance gate |
| PDE Newtonian short-arc comparison (`256^3`, with dressing) | `complete` | Also passed; differential signal versus control is tiny |
| PDE Newtonian long bound orbit | `active` | Implemented and CUDA-validated end-to-end; the first guarded `256^3 / L=48` and `320^3 / L=60` no-refill/no-sponge runs both aborted early on COM drift while the defect remained coherent. The `320^3` control screen then showed `sponge_only` is clearly best, while the first uniform refill law degrades the orbit. |
| Live heavy-source inflow calibration | `active` | Implemented and first no-refill calibration completed: the single centered heavy defect stays coherent and localized, but the first run does not yet show a clean sustained sink-like inflow at larger radii. Boundary-fed reservoir refill is now prepared as the next A/B source-sector branch. |
| ODE Newtonian reference | `complete` | Fitter / shared orbit analysis give near-zero drift with excellent conservation |
| ODE 1PN reference | `blocked` | Waiting until Newtonian reference and shared diagnostics are in place |
| PDE 1PN static self-sector test | `blocked` | Deferred until long Newtonian PDE orbit is clean |
| Source-protocol triad | `blocked` | Follows PDE 1PN static self-sector test |
| Moving-pair / wake cross sector | `blocked` | Later-stage only |
| Old small-box static-background orbit branch | `retired` | Closed due launch saturation, boundary problems, and non-interpretable fits |

## Immediate next step

- Run the boundary-fed reservoir A/B on the single-heavy-source calibration branch:
  - baseline: `./scripts/run_exp01_single_heavy_source_inflow_320_cuda.sh`
  - boundary reservoir: `./scripts/run_exp01_single_heavy_source_inflow_320_boundary_reservoir_cuda.sh`
- Compare shell inflow, total-norm drift, ambient-density proxy, and source coherence between those two runs.
- If the boundary-fed branch produces a cleaner sustained source state, the next branch should add a light defect and test radial infall against the Newtonian `1/r^2` oracle using the same live-source protocol.
