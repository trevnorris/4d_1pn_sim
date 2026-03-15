# Results Journal

Chronological run log for the 4D toy-model implementation work.

## 2026-03-14

### Run 001: Experiment 1 debug closure

- Command:
  `python -m src.experiments.exp01_single_defect_response --config configs/local/exp01_debug.json`
- Summary command:
  `python -m src.scripts.summarize_run --run-dir outputs/runs/exp01_debug`
- Output directory:
  `outputs/runs/exp01_debug`

Key results:

- `kappa_PV_estimate = 1.4989330937578393`
- `d ln a / d ln rho = -0.8910738793457988`
- mean drive coherence `= 0.9995930320024491`
- mean drive higher-mode fraction `= 0.002863130954792723`
- mean drive leakage `= 1.1358112253669895e-06`
- partition fraction error:
  - `E_w = +0.000593`
  - `E_f = -0.000474`
  - `E_PV = -0.000119`

Interpretation:

- The reduced matter plus adiabatic-geometry prototype is internally consistent with the declared closure target on the debug run.
- This supports the reduced closure implementation only.
- This does not validate the full PDE closure claim independently because `a(t)` is still imposed by the adiabatic one-DOF closure model.

Open issues recorded at this point:

- No static-background orbit test yet.
- No free-heavy or clamped protocol comparison yet.
- No Maxwell / KK / mixed-sector implementation yet.

### Run 002: Experiment 2 debug static-background orbit

- Command:
  `python -m src.experiments.exp02_orbit_static_background --config configs/local/exp02_debug.json`
- Summary command:
  `python -m src.scripts.summarize_run --run-dir outputs/runs/exp02_debug`
- Output directory:
  `outputs/runs/exp02_debug`

Key results:

- `Delta phi = -0.3093101158318738`
- `beta_eff = -3.905592352468138`
- mean fit coherence `= 0.5518389574544771`
- mean fit higher-mode fraction `= 0.002706226840715057`
- mean fit leakage `= 1.2129734513096782e-07`
- fitted orbit shape:
  - semi-major axis `= 1.0390987321633502`
  - eccentricity `= 0.45241026407897555`

Interpretation:

- The first imposed-static debug orbit does not support the target `beta_1PN = 3`.
- Leakage and higher-mode occupation are small, so the miss is not being driven by obvious leakage or strong mode contamination.
- Coherence is only moderate, so the current orbit window is not yet a clean compact-defect regime.
- The next action is to retune the static-background setup toward a larger, less deformed, more slowly varying orbit and rerun.

Current status after Run 002:

- Experiment 2 is implemented and produces a fittable orbit summary.
- The first debug run is a negative result for the target claim, but not yet a decisive falsification because the compactness/coherence window is not clean enough.

### Run 003: Experiment 2 tuning sweep

- Commands:
  - internal probe sweep over `exp02_probe_base`, `exp02_probe_wider`, `exp02_probe_faster`, `exp02_probe_deeper`
  - internal long probes `exp02_probe_wider_long`, `exp02_probe_wider_stiff`
- Output directories:
  - `outputs/runs/exp02_probe_base`
  - `outputs/runs/exp02_probe_wider`
  - `outputs/runs/exp02_probe_faster`
  - `outputs/runs/exp02_probe_deeper`
  - `outputs/runs/exp02_probe_wider_long`
  - `outputs/runs/exp02_probe_wider_stiff`

Selected probe results:

- `exp02_probe_base`
  - `beta_eff = -2.6550869874168392`
  - mean fit coherence `= 0.5664421779626891`
  - mean fit higher-mode fraction `= 0.0027959888431221425`
  - mean fit leakage `= 1.212664020615912e-07`
- `exp02_probe_wider`
  - orbit fit failed with `Need at least three periapses to fit precession`
  - mean fit coherence `= 0.6220016413104945`
- `exp02_probe_faster`
  - orbit fit failed with `Need at least three periapses to fit precession`
  - mean fit coherence `= 0.5694347143687051`
- `exp02_probe_deeper`
  - orbit fit failed with `Need at least three periapses to fit precession`
  - mean fit coherence `= 0.45498493683235397`
- `exp02_probe_wider_long`
  - `beta_eff = -6.7561451402197825`
  - mean fit coherence `= 0.7049727736016115`
  - mean fit higher-mode fraction `= 0.0027467674298289543`
  - mean fit leakage `= 1.2312227019221447e-07`
- `exp02_probe_wider_stiff`
  - `beta_eff = -6.359349794832839`
  - mean fit coherence `= 0.8372689272041122`
  - mean fit higher-mode fraction `= 0.005158318135305308`
  - mean fit leakage `= 1.5514303382631785e-07`

