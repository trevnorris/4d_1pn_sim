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

### Run 017: First `256^3` tracer-matched short-arc control

- Command:
  `python -m src.scripts.run_short_arc_static_background --config configs/local/exp02_shortarc_256.json --scenario source_no_dressing`
- Output directory:
  `outputs/runs/exp02_shortarc_256`
- Current status:
  aborted by manual kill after the machine entered heavy swap

Purpose:

- Move from the static force-law diagnostic to the first orbit-relevant acceptance gate on the minimum serious grid identified by Run 016.
- Compare a live defect against a point tracer over a short arc in the same pure-Kepler background, rather than jumping directly to a perihelion fit.
- Use the `source_no_dressing` branch first so any mismatch is attributable to defect launch / finite-size / COM handling before turning the adiabatic dressing response back on.

Branch changes added before launch:

- Added a short-arc comparison module:
  `src/physics/short_arc.py`
- Extended the point tracer with arbitrary initial-state support:
  `src/physics/point_particle.py`
- Added the runnable short-arc CLI:
  `src/scripts/run_short_arc_static_background.py`
- Added the first `256^3` short-arc config:
  `configs/local/exp02_shortarc_256.json`
- Added tests for tracer equivalence, short-arc summaries, and relaxed-checkpoint loading:
  `tests/test_point_particle.py`
  `tests/test_short_arc.py`
  `tests/test_experiments_common.py`

Current technical state:

- `pytest -q` passes after the new short-arc branch was added.
- The runner now supports reusing a pre-relaxed checkpoint, so follow-on `256^3` passes will not need to repeat the full imaginary-time setup.
- The runner also now writes scenario-specific output directories for later `source_with_dressing` comparisons, avoiding overwrite of the control run.

Interpretation before results:

- Run 016 already showed that the static `1/r^2` force law is converged by `64^3` and that `256^3` is mainly needed for defect resolution in cells.
- This short-arc branch is therefore the first orbit-tuning step that is physically worth the wall time.
- The next question is not “does the force law exist?” but “can the resolved defect track the matched tracer cleanly enough over a finite arc to make later perihelion work meaningful?”

Recovered partial artifacts after the abort:

- `checkpoint_relaxed.npz`
  - completed at relaxation step `320`
  - saved centered relaxed state for reuse
- `launch_calibration.json`
  - calibration completed successfully before the abort
  - target speed `= 0.7245688373094719`
  - recommended applied speed `= 0.7245688373094719`
  - realized tangential speed `= 0.7199834498638411`
  - mean radial speed `= 0.0012885926125991009`
  - launch-radius bias `= 5.766979207137979e-04`
  - minimum boundary clearance in the probe window `= 12.001336097717285`
  - `target_reachable = True`
  - `recommended_window_usable = True`
- `checkpoint_inserted.npz`
  - confirms the defect was inserted after calibration
- `checkpoint_step_00512.npz`
  - confirms the live defect evolution reached step `512 / 1536`
  - simulation time at that checkpoint `= 2.88`

Interpretation after the abort:

- The run did not fail immediately for physical reasons.
- The `256^3` control got through the expensive setup stages cleanly enough to produce a reusable relaxed checkpoint and a clean launch-calibration result.
- The most immediately useful artifact is `checkpoint_relaxed.npz`, because it lets follow-on `256^3` runs skip the swap-heavy relaxation stage.
- The launch-calibration result is also scientifically useful:
  the matched tracer setup at `r_p = 12`, `e = 0.05` on the pure-Kepler background appears box-safe and target-reachable at `256^3`.
- What is still missing is the defect timeseries and final short-arc acceptance summary, so there is not yet a physics conclusion about defect-vs-tracer tracking.

Prepared rerun path after the abort:

- dedicated restart config:
  `configs/local/exp02_shortarc_256_restart.json`
- manual wrapper script:
  `scripts/run_exp02_shortarc_256_restart.sh`
