# Codex Handoff: Newtonian-to-1PN Falsification Program for the 4D Toy Model

## Purpose of this document

This is the current project memo for Codex CLI.

The goal is **not** to argue for ontology or to persuade anyone that the toy model is true in nature. The goal is narrower and stricter:

> Determine whether the parent dynamical model really realizes the mathematical pathway to Newtonian gravity and conservative 1PN behavior that has been derived in the papers and symbolic harnesses.

This is a **go / no-go falsification program**.

If the model fails cleanly, that is a success of the program because it answers the question and lets us move on. If it passes all the gates, that means the pathway is dynamically realizable, whether or not anyone accepts the interpretation.

---

## Main strategic pivot

We are no longer going straight from PDE implementation to full orbit / perihelion extraction.

That was too aggressive, too expensive, and too hard to interpret.

We are now explicitly breaking the work into stages:

1. **PDE Newtonian validation**
2. **ODE Newtonian reference**
3. **ODE 1PN reference**
4. **PDE 1PN tests**

The guiding logic is:

- the PDE must first earn the right to claim Newtonian behavior,
- then the ODE can act as the cheap near-exact reference model and analysis oracle,
- then the PDE can be tested for the 1PN perturbation.

This is the most compute-efficient path and gives the cleanest failure modes.

---

## Scientific question

The question is:

> Does the full parent dynamical model realize the reduced Newtonian and 1PN mechanisms already derived on paper, or do those mechanisms break when forced to live as real evolving field dynamics?

That question should be answered in stages.

---

## Current status summary

### 1. Reduced closure prototype

The reduced matter + adiabatic-geometry closure debug run is internally consistent with the declared closure target.

Important numbers from the journal:

- `kappa_PV_estimate ≈ 1.499`
- `d ln a / d ln rho ≈ -0.891`
- very small leakage
- very small higher-mode contamination
- partition fractions consistent with the `11:2:5` target

Interpretation:

- the **reduced closure implementation** behaves as intended,
- but this does **not** independently validate the full PDE closure claim,
- because `a(t)` is still imposed by the adiabatic 1-DOF closure.

### 2. Static-background reduced orbit runs

The present static-background orbit implementation has **not** supported the target self-sector orbit mechanism.

Important conclusions already reached:

- early fitted negative `beta_eff` values from loose periapsis handling should not be over-interpreted,
- the hardened fitter now says the current archive does **not** yet contain a genuinely fit-worthy static-background orbit window,
- launch saturation and box limitations were severe in the small-box branch,
- the small-box orbit branch is effectively closed for now.

Interpretation:

- the earlier static-background orbit misses are real warnings,
- but they are entangled with protocol, box, and initialization issues,
- so they are not yet the final answer.

### 3. Static-background radial infall resolution sweep

This is now the most important completed PDE result so far.

The journal already established:

- `40^3` is underresolved and wrong,
- `64^3`, `96^3`, and `128^3` all reproduce the intended static infall behavior closely,
- the fall law is therefore converged much earlier than orbit-quality dynamics.

User-reported completion for `256^3` adds the decisive final point:

- `dx = 0.1875`
- intrinsic core size `Rg ≈ 1.18539`
- `Rg/dx ≈ 6.32`
- initial radial acceleration / Newtonian oracle `≈ 0.9969`
- `t(0.75 r0)/t_oracle ≈ 1.02436`
- `t(0.50 r0)/t_oracle ≈ 1.03022`

Interpretation:

- the static `1/r^2` fall law is already converged by about `64^3`,
- the reason to go to `256^3` is no longer force-law convergence,
- the reason is **defect resolution in cells**,
- and `256^3` is the first completed point where the defect is resolved by about six cells, making it a much more credible starting point for orbit work.

### 4. New interpretation of current evidence

At this point:

- the **static Newtonian force sector** looks good,
- the first serious `256^3` **short-arc Newtonian orbit gate** has now passed for both `source_no_dressing` and `source_with_dressing`,
- the differential signal between those two short-arc runs is extremely small,
- the **remaining bottleneck** is therefore no longer basic launch stability or defect integrity,
- it is now **long-duration Newtonian bound motion plus conservation-quality diagnostics**,
- and the correct next question is no longer “does radial fall work?” but “can the PDE sustain clean Newtonian bound motion over long enough windows to bound secular drift?”

---

## High-level roadmap

## Stage A — PDE Newtonian validation

### Goal