Interpretation:

- Enlarging the orbit and stiffening the internal confinement improves shape stability and coherence.
- The sign and magnitude of `beta_eff` remain wrong even in the best-tuned probe.
- This pushes the current evidence toward a structural miss in the present reduced static-background implementation rather than a simple bad-initialization problem.

### Run 004: Experiment 2 debug rerun with promoted wider/stiffer setup

- Command:
  `python -m src.experiments.exp02_orbit_static_background --config configs/local/exp02_debug.json`
- Summary command:
  `python -m src.scripts.summarize_run --run-dir outputs/runs/exp02_debug`
- Output directory:
  `outputs/runs/exp02_debug`

Config changes relative to Run 002:

- increased `trap_strength_r` from `0.8` to `1.4`
- increased `trap_strength_w` from `0.6` to `0.9`
- increased periapsis radius from `2.8` to `4.0`
- increased orbit window from `3200` to `6400` steps
- tightened periapsis smoothing / spacing gates

Key results:

- `Delta phi = -0.21962773866839702`
- `beta_eff = -6.359349794832839`
- mean fit coherence `= 0.8372689272041122`
- mean fit higher-mode fraction `= 0.005158318135305308`
- mean fit leakage `= 1.5514303382631785e-07`
- fitted orbit shape:
  - semi-major axis `= 2.024087615945256`
  - eccentricity `= 0.2524320292538663`

Interpretation:

- This is the cleanest static-background orbit window obtained so far.
- Compactness/coherence improved substantially compared with Run 002.
- Even in this cleaner window, `beta_eff` remains strongly negative and far from the target `beta_1PN = 3`.
- The current reduced matter-plus-geometry static-background implementation therefore still does not support the claimed self-sector orbit mechanism.

### Run 005: Experiment 2 local-main refined run

- Command:
  `python -m src.experiments.exp02_orbit_static_background --config configs/local/exp02_local_main.json`
- Summary command:
  `python -m src.scripts.summarize_run --run-dir outputs/runs/exp02_local_main`
- Output directory:
  `outputs/runs/exp02_local_main`

Key results:

- orbit fit failed with `Need at least three periapses to fit precession`
- mean fit coherence `= 0.8278492864788998`
- mean fit higher-mode fraction `= 0.005077195218403913`
- mean fit leakage `= 6.341739450677593e-08`
- mean fit compactness proxy `= 2.3006847696361086`

Trajectory note:

- with the current turning-point gates, the saved trajectory shows only one clean periapsis over the full run window
- this means the local-main configuration did not produce a repeatable enough elliptical sequence for `Delta phi` / `beta_eff` extraction

Interpretation:

- The larger run preserves low leakage and modest mode contamination, and it keeps the defect more coherent than the earliest debug orbit.
- Even so, it still does not produce a usable multi-periapsis orbit fit.
- At this point the bottleneck is the orbit protocol itself, not just resolution.
- Next action: retune the bound-orbit initialization to recover a clean repeating orbit before deciding whether the static-background self-sector failure is fully decisive.

### Run 006: Experiment 2 local-main probe, tighter and slower orbit

- Internal probe output directory:
  `outputs/runs/exp02_local_probe_tighter`

Probe parameters relative to `exp02_local_main`:

- periapsis radius reduced from `4.0` to `3.2`
- velocity scale reduced from `1.0` to `0.92`
- orbit steps reduced to `7000`
- turning-point minimum spacing reduced from `420` to `320`

Key results:

- `Delta phi = -0.07117845438451978`
- `beta_eff = -1.315475699786571`
- mean fit coherence `= 0.7415797395281719`
- mean fit higher-mode fraction `= 0.005066058418297237`
- mean fit leakage `= 5.660997398714049e-08`
- fitted orbit shape:
  - semi-major axis `= 1.2684667498516844`
  - eccentricity `= 0.2154189155026232`

Interpretation:

- This is the first larger-grid orbit probe that produced a repeatable enough periapsis sequence for fitting.
- The result is less pathological than the tuned debug run in the sense that `beta_eff` moved from about `-6.36` to about `-1.32`.
- The sign is still wrong, and it remains far from the target `beta_1PN = 3`.
- Leakage remains very small, so the miss still does not look like a leakage-driven artifact.

### Run 007: Static-background point-particle audit

- Commands:
  - `python -m src.scripts.audit_static_background --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_exp02_debug_configured --mode configured`
  - `python -m src.scripts.audit_static_background --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_exp02_debug_pure_kepler --mode pure_kepler`

Outputs:

- `outputs/runs/audit_exp02_debug_configured`
- `outputs/runs/audit_exp02_debug_pure_kepler`