- key operational changes:
  - reuse the saved relaxed checkpoint instead of repeating the `256^3` imaginary-time setup
  - no intermediate `~500 MB` checkpoints during the short-arc evolution
  - cheap short-arc metrics sampled every `16` steps
  - expensive continuity/leakage diagnostics sampled every `64` steps
  - thread caps applied in the shell wrapper to reduce host-memory pressure

### Run 018: `256^3` tracer-matched short-arc control, restart path

- Command:
  `./scripts/run_exp02_shortarc_256_restart.sh`
- Output directory:
  `outputs/runs/exp02_shortarc_256_restart_source_no_dressing`
- Status:
  complete

Result:

- acceptance gate:
  passed
- tracer angular sweep `= 1.2134609954157165`
- defect angular sweep `= 1.1579382202401192`
- angular sweep error `= -0.05552277517559734`
- normalized position RMS `= 0.042409239298342664`
- normalized radius RMS `= 0.029611022720180742`
- phase RMS `= 0.030474938997419522`
- minimum boundary clearance `= 12.005080223083496`
- mean coherence `= 0.9999983754268912`
- mean higher-mode fraction `= 0.004773383962835164`
- mean leakage `= 2.8372745574706763e-08`
- mean compactness `= 1.1847734631494033`
- mean continuity residual `= 1.3309467414563352e-04`

Interpretation:

- This is the first clean orbit-relevant `256^3` control on the current static pure-Kepler branch.
- The no-dressing defect tracks the matched point tracer well enough over a finite arc to pass every currently declared short-arc gate.
- The printed coherence near `0.999998` is now clearly interpretable as a genuine integrity signal rather than a misleading isolated metric, because the COM / phase / radius tracking gates also passed.
- That means the remaining high-value discriminator is no longer basic launch stability or defect breakup.
- The next run should be the matched `source_with_dressing` short arc from the same relaxed checkpoint, so the comparison isolates the adiabatic dressing response rather than setup noise.

### Run 019: `256^3` tracer-matched short-arc, with dressing enabled

- Command:
  `OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 PYTHONUNBUFFERED=1 python -m src.scripts.run_short_arc_static_background --config configs/local/exp02_shortarc_256_restart.json --scenario source_with_dressing`
- Output directory:
  `outputs/runs/exp02_shortarc_256_restart_source_with_dressing`
- Status:
  complete

Result:

- acceptance gate:
  passed
- tracer angular sweep `= 1.2134616440216153`
- defect angular sweep `= 1.1578454074393119`
- angular sweep error `= -0.05561623658230341`
- normalized position RMS `= 0.04247105442193567`
- normalized radius RMS `= 0.029650197255636845`
- phase RMS `= 0.030524493135500208`
- minimum boundary clearance `= 12.00507926940918`
- mean coherence `= 0.9999978466089382`
- mean higher-mode fraction `= 0.004785304788911585`
- mean leakage `= 2.8533020375713522e-08`
- mean compactness `= 1.1843230294626812`
- mean continuity residual `= 1.3324045920109546e-04`

Direct comparison against Run 018 (`with_dressing - no_dressing`):

- defect angular sweep `= -9.2812800807307e-05`
- angular sweep error `= -9.34614067060746e-05`
- normalized position RMS `= +6.18151235930037e-05`
- normalized radius RMS `= +3.91745354561025e-05`
- phase RMS `= +4.9554138080686e-05`
- mean coherence `= -5.28817952982763e-07`
- mean higher-mode fraction `= +1.19208260764211e-05`
- mean leakage `= +1.60274801006759e-10`
- mean compactness `= -4.50433686722151e-04`
- mean continuity residual `= +1.45785055461942e-07`

Interpretation:

