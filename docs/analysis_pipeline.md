# Analysis Pipeline

This note defines the orbit-analysis path used by the current ODE and PDE work.

## 1. Trajectory source

### ODE reference

- Positions and velocities come directly from the point-particle integrator.

### PDE orbit work

- The primary trajectory is the defect center estimate from the evolving field state.
- In the current short-arc branch, the center is estimated from the effective spatial density used by the solver.

## 2. Velocity handling

- If a trajectory already has velocities, they are used directly.
- If velocities are absent, the shared diagnostics can estimate them by finite differences in time.

## 3. Periapsis detection

Periapses are extracted with the fitter in `src/physics/fitting.py`.

The current logic is:

1. form planar radius `r(t)` from `(x(t), y(t))`
2. optionally smooth `r(t)` with a moving average
3. estimate a characteristic period from the radius spectrum
4. impose a minimum turning-point spacing based on a fraction of that period
5. require local prominence to reject shallow or clustered false extrema
6. keep only a stable suffix of well-separated periapses before fitting

This is meant to reduce false turning points and avoid over-interpreting noisy orbit windows.

## 4. Orbit-shape extraction

Given the accepted periapses and apoapses:

- periapsis radius is the median accepted minimum radius
- apoapsis radius is the median accepted maximum radius
- semimajor axis is `(r_peri + r_apo) / 2`
- eccentricity is `(r_apo - r_peri) / (r_apo + r_peri)`

## 5. Precession fit

- periapsis angles are unwrapped
- the angle is fit as a linear function of orbit index
- the slope is the extracted phase increment / `delta_phi`
- `beta_eff` is then computed from the standard reduced formula currently used in the repo

## 6. Conservation summaries

The shared orbit diagnostics now summarize:

- orbital-energy drift
- angular-momentum-z drift

Each drift summary reports:

- initial value
- mean / min / max
- maximum absolute drift
- RMS drift
- maximum relative drift
- RMS relative drift

For ODE runs, these use the exact integrator velocities.
For PDE runs, later branches may use finite-difference COM velocities or a more specialized conserved-quantity diagnostic, depending on the experiment.

## 7. Short-arc acceptance

The current tracer-matched short-arc gate uses:

- angular sweep
- angular-sweep mismatch
- normalized position RMS
- normalized radius RMS
- phase RMS
- boundary clearance
- coherence
- higher-mode fraction
- leakage

Passing the short-arc gate means the run is operationally clean enough to justify longer-window orbit work.

## 8. Interpretation rule

- A clean short arc does not yet prove a clean long orbit.
- A correct radial fall law does not yet prove a clean Newtonian orbit.
- A nonzero 1PN-looking signal does not count unless it survives the Newtonian gate, the ODE references, and the declared diagnostics.
