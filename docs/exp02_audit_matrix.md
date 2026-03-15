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
- Experiment 2 currently still has mixed-sign loose-gate `beta_eff` results, but those signs are not robust under stricter periapsis spacing gates.
- Leakage and higher-mode occupation are consistently small.
- The bottleneck is now defect launch / COM control plus orbit-fit robustness, not raw resolution.

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

## Recommended order

1. Check A
2. Check B
3. Check C
4. Check D
5. Return to static-background orbit fits with Check E enforced

## Current best evidence before audit completion

- Reduced closure emulator: passes as a regression target.
- Static-background orbit claim: unresolved and still fitter-limited.
- Reason:
  low leakage and low mode contamination persist across many runs, but `beta_eff` is unstable in sign and magnitude under launch choice, runtime, and periapsis-gating choices. That is still the regime where audit failures can masquerade as physics.