- The dressed run is just as clean as the no-dressing control.
- Over this short arc, the measured COM / phase / radius differences are extremely small.
- On the current reduced static-background branch, enabling the adiabatic dressing response does not produce a materially distinct short-arc trajectory at this resolution and window length.
- That is not yet a falsification of any longer-orbit claim, because a tiny effect could still accumulate over much longer arcs.
- But it does mean the short-arc discriminator has now done its job:
  setup noise is under control, and the current dressing implementation appears either weak or practically invisible on this timescale.

### Run 020: ODE Newtonian orbit reference

- Command:
  `python -m src.ode.newtonian_orbit --config configs/local/ode_newtonian_reference.json`
- Output directory:
  `outputs/runs/ode_newtonian_reference`
- Status:
  complete

Result:

- `delta_phi = -1.381192e-04`
- `beta_eff = -2.658986e-02`
- `periapse_count = 6`
- maximum relative orbital-energy drift `= 3.771268e-08`
- maximum relative angular-momentum drift `= 1.511823e-14`

Interpretation:

- The shared orbit-analysis / periapsis / fit pipeline now has a clean Newtonian ODE baseline.
- The extracted precession is consistent with zero at the level needed for current PDE interpretation work.
- Conservation quality is excellent, so the ODE reference is numerically much cleaner than any foreseeable PDE orbit run.
- This does **not** prove the PDE grid will not wobble.
- It does prove that the current fitter and orbit-summary machinery are not creating a large fake precession signal on their own.
- The next Newtonian gate remains a long-window PDE bound orbit with no dressing, compared against this ODE baseline.

### Run 021: PDE Newtonian bound-orbit branch wiring

- New experiment entry point:
  `src/experiments/exp03_pde_newtonian_bound_orbit.py`
- Long-run config:
  `configs/local/exp03_newtonian_bound_orbit_256_restart.json`
- Manual wrapper:
  `scripts/run_exp03_newtonian_bound_orbit_256_restart.sh`
- Shared additions:
  - `src/physics/newtonian_orbit_gate.py`
  - `src/physics/pde_orbit_runtime.py`
  - `docs/run_matrix.md`
  - `docs/analysis_pipeline.md`

Current status:

- full test suite passes after the new long-orbit branch was added
- a `256^3` smoke verification run is active from the saved relaxed checkpoint:
  `python -m src.experiments.exp03_pde_newtonian_bound_orbit --config configs/local/exp03_newtonian_bound_orbit_smoke.json`

Interpretation:

- The next serious Newtonian gate is now implemented, not just planned.
- The remaining open question is runtime / stability on the real `256^3` PDE branch over a long enough window to extract several periapses and compare against the ODE zero-drift baseline.

### Run 022: PDE Newtonian bound-orbit smoke completion

- Command:
  `python -m src.experiments.exp03_pde_newtonian_bound_orbit --config configs/local/exp03_newtonian_bound_orbit_smoke.json`
- Output directory:
  `outputs/runs/exp03_newtonian_bound_orbit_smoke`
- Status:
  complete

Result:

- `newtonian_gate_pass = false`
- `fit_error = Need at least three periapses to fit precession`
- `periapse_count = 0`
- maximum relative orbital-energy drift `= 1.374291e-01`
- maximum relative angular-momentum drift `= 6.433493e-02`
- mean coherence `= 0.999998`
- mean higher-mode fraction `= 5.190919e-03`
- mean leakage `= 2.918110e-08`

Interpretation:

- The `exp03` branch runs end-to-end and writes the full artifact set on the real `256^3` PDE path.
- The defect remains extremely coherent, so the first observed failure mode is not breakup.
- Even before completing a full orbit, the effective COM diagnostics already show nontrivial drift.
- This smoke result is therefore an operational success but not a clean Newtonian-orbit success.

### Run 023: PDE Newtonian bound-orbit guarded CUDA run

- Command:
  `./scripts/run_exp03_newtonian_bound_orbit_256_cuda.sh`
- Output directory:
  `outputs/runs/exp03_newtonian_bound_orbit_256_restart_cuda`
