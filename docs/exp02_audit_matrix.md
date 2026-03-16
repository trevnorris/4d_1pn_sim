# Experiment 2 Audit Matrix

Purpose: turn the static-background orbit work into a staged discriminator rather than a sequence of ad hoc orbit sweeps.

## Current status

- Experiment 1 is kept as a reduced-closure regression only.
- Check A status:
  passed on synthetic oracles.
- Check B status:
  passed after switching the configured background to a pure-Kepler profile.
- Check C status:
  mixed.
  - displaced-rest null test passes cleanly
  - boosted free-translation still shows noticeable COM curvature over the audit window
  - source-present closure-on/off runs remain launch-sensitive and not yet clean-orbit-grade
  - local-main launch calibration now shows a box-safe long-run candidate at `r_p = 16`, while the first speed-reachable point (`r_p = 18`) is boundary-contaminated on the current `40^3` physical box
- After fitter hardening, the current saved Experiment 2 and audit trajectories no longer produce fit-worthy periapsis sets at all.
- Leakage and higher-mode occupation are consistently small.
- The bottleneck is now defect launch / COM control plus orbit-fit robustness, not raw resolution.
- The promoted `r_p = 16` long control completed and failed by inward plunge rather than by marginal periapsis ambiguity.
- The active next control is the wide-box fallback based on `configs/local/exp02_widebox_r18_long.json`.
- A new pre-orbit gate is now active in practice:
  static-background radial infall must show stable fall-rate convergence with increasing `N` before more orbit tuning is worth the wall time.
- That pre-orbit gate has now been met.
  - `64^3` and above reproduce the static `1/r^2` infall law well.
  - `256^3` is the first tested point where the defect is also resolved by about `6.3` cells.
- The active next branch is now a tracer-matched short-arc control at `256^3`, not another small-box perihelion attempt.
- The first `256^3` short-arc control was interrupted by machine swap before completion, but it still established two useful facts:
  - the `256^3` relaxation stage completes and leaves a reusable checkpoint,
  - the launch calibration on the chosen `r_p = 12`, `e = 0.05` control is clean and target-reachable.
- The rerun from the saved relaxed checkpoint now completed successfully for `source_no_dressing` and passed every short-arc acceptance gate.
- The immediate next discriminator is therefore the matched `source_with_dressing` short arc on the same restart path.

## Decision rule

Do not treat any field-derived `beta_eff` as physically meaningful until Checks A-C pass.

If Checks A-C pass and Check D still gives a stable wrong-sign or near-zero self-sector signal, treat that as serious evidence against the current reduced static self-sector implementation.

If Checks A-D pass but static-background orbit still fails while free-heavy later succeeds, pivot interpretation toward mutual-motion / wake channels rather than the advertised static self sector.

## Check A: Orbit fitter oracle audit

Objective:

- Verify the periapsis extractor and `beta_eff` fitter recover the correct sign and approximate magnitude on synthetic trajectories with known answers.

Runs:

1. Newtonian oracle (`beta = 0`)
2. Positive-precession oracle (`beta = +3`)
3. Negative-precession oracle (`beta < 0`)

Pass gates:

- Newtonian oracle returns `|beta_eff| < 0.2`
- Positive oracle returns `beta_eff` within `15%` of target and correct sign
- Negative oracle returns `beta_eff` within `15%` of target magnitude and correct sign
- Fitter uncertainty stays smaller than `25%` of the recovered `Delta phi`

Fail interpretation:

- Any sign error or gross magnitude bias means field-derived `beta_eff` is not interpretable yet.

## Check B: Imposed-background point-particle audit

Objective:

- Determine what apsidal drift the imposed static background plus numerical integrator produces before any defect/internal dynamics are added.

Runs:

1. Point tracer in the current softened background
2. Point tracer in a pure `-mu/r` background over the same orbital annulus
3. Radial-force sampling over the annulus used by the defect orbit

Pass gates:

- Pure `-mu/r` tracer gives `|beta_eff| < 0.2`
- Current imposed background gives `|beta_eff| < 0.5`
- Sampled radial force fits `-mu/r^2` with correction amplitude small compared to the leading term over the fit annulus

Fail interpretation:

- If the background-only tracer already produces retrograde or large spurious precession, the defect run is not isolating self-sector physics.

## Check C: COM/null-force audit

Objective:

- Verify internal confinement and reduced geometry handling decouple cleanly from center-of-mass motion.

Runs:

1. No-source free translation
2. No-source trap-only translated defect
3. Source-present with self-dressing response disabled or frozen

Pass gates:

- Free translation keeps COM velocity drift below `5%` over the audit window
- Null-force orbit fitter gives `|beta_eff| < 0.2` in all three runs
- Shape/coherence remains high enough that the audit is not dominated by defect breakup

Fail interpretation:

- Any nonzero fitted precession or systematic COM drift indicates protocol contamination from confinement, projection, or geometry handling.

## Check D: Direct self-sector measurement

Objective:

- Measure the local self-sector response directly rather than only through perihelion fits.

Runs:

1. Slowly varying static-background sweep for effective COM inertia / kinetic prefactor
2. Compare measured local response against the target sign expected from the static self sector

Pass gates:

- Measured effective self-sector correction is positive over the orbital annulus
- Response is smooth in radius and consistent in sign across nearby operating points

Fail interpretation:

- Near-zero or negative local self-sector response makes a failed orbit test unsurprising and localizes the issue to the implemented self-dressing dynamics.

## Check E: Clean-orbit acceptance gate

Objective:

- Decide when a field-derived static-background orbit result is strong enough to interpret physically.

Required gates:

- at least `4` clean periapses in the fit window
- mean fit coherence `>= 0.8`
- mean fit higher-mode fraction `<= 0.01`
- mean fit leakage `<= 1e-6`
- fit-window choice does not flip the sign of `beta_eff`

Interpretation:

- Only after this gate passes should a nonzero `beta_eff` be treated as evidence for or against the static self-sector claim.

## Check F: Tracer-matched short-arc gate

Objective:

- Verify that a resolved defect can follow the matched point-particle control over a finite orbital arc before attempting a multi-periapsis fit.

Runs:

1. `256^3` pure-Kepler `source_no_dressing` short arc
2. matched `256^3` pure-Kepler `source_with_dressing` short arc after the control is acceptable

Pass gates:

- defect angular sweep at least `1.0` radian over the comparison window
- angular-sweep mismatch `<= 0.12` radians
- normalized position RMS `<= 0.08`
- normalized radius RMS `<= 0.04`
- phase RMS `<= 0.08`
- boundary clearance `>= 8.0`
- mean coherence `>= 0.995`
- mean higher-mode fraction `<= 0.01`
- mean leakage `<= 1e-6`

Fail interpretation:

- If the `no_dressing` control already fails, the remaining bottleneck is still defect launch / finite-size / COM handling rather than any claimed self-sector correction.
- Only if the control passes and the dressed run then departs systematically is there a clean target for later precession fitting.
- If the control cannot even be completed without swap collapse, the remaining bottleneck is operational:
  the `256^3` branch needs checkpoint reuse and/or lighter restart paths before it can serve as a practical overnight discriminator on this machine.

Current status:

- `source_no_dressing` at `256^3`: pass
- `source_with_dressing` at `256^3`: pass
- Differential signal over the matched short arc:
  very small
  - angular-sweep shift `~ -9.3e-05`
  - normalized position-RMS shift `~ +6.2e-05`
  - phase-RMS shift `~ +5.0e-05`
  - coherence / leakage / higher-mode changes all negligible at the current gate level

Interpretation:

- The short-arc gate is now passed for both branches.
- The dressed and undressed trajectories are nearly indistinguishable over this window.
- That localizes the next scientific question:
  either the implemented static dressing effect is genuinely tiny on short arcs, or the relevant signal only emerges after longer accumulation.

## Recommended order

1. Check A
2. Check B
3. Check C
4. Check D
5. Check F
6. Return to static-background orbit fits with Check E enforced

## Current best evidence before audit completion

- Reduced closure emulator: passes as a regression target.
- Static-background orbit claim: unresolved and still fitter-limited.
- Reason:
  low leakage and low mode contamination persist across many runs, but the hardened fitter no longer accepts the current trajectories as having enough well-separated periapses. The launch sweep and the completed `r_p = 16` long control now show why: on the current `40^3` physical box, the box-safe launches are still sub-target enough to fall inward, while the first speed-reachable launches sit too close to the periodic boundary. The next physically meaningful branch is therefore the wider box, not more tuning on the current domain.
  The first two radial-infall sweep points sharpen that further: `40^3` is underresolved and falls too fast, while `64^3` already matches the static infall oracle within about `3%`. So static-force diagnostics converge much earlier than orbit-quality runs, and orbit tuning should wait for the higher-resolution infall points before more wall time is spent there.
  Run 016 now completed that convergence argument: the static infall law is stable from `64^3` upward, and `256^3` is the first tested point with roughly `6` cells across the defect core. The current active discriminator is therefore the `256^3` tracer-matched short-arc gate rather than any immediate return to perihelion fitting.
