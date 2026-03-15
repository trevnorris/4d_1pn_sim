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

### Run 013: Periapsis fitter hardening and reclassification of saved orbit runs

- Code changes:
  - period-aware turning-point spacing in [src/physics/fitting.py](/projects/4d_1pn_sim/src/physics/fitting.py)
  - prominence gating for periapsis / apoapsis candidates in [src/physics/fitting.py](/projects/4d_1pn_sim/src/physics/fitting.py)
  - stable-suffix selection for late-window fitting in [src/physics/fitting.py](/projects/4d_1pn_sim/src/physics/fitting.py)
  - orbit-summary debug fields in [src/physics/diagnostics.py](/projects/4d_1pn_sim/src/physics/diagnostics.py)
- Test commands:
  - `pytest -q tests/test_orbit_fitter.py tests/test_orbit_oracles.py`
  - `pytest -q`

Key results:

- all fitter/oracle tests pass after the hardening changes
- previously ambiguous saved runs now all fail cleanly under the hardened fitter:
  - `outputs/runs/exp02_debug`
  - `outputs/runs/audit_defect_source_no_dressing_v155`
  - `outputs/runs/audit_defect_source_with_dressing_v155`
  - `outputs/runs/audit_defect_source_no_dressing_v155_long`
  - `outputs/runs/audit_defect_source_with_dressing_v155_long`
- common failure mode:
  - `Need at least three periapses to fit precession`

Interpretation:

- This is an improvement, not a regression.
- The old fitter was willing to assign a sign from clustered or weak turning points.
- The hardened fitter now classifies the current Experiment 2 archive honestly: there is not yet a fit-worthy static-background orbit window.
- That means the next runtime spend should go into obtaining trajectories that survive the stricter gates, not into interpreting loose-fit `beta_eff` values.

### Run 014: Local-main launch-calibration sweep to larger periapsis radii

- Commands:
  - `env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m src.scripts.calibrate_defect_launch --config configs/local/exp02_local_main.json --output-dir outputs/runs/calibrate_exp02_local_main`
  - `env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m src.scripts.calibrate_defect_launch --config configs/local/exp02_local_main.json --output-dir outputs/runs/calibrate_local_main_r8 --periapsis-radius 8`
  - `env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m src.scripts.calibrate_defect_launch --config configs/local/exp02_local_main.json --output-dir outputs/runs/calibrate_local_main_r10 --periapsis-radius 10`
  - `env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m src.scripts.calibrate_defect_launch --config configs/local/exp02_local_main.json --output-dir outputs/runs/calibrate_local_main_r12 --periapsis-radius 12`
  - `env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m src.scripts.calibrate_defect_launch --config configs/local/exp02_local_main.json --output-dir outputs/runs/calibrate_local_main_r14 --periapsis-radius 14`
  - `env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m src.scripts.calibrate_defect_launch --config configs/local/exp02_local_main.json --output-dir outputs/runs/calibrate_local_main_r16 --periapsis-radius 16`
  - `env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m src.scripts.calibrate_defect_launch --config configs/local/exp02_local_main.json --output-dir outputs/runs/calibrate_local_main_r17 --periapsis-radius 17`
  - `env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m src.scripts.calibrate_defect_launch --config configs/local/exp02_local_main.json --output-dir outputs/runs/calibrate_local_main_r18 --periapsis-radius 18`
- Output directories:
  - `outputs/runs/calibrate_exp02_local_main`
  - `outputs/runs/calibrate_local_main_r8`
  - `outputs/runs/calibrate_local_main_r10`
  - `outputs/runs/calibrate_local_main_r12`
  - `outputs/runs/calibrate_local_main_r14`
  - `outputs/runs/calibrate_local_main_r16`
  - `outputs/runs/calibrate_local_main_r17`
  - `outputs/runs/calibrate_local_main_r18`

Selected results:

- baseline `r_p = 4`
  - target speed `= 1.3133925536563698`
  - realized tangential speed `= 0.8269290529284465`
  - `target_reachable = false`
- `r_p = 14`
  - target speed `= 0.7020378500174638`
  - realized tangential speed `= 0.6686798667896335`
  - `target_reachable = false`
- `r_p = 16`
  - target speed `= 0.6566962768281849`
  - recommended applied speed `= 0.7552007183524125`
  - realized tangential speed `= 0.633203377402792`
  - mean radius over the measurement window `= 16.002291872447817`
  - mean radial speed `= 0.017366868887643584`
  - estimated steps per orbit `= 13965.75984099152`
  - `target_reachable = false`
- `r_p = 17`
  - target speed `= 0.6370889678382262`
  - recommended applied speed `= 0.73265231301396`
  - realized tangential speed `= 0.6196096757402263`
  - mean radius over the measurement window `= 16.929276690245146`
  - mean radial speed `= -0.038246520241977826`
  - estimated steps per orbit `= 15295.299225454604`
  - `target_reachable = false`