- Status:
  complete, terminated by runtime abort

Result:

- runtime abort triggered at field step `1024` after `704 / 16384` orbit steps
- abort gates:
  `max_rel_energy_drift`, `max_rel_angular_momentum_drift`
- maximum relative orbital-energy drift `= 1.847236e-01`
- maximum relative angular-momentum drift `= 8.746695e-02`
- mean coherence `= 0.9999983784827319`
- mean higher-mode fraction `= 4.709897568153048e-03`
- mean leakage `= 2.630619416238938e-08`
- minimum boundary clearance `= 11.999991416931152`
- point-tracer comparison over the same window:
  - final radial offset `(PDE - tracer) = -1.3913545129944715e-01`
  - angular sweep offset `(PDE - tracer) = -2.459837072839255e-02`
  - position RMS difference `= 1.4884677974948907e-01`
  - radius RMS difference `= 5.339060230033025e-02`

Interpretation:

- The runtime abort guard did its job and prevented spending the full long-run budget on a clearly failing orbit.
- The defect stays healthy and well away from the box boundary, so the dominant failure is still in effective COM orbital quality.
- Relative to the exact tracer, the PDE COM is lagging in angle and falling inward too quickly over the same short window.
- That pattern is consistent with excess effective dissipation / secular drift in the current long-window orbit setup, not with source misconfiguration or defect breakup.
- The next promising branch is not “more time on the same run.” It is a larger physical orbit domain at roughly the same `dx`, so the defect stays pointlike while the orbit curvature and COM confinement coupling are both reduced.
- On the observed `15 GB` A40 memory footprint for `256^3`, `288^3` and likely `320^3` are plausible next candidates; `384^3` is likely too large for a `40 GB` card.

### Prepared next branch: guarded `320^3 / L = 60` Newtonian orbit

- New smoke config:
  `configs/local/exp03_newtonian_bound_orbit_320_cuda_smoke.json`
- New smoke wrapper:
  `scripts/run_exp03_newtonian_bound_orbit_320_cuda_smoke.sh`
- New restart config:
  `configs/local/exp03_newtonian_bound_orbit_320_restart_cuda.json`
- New restart wrapper:
  `scripts/run_exp03_newtonian_bound_orbit_320_cuda_restart.sh`

Branch rationale:

- keep `dx = 0.1875` unchanged from the validated `256^3` branch
- increase the physical box from `L = 48` to `L = 60`
- move the periapsis radius to `r_p = 16`
- keep the same low eccentricity `e = 0.05`
- retain the runtime abort guard so cloud runs still stop early if effective COM drift remains unacceptable
- disable continuity/leakage sampling on this branch because the full `currents()` diagnostic OOMs on an A40 even when the main evolution itself fits comfortably

Expected resource note:

- using the observed A40 `256^3` memory footprint as the baseline, `320^3` should land near `29 GB`, which is practical on a `40 GB` card and leaves room for runtime overhead

### Branch correction: boundary sponge + uniform reservoir refill

After the first `320^3 / L = 60` cloud attempt, the user pointed out two missing controls from earlier exploratory work:

- outgoing wake / sound content should be damped before it wraps through the periodic boundary,
- the ambient medium should be replenished uniformly so the box does not slowly drain.

Repository changes made in response:

- added an optional boundary sponge applied as a real-space amplitude mask during the nonlinear step,
- added a cheap mode-space projected leakage operator that avoids the old `currents()` OOM path,
- added a uniform lowest-mode reservoir refill controller driven by the projected leakage estimate and optional target-norm restoration,
- wired both controls into launch calibration and the `exp03` orbit branch.

Interpretation:

- the earlier `256^3` and `320^3` long-orbit failures remain useful as evidence that the uncorrected branch drifts badly,
- but they are no longer the final word on the intended boxed simulation protocol,
- because they did not include the sponge + refill machinery that the user reports was necessary in previous work.
