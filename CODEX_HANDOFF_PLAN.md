# PyTorch implementation plan for the 4D toy model

## Goal

Build the **smallest PyTorch codebase that can falsify or support the current 4D toy-model story** without hiding the known failure modes behind a bad source protocol or an over-aggressive reduction.

The code should be judged against the existing Wolfram Language symbolic oracles, not against visual plausibility alone.

This plan is optimized for:

1. **fast local iteration on an 8 GB GPU**, then
2. **single-GPU cloud scale-up on a 64 GB card**, then
3. **multi-GPU only if the single 64 GB path is genuinely exhausted**.

The plan intentionally separates:

- **self / closure sector** tests,
- **static-background orbit** tests,
- **source-protocol diagnostics**,
- **moving-pair / wake / EIH cross-term** tests.

That separation is essential because a **clamped source is not equivalent to a static background**, and a **moving-pair wake channel is not the same mechanism as the claimed self-dressed test-mass orbit sector**.

---

## Scientific objective and stopping rules

The code is successful if it can decisively answer at least one of these:

1. the adiabatic closure survives the full PDE dynamics,
2. the static-background test-mass orbit sector survives,
3. the free-heavy moving-pair sector survives,
4. or one of those fails cleanly enough to identify the flaw.

### Earliest falsifiable outcomes

#### Outcome A — closure fails
If the single-defect adiabatic response does **not** approach the target low-frequency closure in the low-leakage regime,

- `kappa_PV -> 3/2`
- `E_w : E_f : E_PV -> 11 : 2 : 5`
- `d ln a / d ln rho -> -57/64`

then stop and report:

> the current adiabatic closure is not realized by the full PyTorch dynamics.

#### Outcome B — static-background orbit fails
If the imposed-static-background orbit run does **not** converge toward the `beta_1PN = 3` perihelion target while the light defect remains compact and leakage / higher-mode contamination stay small, then stop and report:

> the claimed test-mass / static-source self-dressed orbit mechanism is likely absent or incomplete in the full PDE model.

#### Outcome C — pinning was the issue
If imposed-static and free-heavy runs agree, but clamped-source runs fail or differ strongly, report:

> clamping is a bad surrogate for a static source; the older pinning issue was a protocol artifact, not necessarily a theory failure.

#### Outcome D — pair sector fails
If the self-sector passes but the moving-pair / two-live-defect EIH cross structure fails, report:

> the flaw is likely in the wake / vector / pair-interaction sector rather than in the self-dressing sector.

### Interpretation rule

A 1PN-looking signal **does not count as success** if it only appears when one or more of the supposed “small correction channels” are large during the fitting window, especially:

- strong leakage,
- large `J^w E_w`,
- large `F_{mu w}` / mixed-sector excitation,
- large higher-mode occupation,
- obvious defect deformation or loss of coherence.

---

## Constants and oracle targets to hard-code into tests

These come from the existing symbolic stack and should be encoded as the reference targets for regression tests and diagnostic fitting:

- EOS exponent: `n = 5`
- added-mass coefficient for a w-uniform throat: `kappa_add = 1/2`
- wake mixing: `alpha^2 = 3/4`
- minimal wake helical admixture: `a_H = 0`
- vector-sector normalization: `K_vec = 2 / pi^2`
- adiabatic closure target: `kappa_PV = 3/2`
- closure partition target: `E_w : E_f : E_PV = 11 : 2 : 5`
- breathing slope target: `d ln a / d ln rho = -57/64`
- 1PN ledger target: `beta_1PN = 3`
- test-mass perihelion target:
  - `Delta phi = 2*pi*beta*GM / (c^2 a (1-e^2))`
  - with `beta = 3`, this becomes the GR weak-field value
- EIH pair cross targets:
  - coefficient of `v_A · v_B` = `-7/2`
  - coefficient of `(v_A · n_AB)(v_B · n_AB)` = `-1/2`

The code should also preserve the exact projected identities where applicable.

---

## Non-negotiable modeling rules

1. **Do not use a clamped heavy body as the main orbit test.**
   It is only a negative control.

2. **Do not start with two fully live defects.**
   That is too hard to interpret.

3. **Do not let decisive runs live in `N_w = 1`.**
   Use `N_w = 1` only as a debug baseline. Main falsification runs should use `N_w >= 4`.

