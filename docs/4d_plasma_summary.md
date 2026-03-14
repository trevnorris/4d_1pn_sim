4d_plasma.tex

## 1) What this paper is trying to accomplish

This paper extends the unified **4+1D bulk / 3D brane-observer toy model** into a **plasma + electromagnetism** framework:

- **Bulk (“real”) dynamics:** conservative evolution in **four spatial dimensions** \((x,y,z,w)\), with
  - a **localized 4+1 Maxwell sector** (gauge field \(A_M\)) whose kinetic term is weighted by a transverse localization profile \(Z(w)\),
  - a **multi-species charged medium** modeled either as:
    - a **field-based nonrelativistic matter sector** (gauged Schrödinger / GNLS), or
    - a **kinetic Vlasov/PIC** sector (4D space + 4D velocity).

- **Brane (“observable”) dynamics:** what a 3D observer measures is *not* a boundary condition; it is an **operational projection** across \(w\) with a kernel \(W(w)\). This makes the brane system an **open subsystem**: even if bulk evolution is conservative, **projected brane balance laws acquire explicit leakage terms**.

The paper has two big deliverables:

1. **Recovery of standard theory as controlled limits.**
   It shows—under explicit assumptions—how the 4+1 bulk system reduces in stages:
   \[
   \text{(localized 4+1 Maxwell + bulk plasma)}
   \;\Rightarrow\;
   \text{(effective 3+1 Maxwell + brane two-fluid)}
   \;\Rightarrow\;
   \text{(single-fluid MHD)}.
   \]
   The only structural change at the Maxwell/MHD level is that \(\mu_0\) becomes an **effective** \(\mu_0^{\rm eff}=\mu_0/\!\int Z\).

2. **A principled “beyond-MHD” mechanism without ad hoc resistivity.**
   When the controlled-limit suppressions are relaxed, three new correction channels appear:
   - **Mixed-sector electromagnetism:** the *extra* gauge component \(A_w\) and mixed field components \(F_{\mu w}\) are dynamical and produce new force/EMF terms absent in strictly 3+1 Maxwell.
   - **Explicit brane–bulk exchange:** transverse drift \(j^w\neq 0\) produces **leakage sources** in brane continuity and related balances.
   - **Finite-localization transverse modes:** for Gaussian \(Z(w)\), the transverse operator has a **Hermite/KK tower** with masses \(m_n^2\propto n/\lambda^2\), generating computable Yukawa corrections and additional energy/topology reservoirs.

A core interpretive claim is:

> **Reconnection-like non-ideality on the brane can correspond to conservative transport into \(w\) and into higher transverse modes**, rather than local collisional dissipation.

---

## 2) Geometry, indices, and operators (bulk vs brane)

### Coordinates and “brane”
- Bulk spacetime coordinates:
  \[
  x^M=(t,x,y,z,w)\equiv (t,\mathbf{x},w),\qquad \mathbf{x}=(x,y,z),\qquad \mathbf{X}=(x,y,z,w).
  \]
- The operational brane is centered at \(w=0\), but **“on the brane” always means “after projection with \(W(w)\)”**.

### Index conventions
- Bulk spacetime: \(M,N\in\{0,1,2,3,4\}\) with \(0\equiv t\), \(4\equiv w\).
- Brane spacetime: \(\mu,\nu\in\{0,1,2,3\}\).
- Bulk spatial: \(A,B\in\{x,y,z,w\}\).
- Brane spatial: \(a,b,c\in\{x,y,z\}\).

### Metric and differential operators
- Bulk Minkowski metric (mostly plus):
  \[
  \eta_{MN}=\mathrm{diag}(-1,+1,+1,+1,+1).
  \]
- Gradients/Laplacians:
  \[
  \nabla_3=(\partial_x,\partial_y,\partial_z),\quad \Delta_3=\partial_x^2+\partial_y^2+\partial_z^2,
  \]
  \[
  \nabla_4=(\nabla_3,\partial_w),\quad \Delta_4=\Delta_3+\partial_w^2.
  \]
- Bulk d’Alembertian:
  \[
  \Box_5=-\partial_t^2+\Delta_3+\partial_w^2.
  \]
- “Hybrid relativity”: EM is evolved as a relativistic hyperbolic field theory; matter/plasma is nonrelativistic by default.

---

## 3) Localization vs projection (two distinct kernels)

### Localization profile \(Z(w)\) (appears in the *action*)
The electromagnetic kinetic term is weighted by \(Z(w)\ge 0\), assumed integrable:
\[
Z_{\rm int}\equiv \int_{-\infty}^{+\infty} Z(w)\,dw < \infty.
\]
Canonical analytic choice:
\[
Z(w)=\exp\!\left(-\frac{w^2}{\lambda^2}\right),\qquad Z_{\rm int}=\lambda\sqrt{\pi}.
\]
**Physical role:** \(Z\) defines how tightly EM is localized near the brane and sets the transverse length scale \(\lambda\), which controls the Hermite/KK spectrum and when higher modes matter.

### Projection kernel \(W(w)\) (defines what the brane observer measures)
\(W(w)\) is normalized:
\[
\int_{-\infty}^{+\infty} W(w)\,dw = 1,\qquad W(w)\ge 0,\qquad W\ \text{peaked near}\ w=0.
\]
The brane observable associated with a bulk field \(Q(t,\mathbf{x},w)\) is
\[
\overline{Q}(t,\mathbf{x})\equiv \int_{-\infty}^{+\infty} W(w)\,Q(t,\mathbf{x},w)\,dw.
\]
Optional “matched” measurement choice:
\[
W(w)=\frac{Z(w)}{Z_{\rm int}}.
\]

**Key distinction:**
- \(Z(w)\) controls bulk evolution.
- \(W(w)\) defines observation/projection and produces exact open-system identities.

---

## 4) Fields and brane-facing decompositions

### Gauge field and field strength
- Gauge potential: \(A_M(t,\mathbf{x},w)\).
- Field strength:
  \[
  F_{MN}=\partial_M A_N-\partial_N A_M,
  \qquad A_M\mapsto A_M+\partial_M\chi\ \text{(gauge)}.
  \]