Show that the PDE reproduces the Newtonian sector well enough that orbit failure can no longer be blamed on the basic force law.

### What must be demonstrated

1. Static force map consistent with the intended central Newtonian field.
2. Radial infall consistent with the Newtonian oracle.
3. Tangentially launched short-arc Newtonian motion that cleanly tracks the matched tracer.
4. Tangentially launched bounded Newtonian motion over longer windows.
5. No measurable secular apsidal drift beyond pre-declared error bars.
6. Good enough defect coherence and COM tracking over many dynamical times.

### What does **not** count as enough

- a correct radial fall curve alone,
- a clean short arc alone,
- a visually elliptical trajectory with poor conservation,
- a fit that depends on loose periapsis detection or manual cherry-picking.

### Success condition for Stage A

PDE Newtonian orbits exist and are stable enough that:

- a tracer-matched short-arc control passes cleanly first,
- energy drift is small and quantified,
- angular momentum drift is small and quantified,
- fitted periapsis drift is statistically consistent with zero within the declared tolerance,
- results are stable under reasonable timestep / grid / fitter variations.

### Failure condition for Stage A

If radial infall is converged but clean Newtonian bound orbits still cannot be obtained after reasonable numerical improvements, then the model is not yet realizing the Newtonian orbit sector dynamically and this must be treated as a serious warning.

---

## Stage B — ODE Newtonian reference

### Goal

Build a cheap reference model that makes numerical integration error negligible relative to PDE error, while using the **same orbit-analysis pipeline** as the PDE runs.

### Why this matters

The ODE reference is not proof of the PDE. It is the analysis oracle.

It should tell us:

- what a zero-precession orbit looks like under the chosen fitting pipeline,
- whether the extraction code itself creates fake drift,
- what tolerances are reasonable before we spend more GPU time.

### Required features

- exact same initial-condition conventions as the PDE orbit runs,
- same COM / trajectory storage format if practical,
- same periapsis finder,
- same orbital-element fit code,
- same energy / angular-momentum diagnostics.

### Success condition for Stage B

With the ODE Newtonian model,

- extracted perihelion drift is consistent with zero,
- the fitter is stable,
- and the reference orbit is clean enough to set meaningful PDE tolerances.

---

## Stage C — ODE 1PN reference

### Goal

Quantify the target perturbation signal cheaply before trying to read it off expensive PDE runs.

### Required physics model

The ODE 1PN reference must use the **derived reduced 1PN mechanism**, not the old retarded-scalar central-field mechanism.

In practice this means using one of the following equivalent reduced forms:

- the derived dressed-orbit model with `beta_1PN = 3`, or
- the equivalent conservative 1PN point-particle / EIH reduction in the relevant limit.

### Why this matters

This stage tells us:

- the sign and magnitude of the expected precession,
- how many orbits are needed to resolve it,
- how small the PDE numerical drift must be before a 1PN signal can be distinguished.

### Success condition for Stage C

The ODE 1PN pipeline produces the expected positive perturbation with the right scaling and enough numerical cleanliness to define a target PDE error budget.

---

## Stage D — PDE 1PN tests

Only after Stages A–C pass should we spend serious compute on PDE 1PN runs.

This stage is itself broken into subtests.

### D1. Imposed static background / self-sector test

Goal:

- test whether the claimed self-dressed test-mass mechanism exists in a genuinely static source protocol.

### D2. Heavy-but-free source

Goal:

- test whether allowing the heavy source to move slightly changes the result,
- separate genuine self-sector behavior from mutual-motion / wake effects.

### D3. Clamped source negative control

Goal:

- verify whether clamping is an artifact-producing protocol,
- never use clamped source as the main physics test.

### D4. Two-live-defect / wake cross sector

Goal:

- test the moving-pair / wake / EIH cross structure once the simpler sectors are under control.

### Success condition for Stage D

A 1PN-looking signal only counts if:

- it has the correct sign,
- it scales correctly,
- it converges under resolution / timestep / window changes,
- and it appears in the regime where the claimed mechanism says it should.

A signal does **not** count if it only appears when leakage, mixed-sector excitation, or defect breakup is large.

---

## Pass / fail logic for the overall program

## This program counts as a success if it yields a decisive answer of any of these forms:

1. **PDE Newtonian passes, PDE 1PN passes**
   - strongest positive result,
   - the mathematical pathway is dynamically realized.

2. **PDE Newtonian passes, PDE 1PN fails cleanly**
   - still a strong result,
   - the reduced 1PN mechanism is not realized by the parent PDE.

