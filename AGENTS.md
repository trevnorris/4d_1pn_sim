# AGENTS.md

## Repository mission

Build a custom PyTorch simulator for the 4D toy model that can quickly falsify or support the current closure and orbit claims.

The primary scientific targets are in `CODEX_HANDOFF_PLAN.md`. Treat that file as the execution spec.

## Working rules

- Plan first for any task that touches more than one module.
- Prefer small, reviewable commits and working intermediate states.
- Keep the implementation modular: core numerics, physics modules, experiments, diagnostics, tests.
- Preserve deterministic seeds and write restartable checkpoints.
- Run tests after each meaningful change.
- Do not optimize before correctness.

## Physics do-not rules

- Do not use a clamped heavy source as the main 1PN orbit test.
- Use the clamped source only as a negative control.
- Do not start with two live defects.
- Do not let decisive runs live at `N_w = 1`; use `N_w >= 4` for the main falsification runs.
- Do not claim success from trajectories alone; always report leakage, coherence, higher-mode energy, and fit stability.
- Do not turn on AMP or `torch.compile` until float32 / complex64 tests pass.

## Numerical preferences

- Use PyTorch, not TorchGPE, as the main implementation substrate.
- Use 3D pseudo-spectral methods in `(x,y,z)` where practical.
- Use Hermite modes in `w`.
- Prefer imposed static backgrounds over clamped sources for static-source tests.
- Treat isolated-boundary Poisson handling as important for later orbit stages.

## Required regression targets

Keep these symbolic targets hard-coded in tests:

- `n = 5`
- `kappa_add = 1/2`
- `alpha^2 = 3/4`
- `K_vec = 2 / pi^2`
- `kappa_PV = 3/2`
- `E_w : E_f : E_PV = 11 : 2 : 5`
- `d ln a / d ln rho = -57/64`
- `beta_1PN = 3`
- EIH cross coefficients `(-7/2, -1/2)`

## Definition of done for each sprint

A sprint is only done when:

1. code runs,
2. tests pass,
3. commands to reproduce are documented,
4. outputs are written to `outputs/`,
5. the result is summarized in plain language,
6. unresolved assumptions are listed explicitly.

## Commands Codex should create and maintain

Once scaffolded, the repo should support commands like:

- `pytest -q`
- `python -m src.experiments.exp01_single_defect_response --config ...`
- `python -m src.experiments.exp02_orbit_static_background --config ...`
- `python -m src.scripts.summarize_run --run-dir ...`

## Reporting expectations

When finishing a task, always report:

- what files changed,
- what tests were run,
- what passed or failed,
- what scientific claim the current state does or does not support.