- Useful decompositions:
  \[
  A_M=(A_0, A_a, A_w),\qquad F_{\mu\nu}\ \text{and mixed}\ F_{\mu w}.
  \]

### Brane-facing \( \mathbf{E}\) and \(\mathbf{B}\) (measured fields)
Define from the projected field strength:
\[
E_a^{\rm (brane)}(\mathbf{x})\equiv \overline{F_{a0}},
\qquad
B_a^{\rm (brane)}(\mathbf{x})\equiv \frac12\,\epsilon_{abc}\,\overline{F_{bc}}.
\]

### Mixed-sector fields (absent in strict 3+1 Maxwell)
Pointwise in \(w\):
\[
E_w\equiv F_{w0}=-\partial_t A_w-\partial_w A_0,
\qquad
C_a\equiv F_{aw}=\partial_a A_w-\partial_w A_a.
\]
Their brane projections \(\overline{E_w}\), \(\overline{C_a}\) are central beyond-MHD diagnostics.

### Plasma species observables
For each species \(s\):
- bulk number density \(\rho_s(t,\mathbf{x},w)\),
- bulk number current \(j_s^A(t,\mathbf{x},w)\) for \(A\in\{x,y,z,w\}\).

Brane-measured density and brane current:
\[
\overline{\rho_s}(t,\mathbf{x})\equiv \overline{\rho_s},
\qquad
\overline{j_s^a}(t,\mathbf{x})\equiv \overline{j_s^a}.
\]
Brane-observed species velocity (diagnostic):
\[
v_{s,\rm brane}^a \equiv \frac{\overline{j_s^a}}{\overline{\rho_s}}\quad (\overline{\rho_s}>0).
\]

---

## 5) Exact projected balance laws and leakage (open-system brane identities)

### Species continuity in the bulk
Assume each species satisfies bulk continuity:
\[
\partial_t \rho_s + \partial_a j_s^a + \partial_w j_s^w = 0.
\]

