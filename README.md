# 4D 1PN Simulator

PyTorch simulator and falsification harness for the 4D toy-model Newtonian-to-1PN program.

## Current scope

Implemented today:

- Hermite-mode utilities in the transverse direction `w`
- projection and leakage helpers
- matter-only split-step solver in `x,y,z` times Hermite modes
- one-DOF adiabatic geometry closure for `a(t)` with fixed `L = Lambda * a`
- single-defect Experiment 1 closure regression
- single-heavy-source inflow calibration branch
- static-background infall resolution sweep
- tracer-matched `256^3` short-arc controls
- shared ODE/PDE orbit diagnostics
- ODE Newtonian orbit reference
- PDE Newtonian bound-orbit gate runner

Still intentionally missing:

- full Maxwell / KK sector
- free-heavy source runs
- two-live-defect / moving-pair sector
- PDE 1PN interpretation work beyond the current Newtonian gate

The active development plan is in [docs/newtonian_to_1pn_program.md](docs/newtonian_to_1pn_program.md).

## Install

Use the repo environment:

```bash
python -m pip install -e .
```

or:

```bash
python -m pip install -r requirements.txt
```

## Quick checks

Run the full test suite:

```bash
pytest -q
```

Check whether the current Python/Torch environment can actually see CUDA:

```bash
python -m src.scripts.check_cuda_runtime
python -m src.scripts.check_cuda_runtime --require-cuda
```

Important:

- configs that use `"device": "cuda_if_available"` will fall back to CPU
- configs that use `"device": "cuda"` now fail fast if CUDA is not available
- this is deliberate so cloud runs do not silently spend hours on CPU

## Main commands

Experiment 1 closure regression:

```bash
python -m src.experiments.exp01_single_defect_response --config configs/local/exp01_debug.json
python -m src.scripts.summarize_run --run-dir outputs/runs/exp01_debug
```

Single heavy-source inflow calibration on CUDA:

```bash
./scripts/run_exp01_single_heavy_source_inflow_320_cuda.sh
```

Single heavy-source inflow calibration with boundary-fed reservoir refill:

```bash
./scripts/run_exp01_single_heavy_source_inflow_320_boundary_reservoir_cuda.sh
```

Boundary-reservoir tuning screen for the live heavy-source calibration:

```bash
./scripts/run_exp01_single_heavy_source_inflow_320_boundary_screen.sh
```

Interior-shell boundary-reservoir tuning screen for the live heavy-source calibration:

```bash
./scripts/run_exp01_single_heavy_source_inflow_320_boundary_shell_screen.sh
```

Narrow follow-up around the best interior-shell boundary-reservoir branch:

```bash
./scripts/run_exp01_single_heavy_source_inflow_320_boundary_shell_refine.sh
```

Conditioned long confirmation on the current best heavy-source calibration branch:

```bash
./scripts/run_exp01_single_heavy_source_inflow_320_conditioned_long.sh
```

Conditioned long confirmation using the boundary-relaxation collar redesign:

```bash
./scripts/run_exp01_single_heavy_source_inflow_320_boundary_relaxation_conditioned_long.sh
```

Prefilled-bath boundary control with no embedded defect:

```bash
./scripts/run_exp01_prefilled_bath_control_320_boundary_relaxation.sh
```

Prefilled-bath source calibration with an embedded centered defect:

```bash
./scripts/run_exp01_prefilled_bath_source_320_boundary_relaxation.sh
```

Prefilled-bath source calibration with the embedded defect ramped in during conditioning:

```bash
./scripts/run_exp01_prefilled_bath_source_ramped_320_boundary_relaxation.sh
```

Prefilled-bath source calibration starting from an imaginarily relaxed composite source-in-bath state:

```bash
./scripts/run_exp01_prefilled_bath_source_relaxed_320_boundary_relaxation.sh
```

Focused production-refill sweep on the relaxed composite source-in-bath branch:

```bash
./scripts/run_exp01_prefilled_bath_source_relaxed_320_refill_screen.sh
```

Prefilled-bath operator-isolation screen for the no-defect bath control:

```bash
./scripts/run_exp01_prefilled_bath_control_320_operator_screen.sh
```