- `r_p = 18`
  - target speed `= 0.6191391873668903`
  - recommended applied speed `= 0.7120100654719238`
  - realized tangential speed `= 0.6211452541510699`
  - mean radius over the measurement window `= 17.31639465492783`
  - mean radial speed `= -0.46589301605375333`
  - estimated steps per orbit `= 16664.540885979517`
  - `target_reachable = true`

Interpretation:

- The local-main launch response saturates well below the point-particle target at small radius, so the original `r_p = 4` configuration cannot produce a clean Experiment 2 orbit.
- The first speed-reachable point is around `r_p = 18`, but that operating point is already too close to the periodic box edge to trust:
  - the measured mean radius collapses from `18` to about `17.32`,
  - and the mean radial drift becomes large and negative over the short calibration window.
- `r_p = 16` is the best current compromise on the existing `40^3` physical box:
  - it stays centered at the requested radius,
  - keeps radial drift small,
  - and remains only about `3.6%` below the target tangential speed.
- A dedicated long-run config has therefore been promoted at `configs/local/exp02_local_r16_long.json`.
- The next decisive runtime spend is a long `source_no_dressing` control at `r_p = 16`, followed by the dressed Experiment 2 run only if the no-dressing orbit survives the hardened periapsis gate.

### Run 015: Long no-dressing control at `r_p = 16` on the local-main box

- Command:
  `env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m src.scripts.audit_defect_com --config configs/local/exp02_local_r16_long.json --output-dir outputs/runs/audit_defect_source_no_dressing_r16_long --scenario source_no_dressing --steps 60000 --velocity-scale 1.15`
- Output directory:
  `outputs/runs/audit_defect_source_no_dressing_r16_long`

Key results:

- orbit fit failed with `Need at least three periapses to fit precession`
- ballistic RMS `= 2.6347205851957787`
- fitted acceleration norm `= 7.105515381330618e-05`
- mean coherence `= 0.9447685149591416`
- mean higher-mode fraction `= 0.004954518637561705`
- mean leakage `= 8.236142197298735e-08`
- initial tangential speed `= 0.7552007183524125`
- source-radius history:
  - initial radius `= 15.993029226414462`
  - final radius `= 1.4931112086467004`
  - minimum radius `= 1.1361980692033382`
  - maximum radius `= 16.115638275959583`
  - detected periapses `= 0`
  - detected apoapses `= 1`

Interpretation:

- This is not a near-miss orbit and not a fitter artifact.
- The defect plunges inward from the intended `r_p = 16` launch radius to a tight `r ~ 1.5` state without ever forming a repeatable periapsis sequence.
- The clean coherence, leakage, and higher-mode metrics mean the failure is orbital rather than defect-breakup-driven.
- In practical terms, the current `40^3` physical box still cannot realize a correct large-radius periapsis launch for Experiment 2:
  - the box-safe `r_p = 16` point remains sub-target in realized tangential speed,
  - and that shortfall is enough to miss the intended orbit entirely.
- This closes the small-box branch for now.
- The correct next step is the prepared wide-box fallback at `48^3` cells over a `60^3` physical domain, centered on the first speed-reachable radius near `r_p = 18`.

### Run 016: Static-background radial infall resolution sweep on CPU

- Command:
  `python -m src.scripts.sweep_static_infall_resolution --config configs/local/infall_resolution_sweep_cpu.json`
- Output directory:
  `outputs/runs/infall_resolution_sweep_cpu`
- Current status:
  in progress

Purpose:

- Replace orbit-first tuning with a cheaper static-background radial-infall convergence study.
- Sweep `N = 40, 64, 96, 128, 256` on a fixed `48^3` physical domain.
- Use the `source_no_dressing` branch first to determine how many cells are needed before the COM fall rate itself is numerically reliable.

Completed points so far:

- `N = 40`
  - `dx = 1.2`
  - intrinsic initial compactness `= 1.2955085039138794`
  - intrinsic compactness in cells `= 1.079590419928233`
  - `r0 / Rg = 12.338848087874714`
  - initial radial-acceleration ratio to Newtonian oracle `= 2.3766770303121705`
  - `t(0.75 r0) / t_oracle = 0.8022615911479354`
  - `t(0.50 r0)` not reached within the `2200`-step window
  - pre-target coherence `= 0.9943825293671001`
  - pre-target higher-mode fraction `= 0.004742469989736988`
  - pre-target leakage `= 2.9102908958868315e-08`
- `N = 64`
  - `dx = 0.75`
  - intrinsic initial compactness `= 1.1854418516159058`
  - intrinsic compactness in cells `= 1.5805891354878743`
  - `r0 / Rg = 13.497077041941004`
  - initial radial-acceleration ratio to Newtonian oracle `= 0.995479263257565`
  - `t(0.75 r0) / t_oracle = 1.024586264857558`
  - `t(0.50 r0) / t_oracle = 1.030389168167338`
  - pre-target coherence `= 0.9999985741633995`
  - pre-target higher-mode fraction `= 0.0048731213627273545`
  - pre-target leakage `= 2.9393178276139396e-08`