### Projected (brane) continuity acquires a leakage source
Projecting with \(W(w)\) yields the exact identity
\[
\partial_t \overline{\rho_s} + \partial_a \overline{j_s^a} = S_{\rm leak}^{(s)}(t,\mathbf{x}),
\]
where
\[
S_{\rm leak}^{(s)}
\equiv
-\Big[W j_s^w\Big]_{-\infty}^{+\infty}
+\int_{-\infty}^{+\infty} W'(w)\,j_s^w(t,\mathbf{x},w)\,dw.
\]
Under decay/compact-support assumptions the boundary term vanishes and leakage is carried by the \(W'(w)\) overlap.

**Interpretation:** even with conservative bulk dynamics, brane-measured density can change because material flows through \(w\) across the measurement profile.

---

## 6) Electromagnetic sector (localized 4+1 Maxwell)

### Localized Maxwell action
\[
S_{\rm EM}[A;Z]
=
\int dt\,d^3x\,dw\,
\left[
-\frac{Z(w)}{4\mu_0}F_{MN}F^{MN}
-\frac{1}{2\xi\mu_0}(\partial\!\cdot\!A)^2
- A_M J^M
\right].
\]
- \(\xi\) is a gauge-fixing parameter for invertibility/hyperbolicity.
- Gauge invariance of \(-A_MJ^M\) requires \(\partial_M J^M=0\) (up to boundary terms).

### Euler–Lagrange field equations
\[
\partial_M\!\left(Z(w)\,F^{MN}\right) + \frac{1}{\xi}\,\partial^N(\partial\!\cdot\!A) = \mu_0 J^N.
\]
- Bianchi identity (exact): \(\partial_{[L}F_{MN]}=0\).
- Divergence consistency identity:
  \[
  \frac{1}{\xi}\,\Box_5(\partial\!\cdot\!A) = \mu_0\,\partial_N J^N.
  \]
  So for conserved current, the gauge-fixing term does not contaminate gauge-invariant observables.

### Physical role of \(A_w\)
In 4+1 Maxwell, \(A_w\) is a **genuine dynamical degree of freedom**, not merely “extra gauge.”
It sources:
- transverse electric field \(E_w\),
- mixed field \(C_a=F_{aw}\),
and couples directly to plasma via \(J^w\) and via mixed Lorentz-force terms.

### Controlled reduction to effective 3+1 Maxwell (Step 1)
Assume (for \(|w|\) in the support of \(Z\)):
1. **Zero-mode dominance (brane components):**
   \[
   A_\mu(t,\mathbf{x},w)\simeq a_\mu(t,\mathbf{x}),\qquad \partial_w A_\mu\simeq 0.
   \]
2. **Mixed components negligible:** \(F_{\mu w}\simeq 0\) (i.e. \(E_w\simeq 0\) and \(C_a\simeq 0\)).
3. **No net transverse current:** \(J^w\simeq 0\).
4. Axial gauge \(A_w=0\) is optional.

Integrating over \(w\) yields standard 3+1 Maxwell with an effective coupling:
\[
\mu_0^{\rm eff} \equiv \frac{\mu_0}{Z_{\rm int}},
\qquad
\epsilon_0^{\rm eff}\mu_0^{\rm eff}=c^{-2}.
\]
In brane vector form:
\[
\nabla_3\cdot \mathbf{B}=0,\qquad \nabla_3\times \mathbf{E}=-\partial_t \mathbf{B},
\]
\[
\nabla_3\cdot \mathbf{E}=\frac{\rho_q}{\epsilon_0^{\rm eff}},
\qquad
\nabla_3\times \mathbf{B}-\frac{1}{c^2}\partial_t \mathbf{E}=\mu_0^{\rm eff}\mathbf{J}.
\]

---

## 7) Plasma matter sector (multi-species)

The paper supports multiple matter realizations that share the same bulk gauge coupling and continuity structure.

### Option (field-based): multi-species gauged GNLS (“Schrödinger plasma”)

#### Covariant derivatives
For species \(s\) with charge \(q_s\) and mass \(m_s\):
\[
D_t^{(s)}=\partial_t+\frac{i q_s}{\hbar}A_0,
\qquad
D_A^{(s)}=\partial_A-\frac{i q_s}{\hbar}A_A,
\qquad A\in\{x,y,z,w\}.
\]

#### GNLS equation
\[
i\hbar D_t^{(s)}\psi_s
=
\left[
-\frac{\hbar^2}{2m_s}D_A^{(s)}D_A^{(s)}
+V_{{\rm conf},s}(\mathbf{x},w)
+h_s(\rho_s)
\right]\psi_s,
\qquad \rho_s=|\psi_s|^2,
\]
where \(h_s(\rho_s)=dU_s/d\rho_s\) encodes a barotropic EOS via an internal-energy density \(U_s(\rho_s)\).
- \(V_{{\rm conf},s}\) is optional confinement/localization potential for species \(s\).

#### Number current and charge 5-current
Bulk number current:
\[
j_s^A = \frac{\hbar}{m_s}\,\Im\!\left(\psi_s^\ast D_A^{(s)}\psi_s\right).
\]
Charge 5-current:
\[
J_s^0=q_s\rho_s,\qquad J_s^A=q_s j_s^A.
\]
Exact bulk continuity:
\[
\partial_t\rho_s+\partial_A j_s^A=0
\quad\Rightarrow\quad
\partial_M J_s^M=0.
\]

#### Madelung transform and canonical momentum (important computationally)
Write
\[
\psi_s=\sqrt{\rho_s}\,e^{i\theta_s}.
\]
Define bulk velocity (4D space) via \(j_s^A=\rho_s v_s^A\):
\[
v_s^A=\frac{\hbar}{m_s}\left(\partial^A\theta_s-\frac{q_s}{\hbar}A^A\right).
\]
Canonical vs kinetic momentum:
\[
p^{\rm can}_{s,A}\equiv \hbar\,\partial_A\theta_s,\qquad
p^{\rm kin}_{s,A}\equiv m_s v_{s,A},\qquad
p^{\rm can}_{s,A}=p^{\rm kin}_{s,A}+q_s A_A.
\]
**Why it matters:** evolving \(\psi_s\) evolves canonical momentum without singularities as \(\rho_s\to 0\), unlike raw velocity.

#### Euler-like momentum equation (exact, bulk)
From GNLS:
\[
m_s(\partial_t+v_s^B\partial_B)v_{s,A}
=
q_s\left(E_A+v_s^B F_{AB}\right)
-\partial_A\!\left(V_{{\rm conf},s}+h_s(\rho_s)+Q_s(\rho_s)\right),
\]
with
\[
E_A\equiv F_{A0}=-\partial_t A_A-\partial_A A_0,
\qquad
F_{AB}=\partial_A A_B-\partial_B A_A,
\]
and quantum (dispersive) potential
\[
Q_s(\rho_s)=-\frac{\hbar^2}{2m_s}\frac{\Delta_4\sqrt{\rho_s}}{\sqrt{\rho_s}}.
\]
**Classical two-fluid limit:** drop \(Q_s\) (or take \(\hbar\to 0\) in a controlled way) while retaining the pressure/enthalpy closure \(h_s(\rho_s)\).

#### Transverse (\(w\)) momentum and why \(A_w\) matters
The \(A=w\) component reads
\[
m_s(\partial_t+v_s^B\partial_B)v_{s,w}
=
q_s\left(E_w+v_s^a F_{wa}\right)
-\partial_w\!\left(V_{{\rm conf},s}+h_s+Q_s\right),
\]
with \(E_w=F_{w0}=-\partial_t A_w-\partial_w A_0\).
Thus, dynamical \(A_w\) and mixed fields \(F_{wa}\) generically drive \(v_{s,w}\neq 0\),
hence \(j_s^w\neq 0\) and therefore **brane leakage** \(S_{\rm leak}^{(s)}\neq 0\).

#### Useful kinematic “London-type” identity (canonical vorticity constraint)
Away from phase singularities:
\[
\partial_A v_{s,B}-\partial_B v_{s,A} = -\frac{q_s}{m_s}F_{AB}.
\]
This ties canonical vorticity to gauge flux in the bulk; brane non-ideality can arise from projection/leakage even while this bulk constraint holds.

### Option (kinetic): 4D Vlasov / PIC plasma

Species distribution \(f_s(t,\mathbf{x},w;\mathbf{v})\) with \(\mathbf{v}\in\mathbb{R}^4\) evolves via
\[
\partial_t f_s + v^A\partial_A f_s
+ \frac{q_s}{m_s}\left(E_A+v^B F_{AB}\right)\partial_{v_A}f_s
= C_s[f],
\]
where \(C_s[f]\) is an optional collision operator chosen to preserve overall charge conservation.
Densities/currents are the usual velocity moments (paper defines them explicitly).

---

## 8) Full coupled 4+1D plasma–EM system (simulation target)

### Total action and Maxwell equation
\[
S_{\rm tot}=S_{\rm EM}[A;Z] + \sum_{s=1}^S S_{{\rm matt},s}[\text{matter}_s,A] + S_{\rm ext}[A].
\]
Maxwell with total current:
\[
\partial_M\!\left(Z(w)F^{MN}\right)+\frac{1}{\xi}\partial^N(\partial\!\cdot\!A)
=\mu_0\left(J_{\rm ext}^N+\sum_s J_s^N\right),
\qquad
\partial_M J_{\rm tot}^M=0.
\]

### Compact “box form” of the bulk PDE system
The paper highlights (schematically) that the simulation target is:
- localized Maxwell in potentials (hyperbolic gauge),
- plus either GNLS matter per species, or Vlasov per species,
- with exact current conservation and Bianchi identities.

### Constraints, gauges, and well-posedness
- Evolving potentials \(A_M\) automatically satisfies the homogeneous Maxwell equations.
- \(N=0\) component is Gauss-like constraint content; \(N=A\) are evolution.
- Gauge-fixing yields a manifestly hyperbolic operator.
- The full theory **retains** \(A_w\) and \(F_{\mu w}\) as physical channels; axial gauge is treated as a controlled simplification, not a defining assumption.
- Boundary/localization assumptions: decay in \(w\) or effective truncation via spectral/mode truncation.

### Bulk energy ledger (key verification tool)

Electromagnetic energy density (localized):
\[
u_{\rm EM}
=
\frac{Z(w)}{2\mu_0}\left(E_AE_A+\frac12 F_{AB}F_{AB}\right).
\]
In brane/mixed decomposition this includes contributions from \(\mathbf{E}\), \(\mathbf{B}\) and also \(E_w\), \(\mathbf{C}\).

GNLS matter energy density (per species, gauge-invariant):
\[
u_s
=
\frac{\hbar^2}{2m_s}(D_A\psi_s)^\ast(D_A\psi_s)
+V_{{\rm conf},s}\rho_s
+U_s(\rho_s).
\]
Total bulk energy:
\[
\mathcal{E}_{\rm tot}(t)=\int d^3x\,dw\,\big(u_{\rm EM}+\sum_s u_s\big),
\]
which is conserved under stated boundary/localization assumptions (and conservative collision models).

A key exchange term in the EM–matter coupling is the work density
\[
J^A E_A = J^a E_a + J^w E_w,
\]
so \(J^wE_w\) is the explicit scalar-photon work channel when \(A_w\) is active.

---

## 9) Controlled reduction to MHD (and where it can fail)

The paper organizes the recovery of standard 3+1 plasma physics in three steps.

### Step 1: localized 4+1 Maxwell → effective 3+1 Maxwell
Controlled assumptions (summarized):
- \(A_\mu\) zero-mode dominant and \(\partial_w A_\mu\approx 0\),
- \(F_{\mu w}\approx 0\) (so \(E_w\approx 0\), \(C_a\approx 0\)),
- \(J^w\approx 0\).

Result:
- standard 3+1 Maxwell with \(\mu_0\to \mu_0^{\rm eff}=\mu_0/Z_{\rm int}\).

### Step 2: bulk plasma → brane two-fluid
Assume species are effectively brane-supported at the measurement scale:
\[
j_s^w\approx 0\ \Rightarrow\ S_{\rm leak}^{(s)}\approx 0,
\]
so projected continuity reduces to ordinary 3D continuity. If starting from GNLS, drop \(Q_s\) to reach classical fluid equations.

### Step 3: brane two-fluid → single-fluid MHD
Standard assumptions:
- quasi-neutrality \(n_i\simeq n_e\equiv n\),
- small electron inertia \(m_e/m_i\ll 1\),
- optionally neglect displacement current (Darwin/MHD ordering).

With brane 3-vectors \(\mathbf{E},\mathbf{B}\) and brane current \(\mathbf{J}\), two-fluid equations:
\[
\partial_t n_s + \nabla_3\cdot(n_s\mathbf{v}_s)=0,
\]
\[
m_s n_s(\partial_t+\mathbf{v}_s\cdot\nabla_3)\mathbf{v}_s
=
q_s n_s(\mathbf{E}+\mathbf{v}_s\times\mathbf{B})-\nabla_3 p_s + \mathbf{R}_s,
\quad \sum_s\mathbf{R}_s=0.
\]

Single-fluid definitions:
\[
\rho \equiv m_i n_i+m_e n_e\simeq (m_i+m_e)n,\qquad
\mathbf{v}=\frac{m_i n_i\mathbf{v}_i+m_e n_e\mathbf{v}_e}{\rho},
\qquad
\mathbf{J}=e n(\mathbf{v}_i-\mathbf{v}_e).
\]

Generalized Ohm law (electron momentum, inertialess-electron limit):
\[
\mathbf{E}+\mathbf{v}\times\mathbf{B}
=
\frac{\mathbf{J}\times\mathbf{B}}{en}
-\frac{1}{en}\nabla_3 p_e
+\frac{\mathbf{R}_e}{en}.
\]
Resistive closure: \(\mathbf{R}_e\approx en\,\eta\,\mathbf{J}\).
Ideal MHD sub-limit:
\[
\mathbf{E}=-\mathbf{v}\times\mathbf{B}.
\]
Induction equation:
\[
\partial_t\mathbf{B}=\nabla_3\times(\mathbf{v}\times\mathbf{B})
\quad\text{(ideal)},
\]
and with extended-MHD terms:
\[
\partial_t\mathbf{B}
=
\nabla_3\times(\mathbf{v}\times\mathbf{B})
-\nabla_3\times\!\left(\frac{\mathbf{J}\times\mathbf{B}}{en}\right)
+\nabla_3\times\!\left(\frac{1}{en}\nabla_3 p_e\right)
-\nabla_3\times\!\left(\frac{\mathbf{R}_e}{en}\right).
\]

**Where the parent 4D theory re-enters:** the MHD limit fails when any of
\(\{j^w,\ J^w,\ A_w,\ F_{\mu w},\ \partial_w(\cdot),\ \text{higher modes}\}\) become appreciable.

---

## 10) Beyond-MHD extensions from 4D interactions (core novelty)

The controlled MHD limit suppressed:
\[
\partial_w(\cdot)\approx 0,\quad A_w\approx 0,\quad F_{\mu w}\approx 0,\quad J^w\approx 0,\quad \text{(zero-mode dominance)}.
\]
Beyond MHD, these are allowed to be non-negligible.

### 10.1 Three coupled correction classes
1. **Mixed-sector electromagnetism (scalar-photon channel).**
   \[
   E_w=F_{w0}=-\partial_t A_w-\partial_w A_0,\qquad
   C_a=F_{aw}=\partial_a A_w-\partial_w A_a.
   \]
2. **Explicit brane–bulk exchange (leakage).**
   Species drift \(j_s^w\neq 0\Rightarrow S_{\rm leak}^{(s)}\neq 0\).
3. **Finite-localization / transverse-mode tower (Hermite/KK).**
   For Gaussian \(Z\), modes have masses \(m_n^2=2n/\lambda^2\) and provide additional reservoirs; static interactions get Yukawa corrections on \(r\sim \lambda\).

A practical “when do higher modes matter?” heuristic:
\[
\chi_\lambda \equiv \lambda\,|\nabla_3\ln(\cdot)|,
\]
evaluated on relevant brane structures; \(\chi_\lambda\ll 1\) suggests MHD-like behavior; \(\chi_\lambda\gtrsim 1\) suggests beyond-MHD relevance.

### 10.2 Projection covariances (unresolved transverse structure)
Define the exact covariance with respect to \(W\):
\[
\mathrm{Cov}_W[Q,R]\equiv \overline{QR}-\overline{Q}\,\overline{R}.
\]
A key identity:
\[
\overline{\mathbf{v}\times\mathbf{B}}
=
\overline{\mathbf{v}}\times\overline{\mathbf{B}}
+\mathrm{Cov}_W[\mathbf{v},\mathbf{B}]_{\times}
=
\overline{\mathbf{v}}\times\overline{\mathbf{B}}+\overline{\mathbf{v}'\times\mathbf{B}'}.
\]
This “covariance EMF” is *not* turbulence-specific; it measures \(w\)-structure.

### 10.3 Mixed-sector Lorentz-force splitting (shows the new channels)
For species \(s\), brane components:
\[
q_s\Big(E_a+F_{ab}v_s^b+F_{aw}v_s^w\Big)
=
q_s\Big(E_a+(\mathbf{v}_s\times\mathbf{B})_a+v_s^w C_a\Big).
\]
Transverse component:
\[
q_s\Big(E_w+F_{wb}v_s^b\Big)=q_s\Big(E_w-v_s^a C_a\Big).
\]
So:
- \(v_s^w C_a\) is a new **brane force channel**;
- \(E_w\) is a new **transverse acceleration channel** that generates \(v^w\) and hence leakage.

### 10.4 Generalized Ohm’s law with 4D/projection corrections (key result)

#### Pointwise (bulk) generalized Ohm law from electron momentum
With electron density \(n_e\), brane velocity \(\mathbf{v}_e\), transverse velocity \(v_e^w\), and
4D convective derivative
\[
D_t^{(4)}=\partial_t+v_e^a\partial_a+v_e^w\partial_w,
\]
the bulk (pointwise in \(w\)) Ohm law is:
\[
\mathbf{E}
=
-\mathbf{v}_e\times\mathbf{B}
-\;v_e^w\,\mathbf{C}
-\frac{1}{e n_e}\nabla_3 p_e
+\frac{1}{e n_e}\mathbf{R}_e
-\frac{m_e}{e}\,D_t^{(4)}\mathbf{v}_e
+\cdots.
\]

#### Exact projected (brane-facing) identity
Projecting gives:
\[
\overline{\mathbf{E}}
=
-\overline{\mathbf{v}_e\times\mathbf{B}}
-\overline{v_e^w\,\mathbf{C}}
-\overline{\frac{1}{e n_e}\nabla_3 p_e}
+\overline{\frac{1}{e n_e}\mathbf{R}_e}
-\frac{m_e}{e}\,\overline{D_t^{(4)}\mathbf{v}_e}
+\cdots.
\]

#### Quasi-neutral MHD-form rewrite + topology EMF
Under quasi-neutral ordering with \(\overline{n}\equiv \overline{n_e}\simeq \overline{n_i}\),
define brane current \(\overline{\mathbf{J}}\) and single-fluid velocity \(\overline{\mathbf{v}}\),
and use \(\overline{\mathbf{v}}-\overline{\mathbf{v}_e}\approx \overline{\mathbf{J}}/(e\overline{n})\).
Then:
\[
\boxed{
\overline{\mathbf{E}}+\overline{\mathbf{v}}\times\overline{\mathbf{B}}
=
\frac{\overline{\mathbf{J}}\times\overline{\mathbf{B}}}{e\,\overline{n}}
-\frac{1}{e\,\overline{n}}\nabla_3\overline{p_e}
+\eta\,\overline{\mathbf{J}}
-\frac{m_e}{e}\,\mathcal{I}_e
+\boldsymbol{\mathcal{E}}_{\rm topo}
+\cdots
}
\]
Here \(\eta\overline{\mathbf{J}}\) and \(\mathcal{I}_e\) are chosen brane closures for resistivity and electron inertia if retained.

The genuinely new contribution is the **topology EMF**
\[
\boldsymbol{\mathcal{E}}_{\rm topo}
\equiv
\boldsymbol{\mathcal{E}}_{\rm cov}
+\boldsymbol{\mathcal{E}}_{w}
+\boldsymbol{\mathcal{E}}_{\rm proj},
\]
with
\[
\boldsymbol{\mathcal{E}}_{\rm cov}
=
\overline{\mathbf{v}_e}\times\overline{\mathbf{B}}
-\overline{\mathbf{v}_e\times\mathbf{B}}
= -\mathrm{Cov}_W[\mathbf{v}_e,\mathbf{B}]_{\times},
\]
\[
\boldsymbol{\mathcal{E}}_{w}=-\overline{v_e^w\,\mathbf{C}},
\qquad \mathbf{C}=(F_{xw},F_{yw},F_{zw}),
\]
and \(\boldsymbol{\mathcal{E}}_{\rm proj}\) is a bookkeeping bundle of projection-noncommutation residuals (ratios/closures), e.g.
\[
\left(
-\overline{\frac{1}{e n_e}\nabla_3 p_e}
+\frac{1}{e\,\overline{n}}\nabla_3\overline{p_e}
\right)
+
\left(
\overline{\frac{1}{e n_e}\mathbf{R}_e}
-\eta\,\overline{\mathbf{J}}
\right)
-\frac{m_e}{e}\left(\overline{D_t^{(4)}\mathbf{v}_e}-\mathcal{I}_e\right)
+\cdots.
\]

**Interpretation:** \(\boldsymbol{\mathcal{E}}_{\rm topo}\) plays the structural role that “\(\eta \mathbf{J}\)” plays in resistive MHD (it enters through a curl in the induction equation), but it corresponds to **export into transverse degrees of freedom** rather than heating.

### 10.5 Brane induction equation with topology EMF
Projected Faraday:
\[
\partial_t \overline{\mathbf{B}}=-\nabla_3\times\overline{\mathbf{E}}.
\]
Substituting the brane Ohm form yields:
\[
\boxed{
\partial_t\overline{\mathbf{B}}
=
\nabla_3\times(\overline{\mathbf{v}}\times\overline{\mathbf{B}})
-\nabla_3\times\left[
\frac{\overline{\mathbf{J}}\times\overline{\mathbf{B}}}{e\,\overline{n}}
-\frac{1}{e\,\overline{n}}\nabla_3\overline{p_e}
+\eta\,\overline{\mathbf{J}}
-\frac{m_e}{e}\mathcal{I}_e
+\boldsymbol{\mathcal{E}}_{\rm topo}
\right]
+\cdots.
}
\]
A reconnection/topology proxy is the parallel component
\[
\overline{E}_\parallel
=
\frac{\overline{\mathbf{E}}\cdot\overline{\mathbf{B}}}{|\overline{\mathbf{B}}|}
\sim
\left(\eta\,\overline{\mathbf{J}}-\frac{m_e}{e}\mathcal{I}_e+\boldsymbol{\mathcal{E}}_{\rm topo}+\cdots\right)\cdot\frac{\overline{\mathbf{B}}}{|\overline{\mathbf{B}}|},
\]
showing that \(\overline{E}_\parallel\) can arise even when \(\eta=0\).

---

## 11) Transverse-mode (Hermite/KK) machinery for Gaussian localization

This is the formal basis for the “3D×modes” solver and for computable finite-width corrections.

### Sturm–Liouville eigenproblem induced by \(Z(w)\)
In source-free regions (and an appropriate hyperbolic gauge), brane components separate as:
\[
\Box_4 A_\mu + \frac{1}{Z(w)}\frac{d}{dw}\!\left(Z(w)\frac{dA_\mu}{dw}\right)=0,
\qquad \Box_4=-\partial_t^2+\Delta_3.
\]
Mode expansion:
\[
A_\mu(x,w)=\sum_{n\ge 0} a_\mu^{(n)}(x)\,f_n(w),
\]
with eigenfunctions satisfying
\[
-\frac{d}{dw}\!\left(Z(w)\frac{df_n}{dw}\right)=m_n^2\,Z(w)\,f_n(w).
\]
Inner product induced by the action:
\[
\langle f,g\rangle_Z=\int Z(w) f(w)g(w)\,dw.
\]

### Gaussian soft wall → Hermite spectrum
For
\[
Z(w)=\exp\!\left(-\frac{w^2}{\lambda^2}\right),
\]
solutions are Hermite polynomials:
\[
f_n(w)=H_n\!\left(\frac{w}{\lambda}\right),
\qquad
m_n^2=\frac{2n}{\lambda^2},
\qquad n=0,1,2,\ldots
\]
- \(n=0\) is the massless Maxwell mode.
- \(n\ge 1\) are massive Proca-like 3+1 modes with masses set by \(\lambda\).

Norm:
\[
\|f_n\|_Z^2=\int e^{-w^2/\lambda^2}H_n(w/\lambda)^2\,dw
=\lambda\sqrt{\pi}\,2^n n!.
\]
Orthonormal basis:
\[
\phi_n(w)=\frac{H_n(w/\lambda)}{\sqrt{\lambda\sqrt{\pi}\,2^n n!}},
\qquad \langle \phi_n,\phi_m\rangle_Z=\delta_{nm}.
\]

### Brane coupling weights and parity selection
For strictly brane-localized sources \(J_\mu(x,w)=J_{b,\mu}(x)\delta(w)\), mode coupling is controlled by
\[
c_n\equiv \frac{f_n(0)^2}{\|f_n\|_Z^2}.
\]
Hermite parity implies:
\[
H_n(0)=0\ \text{for odd }n\quad\Rightarrow\quad c_{2m+1}=0.
\]
Even-mode closed form:
\[
c_{2m}=\frac{1}{\lambda\sqrt{\pi}}\frac{1}{4^m}\binom{2m}{m},
\qquad
c_0=\frac{1}{\lambda\sqrt{\pi}}=\frac{1}{Z_{\rm int}}.
\]

### Effective 3+1 mode equations and propagator
Mode wave equation (schematic):
\[
(\Box_4+m_n^2)a_\mu^{(n)}(x)=\mu_0\,J_\mu^{(n)}(x)+\text{(gauge-driver terms)},
\]
with
\[
J_\mu^{(n)}(x)=\frac{1}{\|f_n\|_Z^2}\int Z(w)f_n(w)J_\mu(x,w)\,dw.
\]
Effective brane propagator:
\[
D_{\rm eff}(k^2)=\sum_{n\ge 0}\frac{c_n}{k^2-m_n^2+i\epsilon}.
\]

### Coulomb law + Yukawa tower (static limit)
For a point charge \(q\) on the brane:
\[
A_0(r)=\frac{\mu_0 q}{4\pi r}\sum_{n\ge 0}c_n e^{-m_n r},
\qquad r=|\mathbf{x}|.
\]
Zero-mode piece reproduces Coulomb with \(\mu_0^{\rm eff}=\mu_0 c_0=\mu_0/Z_{\rm int}\); massive modes add Yukawa corrections at \(r\sim \lambda\).

---

## 12) Energy and helicity budgets with projection (explicit leakage + covariance reservoirs)

This is the ledger machinery supporting the “topology export” interpretation.

### 12.1 Projection identities and Reynolds-style decomposition in \(w\)
Projection commutes with \(t\) and brane derivatives:
\[
\overline{\partial_t Q}=\partial_t\overline{Q},\qquad \overline{\partial_a Q}=\partial_a\overline{Q},
\]
but not with \(\partial_w\):
\[
\overline{\partial_w Q}
=
\Big[WQ\Big]_{-\infty}^{+\infty}
-\int W'(w)Q\,dw.
\]
Define fluctuations:
\[
Q'=Q-\overline{Q},\qquad \overline{Q'}=0,
\]
so products satisfy:
\[
\overline{QR}=\overline{Q}\,\overline{R}+\overline{Q'R'}.
\]
The covariance \(\overline{Q'R'}\) is the exact “unresolved transverse structure” reservoir.

