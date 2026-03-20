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

- First isolate which bath operator is exciting the prefilled box:
  - `./scripts/run_exp01_prefilled_bath_control_320_operator_screen.sh`
- The four no-defect controls are:
  - bare prefilled bath
  - sponge only
  - boundary relaxation only
  - sponge + boundary relaxation
- The sponge-enabled prefilled-bath cases now use a bath-preserving sponge that damps perturbations relative to the uniform bath instead of damping the bath itself.
- The next branch should only be promoted after the no-defect bath stays near zero shell flux without building artificial structure in the center.
- The embedded-defect prefilled-bath source branch remains the follow-on, not the immediate next run:
  - `./scripts/run_exp01_prefilled_bath_source_320_boundary_relaxation.sh`
- The promoted source follow-on is now the relaxed composite branch:
  - `./scripts/run_exp01_prefilled_bath_source_relaxed_320_boundary_relaxation.sh`
- Purpose:
  - build the full bath-plus-defect composite at `t=0`,
  - imaginary-time relax that composite before real-time evolution,
  - then apply the same conditioning and production protocol to the already matched source-in-bath state.
- The next isolated lever after that relaxed-source control is production refill strength:
  - `./scripts/run_exp01_prefilled_bath_source_relaxed_320_refill_screen.sh`
- This screen keeps the bath, source initialization, sponge, and boundary-relaxation geometry fixed and only raises `production_refill_scale` above the successful `0.5` baseline.
- The promoted follow-on after that refill screen is a source-compactness screen at the chosen `production_refill_scale = 0.75` control:
  - `./scripts/run_exp01_prefilled_bath_source_relaxed_320_compactness_screen.sh`
- This screen keeps the bath and boundary protocol fixed and varies only `initializer.defect_target_norm` around the `6.0` baseline to test whether a more compact or weaker source cleans up the outer-shell inflow.
