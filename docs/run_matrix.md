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
| Live heavy-source inflow calibration | `active` | Implemented and multiple initial branches completed: the no-refill control keeps the source coherent but shows almost no outer inflow, the first boundary-fed reservoir restores box norm and creates positive outer-shell inflow but puffs the source up too much, and the first cap/shape screen showed the cap was not the active knob. The next step is an interior-feed-shell reservoir screen that separates refill placement from the sponge zone. |
| ODE Newtonian reference | `complete` | Fitter / shared orbit analysis give near-zero drift with excellent conservation |
| ODE 1PN reference | `blocked` | Waiting until Newtonian reference and shared diagnostics are in place |
| PDE 1PN static self-sector test | `blocked` | Deferred until long Newtonian PDE orbit is clean |
| Source-protocol triad | `blocked` | Follows PDE 1PN static self-sector test |
| Moving-pair / wake cross sector | `blocked` | Later-stage only |
| Old small-box static-background orbit branch | `retired` | Closed due launch saturation, boundary problems, and non-interpretable fits |

## Immediate next step

- Reset the source-sector baseline around a prefilled bath rather than asking the box to fill itself from near-vacuum:
  - `./scripts/run_exp01_prefilled_bath_control_320_boundary_relaxation.sh`
  - `./scripts/run_exp01_prefilled_bath_source_320_boundary_relaxation.sh`
- The control run should:
  - start from a uniform mode-0 bath at the target ambient density,
  - include no embedded defect and no confinement trap,
  - verify that shell inflow stays near zero under the boundary protocol.
- The source run should:
  - start from the same prefilled bath,
  - embed the centered defect directly into that bath,
  - then use conditioning plus boundary relaxation before measuring production inflow.
- Promote the live-source path only if the bath control stays quiet and the embedded-defect branch settles into inward outer-shell flow without the old fill-from-vacuum transients.