### 12.2 Bulk EM energy and Poynting flux (localized Maxwell)
Energy density:
\[
u_{\rm EM}
=
\frac{Z(w)}{2\mu_0}\left(|\mathbf{E}|^2+E_w^2+|\mathbf{B}|^2+|\mathbf{C}|^2\right),
\]
where \(\mathbf{E}=(E_x,E_y,E_z)\), \(\mathbf{B}=\nabla_3\times\mathbf{A}\), \(\mathbf{C}=(C_x,C_y,C_z)\).

4D Poynting flux:
\[
S_{\rm EM}^A=\frac{Z(w)}{\mu_0}E_B F_{BA}.
\]
Component split:
\[
S_{\rm EM}^a=\frac{Z}{\mu_0}\Big[(\mathbf{E}\times\mathbf{B})_a - E_w C_a\Big],
\qquad
S_{\rm EM}^w=\frac{Z}{\mu_0}\,\mathbf{E}\cdot\mathbf{C}.
\]
Bulk energy identity:
\[
\partial_t u_{\rm EM}+\partial_A S_{\rm EM}^A = -J^A E_A = -(J^aE_a+J^wE_w).
\]
So \(J^wE_w\) is an explicit scalar-photon work channel, and \(S_{\rm EM}^w\) is explicit Poynting transport along \(w\) enabled by mixed structure \(\mathbf{C}\).

