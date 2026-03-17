# Experiment 3 Newtonian Orbit Status Memo

Date: 2026-03-17

This memo summarizes what the current `exp03` static-background Newtonian orbit branch has established, what it has not established, and why the next branch should likely focus on density-locked or more self-consistent source dynamics rather than continuing to treat the imposed static background as the final scientific target.

## Executive summary

- The reduced codebase already supports a clean static Newtonian `1/r^2` infall law.
- The live defect can survive short-arc orbital motion and remain highly coherent.
- The long-window static-background orbit branch still shows a persistent secular non-conservative channel.
- Recent diagnostics now suggest that this is not explained by simple bulk box drainage alone.
- There is also a serious conceptual limitation in the static-background reduction: if the toy model’s effective source strength is maintained by defect-structure feedback against ambient-density changes, then freezing the source while the medium evolves may create an artificial drift in the effective coupling.
- Because of that, the static-background branch has been useful as a diagnostic control, but it may be nearing its scientific ceiling.

## What has been established so far

### 1. Reduced closure emulator works

`exp01` reproduces the reduced closure targets well:

- `kappa_PV ≈ 1.499`
- `d ln a / d ln rho ≈ -0.891`
- very small leakage
- very small higher-mode contamination

This supports the reduced closure emulator only. It does not yet validate the full self-consistent PDE claim.

### 2. Static Newtonian force law is real in the current solver

The infall-resolution sweep established:

- `40^3` is underresolved and wrong
- `64^3` and above already recover the static `1/r^2` acceleration well
- `256^3` is the first tested point where the defect is also reasonably resolved in cell units

So the solver is not failing because it cannot reproduce basic Newtonian attraction.

### 3. The long-orbit bottleneck is not obvious defect breakup

Across the best `exp03` runs:

- coherence usually remains high
- higher-mode fraction stays modest
- the defect remains structurally intact

The long-orbit failure is instead showing up as secular COM degradation:

- effective orbital-energy drift
- effective angular-momentum drift
- inward spiral over long windows

## Current best static-background orbit regime

The most useful `320^3` branch so far is:

- imposed analytic pure-Kepler background
- `L = 60`
- `trap_strength_r = 0.125`
- `trap_strength_w = 0.9`
- sponge enabled
- no refill in the promoted control branch

This came out of a series of trap-strength screens:

- high `trap_strength_r` strongly worsened COM drift
- very low `trap_strength_r` (`0.05`, `0.10`) deconfined the defect and failed on coherence
- the sweet spot is around `0.125` to `0.15`

The best current trap tradeoff is `trap_strength_r = 0.125`.

## Latest velocity-refine result

The latest overnight run in `diagnostic-refine-out.log` confirms that the launch-calibration bug was fixed: the refined velocity cases now launch at genuinely different effective speeds.

Short refine runs at `trap_strength_r = 0.125`:

| velocity_scale | final radius at `t=56.64` | max rel energy drift | max rel ang-mom drift | mean tangential accel | max rel total norm drop | mean coherence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.975` | `15.0845` | `9.444e-02` | `4.658e-02` | `-4.713e-04` | `6.014e-03` | `0.991759` |
| `0.978` | `15.2385` | `9.471e-02` | `4.655e-02` | `-4.717e-04` | `5.985e-03` | `0.991760` |
| `0.981` | `15.3924` | `9.505e-02` | `4.657e-02` | `-4.671e-04` | `5.955e-03` | `0.991760` |
| `0.983` | `15.4949` | `9.528e-02` | `4.658e-02` | similar | similar | `0.991761` |

Interpretation:

- all four runs completed the full `4096` steps cleanly
- none passed the Newtonian gate
- none produced enough turning points for a periapsis fit
- all still drift inward over time
- the branch is now in a true tuning regime, not a totally unstable regime

Long confirmations at `0.978` and `0.981`:

- both reached step `7168`
- both then aborted on energy drift and coherence
- both are extremely similar
- both still spiral inward over longer windows

## New diagnostic takeaways

### 1. Drag-like signal exists

The newly added drag audit reports a small but persistent negative mean tangential acceleration:

- example: `mean_tangential_acceleration ≈ -4.7e-04`

This is consistent with a weak drag-like torque / tangential sink acting on the COM.

Important caveat:

- this does **not** prove the toy-model physics contains drag
- it only shows the current reduced numerical protocol is producing drag-like behavior

Likely causes include:

- confinement-induced COM/internal coupling
- boundary/sponge backreaction
- projection or bookkeeping asymmetry
- refill/sink terms that are not momentum-neutral
- finite-grid anisotropy

### 2. Bulk box drainage is probably not the whole story

The new density audit shows that the total norm drop over the short refine window is only about:

- `max_rel_total_norm_drop ≈ 6e-03`

That is much smaller than the effective orbital-energy drift over the same window:

- `max_rel_energy_drift ≈ 9e-02`

So the current evidence does **not** support the idea that the observed orbital degradation is explained purely by simple bulk box drainage.

That said, bulk density still matters conceptually because in the toy model the defect/source structure may respond to ambient density.

## Important conceptual limitation of the static-background branch

The static-background branch imposes the central field by hand.

That means:

- the orbiting defect is live
- the central source is **not** live
- source strength is represented by fixed analytic `mu`

This is useful as a diagnostic reduction, but it is not the full toy model.

### Why this may matter a lot

A key interpretation discussed during this phase is:

- in the toy model, effective gravitational strength may remain approximately constant because defect structure adapts to ambient-density changes
- if ambient density drops, the throat opening could increase, raising inflow and compensating the source strength
- if that is true, then a fixed static source in a changing medium is not self-consistent

In that case, freezing the source may produce an artificial drift in the effective coupling, i.e. an apparent time-varying `G`, even if the full toy model would have self-corrected.

That makes the static-background branch potentially “close but not quite” for a principled reason, not just because of bad tuning.

## Why density locking / refill was proposed

The rationale for trying to keep the superfluid density constant was not merely numerical stabilization.

It was a reduced-physics strategy:

- if bulk density is held constant, the defect throat size should not need to change much
- then a fixed-source approximation becomes more defensible
- this avoids having to model the full dynamic throat-response sector just to test Newtonian orbits

So the goal of refill was physically motivated.

The issue is only that the **first** refill implementation was too naive:

- uniform reinjection degraded the orbit badly
- it likely was not momentum-neutral
- therefore it should not be treated as the final density-locking protocol

## Current interpretation

The current evidence is more consistent with:

- a numerical / protocol non-conservative channel in the static-background branch

than with:

- a failure of the underlying Newtonian central-force idea itself

At the same time, the static-background branch may have an intrinsic ceiling because it freezes source feedback that may be essential to maintaining an effectively constant `G`.

So both things may be true at once:

1. there is still a simulation/protocol artifact creating drag-like loss
2. the frozen-source reduction may itself be too constrained to ever become fully decisive

## Recommended next steps

### Updated priority after external review

After external review of the current run history and memo, the recommended order of operations should be tightened:

1. **Localize the secular sink first.**
   The strongest present evidence still points to a protocol-level torque / confinement coupling issue before it points to frozen-source inconsistency as the dominant failure. The most important immediate question is: which operator is bleeding effective orbital energy and angular momentum?

2. **Use density locking only as a controlled diagnostic branch.**
   Density locking is still well-motivated physically in this toy-model reduction, but the first refill implementations made the orbit worse. So the next refill branch should be treated as a bias-free A/B test against the baseline control, not as the new default physics branch.

3. **Promote the source sector only after the sink is localized.**
   If the secular tangential sink survives the operator budget and a carefully neutral density-locking test, then the next stronger branch should be a more self-consistent source protocol, ideally a live heavy-source / large-mass-ratio branch rather than more static-background tuning.

### Near term

- Continue using the new drag audit and box-density audit on any future `exp03` runs.
- Inspect `box_density_audit.radius_total_norm_correlation` on the newest summaries to test whether norm loss and inward drift actually track each other.
- Keep the current best control branch fixed while adding **operator-resolved budgets** for:
  - `ΔE`
  - `ΔLz`
  - `Δnorm`
  - and, if practical, tangential residual contribution

  broken out by:
  - linear half step
  - nonlinear / confinement step
  - sponge application
  - refill application when enabled

- Treat the current `sponge_only` branch as the baseline control, not as the preferred final reduced physical model.

### Density-locking branch

- Design a **momentum-neutral density-locking refill** rather than uniform per-step reinjection.
- Do not promote another refill branch unless it is explicitly neutral in the quantities that matter most for orbit quality:
  - net linear momentum
  - net angular momentum about the source
  - as much phase / canonical-momentum bias as possible
- Use this branch as a diagnostic A/B test of the “frozen source in a changing medium” concern, not as the new default branch until it proves it is not creating its own torque channel.

### Medium term

- If the secular sink survives the operator budget and a bias-neutral density-locking branch, promote a more self-consistent source protocol.
- Likely next candidate:
  - quasi-self-consistent source response, or
  - a live heavy-source / large-mass-ratio branch

Preference:

- a live heavy-source / large-mass-ratio branch is preferable to clamped or pinned sources once the static-background control has given everything useful it can, because the moving-body wake / response sector is closer to the real conservative pair problem than another frozen-source reduction.

### Decision rule

If the branch still shows:

- negative mean tangential residual,
- substantial energy drift,
- and only weak correlation between bulk density drop and orbital degradation,

then the main problem is probably not simple fluid depletion. It is more likely confinement/source inconsistency or another non-conservative coupling in the reduced orbit protocol.

Operational gate before spending major cloud time on more physical complexity:

- do not spend major cloud time interpreting dressing or source-response effects until the no-dressing Newtonian PDE orbit can shadow the ODE Newtonian baseline for several periods with acceptably small secular `ΔE` and `ΔLz`

## Files most relevant for external review

- latest overnight log:
  - `diagnostic-refine-out.log`
- status overview:
  - `docs/results_journal.md`
  - `docs/run_matrix.md`
- current Newtonian program memo:
  - `docs/newtonian_to_1pn_program.md`
- main experiment entry point:
  - `src/experiments/exp03_pde_newtonian_bound_orbit.py`
- drag and density diagnostics:
  - `src/physics/orbit_diagnostics.py`

## Bottom line

The project appears to have a credible path to a Newtonian orbit result, but the present static-background branch is probably not the final scientific form of that result.

It has already been valuable because it showed:

- the solver can reproduce Newtonian infall
- the defect can remain coherent over orbital windows
- the long-orbit failure is narrowing to a specific secular sink

The most important question now is not “can we keep tuning static backgrounds forever,” but:

- can we build a reduced protocol that preserves constant ambient density and does not inject momentum bias, or
- do we need to move to a more self-consistent source sector to get a decisive Newtonian orbit?
