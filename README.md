# 4D 1PN Simulator

PyTorch prototype for the 4D toy-model Sprint 1 scope:

- Hermite-mode utilities in the transverse direction `w`
- projection and leakage helpers
- matter-only split-step solver in `x,y,z` times Hermite modes
- one-DOF adiabatic geometry closure for `a(t)` with fixed `L = Lambda * a`
- single-defect Experiment 1 runner and summary script

The current implementation is intentionally limited to the matter plus geometry sector. The Maxwell, free-heavy, and two-live-defect sectors are left as explicit placeholders for later sprints.