### 12.3 Projected (brane) EM energy budget and explicit \(w\)-leakage
Projecting yields:
\[
\partial_t\overline{u_{\rm EM}}+\partial_a\overline{S_{\rm EM}^a}
=
-\overline{J^A E_A}
+\mathcal{L}_{\rm EM}^{(w)},
\]
where the transverse leakage power density is
\[
\mathcal{L}_{\rm EM}^{(w)}
\equiv
-\int W\,\partial_w S_{\rm EM}^w\,dw
=
-\Big[W S_{\rm EM}^w\Big]_{-\infty}^{+\infty}
+\int W'(w)S_{\rm EM}^w\,dw.
\]
Thus, brane-measured EM energy can change due to flux across the measurement kernel in \(w\) even if bulk energy is conserved.

### 12.4 Resolved vs projected energy (covariance energy reservoir)
A brane-only model would often use a “resolved” energy built from projected fields, e.g.
\[
u_{\rm EM}^{\rm (res)}(\mathbf{x})
\equiv
\frac{1}{2\mu_0^{\rm eff}}\left(|\overline{\mathbf{E}}|^2+|\overline{\mathbf{B}}|^2\right).
\]
But \(\overline{u_{\rm EM}}\neq u_{\rm EM}^{\rm(res)}\) in general; their difference is a computable covariance/mode-energy reservoir (energy stored in \(n\ge 1\) modes and in the mixed sector \((E_w,\mathbf{C})\)).

