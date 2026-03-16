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
| PDE Newtonian long bound orbit | `active` | Implemented and CUDA-validated end-to-end; the first guarded `256^3 / L=48` run aborted early on COM energy/angular-momentum drift while the defect remained coherent, so the promoted next branch is `320^3 / L=60` |
| ODE Newtonian reference | `complete` | Fitter / shared orbit analysis give near-zero drift with excellent conservation |
| ODE 1PN reference | `blocked` | Waiting until Newtonian reference and shared diagnostics are in place |
| PDE 1PN static self-sector test | `blocked` | Deferred until long Newtonian PDE orbit is clean |
| Source-protocol triad | `blocked` | Follows PDE 1PN static self-sector test |
| Moving-pair / wake cross sector | `blocked` | Later-stage only |
| Old small-box static-background orbit branch | `retired` | Closed due launch saturation, boundary problems, and non-interpretable fits |

## Immediate next step

- Run the guarded `320^3 / L=60` Newtonian smoke branch on GPU, then promote to the matching long restart branch if the smoke result is operationally clean.