4. **Do not claim success from trajectories alone.**
   A result only counts with diagnostics: coherence, leakage, higher-mode energy, mixed-sector work, and fit stability.

5. **Do not enable mixed precision before float32 / complex64 invariants are working.**

6. **Do not distribute across multiple GPUs before the single-GPU code is correct and profiled.**

7. **Do not bake away the source-protocol question.**
   The code must support all three protocols:
   - imposed static background,
   - heavy but free source,
   - clamped source.

---

## Recommended codebase structure

```text
repo/
  AGENTS.md
  README.md
  pyproject.toml
  requirements.txt
  configs/
    local/
    cloud/
  reference/
    symbolic_targets.yaml
    notes/
  src/
    core/
      grids.py
      units.py
      hermite.py
      projection.py
      fft_ops.py
      isolated_poisson.py
      checkpoints.py
      io.py
      profiling.py
    physics/
      eos.py
      matter_gnls.py
      geometry.py
      background_sources.py
      defects.py
      observables.py
      diagnostics.py
      fitting.py
    em/
      maxwell_modes.py
      gauge_constraints.py
      kk_modes.py
      mixed_sector.py
    experiments/
      exp01_single_defect_response.py
      exp02_orbit_static_background.py
      exp03_source_protocol_triad.py
      exp04_maxwell_kk_validation.py
      exp05_free_heavy_orbit.py
      exp06_two_live_defect_eih.py
    scripts/
      run_experiment.py
      build_initial_conditions.py
      summarize_run.py
      compare_to_oracle.py
  tests/
    test_projection_identities.py
    test_hermite_basis.py
    test_kk_spectrum.py
    test_kappa_pv_targets.py
    test_wake_targets.py
    test_lockin_zeff.py
    test_orbit_fitter.py
  outputs/
    runs/
    figures/
    tables/
```

---

## Numerical architecture

## 1. Spatial representation

### Brane directions `(x, y, z)`
Use a **3D pseudo-spectral representation** with `torch.fft.fftn` / `ifftn` for the linear kinetic pieces and for convolution-based solvers where appropriate.

Reasons:

- clean split-step GNLS evolution,
- efficient GPU execution,
- natural path to large local and cloud runs,
- direct compatibility with the Hermite-mode decomposition in `w`.

### Transverse direction `w`
Use a **truncated Hermite basis** induced by Gaussian localization.

Represent fields as:

- matter: `psi_n(x,y,z,t)`
- later EM: `A_mu^(n)(x,y,z,t)` and optionally `A_w^(n)(x,y,z,t)`

The implementation should support `N_w = 1, 2, 4, 8, ...` with the first meaningful physics target at `N_w = 4`.

### Nonlinear couplings in `w`
Compute nonlinear terms pseudo-spectrally in the transverse direction:

1. reconstruct fields at quadrature nodes `w_q`,
2. compute products pointwise,
3. project back to Hermite modes.

This follows the large-run strategy already suggested by the 4D EM / plasma writeups.

---

## 2. Matter solver

Use a custom PyTorch solver for the gauged / ungauged GNLS matter sector.

### Stage-1 matter-only core
Start with **matter + geometry**, without live Maxwell.

Minimum live state:

- `psi_n(x,y,z,t)` for `n = 0..N_w-1`
- geometry variable `a(t)`
- fixed ratio `L = Lambda * a` initially

Recommended first integrator:

- **imaginary-time / damped relaxation** for static defect preparation,
- **Strang split** or split-step spectral integrator for real-time evolution,
- geometry updated either:
  - adiabatically by re-minimization each macro-step, or
  - with a damped ODE substep after the adiabatic version is stable.

### Local nonlinear pieces
Include:

- confinement `V_conf(x,y,z,w ; a, L)`
- EOS / enthalpy sector with `n = 5`
- optional external background field or enthalpy profile

### Recommended implementation order
1. single-mode `N_w = 1` debug version,
2. multi-mode matter-only version,
3. adiabatic geometry coupling,
4. defect initializer,
5. diagnostics,
6. only then Maxwell / mixed sector.

---

## 3. Geometry closure

### First implementation
Use the explicit adiabatic closure first, not a full wall dynamics model.

That means:

- a single collective coordinate `a(t)`
- fixed aspect ratio `L = Lambda * a`
- for each external state / drive, solve for the instantaneous or slowly varying `a`

### Second implementation
Add a damped ODE option:

```text
M_a a_ddot + Gamma_a a_dot = -dH_tot/da
```

This is needed only after the adiabatic route is working, so that you can measure:

- frequency response,
- memory effects,
- resonant failure of a local closure.

---

## 4. Background source handling

### Main static-source test
Use an **imposed static background** or a **precomputed stationary source profile**.

Do **not** emulate this by clamping a live defect.

Recommended implementation:

- a module that generates an external central background in one of two forms:
  1. analytic weak-field profile,
  2. numerically precomputed stationary heavy-source field stored on the grid.

### Free-heavy source test
Later, allow the heavy source to be fully live and very massive, but still free.

### Clamped source test
Support a clamped protocol as a negative control only.

---

## 5. Poisson / source-field handling

For the static-background orbit stage, the quickest path is to **avoid solving the source-field problem live** and instead impose the background directly.

For later free-heavy and two-body stages, add an **isolated Poisson solver** or equivalent source-field evolution that does not suffer from periodic image artifacts.

Recommended first implementation:

- zero-padded isolated Green-function convolution via FFT,
- verified against analytic `1/r` test cases.

Do **not** rely on naive periodic Poisson for orbit-quality two-body physics.

---

## 6. Maxwell / wake sector

This is a second-stage module, not the first thing to build.

### Maxwell stage 0
Write tests and utilities first:

- Gaussian KK / Hermite spectrum
- `m_n^2 = 2 n / lambda^2`
- even-mode brane couplings only
- Coulomb + Yukawa correction pattern

### Maxwell stage 1
Implement the brane-effective / zero-mode Maxwell sector first:

- `A_mu^(0)` only
- `A_w = 0`
- `J^w = 0`
- confirm effective coupling and source normalization

### Maxwell stage 2
Add full mode stacks and mixed sector:

- `A_mu^(n)`
- optional `A_w^(n)`
- mixed fields `F_{mu w}`
- diagnostics for `E_w`, `C_a`, `J^w E_w`, and `S_EM^w`

### Wake / pair sector
Use the existing wake coefficients as oracle targets when the pair sector is turned on:

- `alpha^2 = 3/4`
- `a_H = 0`
- `K_vec = 2 / pi^2`
- pair cross coefficients `(-7/2, -1/2)`

---

## Diagnostics and observables

Every experiment must log a structured diagnostics bundle.

## A. Core defect diagnostics

- brane mass / norm
- center of mass on the brane
- radius of gyration / compactness
- bound mass fraction within a defect window
- phase winding / topological integrity if used
- defect mode spectrum in `w`

## B. Projection and open-system diagnostics

- `rho_brane`
- `J_brane`
- exact continuity residual
- leakage source `S_leak`
- cumulative leaked mass fraction
- covariance terms from projection where available

## C. Closure diagnostics

- `F_eq(rho)`
- `a_eq(rho)`
- fitted `d ln F_eq / d ln rho`
- fitted `d ln a / d ln rho`
- fitted `kappa_PV`
- internal energy partition `(E_w, E_f, E_PV)`
- low-frequency response matrix `Z_eff(omega)`

## D. Orbit diagnostics

- center-of-mass trajectory of the light defect
- osculating orbital elements
- periapsis times and angles
- fitted precession per orbit `Delta phi`
- fitted `beta_eff`
- confidence interval and drift with fit window

## E. Mixed-sector / beyond-reduction diagnostics

- mode energies `E_n`, especially `sum_{n>0} E_n / E_tot`
- mixed-sector field norms `||E_w||`, `||C||`
- integrated `J^w E_w`
- projected EM energy leakage in `w`
- brane helicity transfer if EM is on

### Mandatory interpretation rule

A run does **not** count as validating the reduced mechanism unless the fit is taken over a window where:

- defect coherence is stable,
- leakage is small,
- higher-mode energy is small,
- and the result is resolution-stable.

---

## Exact helper algorithms to include

These come straight from the logic already present in the symbolic harnesses and should be reimplemented numerically.

### 1. Lock-in extraction for driven response
For a harmonic drive at frequency `omega`, recover complex amplitudes with:

```text
A(omega) = mean_t[ signal(t) * exp(-i omega t) ]
```

Use this to build port matrices `U(omega)` and `J(omega)` and estimate:

```text
Z_eff(omega) = J(omega) @ inv(U(omega))
```