### 12.5 Magnetic helicity: projected vs resolved and “subscale helicity”
At fixed \(w\), standard helicity identity:
\[
\partial_t(\mathbf{A}\cdot\mathbf{B})
+\nabla_3\cdot(\Phi\,\mathbf{B}+\mathbf{E}\times\mathbf{A})
=
-2\,\mathbf{E}\cdot\mathbf{B},
\qquad \Phi=A_0.
\]
Projected helicity density/flux:
\[
\overline{h}\equiv \overline{\mathbf{A}\cdot\mathbf{B}},
\qquad
\overline{\mathbf{F}}_h\equiv \overline{\Phi\,\mathbf{B}+\mathbf{E}\times\mathbf{A}},
\]
gives:
\[
\partial_t\overline{h}+\nabla_3\cdot\overline{\mathbf{F}}_h = -2\,\overline{\mathbf{E}\cdot\mathbf{B}}.
\]
Resolved helicity built from projected fields:
\[
h_{\rm res}=\overline{\mathbf{A}}\cdot\overline{\mathbf{B}},
\qquad
\partial_t h_{\rm res}+\nabla_3\cdot\mathbf{F}_{h,{\rm res}}=-2\,\overline{\mathbf{E}}\cdot\overline{\mathbf{B}}.
\]
Define **subscale (transverse-structure) helicity**:
\[
h_{\rm sub}\equiv \overline{h}-h_{\rm res}=\overline{\mathbf{A}'\cdot\mathbf{B}'}.
\]
It obeys the exact transfer equation:
\[
\partial_t h_{\rm sub}+\nabla_3\cdot\mathbf{F}_{h,{\rm sub}}
=
-2\Big(\overline{\mathbf{E}\cdot\mathbf{B}}-\overline{\mathbf{E}}\cdot\overline{\mathbf{B}}\Big)
=
-2\,\overline{\mathbf{E}'\cdot\mathbf{B}'}.
\]
**Interpretation:** brane-resolved helicity can evolve because helicity is transferred into transverse structure (higher modes / mixed sector), even without collisional dissipation.