- `N = 96`
  - `dx = 0.5`
  - intrinsic initial compactness `= 1.1853885650634766`
  - intrinsic compactness in cells `= 2.370777130126953`
  - `r0 / Rg = 13.497688600691667`
  - initial radial-acceleration ratio to Newtonian oracle `= 0.9971278091851951`
  - `t(0.75 r0) / t_oracle = 1.0243053129570847`
  - `t(0.50 r0) / t_oracle = 1.0301781111499861`
  - pre-target coherence `= 0.99999873035894`
  - pre-target higher-mode fraction `= 0.004872948713435041`
  - pre-target leakage `= 2.9408555607089695e-08`
- `N = 128`
  - `dx = 0.375`
  - intrinsic initial compactness `= 1.1853886842727661`
  - intrinsic compactness in cells `= 3.161036491394043`
  - `r0 / Rg = 13.497690461391239`
  - initial radial-acceleration ratio to Newtonian oracle `= 0.9968174353332463`
  - `t(0.75 r0) / t_oracle = 1.024319524557313`
  - `t(0.50 r0) / t_oracle = 1.0301908872978893`
  - pre-target coherence `= 0.9999987193589412`
  - pre-target higher-mode fraction `= 0.004872959688166528`
  - pre-target leakage `= 2.940799678579199e-08`
- `N = 256`
  - `dx = 0.1875`
  - intrinsic initial compactness `= 1.1853893995285034`
  - intrinsic compactness in cells `= 6.322076797485352`
  - `r0 / Rg = 13.497682316982736`
  - initial radial-acceleration ratio to Newtonian oracle `= 0.9968848413240142`
  - `t(0.75 r0) / t_oracle = 1.02435718374884`
  - `t(0.50 r0) / t_oracle = 1.030223632637699`
  - pre-target coherence `= 0.9999987325247597`
  - pre-target higher-mode fraction `= 0.004873979617710289`
  - pre-target leakage `= 2.9394150579276773e-08`

Interim interpretation:

- The infall diagnostic is behaving exactly as hoped:
  - `40^3` is clearly underresolved and falls too fast,
  - `64^3` already reproduces the static Newtonian infall rate to about `3%`,
  - `96^3` and `128^3` do not materially change that fall-rate answer.
- `256^3` confirms that the fall-rate curve has already saturated; it mainly improves defect resolution in cell units.
- That means radial infall converges much earlier than orbit-quality dynamics.
- The defect is still only about `1.58` cells wide at `64^3`, so this should not be over-interpreted as an orbit-ready grid.
- The current plateau from `64^3` through `128^3` implies that the infall-rate error is no longer the main grid-setting constraint.
- The remaining grid-setting constraint for orbit work is defect resolution in cell units:
  - about `1.58` cells at `64^3`,
  - about `2.37` cells at `96^3`,
  - about `3.16` cells at `128^3`,
  - and expected to be a bit above `6` cells at `256^3` if the intrinsic physical compactness stays near `1.185`.
- The current evidence supports a two-stage conclusion:
  - `64^3` may already be enough for coarse static-force / infall diagnostics,
  - orbit work should not start below `256^3` on the current physical setup, because that is the first completed point where the defect core is resolved by roughly `6` cells while the static force law is already converged.

Force-law check on the completed infall traces:

- For a static pure-Kepler background, the relevant quantity is the COM radial acceleration, which should scale like `-mu / r^2`.
- Measured over the pre-target infall window, the completed runs give:
  - `N = 40`: clearly wrong
    - log-log slope of measured inward radial acceleration versus radius `≈ +0.055`
    - initial acceleration ratio to the `1/r^2` oracle `≈ 2.38`
  - `N = 64`: consistent with `1/r^2`
    - log-log slope `≈ -1.958`
    - initial acceleration ratio to the oracle `≈ 0.995`
    - crossing times remain within about `3%` of the exact Newtonian free-fall solution
  - `N = 96`: consistent with `1/r^2`
    - log-log slope `≈ -1.954`
    - initial acceleration ratio to the oracle `≈ 0.997`
  - `N = 128`: consistent with `1/r^2`
    - log-log slope `≈ -1.956`
    - initial acceleration ratio to the oracle `≈ 0.997`
  - `N = 256`: consistent with `1/r^2`
    - log-log slope `≈ -1.957`
    - initial acceleration ratio to the oracle `≈ 0.997`
- Interpretation:
  - the coarse `40^3` grid does not reproduce the intended static force law,
  - from `64^3` upward the completed runs already follow the expected `1/r^2` acceleration law to good accuracy for this diagnostic,
  - so the remaining reason to push toward `256^3` is defect resolution for future orbit work, not to repair the basic static fall law itself.