3. **PDE Newtonian fails despite force-law convergence**
   - strong negative result,
   - the orbit sector is not dynamically realizable under the current parent implementation.

4. **Static-background fails but heavy-free passes**
   - indicates that the signal is primarily motion-coupled / wake-mediated,
   - this is acceptable for the pair sector,
   - but it weakens or falsifies the claimed static-source self-sector interpretation.

5. **Imposed-static passes and clamped fails**
   - pinning is a protocol artifact,
   - older pinning problems should not be treated as theory failure.

## The program should be declared failed or stalled if:

- the PDE never sustains a clean Newtonian orbit,
- the 1PN signal never becomes distinguishable from numerical drift,
- success depends on non-convergent settings,
- or the required compute becomes so extreme that the pathway is not practically testable.

---

## Immediate implementation priorities for Codex

## Priority 1 — Freeze the current lesson from the journal

Codex should treat the present status as:

- **reduced closure prototype:** positive but not decisive,
- **static-background reduced orbit implementation:** currently negative / inconclusive,
- **static radial infall:** positive and converged for force-law purposes,
- **new compute bottleneck:** orbit-quality defect resolution and launch fidelity.

Do not continue orbit-first interpretation work on the old small-box branch.

## Priority 2 — Add / finish the ODE reference pipeline

Create a lightweight orbit-reference module set that shares analysis code with the PDE side.
In practice, shared diagnostics should be treated as part of this priority, not as a later cleanup.

Suggested modules:

- `src/ode/newtonian_orbit.py`
- `src/ode/orbit_1pn_beta.py`
- `src/ode/common_orbit_diagnostics.py`

These should plug into the same fitter / periapsis / conservation machinery already being used for PDE outputs, or the PDE pipeline should be refactored so both ODE and PDE use one shared diagnostics layer.

## Priority 3 — Promote PDE Newtonian orbit work above PDE 1PN work

The next major PDE objective is **not** perihelion.
It is a clean Newtonian orbit.

Suggested experiment split:

- `exp03_pde_newtonian_bound_orbit`
- `exp03a_pde_newtonian_orbit_sweep`
- `exp03b_pde_newtonian_orbit_box_timestep_sweep`

These should run with the simplest physics needed to realize the already-validated static force law and a tangential launch.
The short-arc `256^3` control should now be treated as the entry gate to this stage, not as the final success condition.

## Priority 4 — Use 256^3 as the new minimum serious orbit grid

For orbit attempts, treat `256^3` as the new default minimum if memory and runtime allow, because:

- force-law convergence is already achieved,
- the remaining need for resolution is defect geometry in cell units,
- and `Rg/dx ≈ 6.32` is the first clearly more respectable orbit starting point.

Local 8 GB runs can still be used for scaffolding, diagnostics code, and reduced tests, but serious orbit attempts should assume cloud or larger memory if needed.

## Priority 5 — Postpone Maxwell / KK / mixed-sector complexity until Newtonian orbit is clean

Do not spend major effort on the full Maxwell / KK / mixed-sector implementation until the Newtonian PDE orbit stage is under control.

Those sectors matter later for the full parent theory, but right now they add complexity before the base orbital question has been answered.

---

## Compute strategy

### Local machine (8 GB GPU)

Use for:

- code scaffolding,
- debug runs,
- unit tests,
- ODE development,
- reduced closure checks,
- static infall and small-scope Newtonian orbit debugging,
- fitter and diagnostics validation.

### Single large cloud GPU (preferred next step)

Use a single large-memory GPU, ideally around 64 GB, for:

- `256^3`-class orbit work,
- longer orbit windows,
- larger box runs,
- defect-resolution studies,
- first serious PDE Newtonian orbit campaigns,
- and later PDE 1PN campaigns.

### Multi-GPU

Do **not** use multi-GPU until all of these are true:

- single-GPU Newtonian orbit runs are scientifically interpretable,
- the diagnostics and data products are stable,
- profiling shows single-GPU memory or runtime is the actual bottleneck.

---

## Numerical philosophy

### Central rule

A correct radial fall law is **necessary** for Newtonian orbit behavior, but not **sufficient**.

A bound orbit is more demanding because it accumulates small errors over long times.

Therefore, Codex should not assume:

> “correct fall implies Newtonian orbit is already done.”

Instead Codex should assume:

> “correct fall means the static force sector is plausible; now the orbit-quality numerics must be tested separately.”