---

## 13) Computation plan (massive simulations)

Two complementary solver families are proposed.

### 13.1 Direct 4D-grid solver
- Discretize \((x,y,z,w)\) explicitly.
- Evolve potentials \(A_M\) with a hyperbolic gauge driver.
- Plasma representation options: 4D two-fluid, GNLS fields, or kinetic Vlasov/PIC.

Purpose: ground truth + validation for reduced solvers.

### 13.2 3D×modes solver (recommended for “massive” runs)
Represent \(w\)-dependence in a truncated Hermite basis (Gaussian \(Z\)):
\[
A_M(t,\mathbf{x},w)\approx \sum_{n=0}^{N_w-1} a_M^{(n)}(t,\mathbf{x})\,\phi_n(w),
\qquad m_n^2=\frac{2n}{\lambda^2}.
\]
Key property: linear operators are diagonal in mode index (wave operator + mass term), so propagation is embarrassingly parallel over modes.

Nonlinear couplings (currents, products) are handled pseudo-spectrally in \(w\) using quadrature nodes \(w_q\):
- reconstruct fields at nodes,
- compute nonlinear products pointwise,
- project back to modes by quadrature.

### 13.3 Coupling algorithm (typical timestep outline)
At each timestep:
1. (Mode solver) reconstruct fields at \(w_q\).
2. Advance plasma (two-fluid / GNLS split-step / PIC push).
3. Deposit/compute charge-current \(J^M\) (charge-conserving deposition for PIC).
4. Advance Maxwell in potentials.
5. Apply gauge/constraint control.
6. Compute brane observables \(\overline{(\cdot)}\) and leakage diagnostics.