Key results:

- configured softened background:
  - `beta_eff = -10.545928`
  - `Delta phi = -0.146440`
- pure Kepler tracer:
  - `beta_eff = -0.001847`
  - `Delta phi = -0.000026`

Additional larger-orbit tracer checks:

- tighter/slower local-main probe surrogate:
  - point-tracer `beta_eff = -14.308991393907913`
- mid local-main probe surrogate:
  - point-tracer `beta_eff = -12.918078274694201`

Interpretation:

- The imposed softened static background by itself produces strong retrograde precession.
- The pure `-mu/r` tracer is essentially clean, so the orbit fitter/integrator is not the source of the sign problem in isolation.
- This means the current imposed background protocol is a major contaminant.
- Therefore the earlier negative `beta_eff` defect runs cannot be interpreted as clean falsifications of the static self sector.
- The positive `beta_eff` seen in the larger-grid `exp02_local_probe_mid` field run now looks more like partial cancellation of a background-induced retrograde drift than direct confirmation of the target `beta = 3`.

### Run 008: Experiment 2 debug rerun after switching to pure Kepler background

- Command:
  `python -m src.experiments.exp02_orbit_static_background --config configs/local/exp02_debug.json`
- Summary command:
  `python -m src.scripts.summarize_run --run-dir outputs/runs/exp02_debug`
- Background audit commands:
  - `python -m src.scripts.audit_static_background --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_exp02_debug_configured --mode configured`
  - `python -m src.scripts.audit_static_background --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_exp02_debug_pure_kepler --mode pure_kepler`

Key results:

- configured point-tracer background:
  - `beta_eff = -0.001847`
  - `Delta phi = -0.000026`
- pure Kepler control:
  - `beta_eff = -0.001847`
  - `Delta phi = -0.000026`
- defect orbit run:
  - orbit fit failed with `Need at least three periapses to fit precession`
  - mean fit coherence `= 0.7020526365811626`
  - mean fit higher-mode fraction `= 0.005029659640043974`
  - mean fit leakage `= 1.2169316518662044e-07`
  - final snapshot coherence `= 0.9661717414855957`
  - final snapshot `kappa_PV = 1.5024799944486666`
  - final snapshot `d ln a / d ln rho = -0.88944614708745`

Interpretation:

- The background protocol itself is now clean at the point-particle level.
- The default debug defect orbit still does not produce a fit-ready multi-periapsis window under that clean background.
- That shifts the bottleneck away from the background profile and toward defect COM dynamics or orbit initialization in the field solver.
- The next action is a direct COM/null-force audit of the defect solver.

### Run 009: Defect COM and null-force audit

- Commands:
  - `python -m src.scripts.audit_defect_com --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_defect_displaced_rest --scenario displaced_rest --steps 1600`
  - `python -m src.scripts.audit_defect_com --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_defect_free_translation --scenario free_translation --steps 1600`
  - `python -m src.scripts.audit_defect_com --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_defect_source_no_dressing --scenario source_no_dressing --steps 4000`
  - `python -m src.scripts.audit_defect_com --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_defect_source_with_dressing --scenario source_with_dressing --steps 4000`

Key results:

- displaced rest:
  - ballistic RMS `= 3.2258534482994613e-06`
  - fitted acceleration norm `= 5.702785701456793e-09`
  - mean coherence `= 0.9999864444136619`
- free translation:
  - after reducing the probe speed to avoid periodic wrapping, ballistic RMS `= 0.15927468091834318`
  - fitted acceleration norm `= 7.456127739084751e-04`
  - mean coherence `= 0.9998111294209957`
- source present, no dressing:
  - orbit fit still failed at `4000` steps
  - ballistic RMS `= 0.5397085166256019`
  - fitted acceleration norm `= 0.0013576777264963972`
  - mean coherence `= 0.6988283161032531`
- source present, with dressing:
  - orbit fit still failed at `4000` steps
  - ballistic RMS `= 0.4836900233270701`
  - fitted acceleration norm `= 0.000690497683497452`
  - mean coherence `= 0.6854087783065107`

Interpretation:

- A displaced defect at rest stays put to machine precision, so the co-moving confinement is not simply pinning the COM back to the origin.
- A boosted defect in nominally force-free motion still develops noticeable COM curvature over the audit window.
- The source-present cases therefore remain contaminated by launch / COM-response issues even after the background profile itself was cleaned up.
- The next action is launch calibration with longer no-dressing runs before attributing any perihelion signal to self-dressing.

### Run 010: No-dressing launch calibration sweep, long runs

