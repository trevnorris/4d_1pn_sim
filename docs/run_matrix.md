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
| ODE Newtonian reference | `complete` | Fitter / shared orbit analysis give near-zero drift with excellent conservation |
| ODE 1PN reference | `blocked` | Waiting until Newtonian reference and shared diagnostics are in place |
| PDE 1PN static self-sector test | `blocked` | Deferred until long Newtonian PDE orbit is clean |
| Source-protocol triad | `blocked` | Follows PDE 1PN static self-sector test |
| Moving-pair / wake cross sector | `blocked` | Later-stage only |
| Old small-box static-background orbit branch | `retired` | Closed due launch saturation, boundary problems, and non-interpretable fits |

## Immediate next step

- Run the guarded `320^3 / L=60` Newtonian `sponge_only` narrow velocity refinement on the best trap branch `trap_strength_r = 0.125`, testing `velocity_scale = 0.975, 0.978, 0.981, 0.983` while using the completed `0.97` and `0.985` runs as anchors.
- For overnight server use, a follow-on wrapper is available that waits for that refine batch to finish and then runs two `12288`-step confirmations at `velocity_scale = 0.978` and `0.981`.