with a stable solve / pseudoinverse fallback.

### 2. Poisson-regime diagnostic ratios
Implement a helper that estimates the size of the terms dropped when replacing the exact longitudinal identity by a Poisson equation. At minimum log:

- `|d_t rho| / |source|`
- `|grad rho · (grad phi + v_T)| / |source|`

### 3. Orbit fit helper
Implement a robust precession fitter that:

- identifies successive periapses,
- unwraps the periapsis angle,
- fits a linear trend in orbit index,
- reports `Delta phi` and uncertainty.

### 4. Protocol comparison helper
Given three runs with matched initial conditions,

- imposed static,
- free heavy,
- clamped,

emit a single comparison table with the main physics outputs.

---

## Experiment ladder

## Experiment 0 — codebase and unit-test scaffold

### Objective
Create the project skeleton, CI tests, mode basis, projection machinery, and numerical utilities.

### Required tests
- Hermite basis orthonormality
- Gaussian KK spectrum
- even/odd coupling rule
- projected continuity identity on manufactured data
- lock-in `Z_eff` extraction on manufactured data
- wake-target constants regression
- orbit fitter on a manufactured precessing ellipse

### Exit criterion
All unit tests pass on CPU and on one CUDA device.

---

## Experiment 1 — single-defect relaxation and closure

### Objective
Measure whether the adiabatic closure actually emerges in the full matter+geometry solver.

### Setup
- `N_w = 4` main run, `N_w = 1` debug baseline
- one compact defect in a large box
- background density `rho_0`
- adiabatic or quasi-adiabatic ambient-density modulation
- no live Maxwell yet

### Procedure
1. build a static defect by imaginary-time relaxation,
2. verify defect stability in real time at fixed `rho_0`,
3. sweep small ambient density perturbations around `rho_0`,
4. optionally add a sinusoidal drive at very low frequency,
5. extract:
   - `kappa_PV(omega)`
   - `E_w : E_f : E_PV`
   - `d ln a / d ln rho`
   - `Z_eff(omega)`

### Minimum pass criteria
For the low-frequency, low-leakage window, the run should trend toward:

- `kappa_PV ≈ 1.5`
- partition near `11:2:5`
- `d ln a / d ln rho ≈ -57/64`

At coarse local resolution, accept trend-level agreement before chasing high precision.

### Failure report if missed
State clearly whether the miss is associated with:

- excessive leakage,
- large higher-mode occupancy,
- geometry ringing / nonadiabaticity,
- inability to define a stable low-frequency `Z_eff`.

---

## Experiment 2 — static-background orbit (main self-sector falsifier)

### Objective
Test the claimed test-mass / static-source self-dressed orbit mechanism without the pinning ambiguity.

### Setup
- light live defect
- imposed static heavy-source background
- weak-field elliptical orbit
- `N_w = 4` main run
- matter + geometry solver only at first

### Procedure
1. prepare a relaxed light defect,
2. insert it into the imposed central background,
3. initialize a bound orbit,
4. run many orbital periods,
5. fit `Delta phi` and `beta_eff`,
6. log coherence, leakage, and higher-mode energy.

### Minimum pass criteria
The fitted `beta_eff` should move toward `3` with refinement, while:

- defect compactness remains stable,
- leakage stays small in the fit window,
- higher-mode energy stays small in the fit window.

### This experiment answers
Whether the full PDE realizes the claimed self-sector orbit correction in a truly static background.

---

## Experiment 3 — source-protocol triad

### Objective
Diagnose the old pinning issue directly.

### Protocols
Run the same nominal orbit under:

1. imposed static background,
2. heavy but free source with large mass ratio,
3. clamped heavy source.

### Compare
- `Delta phi`
- `beta_eff`
- defect compactness
- cumulative leakage
- `J^w E_w` if active
- `sum_{n>0} E_n / E_tot`
- heavy-source recoil for the free-heavy case

### Interpretation table

#### Case 1
Imposed static passes, free-heavy passes, clamped fails:

> clamping is the bad proxy.

#### Case 2
Imposed static fails, free-heavy passes:

> the 1PN signal is being generated mainly by mutual-motion / wake channels, which is a problem for the static-source test-mass claim.

#### Case 3
Imposed static passes, free-heavy fails:

> the self sector is okay; the pair / propagation / wake sector is the likely flaw.

#### Case 4
All three fail:

> the issue is deeper than pinning.

---

## Experiment 4 — Maxwell / KK validation

### Objective
Validate the localized 4+1 Maxwell implementation before using it in moving-pair physics.

### Checks
- KK masses follow `m_n^2 = 2n / lambda^2`
- odd modes decouple from brane-localized sources
- Coulomb + Yukawa correction reproduced
- zero-mode reduction recovers effective 3+1 Maxwell
- moving-source retarded structure is causal

### Exit criterion
All Maxwell / KK regression tests pass and the mode-resolved energy ledger closes.

---

## Experiment 5 — free-heavy source with live propagation channels

### Objective
Repeat the orbit test with a live heavy source and the propagation channels that could matter for the old pinning issue.

### Setup
- large mass ratio
- heavy source free, not clamped
- activate the minimum required pair / propagation sector
- keep the problem as close as possible to the static-background orbit test otherwise

### Goal
Determine whether allowing genuine source motion changes the measured 1PN signal in a way consistent with the old concern.

---

## Experiment 6 — two live defects and EIH fit

### Objective
Only after the previous tests pass or cleanly isolate the issue, test the genuine two-body pair sector.

### Outputs
Fit the effective pair coefficients and compare against the EIH targets:

- `C_parallel = -7/2`
- `C_L = -1/2`

### Acceptable outcome
Even a clean failure is scientifically useful here, because it isolates the wake / vector sector.

---

## Local 8 GB GPU plan

The 8 GB GPU is enough for **development and quick falsification**, but not for the largest decisive runs.

### Recommended local targets

#### Matter-only / closure stage
- `96^3 x N_w=4` or `128^3 x N_w=4`
- `complex64` for matter fields
- `float32` for real fields and diagnostics

#### Static-background orbit stage
- start at `96^3 x 4`
- then `128^3 x 4`
- only increase `N_w` after the orbit fitter and diagnostics are stable

#### Maxwell stage on 8 GB
- use `96^3 x 4` or `128^3 x 2-4` first
- expect to reduce either spatial size or mode count once the gauge stack is live

### Local performance rules
- use power-of-two FFT sizes when practical
- do not enable AMP until invariants pass in float32 / complex64
- profile memory before raising both `N` and `N_w`
- checkpoint outputs often and keep runs short during development

### Rough memory rule of thumb
For one field stack with shape `(N_w, N, N, N)`:

- float32 real field size ≈ `4 * N_w * N^3` bytes
- complex64 field size ≈ `8 * N_w * N^3` bytes

Examples:

- `128^3 x 4`: one complex field ≈ 0.062 GB
- `192^3 x 4`: one complex field ≈ 0.211 GB
- `256^3 x 8`: one complex field ≈ 1.000 GB

A real simulation stores multiple live fields and scratch buffers, so budget several times these numbers.

---

## 64 GB cloud GPU plan

A single 64 GB GPU should be the first cloud target.

### Why single 64 GB first
- far simpler debugging
- avoids premature distributed complexity
- likely enough for the decisive `N_w = 8` runs at meaningful spatial resolution
- easier reproducibility for scientific debugging

### Recommended cloud targets

#### Matter + geometry decisive runs
- `192^3 x 8`
- then `256^3 x 8` if needed

#### Maxwell + mixed sector
- `192^3 x 4-8`
- only increase to `256^3` after the ledger is stable

### Likely use of 64 GB
A single 64 GB GPU is likely sufficient for:

- closure experiment at production resolution,
- static-background orbit experiment with meaningful mode count,
- source-protocol triad,
- first free-heavy runs.

Use multi-GPU only if:

- `256^3 x 8` plus full gauge / mixed sector is too slow or too memory-heavy,
- or you need wide parameter sweeps rather than one gold-standard run.

---

## Multi-GPU and cluster guidance

Do not build the distributed version first.

### First distributed target
Use **single-node multi-GPU** with one process per GPU.

Recommended decomposition order:

1. **mode decomposition across `n`** if the implementation stays mostly diagonal in mode index,
2. otherwise **spatial domain decomposition** with halo exchange.

### PyTorch recommendation
Use `torchrun` + `torch.distributed` with NCCL on Linux/CUDA.

### What not to use first
Do not reach for FSDP as the first scaling tool. This is a simulation with explicit state tensors, not a parameter-heavy training model.

### Cluster threshold
Only consider multi-node when at least one of these is true:

- single 64 GB GPU cannot hold the target run,
- single-node throughput is too slow for the needed sweep,
- mode or domain decomposition is already working on one node.

---

## Precision and optimization policy

### Baseline
- matter fields: `complex64`
- real fields: `float32`
- diagnostics that accumulate over long times: promote to `float64` on CPU as needed

### After correctness only
- test `torch.compile` on stable kernels
- test optional autocast only for non-critical kernels or after invariants are verified

### Do not do this early
- no FP16-first development
- no compile-first development
- no distributed-first development

---

## Reproducibility requirements

Every run should write:

- full config file
- git commit if available
- hardware info
- random seeds
- PyTorch / CUDA versions
- wall-clock timing
- diagnostics summary JSON
- one HDF5 / NPZ checkpoint stream for restart and post-processing

Save at least:

- initial condition snapshot,
- mid-run snapshot,
- final snapshot,
- diagnostic time series.

---

## Acceptance criteria by stage

## Stage 0 acceptance
- all unit tests pass
- projection identities verified numerically
- synthetic lock-in and orbit-fit tests pass

## Stage 1 acceptance
- relaxed defect is stable at fixed background
- closure diagnostics run end-to-end
- at least trend-level movement toward the `(11:2:5, 3/2, -57/64)` targets

## Stage 2 acceptance
- static-background orbit produces a stable fitted `Delta phi`
- `beta_eff` moves toward `3` under refinement
- diagnostics show the fit window is genuinely low-leakage / low-mode-excitation

## Stage 3 acceptance
- protocol triad runs on matched initial data
- interpretation table can be populated cleanly

## Stage 4 acceptance
- Maxwell / KK tests pass against closed-form targets
- zero-mode reduction reproduced
- causal retarded behavior verified

## Stage 5 acceptance
- free-heavy runs produce interpretable results with the same diagnostics as the static-background run

## Stage 6 acceptance
- two-body pair fit either approaches EIH or fails in a way that cleanly localizes the flaw

---

## Concrete first implementation sprint

This is the first thing Codex should build.

### Sprint goal
Create a runnable matter+geometry prototype that can execute Experiment 1 and prepare Experiment 2.

### Required deliverables
1. repo scaffold
2. Hermite basis and quadrature utilities
3. projection / leakage utilities
4. matter-only split-step solver in 3D x modes
5. adiabatic geometry closure with one DOF `a`
6. defect initializer by imaginary-time relaxation
7. diagnostics bundle for closure tests
8. pytest suite for symbolic targets and manufactured-data helpers
9. CLI entry point for `exp01_single_defect_response`
10. plotting / summary script for closure outputs

### Explicitly out of scope for sprint 1
- full Maxwell stack
- free-heavy orbit
- two-live-defect runs
- distributed training / multi-GPU

---

## Exact tasks for Codex, in order

1. Create project skeleton and dependencies.
2. Add Hermite basis generator and Gaussian localization helpers.
3. Add projection and leakage identity helpers.
4. Add split-step matter solver in 3D x modes.
5. Add one-DOF adiabatic geometry module.
6. Add defect relaxation and restartable checkpointing.
7. Add closure diagnostics and fitting utilities.
8. Add unit tests for all symbolic targets.
9. Add experiment runner for single-defect response.
10. Add summary notebook or script that prints pass/fail against the closure targets.
11. Only after that, add the static-background orbit experiment.

---

## What the final answer from Codex should include after sprint 1

Codex should return:

1. a list of created files,
2. a short explanation of the solver architecture,
3. exact commands to run the tests,
4. exact commands to run Experiment 1 locally,
5. a note about any assumptions or placeholders that remain,
6. a concise report of whether the closure target appears to hold on the first local run.

---

## Preferred user workflow with Codex CLI

1. Start in the repo root.
2. Ensure `AGENTS.md` is present.
3. Hand Codex this plan.
4. Ask it to work in **plan-first mode** for the first major task.
5. Have it implement only sprint 1 first.
6. Review tests and the first response report.
7. Then advance to the static-background orbit stage.

---

## Summary of the shortest credible route

The shortest path is:

1. **single-defect closure**,
2. **static-background orbit**,
3. **source-protocol triad**,
4. **then** free-heavy / pair / EIH.

That sequence is the fastest route to a result that is both scientifically interpretable and useful, whether it succeeds or fails.
