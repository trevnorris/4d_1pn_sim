Read `AGENTS.md` and `CODEX_HANDOFF_PLAN.md` completely and follow them.

Work in plan-first mode.

Your task is to implement **Sprint 1 only** from `CODEX_HANDOFF_PLAN.md`:

1. create the project scaffold,
2. implement the Hermite-basis and projection utilities,
3. implement a matter-only 3D x modes split-step solver,
4. implement a one-DOF adiabatic geometry closure for `a(t)` with fixed `L = Lambda * a`,
5. implement defect initialization by imaginary-time relaxation,
6. implement the closure diagnostics needed for Experiment 1,
7. add unit tests for:
   - projection identities,
   - Hermite basis,
   - lock-in `Z_eff` extraction,
   - symbolic target constants,
   - orbit fitter on manufactured data,
8. add a runnable `exp01_single_defect_response` command,
9. add a summary script that compares the run output against the closure targets.

Important constraints:

- Do not implement the full Maxwell sector yet.
- Do not implement free-heavy or two-live-defect runs yet.
- Keep the code runnable on a local 8 GB GPU.
- Use `complex64` / `float32` first.
- Keep the implementation restartable and testable.
- Add clear config files for local development.

When done, return:

- the file tree,
- exact commands to run tests,
- exact commands to run Experiment 1 locally,
- a short explanation of the solver design,
- and a concise list of remaining placeholders.