### Orbit-quality requirements

Every serious PDE orbit run should log and summarize at least:

- COM trajectory,
- defect compactness / coherence,
- energy drift,
- angular-momentum drift,
- turning-point sequence quality,
- orbit-fit residuals,
- mode contamination if applicable,
- leakage if applicable.

No orbit result should be declared meaningful without those diagnostics.

---

## Concrete experiment ladder

## Experiment A — PDE static force / infall regression

This is mostly complete.

Required outputs:

- inward radial acceleration vs radius,
- log-log slope,
- initial acceleration ratio to oracle,
- crossing times to multiple target radii,
- defect compactness in cells,
- coherence / leakage / higher-mode fraction.

This should now be treated as the completed Newtonian-force regression suite.

## Experiment B — PDE Newtonian bound orbit

Physics:

- use the simplest PDE sector consistent with the validated static source behavior,
- no 1PN dressing,
- no extra mixed-sector complexity unless strictly necessary.

Primary question:

- can the PDE sustain a clean bound orbit with negligible secular apsidal drift?

Current status:

- the prerequisite short-arc control on the `256^3` branch has passed,
- but the long-orbit / zero-precession Newtonian gate is still not passed.

Outputs:

- periapsis sequence,
- fitted semimajor axis / eccentricity,
- apparent precession,
- energy drift,
- angular momentum drift,
- coherence / compactness statistics.

This is the next critical gate.

## Experiment C — ODE Newtonian reference

Primary question:

- does the analysis pipeline itself return zero drift when it should?

Outputs:

- same orbit-fit products as Experiment B,
- plus tolerance bands that the PDE must match or beat.

## Experiment D — ODE 1PN reference

Primary question:

- what is the actual target signal size and runtime requirement for 1PN detection?

Outputs:

- fitted positive precession,
- scaling with initial conditions,
- minimum number of orbits needed for robust detection.

## Experiment E — PDE 1PN self-sector test

Primary question:

- does the PDE static-background implementation realize the self-dressed 1PN mechanism?

Outputs:

- same orbit products as Experiments B–D,
- plus leakage / mode / mixed-sector diagnostics if active.

## Experiment F — Source-protocol triad

Run the same orbit three ways:

1. imposed static background,
2. heavy but free source,
3. clamped source.

Primary question:

- is pinning an artifact,
- and which sector is actually generating the observed signal?

## Experiment G — PDE moving-pair / wake cross sector

Only after the above stages are working.

Primary question:

- does the PDE realize the EIH cross tensor dynamically?

---

## Repository / documentation expectations

Codex should maintain these artifacts in the repo:

1. `results_journal.md`
   - append every significant run,
   - do not rewrite history,
   - record both positive and negative results.

2. `reference/oracle_targets.yaml`
   - store the current fixed target constants and formulas.
   - if the repo continues to use `reference/symbolic_targets.json` instead, that file should be treated as the canonical source instead of creating a parallel target file.

3. `docs/newtonian_to_1pn_program.md`
   - this document, or a repo copy of it.

4. `docs/run_matrix.md`
   - a short table of which experiments are complete, active, blocked, or retired.

5. `docs/analysis_pipeline.md`
   - define exactly how COM, periapses, orbital elements, and drift are measured.

The analysis pipeline must be shared between ODE and PDE wherever possible.
At the moment, these last two docs should be treated as near-term required work rather than optional polish.

---

## Recommended language for future summaries

When summarizing progress, use language like:

- “static force-law validation passed,”
- “Newtonian orbit gate not yet passed,”
- “ODE reference established,”
- “1PN target signal quantified,”
- “PDE 1PN mechanism supported / not supported in the tested regime.”

Avoid language like:

- “the ontology is proven,”
- “gravity has been derived in nature,”
- “the model is correct.”

This project is about validating or falsifying a **mathematical pathway**, not proving metaphysical claims.

---

## Bottom line for Codex

The new rule is simple:

> Stop trying to jump directly from PDE implementation to orbit precession claims.

Instead:

1. lock down **PDE Newtonian**,
2. build the **ODE reference and shared diagnostics**,
3. quantify the **ODE 1PN target**,
4. then test **PDE 1PN**.

The most important current result is that the **static fall law is already converged** and that the `256^3` **short-arc Newtonian gate is now clean**, while the real remaining problem is **long-window Newtonian orbit quality, conservation diagnostics, and shared ODE/PDE analysis**.

That is the branch we are on now.