### 13.4 Diagnostics for topology/reconnection
The paper emphasizes recording:
- bulk global energy \(\mathcal{E}_{\rm tot}(t)\),
- mode energy spectrum \(E^{(n)}_{\rm EM}\) (for \(n\ge 1\) excitation),
- scalar-photon channel energy and work \(J^wE_w\),
- leakage sources \(S_{\rm leak}^{(s)}\) and integrated exchange over regions,
- brane proxies like \(E_\parallel\), helicity change, and the computed \(\boldsymbol{\mathcal{E}}_{\rm topo}\).

Convergence is “4D-converged” when brane fields converge in \((x,y,z)\) **and** leakage/mode spectra stabilize under increasing \(N_w\) (or \(w\)-grid fidelity).

---

## 14) Validation plan (what to test)

### Controlled-limit benchmarks (MHD/Maxwell regression)
Run with:
\[
\partial_w(\cdot)\approx 0,\quad A_w\approx 0,\quad F_{\mu w}\approx 0,\quad J^w\approx 0,
\quad N_w=1.
\]
Verify:
- Maxwell: vacuum waves, Coulomb solution, charge conservation, Gauss constraints.
- Two-fluid/MHD waves: Alfvén, fast/slow magnetosonic, (optional) whistler/Hall dispersion.
- Standard MHD benchmarks: Brio–Wu shock tube, Orszag–Tang vortex, field-loop advection, etc.

### Beyond-MHD tests (4D effects)
Key tests include:
- **Scalar-photon channel:** vacuum \(A_w\) pulse propagation; matter response to imposed \(E_w\) producing \(v_w\) drift and measurable leakage.
- **Leakage identity closure:** verify \(\partial_t\overline{\rho_s}+\partial_a\overline{j_s^a}=S_{\rm leak}^{(s)}\) holds discretely.
- **Finite localization / tower:** validate Coulomb + Yukawa form for a brane point source; observe mode excitation vs gradient thickness \(\sim \lambda\).
- **Reconnection via topology export:** compare controlled-limit run vs full 4D-interaction run; require “ledger closure” (reconnected flux correlates with \(S_{\rm leak}\), \(J^wE_w\), mixed-sector energy growth, and/or transfer into higher modes), not just numerical diffusion.

Acceptance criteria emphasize:
- exact projected identities holding discretely,
- bulk energy conservation when collisions are off,
- convergence of leakage and mode spectra with increased transverse fidelity.

---

## 15) Geometry DOFs coupled to plasma loads (appendix-level extension)

The model can include low-dimensional geometry variables \(\Theta^I(t)\) (e.g. throat radius \(a(t)\), extent \(L(t)\), or directly the EM localization width \(\lambda(t)\)) that parameterize \(Z(w;\Theta)\) and/or matter confinement \(V_{\rm conf}(\cdot;\Theta)\).

### Geometry Lagrangian (collective-coordinate closure)
\[
\mathcal{L}_{\rm geom}
=
\frac12 M_{IJ}\dot{\Theta}^I\dot{\Theta}^J
-
E_{\rm geom}(\Theta)
-
E_{\rm ratio}(\Theta),
\]
with optional ratio penalty (for \(\Theta=(a,L)\)):
\[
E_{\rm ratio}(a,L)=\frac{\kappa}{2}(L-\alpha a)^2.
\]

### Forces from total Hamiltonian (ledger definition)
Let
\[
H_{\rm tot}=H_{\rm EM}[A;\Theta]+H_{\rm mat}[\text{matter};\Theta]+E_{\rm geom}(\Theta)+E_{\rm ratio}(\Theta).
\]
Define generalized force:
\[
F_I\equiv -\frac{\partial H_{\rm tot}}{\partial \Theta^I}.
\]
EM loading contribution (if only \(Z\) depends on \(\Theta\)):
\[
F_I^{\rm (EM)}
=
-\int d^3x\,dw\,
\frac{\partial_{\Theta^I}Z(w;\Theta)}{2\mu_0}\left(E_AE_A+\frac12 F_{AB}F_{AB}\right).
\]
Matter loading typically enters through \(V_{\rm conf}\):
\[
F_I^{\rm (mat)}\sim -\sum_s\int d^3x\,dw\,\rho_s\,\partial_{\Theta^I}V_{\rm conf}(\mathbf{x},w;\Theta),
\]
(with the equivalent phase-space form for kinetic matter).

### Geometry dynamics (simulation-friendly)
A baseline damped evolution law:
\[
M_{IJ}\ddot{\Theta}^J+\Gamma_{IJ}\dot{\Theta}^J=F_I,
\]
with overdamped and quasi-static limits as controlled sub-regimes.

---

## 16) What you should carry forward as “the essence” for later reasoning

1. **Two kernels, two roles:** \(Z(w)\) shapes bulk EM dynamics; \(W(w)\) defines brane observables and produces exact leakage/covariance terms.
2. **Bulk is conservative, brane is open:** projected balances acquire explicit leakage \(S_{\rm leak}\) and covariance reservoirs.
3. **MHD is recovered in a controlled limit:** suppress \(A_w\), \(F_{\mu w}\), \(J^w\), and transverse structure; then 3+1 Maxwell + two-fluid + MHD emerge with \(\mu_0\to\mu_0^{\rm eff}\).
4. **Beyond-MHD is not a “closure guess” here:** it is the computable, diagnosable consequence of retaining
   - mixed-sector fields \(E_w,\mathbf{C}\),
   - transverse drift \(v^w\) and \(J^w\),
   - and finite-\(\lambda\) transverse modes.
5. **Key brane non-ideality object:** the **topology EMF** \(\boldsymbol{\mathcal{E}}_{\rm topo}\), which enters generalized Ohm’s law and the induction equation and can drive reconnection-like behavior with bulk energy conservation.
6. **Ledger closure is the scientific test:** brane topology change must correlate with energy/helicity transport into \(w\)/modes (and with explicit leakage and \(J^wE_w\)) rather than being attributed solely to resistive heating.