The sponge-enabled prefilled-bath controls now use a bath-preserving sponge that damps deviations from the uniform bath in the boundary collar instead of multiplying the bath itself down.

ODE Newtonian reference:

```bash
python -m src.ode.newtonian_orbit --config configs/local/ode_newtonian_reference.json
```

Short-arc `256^3` control from the saved relaxed checkpoint:

```bash
./scripts/run_exp02_shortarc_256_restart.sh
python -m src.scripts.run_short_arc_static_background --config configs/local/exp02_shortarc_256_restart.json --scenario source_with_dressing
```

PDE Newtonian bound-orbit gate on CPU restart path:

```bash
./scripts/run_exp03_newtonian_bound_orbit_256_restart.sh
```

PDE Newtonian bound-orbit gate with explicit CUDA requirement:

```bash
./scripts/run_exp03_newtonian_bound_orbit_256_cuda.sh
```

Promoted next cloud-GPU branch:

```bash
./scripts/run_exp03_newtonian_bound_orbit_320_sponge_only_smoke.sh
./scripts/run_exp03_newtonian_bound_orbit_320_sponge_only_restart.sh
```

Screening matrix for the current `320^3` branch:

```bash
./scripts/run_exp03_newtonian_bound_orbit_320_screen.sh
```

Trap-strength screen for the promoted `320^3` `sponge_only` branch:

```bash
./scripts/run_exp03_newtonian_bound_orbit_320_trap_screen.sh
```

Lower-trap follow-up screen for the same branch:

```bash
./scripts/run_exp03_newtonian_bound_orbit_320_trap_low_screen.sh
```

Narrow refinement around the best current trap range:

```bash
./scripts/run_exp03_newtonian_bound_orbit_320_trap_narrow_screen.sh
```

Follow-up refinement screen around the current low-trap optimum:

```bash
./scripts/run_exp03_newtonian_bound_orbit_320_trap_refine_screen.sh
```

Velocity screen on top of the best trap candidates:

```bash
./scripts/run_exp03_newtonian_bound_orbit_320_velocity_screen.sh
```

Narrow velocity refinement on the best trap branch:

```bash
./scripts/run_exp03_newtonian_bound_orbit_320_velocity_refine_t0125.sh
```

Overnight follow-on that waits for the current refine batch, then runs 2 longer confirmations:

```bash
./scripts/run_exp03_newtonian_bound_orbit_320_velocity_refine_then_confirm.sh
```

## Runtime guidance

- The `256^3` long-orbit PDE branch is a serious run, not a quick local sanity check.
- CPU runs can take many hours.
- The CUDA wrapper is the intended fire-and-forget path for cloud GPUs because it performs a preflight check before starting the long job.
- The long `exp03` restart configs now include a runtime abort guard. If effective COM drift, defect integrity, or boundary clearance go decisively off-rail, the run stops early and still writes `summary.json` plus `plain_language_summary.txt`.
- Screening configs can now disable the large checkpoint artifacts and keep only `summary.json`, `plain_language_summary.txt`, `timeseries.npz`, and small JSON metadata. This is the intended low-disk mode for broad cloud sweeps.
- The current long-orbit restart configs reuse the saved relaxed checkpoint at `outputs/runs/exp02_shortarc_256/checkpoint_relaxed.npz` to avoid repeating the most expensive setup stage.
- The current recommended cloud branch is `320^3` with `L = 60`, using the promoted `sponge_only` protocol. Run it first as a guarded smoke path and then as a restart from the smoke run's `checkpoint_relaxed.npz`.
- On the `320^3` branch, the full continuity residual diagnostic remains disabled (`continuity_stride = 0`) because `currents()` OOMs on an A40 even though the main evolution fits.
- The current data say the boundary sponge helps, while the first uniform refill law hurts orbit quality. Refill is still scientifically important for the boxed model, but it needs a better budgeted/state-dependent implementation before it should be promoted back into the long-run path.

## Documentation

Current status and run history:

- [docs/results_journal.md](docs/results_journal.md)
- [docs/run_matrix.md](docs/run_matrix.md)
- [docs/analysis_pipeline.md](docs/analysis_pipeline.md)
- [docs/exp02_audit_matrix.md](docs/exp02_audit_matrix.md)

Target constants:

- [reference/symbolic_targets.json](reference/symbolic_targets.json)