- Commands:
  - `python -m src.scripts.audit_defect_com --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_defect_source_no_dressing_v125 --scenario source_no_dressing --steps 9000 --velocity-scale 1.25`
  - `python -m src.scripts.audit_defect_com --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_defect_source_no_dressing_v140 --scenario source_no_dressing --steps 9000 --velocity-scale 1.4`
  - `python -m src.scripts.audit_defect_com --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_defect_source_no_dressing_v155 --scenario source_no_dressing --steps 9000 --velocity-scale 1.55`

Key results:

- `vscale = 1.25`
  - orbit fit failed with `Need at least three periapses to fit precession`
  - mean coherence `= 0.828844839909742`
  - mean higher-mode fraction `= 0.005116807230407112`
  - mean leakage `= 1.4082769923591823e-07`
- `vscale = 1.40`
  - loose-gate fit gave `beta_eff = 0.17129309959275577`
  - `Delta phi = 0.0066931655812931985`
  - mean coherence `= 0.6995243121978155`
  - mean higher-mode fraction `= 0.005174118793802336`
  - mean leakage `= 1.4858432713610443e-07`
- `vscale = 1.55`
  - loose-gate fit gave `beta_eff = 0.6128528623256899`
  - `Delta phi = 0.023784707934109493`
  - mean coherence `= 0.7263204965411231`
  - mean higher-mode fraction `= 0.005207573611067261`
  - mean leakage `= 1.4916031108222417e-07`

Post-processing note:

- Re-running the saved trajectories with stricter periapsis spacing gates (`min_spacing >= 500`) removes these fits entirely.
- So these positive `beta_eff` values are not yet robust evidence; they depend on the current loose turning-point detector.

Interpretation:

- Longer no-dressing runs can be made fittable with stronger launches.
- The defect can therefore execute at least a marginally repeatable source-driven orbit under the clean background.
- But the current orbit fitter is still too permissive, and the sign / magnitude extracted from these runs is not yet stable under stricter periapsis gating.

### Run 011: Matched with-dressing comparison at `vscale = 1.55`

- Command:
  `python -m src.scripts.audit_defect_com --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_defect_source_with_dressing_v155 --scenario source_with_dressing --steps 9000 --velocity-scale 1.55`

Key results:

- loose-gate fit gave `beta_eff = -2.3021411183556237`
- `Delta phi = -0.09463516094185148`
- mean coherence `= 0.691257973316797`
- mean higher-mode fraction `= 0.0052698722082395975`
- mean leakage `= 1.4441119641584157e-07`

Post-processing note:

- Re-running the saved trajectory with stricter periapsis spacing gates (`min_spacing >= 500`) removes the fit entirely.

Interpretation:

- At matched launch conditions, turning the closure on changes the loose-gate orbit fit substantially.
- But that sign change is not yet robust, because the fit disappears once spurious closely spaced turning points are rejected.
- The correct next step is a still longer matched pair, not a scientific claim.

### Run 012: Matched very-long pair at `vscale = 1.55`

- Commands:
  - `python -m src.scripts.audit_defect_com --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_defect_source_no_dressing_v155_long --scenario source_no_dressing --steps 18000 --velocity-scale 1.55`
  - `python -m src.scripts.audit_defect_com --config configs/local/exp02_debug.json --output-dir outputs/runs/audit_defect_source_with_dressing_v155_long --scenario source_with_dressing --steps 18000 --velocity-scale 1.55`

Key results:

- no dressing:
  - loose-gate fit gave `beta_eff = -1.3900147056197938`
  - `Delta phi = -0.06121898594026229`
  - mean coherence `= 0.7990987209129062`
  - mean higher-mode fraction `= 0.005173120335953585`
  - mean leakage `= 1.4708067008146147e-07`
- with dressing:
  - loose-gate fit gave `beta_eff = -0.9362285634675853`
  - `Delta phi = -0.040343906519781376`
  - mean coherence `= 0.7866076663898474`
  - mean higher-mode fraction `= 0.005246305871683448`
  - mean leakage `= 1.4348982160986265e-07`

Post-processing note:

- With stricter periapsis spacing (`min_spacing >= 500`), both fits again disappear.
- The saved long trajectories only provide two clearly separated periapsis candidates; the additional turning points come in short clusters and are not trustworthy.

Interpretation:

- The longer matched pair improves coherence and reduces ambiguity from short transients.
- Even so, the current protocol still does not yield three widely separated periapses under a physically defensible gate.
- The state of the project is now clearer:
  - the background protocol is fixed,
  - the defect launch / COM response is only partially controlled,
  - and the current Experiment 2 perihelion extraction is still fitter-limited rather than evidence-limited.
