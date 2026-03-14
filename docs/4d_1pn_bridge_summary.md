4d_1pn_bridge.tex — Comprehensive summary (Paper 8 / “bridge” paper)

## 0) What this paper is doing in the series

This document is a **derivation supplement** to the unified **4D-spatial (3+1 brane + 1 bulk coordinate w)** action-based toy model introduced in `4d.tex`. Its narrow goal is to **remove phenomenological “knobs”** that appeared in earlier brane-facing effective descriptions (Papers I–VI) by showing which of those coefficients are **forced by**:

1. **Geometry/topology** of the defect as a *w*-extended throat (vs a compact 4D bubble),
2. **Weak-field optical consistency** (refraction/bending/Shapiro) → fixes the EOS *exponent*,
3. **1PN/EIH matching** of the velocity-dependent two-body interaction tensors, plus
4. **Wave-supported inertial mass** → reproduces special-relativistic kinematics.

The paper also makes a second, structural contribution:

- It restates the **controlled brane reduction** viewpoint: brane physics is obtained by an explicit **projection/measurement map**, not by imposing stitched boundary conditions. The reduction is organized so that every obstruction to a closed 3D theory (leakage, extra stress, mode-mixing, resonances) is **explicit** and can be tested/closed later.

Finally, it identifies what **remains undetermined** (response/compliance and open-system coupling operators) and gives a **minimal derivation program** for computing them *within the same 4D model*.

---

## 1) “Headline” derived values (carry-forward constants)

Within the assumptions stated in each section, the following are **fixed** (non-tunable):

### 1.1 Added-mass coefficient (topology discriminator)

- **Throat uniform in w** (topology \(S^2 \times \mathbb{R}_w\) for a brane-tangent translation):
  \[
  \kappa_{\rm add}=\frac{1}{2}.
  \]
- **Counterfactual 4D bubble** (compact \(B^4\) defect):
  \[
  \kappa_{\rm add}^{(B^4)}=\frac{1}{3}.
  \]

Interpretation: \(\kappa_{\rm add}=1/(d_{\rm eff}-1)\), where \(d_{\rm eff}\) is the number of spatial directions in which the **exterior potential flow** must rearrange.

### 1.2 Weak-field optics fixes the EOS exponent

- Barotropic polytrope \(P(\rho)=K_{\rm EOS}\rho^n\).
- Matching the **weak-field refractive coefficient** required by bending + Shapiro fixes:
  \[
  n=5.
  \]

### 1.3 1PN/EIH vector-interaction sector constants

A moving defect’s far-field “wake” basis yields velocity-dependent pair couplings. Matching the EIH cross-velocity tensors gives a one-parameter family, but the thermodynamic identity implied by \(n=5\) collapses the family to a unique point:

\[
\alpha^2=\frac{3}{4}, \qquad a_H=0, \qquad K_{\rm vec}=\frac{2}{\pi^2}.
\]

Here:
- \(\alpha^2\) = longitudinal/compressible wake-mixing weight,
- \(a_H\) = helical transverse admixture parameter (parity-even sector depends on \(a_H^2\)),
- \(K_{\rm vec}\) = dimensionless normalization of the overlap/interaction functional **(not** the EOS constant).

### 1.4 Wave-supported mass reproduces special-relativistic kinematics

If defect rest mass is **trapped wave energy** of a mode with linear dispersion \(\omega=c|\mathbf{k}|\), then a boosted trapped mode yields

\[
E(v)=\gamma(v)E_0,
\qquad
p=\gamma m_0 v,
\qquad
\gamma=\frac{1}{\sqrt{1-v^2/c^2}}.
\]

In particular the low-velocity expansion fixes the **universal** \(v^4\) coefficient

\[
\gamma = 1+\frac{1}{2}\beta^2+\frac{3}{8}\beta^4+\cdots,
\qquad
\beta=v/c.
\]

### 1.5 Conditional (protocol-dependent) but *one explicit closure is given*

- The paper emphasizes \(\kappa_{\rm PV}\) is generally a **response coefficient** (protocol- and possibly frequency-dependent).
- However it provides **one explicit adiabatic 1-DOF closure** (declared assumptions) that yields:
  \[
  \kappa_{\rm PV}=\frac{3}{2},
  \qquad
  E_w:E_f:E_{\rm PV}=11:2:5,
  \qquad
  \frac{d\ln a}{d\ln\rho}=-\frac{57}{64}.
  \]
Under this closure, the 1PN “precession ledger” becomes
\[
\beta_{\rm 1PN}=\kappa_\rho+\kappa_{\rm add}+\kappa_{\rm PV}=1+\frac{1}{2}+\frac{3}{2}=3.
\]

---

## 2) Minimal dictionary of the unified 4D model used by this paper

This paper is “downstream” of `4d.tex`, but it restates the minimum set of definitions required for the derivations.

### 2.1 Coordinates, fields, indices

- Spacetime: \(X^M=(t,x,y,z,w)\).
- Bulk spatial coordinates: \(\mathbf{X}=(x,y,z,w)\in\mathbb{R}^4\).
- Bulk spatial gradient: \(\nabla_4=(\partial_x,\partial_y,\partial_z,\partial_w)\).

**Dynamical variables:**
\[
(\psi(\mathbf{X},t),\; A_M(\mathbf{X},t),\; a(t),\; L(t)).
\]
- \(\psi\): complex order parameter; \(\rho=|\psi|^2\).
- \(A_M\): optional genuine (4+1)D gauge field.
- \(a(t),L(t)\): reduced geometric DOFs representing throat “radius” and “length”.

### 2.2 Matter sector: gauged 4D GNLS and stiff EOS ladder

EOS (ultimately forced to \(n=5\) by optics):
\[
P(\rho)=K_{\rm EOS}\rho^5.
\]

Action-level thermodynamic identities:
\[
h(\rho)=\frac{dU}{d\rho},
\qquad
P(\rho)=\rho\,h(\rho)-U(\rho).
\]

For \(P=K_{\rm EOS}\rho^5\):
\[
U(\rho)=\frac{K_{\rm EOS}}{4}\rho^5,
\qquad
h(\rho)=\frac{5K_{\rm EOS}}{4}\rho^4.
\]

Gauge-covariant derivatives:
\[
D_t=\partial_t+\frac{i q}{\hbar}A_0,
\qquad
D_i=\partial_i-\frac{i q}{\hbar}A_i.
\]

Bulk GNLS equation:
\[
i\hbar D_t\psi
=
\left[
-\frac{\hbar^2}{2m}D_iD_i
+V_{\rm conf}(\mathbf{X};a,L)
+h(\rho)
\right]\psi.
\]

Current and exact continuity:
\[
j^i=\frac{\hbar}{m}\Im(\psi^\ast D^i\psi),
\qquad
\partial_t\rho+\partial_i j^i=0
\quad (i\in\{x,y,z,w\}).
\]

### 2.3 Madelung/hydrodynamic form and vorticity–gauge identity

Madelung transform:
\[
\psi=\sqrt{\rho}\,e^{i\theta}.
\]

Gauge-invariant velocity:
\[
v_i=\frac{\hbar}{m}\partial_i\theta-\frac{q}{m}A_i.
\]

Quantum potential:
\[
Q(\rho)=-\frac{\hbar^2}{2m}\frac{\nabla_4^2\sqrt{\rho}}{\sqrt{\rho}}.
\]

Euler-like momentum equation (structural):
\[
m(\partial_t+v_j\partial_j)v_i
=
q(E_i+v_j B_{ij})-\partial_i\big(V_{\rm conf}+h(\rho)+Q(\rho)\big).
\]

Field strength pieces:
\[
E_i=-\partial_tA_i-\partial_iA_0,
\qquad
B_{ij}=\partial_iA_j-\partial_jA_i.
\]

Vorticity identity from minimal coupling:
\[
\Omega_{ij}\equiv \partial_i v_j-\partial_j v_i
=
-\frac{q}{m}B_{ij}.
\]

### 2.4 Gauge sector (if enabled): localized Maxwell + neutrality bookkeeping

Maxwell Lagrangian with localization profile \(Z(w)\):
\[
\mathcal{L}_{\rm EM}=
-\frac{1}{4\mu_0}Z(w)F_{MN}F^{MN}-\frac{1}{2\xi\mu_0}(\partial_MA^M)^2
+ A_N J^N_{\rm ext}.
\]

Field equation:
\[
\partial_M\big(Z(w)F^{MN}\big)+\frac{1}{\xi}\partial^N(\partial\cdot A)
=
\mu_0(J_{\rm ch}^N+J_{\rm ext}^N).
\]

Matter charge current from minimal coupling uses the GNLS current; the charge density is defined with a neutralizing background (“jellium”):
\[
J^0_{\rm ch}=q(|\psi|^2-\rho_0).
\]

### 2.5 Geometry through confinement and generalized forces

Geometry enters through a smooth confinement potential \(V_{\rm conf}(\mathbf{X};a,L)\), plus a symbolic geometric energy \(E_{\rm geom}(a,L)\).

Matter contribution to generalized forces is Hellmann–Feynman:
\[
F_a^{(\psi)}=-\frac{\partial H_\psi}{\partial a}
=-\int d^4X\,\rho\,\partial_a V_{\rm conf},
\qquad
F_L^{(\psi)}=-\int d^4X\,\rho\,\partial_L V_{\rm conf}.
\]

Geometry closure options:
- Static equilibrium: \(\partial_{a,L}H_{\rm tot}=0\).
- Dynamic “breathing” law (symbolic):
\[
M_{ab}\ddot q^b+C_{ab}\dot q^b=-\frac{\partial H_{\rm tot}}{\partial q^a},
\qquad q^a=(a,L).
\]

### 2.6 Brane observables via projection (open-system structure)

A brane observer accesses \((x,y,z)\) only, so brane observables are defined by a fixed **projection weight** \(W(w)\ge 0\) localized near \(w=0\). With finite window \(|w|\le W_{\rm proj}\) and normalized weight \(\widetilde{W}\),

\[
\mathcal{P}_W[f](x,y,z,t)=\int_{-W_{\rm proj}}^{W_{\rm proj}}\widetilde{W}(w)\,f(x,y,z,w,t)\,dw.
\]

Define:
\[
\rho_{\rm brane}=\mathcal{P}_W[\rho],
\qquad
\mathbf{J}_{\rm brane}=\mathcal{P}_W[(j^x,j^y,j^z)].
\]

Exact projected continuity (open system):
\[
\partial_t\rho_{\rm brane}+\nabla_3\cdot \mathbf{J}_{\rm brane}=S_\rho,
\]
with **leakage/source**:
\[
S_\rho=
-\Big[\widetilde{W}\,J_w\Big]_{-W_{\rm proj}}^{+W_{\rm proj}}
+\int_{-W_{\rm proj}}^{W_{\rm proj}}\widetilde{W}'(w)\,J_w\,dw,
\qquad
J_w=j^w.
\]

---

## 3) Added mass: why \(\kappa_{\rm add}=1/2\) for a w-uniform throat

### 3.1 Regime assumptions

This derivation assumes a **quasi-static, low-Mach, irrotational exterior** flow:

- incompressible: \(\nabla\cdot \mathbf{v}=0\),
- irrotational: \(\nabla\times\mathbf{v}=0\),
- hence \(\mathbf{v}=\nabla\phi\) with \(\nabla^2\phi=0\) in the exterior.

Define displaced mass:
\[
M_{\rm disp}=\rho_0 V_{\rm exc},
\]
and **added mass**:
\[
M_{\rm add}=\kappa_{\rm add}M_{\rm disp}.
\]

### 3.2 General d-dimensional ball result

For a translating \(d\)-ball of radius \(a\), the dipole (\(\ell=1\)) harmonic gives
\[
\kappa_{\rm add}(d)=\frac{1}{d-1}.
\]
In particular:
\[
\kappa_{\rm add}(3)=\frac{1}{2},
\qquad
\kappa_{\rm add}(4)=\frac{1}{3}.
\]

### 3.3 Applying to the defect: throat vs bubble

- **Throat** (uniform along \(w\)): choose \(\phi(x,y,z,w)=\phi_3(x,y,z)\), so \(\nabla_4^2\phi=\nabla_3^2\phi_3\).
  Each \(w\)-slice is the usual 3D sphere problem, energy is extensive in \(L\), and the coefficient is exactly
  \[
  \kappa_{\rm add}^{\rm(throat)}=\frac{1}{2}.
  \]
- **Bubble** (compact 4D \(B^4\)): the exterior flow is genuinely 4D, giving
  \[
  \kappa_{\rm add}^{(B^4)}=\frac{1}{3}.
  \]

**Key point:** \(\kappa_{\rm add}\) is fixed by exterior geometry/topology and is independent of EOS, gauge sector, or internal support mechanism.

---

## 4) Optics: refractive coefficient fixes EOS exponent \(n\)

### 4.1 Acoustic-optics dictionary

Define refractive index in terms of a spatially varying signal speed:
\[
N(\mathbf{x})=\frac{c_0}{c_s(\mathbf{x})},
\]
with \(c_s\to c_0\) as \(r\to\infty\).

For polytropic EOS \(P(\rho)=K_{\rm EOS}\rho^n\),
\[
c_s^2(\rho)=\frac{dP}{d\rho}=nK_{\rm EOS}\rho^{n-1}.
\]
Define background \(\rho_0\) via
\[
c_0^2=nK_{\rm EOS}\rho_0^{n-1}.
\]

For small density contrast \(\delta=(\rho-\rho_0)/\rho_0\), one finds
\[
\frac{\Delta c_s}{c_0}\simeq \frac{n-1}{2}\delta,
\qquad
N\simeq 1-\frac{n-1}{2}\delta.
\]
Define the single optical coefficient
\[
\alpha_n\equiv \frac{n-1}{2}.
\]

### 4.2 Weak-field density profile: \(\delta\simeq \Phi/c_0^2\)

Assume weak-field static barotropic balance:
\[
\frac{1}{\rho}\frac{dP}{dr}=\frac{d\Phi}{dr}.
\]
For \(\Phi(r)=-GM/r\), linearization yields
\[
\frac{\Delta\rho}{\rho_0}\simeq \frac{\Phi(r)}{c_0^2}=-\frac{GM}{c_0^2 r}.
\]

### 4.3 Index profile and the unique exponent selection

Substitute into \(N(\delta)\):
\[
N(r)\simeq 1-\frac{n-1}{2}\frac{\Phi(r)}{c_0^2}
=1+\frac{n-1}{2}\frac{GM}{c_0^2 r}
=1+\alpha_n\frac{GM}{c_0^2 r}.
\]

The required GR-matching weak-field coefficient is
\[
N_{\rm GR}(r)\simeq 1+2\frac{GM}{c^2 r}
\quad(r\gg r_H),
\]
and identifying \(c_0\leftrightarrow c\) yields
\[
\alpha_n=2
\quad\Rightarrow\quad
\frac{n-1}{2}=2
\quad\Rightarrow\quad
n=5.
\]

### 4.4 Consistency check: bending and Shapiro depend on the same coefficient

- Deflection for impact parameter \(b\):
  \[
  \Delta\theta_n = \frac{2\alpha_n GM}{b c^2}=\frac{(n-1)GM}{b c^2}.
  \]
  Matching GR \(\Delta\theta=4GM/(bc^2)\) again demands \(\alpha_n=2\Rightarrow n=5\).

- Shapiro delay:
  \[
  \Delta t_n
  =
  \alpha_n\frac{GM}{c^3}\ln\!\left(\frac{4r_E r_R}{b^2}\right),
  \]
  again fixing the same \(\alpha_n\).

### 4.5 Consequence inside the GNLS: nonlinearity is fixed in form

With \(n=5\):
\[
P=K_{\rm EOS}\rho^5,
\qquad
c_s^2=5K_{\rm EOS}\rho^4,
\qquad
h(\rho)=\frac{5K_{\rm EOS}}{4}\rho^4,
\]
so the GNLS nonlinear term is \(h(|\psi|^2)\propto |\psi|^8\).

---

## 5) 1PN interaction sector: deriving \(\alpha^2\) and \(K_{\rm vec}\) from EIH + thermodynamics

### 5.1 The EIH “target” tensor structures

For two defects \(A,B\) with separation unit vector \(\hat{\mathbf{n}}_{AB}\),
the vector-sector pair Lagrangian is written (EIH-inspired) as
\[
L_{\rm vec}^{(AB)}
=
\frac{G m_A m_B}{c^2 r_{AB}}
\left[
C_\parallel\,\mathbf{v}_A\cdot\mathbf{v}_B
+
C_L(\mathbf{v}_A\cdot\hat{\mathbf{n}}_{AB})(\mathbf{v}_B\cdot\hat{\mathbf{n}}_{AB})
+\cdots
\right].
\]

EIH/GR fixes the cross-velocity coefficients:
\[
C_\parallel^{\rm(EIH)}=-\frac{7}{2},
\qquad
C_L^{\rm(EIH)}=-\frac{1}{2}.
\]

### 5.2 Toy-model wake basis yields closed forms for \(C_\parallel\) and \(C_L\)

This paper assumes (from earlier wake/overlap constructions) that the EIH tensor coefficients reduce to
\[
C_\parallel(\alpha,a_H)=K_{\rm vec}\pi^2(-1+a_H^2-\alpha^2),
\qquad
C_L(\alpha,a_H)=K_{\rm vec}\pi^2(-1+a_H^2+\alpha^2).
\]

Here:
- \(\alpha\): longitudinal/compressible contribution,
- \(a_H\): optional helical transverse contribution (parity-even sector depends on \(a_H^2\)),
- \(K_{\rm vec}\): overall normalization of the overlap energy.

### 5.3 EIH matching alone: invariants and a one-parameter family

Take difference and sum:
\[
C_L-C_\parallel = 2K_{\rm vec}\pi^2\alpha^2,
\qquad
C_L+C_\parallel = 2K_{\rm vec}\pi^2(-1+a_H^2).
\]

Impose EIH targets:
\[
3=2K_{\rm vec}\pi^2\alpha^2 \Rightarrow K_{\rm vec}\alpha^2=\frac{3}{2\pi^2},
\]
\[
-4=2K_{\rm vec}\pi^2(-1+a_H^2)\Rightarrow K_{\rm vec}(1-a_H^2)=\frac{2}{\pi^2}.
\]

Hence
\[
\alpha^2(a_H^2)=\frac{3}{4}(1-a_H^2),
\qquad
K_{\rm vec}(a_H^2)=\frac{2}{\pi^2(1-a_H^2)},
\qquad
0\le a_H^2<1.
\]
EIH matching fixes **two invariants** but leaves **one apparent knob** \(a_H^2\).

### 5.4 Thermodynamic closure from the EOS exponent fixes \(\alpha^2\)

Action-level identity for barotropic GNLS fluids:
\[
P=\rho h-U.
\]
For polytrope \(P=K_{\rm EOS}\rho^n\), the compatible internal energy density is
\[
U=\frac{K_{\rm EOS}}{n-1}\rho^n,
\qquad
\frac{U}{P}=\frac{1}{n-1}.
\]

The paper defines a minimal thermodynamic closure for the wake fraction:
\[
\alpha^2_{\rm thermo}=1-\frac{U}{P}=1-\frac{1}{n-1}.
\]

With \(n=5\), this becomes
\[
\alpha^2=\frac{3}{4}.
\]

### 5.5 Collapse of the family → unique point

Combine \(\alpha^2=3/4\) with \(\alpha^2(a_H^2)=\frac{3}{4}(1-a_H^2)\):
\[
\frac{3}{4}=\frac{3}{4}(1-a_H^2)\Rightarrow a_H^2=0.
\]
Then the normalization becomes
\[
K_{\rm vec}=\frac{2}{\pi^2}.
\]

Thus the unique consistent point is:
\[
\boxed{\alpha^2=\frac{3}{4},\quad a_H=0,\quad K_{\rm vec}=\frac{2}{\pi^2}.}
\]

Interpretation: the interaction sector constants are **not free** once the EOS exponent is fixed by optics; they inherit values from the same microphysics.

---

## 6) Special relativity from wave-supported mass

### 6.1 Rest energy from a trapped, massless mode

Assume the defect supports a stable transverse standing mode with characteristic transverse wavenumber \(k_\perp\) and a linear, isotropic dispersion
\[
\omega=c|\mathbf{k}|.
\]
In the defect rest frame, take \(|\mathbf{k}|=k_\perp\), so
\[
\omega_0=ck_\perp,
\qquad
E_0=\hbar\omega_0,
\qquad
m_0=\frac{E_0}{c^2}.
\]

### 6.2 Boosted trapped mode: group velocity must match defect velocity

For a defect moving at speed \(v\) along \(x\), the trapped pattern must be carried with it. Impose the **group velocity matching** condition:
\[
v=\frac{\partial \omega}{\partial k_x}.
\]
With \(\omega=c\sqrt{k_\perp^2+k_x^2}\), this gives
\[
k_x^2=\frac{v^2}{c^2-v^2}k_\perp^2
=\gamma^2\frac{v^2}{c^2}k_\perp^2,
\qquad
\gamma=(1-v^2/c^2)^{-1/2}.
\]
Then
\[
\omega(v)=c\sqrt{k_\perp^2+k_x^2}=\gamma ck_\perp=\gamma\omega_0,
\]
so
\[
E(v)=\hbar\omega(v)=\gamma E_0.
\]

### 6.3 Universal \(v^4\) coefficient

Expand:
\[
E(v)=E_0+\frac{1}{2}\left(\frac{E_0}{c^2}\right)v^2
+\frac{3}{8}\left(\frac{E_0}{c^2}\right)\frac{v^4}{c^2}
+\mathcal{O}(v^6/c^4).
\]
Thus the coefficient \(3/8\) is universal (Taylor coefficient of \(\gamma\)).

### 6.4 Momentum and invariant relation

Using \(p_x=\hbar k_x\) and the expression for \(k_x\),
\[
p=\gamma m_0 v.
\]
Then
\[
E^2-p^2c^2=E_0^2=m_0^2c^4.
\]

### 6.5 Time dilation from phase along the worldline

For a plane-wave phase \(\Phi=k_x x-\omega t\), along \(x=vt\):
\[
\frac{d\Phi}{dt}=k_x v-\omega=-(\omega-vk_x).
\]
With \(\omega=\gamma\omega_0\) and \(k_x=\gamma(v/c^2)\omega_0\),
\[
\omega_{\rm clock}\equiv \omega-vk_x=\frac{\omega_0}{\gamma}.
\]
So internal wave-based clocks tick slower by \(1/\gamma\) in the background frame.

### 6.6 Length contraction from wave-supported rods

A simple “light clock rod” argument: for rod length \(\ell\) along motion, forward/back travel times give
\[
t_\parallel=\frac{\ell}{c-v}+\frac{\ell}{c+v}=\frac{2\ell}{c}\gamma^2.
\]
Time dilation requires \(t_\parallel=\gamma t_0=\gamma(2\ell_0/c)\), forcing
\[
\ell=\frac{\ell_0}{\gamma}.
\]
This is Lorentz–FitzGerald contraction as a **self-consistency condition** for wave-bound matter.

---

## 7) Preferred-frame considerations: what is claimed and what is not

The model’s ontology includes an ambient medium → a distinguished background rest frame exists microscopically. The paper’s stance is:

- **Ontology preferred frame** does *not* automatically imply **operational detectability**.
- In a controlled regime, Lorentz symmetry can be an **emergent operational symmetry** for brane observers built from wave-supported bound states.

### 7.1 Emergent Lorentz structure in the signal sector (controlled regime)

From projected continuity + a longitudinal reduction, linearized longitudinal potential \(\varphi\) satisfies (schematically):
\[
\varphi_{tt}-c^2\nabla^2\varphi = -\frac{c^2}{\rho_0}S_{\rm brane}.
\]
In the free limit \(S_{\rm brane}\to 0\), the wave equation is Lorentz invariant with invariant speed \(c\).

### 7.2 Where preferred-frame effects can re-enter

Preferred-frame signatures can arise through failure of controlled assumptions, including:

1. **Dispersion** beyond linear regime (quantum pressure, nonlinearities) → non-universal cones.
2. **Open-system leakage** (\(S_\rho\neq 0\)) → brane not closed.
3. **Projection-induced stress** (extra stress \(R_{ij}\neq 0\)) from w-structure.
4. **Sector non-universality** (different characteristic speeds across longitudinal, transverse/gauge, geometry modes).
5. **Dissipation/drive/reservoir coupling** selecting time direction and frame.

The paper treats these as explicit, identifiable channels rather than hidden assumptions.

---

## 8) Controlled reduction to brane-effective equations

This paper emphasizes: it does not posit a brane PDE by fiat. Brane physics is obtained via:

- projection \( \mathcal{P}_W \),
- chosen measurement surface \(\Gamma\) and port basis \(\{P_i\}\),
- chosen effort/flux variables.

### 8.1 Effort/flux variables and ports

Effort variable is chosen as enthalpy perturbation:
\[
u=\delta h(\rho_{\rm brane})\approx h'(\rho_{\rm brane,0})\delta\rho_{\rm brane}.
\]
For \(n=5\), \(h'(\rho)=5K_{\rm EOS}\rho^3\).

Given port basis functions \(P_i\) on \(\Gamma\),
\[
u_i(t)=\int_\Gamma \overline{P_i}\,u\,d\mu,
\qquad
j_i(t)=\int_\Gamma \overline{P_i}\,j\,d\mu,
\qquad
j=\mathbf{J}_{\rm brane}\cdot\hat{\mathbf{n}}.
\]
A second diagnostic output is “leakage flux” via \(J_w\) on monitor surfaces \(w=\pm W_{\rm cut}\).

### 8.2 Exact projected continuity and an exact divergence identity

Exact open-system continuity:
\[
\partial_t \rho_{\rm brane}+\nabla_3\cdot\mathbf{J}_{\rm brane}=S_\rho.
\]

Exact identity for \(\nabla\cdot\mathbf{v}_{\rm brane}\) with \(\mathbf{v}_{\rm brane}=\mathbf{J}_{\rm brane}/\rho_{\rm brane}\):
\[
\nabla_3\cdot\mathbf{v}_{\rm brane}
=
\frac{S_\rho-\partial_t\rho_{\rm brane}}{\rho_{\rm brane}}
-\frac{\mathbf{J}_{\rm brane}\cdot\nabla_3\rho_{\rm brane}}{\rho_{\rm brane}^2}.
\]

### 8.3 Projected momentum balance, extra stress, and open-system correction

A projected momentum-flux form:
\[
\partial_t J^{\rm brane}_i+\partial_j\Pi_{ij}
=
F_i^{\rm pot}+F_i^{\rm em}+S_{J_i}.
\]

With
\[
\Pi_{ij}=\int \widetilde{W}(w)\frac{J_iJ_j}{\rho}\,dw,
\]
and momentum-leakage source
\[
S_{J_i}
=
-\Big[\widetilde{W}\frac{J_iJ_w}{\rho}\Big]_{-W_{\rm proj}}^{+W_{\rm proj}}
+\int \widetilde{W}'(w)\frac{J_iJ_w}{\rho}\,dw.
\]

Potential-force term packages enthalpy, confinement, quantum pressure:
\[
F^{\rm pot}_i
=
-\int \widetilde{W}\,\frac{\rho}{m}\,\partial_i\mu_{\rm eff}\,dw,
\qquad
\mu_{\rm eff}=V_{\rm conf}+h(\rho)+Q(\rho).
\]

Define extra stress (projection non-commutativity):
\[
R_{ij}=\Pi_{ij}-\rho_{\rm brane}v^{\rm brane}_iv^{\rm brane}_j.
\]

Acceleration-form identity:
\[
\rho_{\rm brane}(\partial_t+\mathbf{v}_{\rm brane}\cdot\nabla_3)\mathbf{v}_{\rm brane}
=
\mathbf{F}_{\rm tot}
-\nabla_3\cdot\mathbf{R}
-\mathbf{v}_{\rm brane}S_\rho.
\]
The term \(-\mathbf{v}_{\rm brane}S_\rho\) is the characteristic open-system correction.

### 8.4 Minimal w-mode truncation and closure hierarchy

Two-mode Galerkin ansatz:
\[
\psi(\mathbf{x},w,t)\approx \psi_0(\mathbf{x},t)\chi_0(w)+\varepsilon\,\psi_1(\mathbf{x},t)\chi_1(w).
\]

- Separable limit \(\varepsilon=0\): \(J_w\simeq 0\Rightarrow S_\rho\simeq 0\) and \(R_{ij}=0\); brane becomes a closed 3D fluid system.
- Corrections \(\varepsilon\neq 0\) generate \(S_\rho\) and \(R_{ij}\) via mode mixing, controlled by overlap integrals \(M_{nm}\) and \(L_{nm}\) involving \(\widetilde{W}\) and \(\widetilde{W}'\).

### 8.5 Poisson candidate is a regime statement, not an axiom

Helmholtz decomposition:
\[
\mathbf{v}_{\rm brane}=\nabla_3\phi_3+\mathbf{v}_T,
\qquad
\nabla_3\cdot\mathbf{v}_T=0.
\]
Definition:
\[
\nabla_3^2\phi_3=\nabla_3\cdot\mathbf{v}_{\rm brane}.
\]

Under linearized quasi-static assumptions (\(\partial_t\delta\rho\) negligible, products small),
\[
\nabla_3\cdot\mathbf{v}_{\rm brane}\approx \frac{S_\rho}{\rho_0}
\quad\Rightarrow\quad
\rho_0\nabla_3^2\phi_3\approx S_\rho.
\]

Equivalently, linearized acoustics yields forced wave equation:
\[
\partial_t^2\phi_3-\frac{c_{s,0}^2}{m}\nabla_3^2\phi_3
=
-\frac{c_{s,0}^2}{m\rho_0}S_\rho,
\]
whose quasi-static limit recovers the Poisson candidate.

### 8.6 Gauge localization and brane-effective Maxwell sector

If Maxwell action has localization factor \(Z(w)\),
\[
S_{\rm EM}=-\frac{1}{4\mu_0}\int d^4x\,dw\,Z(w)F_{MN}F^{MN},
\]
and gauge field admits a dominant brane-localized mode
\[
A_\mu(x,w)\approx a_\mu(x)f(w),
\qquad
A_w\approx 0,
\]
then integrating over \(w\) yields an effective 3+1 Maxwell action with coupling rescaling
\[
S_{\rm EM}^{\rm eff}\approx -\frac{Z_{\rm int}}{4\mu_0}\int d^4x\,f_{\mu\nu}f^{\mu\nu},
\qquad
Z_{\rm int}=\int dw\,Z(w)|f(w)|^2,
\]
so
\[
\mu_{0,\rm eff}=\frac{\mu_0}{Z_{\rm int}}.
\]

Brane-observed fields are defined by projection:
\[
E_i^{\rm brane}=\mathcal{P}_W[F_{0i}],
\qquad
B_i^{\rm brane}=\frac{1}{2}\epsilon_{ijk}\mathcal{P}_W[F_{jk}],
\qquad i,j,k\in\{x,y,z\}.
\]

---

## 9) Undetermined response coefficients: what remains symbolic, and how to derive them

The paper draws a hard line: **anything representing internal response** of the throat (breathing, relaxation, exchange) depends on a declared protocol/regime and is not “derived” unless that response problem is solved.

### 9.1 The 1PN “precession ledger” and \(\kappa_{\rm PV}\)

Earlier orbital bookkeeping uses:
\[
\beta_{\rm 1PN}=\kappa_\rho+\kappa_{\rm add}+\kappa_{\rm PV}.
\]
- \(\kappa_\rho\): rest-mass normalization (taken as 1 in the standard ledger).
- \(\kappa_{\rm add}\): exterior added mass (derived here as 1/2 for throat).
- \(\kappa_{\rm PV}\): additional inertia due to internal work as geometry responds to environment.

**Key point:** \(\kappa_{\rm PV}\) depends on how geometric DOFs \(q^a=(a,L)\) respond to an external control \(\Xi\) (e.g., ambient density, potential).

### 9.2 Energy-based response framework (generic linear response)

Total energy functional has form:
\[
H_{\rm tot}[\psi,A;q^a;\Xi]=H_{\rm fluid}+H_{\rm wave}+E_{\rm geom}+H_{\rm aux}.
\]
Generalized forces:
\[
F_a=-\frac{\partial H_{\rm tot}}{\partial q^a}.
\]
Equilibrium closure:
\[
\partial_{q^a}H_{\rm tot}=0.
\]
Optional dynamic closure:
\[
M_{ab}\ddot q^b+C_{ab}\dot q^b=-\partial_{q^a}H_{\rm tot}.
\]

Introduce small perturbation parameter \(\epsilon\) describing environmental change. Expand:
\[
H_{\rm tot}(q,\epsilon)=
H_0+H_\epsilon\epsilon+\frac{1}{2}H_{\epsilon\epsilon}\epsilon^2
+\frac{1}{2}K_{ab}\delta q^a\delta q^b+f_a\delta q^a\epsilon+\cdots,
\]
with stiffness matrix \(K_{ab}=\partial_{q^a}\partial_{q^b}H|_0\) and mixed coupling \(f_a=\partial_{q^a}\partial_\epsilon H|_0\).

In the adiabatic regime:
\[
\delta q^a_{\rm ad}=-(K^{-1})^{ab}f_b\,\epsilon+\mathcal{O}(\epsilon^2),
\]
giving an effective energy shift
\[
H_{\rm eff}(\epsilon)
=
H_0+H_\epsilon\epsilon
+\frac{1}{2}\left(H_{\epsilon\epsilon}-f_a(K^{-1})^{ab}f_b\right)\epsilon^2+\cdots.
\]
\(\kappa_{\rm PV}\) is then read off by matching \(H_{\rm eff}\) (and velocity-coupled extensions) to the brane point-particle 1PN Lagrangian.

### 9.3 Explicit one-DOF adiabatic closure that yields \(\kappa_{\rm PV}=3/2\)

This closure is *declared* and conditional; it is included because it demonstrates how a response coefficient can become derived once the protocol is fixed.

**Protocol:**
- External variable: ambient background density \(\rho\) at defect location.
- Use weak-field relation \(\delta\rho/\rho_0\simeq \Phi/c_0^2\).
- Adiabatic: geometry relaxes to minimize an effective rest-energy functional for each \(\rho\).
- Reduce geometry to 1 DOF: \(L=\Lambda a\) with fixed aspect ratio \(\Lambda\).

**Reduced energy model:**
\[
F(a,\rho)=E_w+E_f+E_{\rm PV},
\]
with scalings:
\[
E_w=\frac{\mathcal{C}_w\,c_s(\rho)}{a},
\qquad
E_f=\frac{\mathcal{C}_f}{\rho\,a^2},
\qquad
E_{\rm PV}=\mathcal{C}_{\rm PV}P(\rho)V(a)
=\mathcal{C}_{\rm PV}K_{\rm EOS}\rho^n(\pi\Lambda a^3).
\]
For polytrope \(P=K_{\rm EOS}\rho^n\): \(c_s\propto\rho^{(n-1)/2}\).

**Virial identity from equilibrium \(\partial_aF=0\):**
Given \(a\)-powers \((-1,-2,+3)\),
\[
E_w+2E_f=3E_{\rm PV}.
\]
Define \(x=E_f/E_w\). Then
\[
\frac{E_{\rm PV}}{E_w}=\frac{1+2x}{3},
\qquad
F=E_w\frac{4+5x}{3}.
\]

**Envelope-theorem density slope:**
\[
\frac{d\ln F}{d\ln\rho}
=
\frac{\left(\frac{n-1}{2}\right)E_w+(-1)E_f+nE_{\rm PV}}{F}
=
\frac{\frac{5n-3}{2}+(2n-3)x}{4+5x}.
\]
For \(n=5\):
\[
\frac{d\ln F}{d\ln\rho}=\frac{11+7x}{4+5x}.
\]

**Mapping to \(\kappa_{\rm PV}\):**
Using estimator \(\kappa_{\rm PV}=(d\ln F/d\ln\rho)-\kappa_\rho\) with \(\kappa_\rho=1\), the target \(\kappa_{\rm PV}=3/2\) is equivalent to
\[
\frac{d\ln F}{d\ln\rho}=\kappa_\rho+\kappa_{\rm PV}=\frac{5}{2}.
\]
Solve:
\[
\frac{11+7x}{4+5x}=\frac{5}{2}\Rightarrow x=\frac{2}{11}.
\]

**Universal partition:**
Use virial to obtain
\[
E_w:E_f:E_{\rm PV}=11:2:5,
\qquad
(f_w,f_f,f_{\rm PV})=\left(\frac{11}{18},\frac{2}{18},\frac{5}{18}\right).
\]

**Breathing slope prediction:**
\[
\frac{d\ln a}{d\ln\rho}
=
-\frac{-\frac{n-1}{2}+2x+n(1+2x)}{4+10x}.
\]
For \(n=5,\ x=2/11\):
\[
\frac{d\ln a}{d\ln\rho}=-\frac{57}{64}\approx -0.890625.
\]

**What remains to calibrate even in this closure:**
The absolute scale \(a(\rho_0)\) is not fixed because \(\mathcal{C}_w,\mathcal{C}_f,\mathcal{C}_{\rm PV},\Lambda\) enter multiplicatively; only the dimensionless partition and \(\kappa_{\rm PV}\) are fixed.

### 9.4 Frequency dependence

If the response is not adiabatic, solve the linearized dynamic law to obtain compliance \(\delta q^a(\omega)/\epsilon(\omega)\) and treat
\[
\kappa_{\rm PV}\to \kappa_{\rm PV}(\omega),
\qquad
\kappa_{\rm PV}=\lim_{\omega\to 0}\kappa_{\rm PV}(\omega).
\]

### 9.5 Open-system exchange and the effective mouth operator \(Z^{\rm eff}(\omega)\)

To characterize defect–brane coupling without imposing stitched boundary conditions, define an operational response operator via a drive/measure protocol near the mouth:

- Choose effort variable \(u(\mathbf{s},t)\) (here: enthalpy perturbation),
- Choose measured flux \(j(\mathbf{s},t)\) (e.g., normal brane mass flux on \(\Gamma\), plus optional leakage flux in \(w\)),
- Choose port basis \(\{P_i\}\) on measurement region \(\Gamma\).

Port amplitudes:
\[
u_i(t)=\int_\Gamma \overline{P_i(\mathbf{s})}u(\mathbf{s},t)\,d\mu,
\qquad
j_i(t)=\int_\Gamma \overline{P_i(\mathbf{s})}j(\mathbf{s},t)\,d\mu.
\]

Define the effective operator:
\[
j_i(\omega)=\sum_j Z^{\rm eff}_{ij}(\omega)u_j(\omega).
\]

**Low-frequency locality gate:**
A necessary condition for a local-in-time effective closure is that
\[
Z^{\rm eff}_{ij}(\omega)\sim Z^{(0)}_{ij}+i\omega Z^{(1)}_{ij}+\omega^2 Z^{(2)}_{ij}+\cdots
\]
is stable away from resonances (insensitive to numerical damping, monitoring surfaces, and port conventions). If orbital-relevant frequencies hit sharp resonances, the correct closure is nonlocal (memory).

### 9.6 Symbolic parameters kept in the paper

The paper explicitly keeps symbolic:

- **Units/scale:** \(m,\hbar\) and any global normalization mapping to physical units.
- **Gauge/EM:** \(q,\mu_0\), localization thickness, gauge fixing.
- **Geometry energy:** ambient bulk pressure \(P_{\rm vac}\), surface tension \(\sigma\), higher-order geometric terms.
- **Adiabatic closure normalizations:** \(\Lambda\), \(\mathcal{C}_w,\mathcal{C}_f,\mathcal{C}_{\rm PV}\).
- **Reservoir/dissipation:** chemical-potential coupling, PML/sponge parameters, drive strengths/frequencies.
- **Microphysics calibration:** any geometric correction factors mapping defect geometry → effective mass/charge.

### 9.7 Minimal future-work derivation program

The paper records a modular program:

1. Declare the perturbation variable \(\epsilon\) (how environment enters).
2. Compute equilibria + stiffness \(K_{ab}\) and couplings \(f_a\).
3. Choose response regime (adiabatic elimination vs driven dynamics) → compliance.
4. Match to brane effective 1PN point-particle theory → extract \(\kappa_{\rm PV}\), higher response.
5. Extract \(Z^{\rm eff}(\omega)\) and test locality.
6. Run invariance tests (monitor placement, projection window, damping) to ensure extracted parameters are physical.

---

## 10) Appendices: what they provide and which formulas are most reusable

This paper includes several appendices that “lock down” derivations.

### 10.1 Notation and conventions
- Clarifies symbols, coordinate splits, and the dual “K” notation issue.

### 10.2 Full variational derivations
From the action:
- GNLS equation via \(\delta S/\delta\psi^\ast\).
- Noether current and exact continuity.
- Maxwell with localization via \(\delta S/\delta A_N\).
- Hellmann–Feynman generalized forces in \((a,L)\).
- Madelung transform yielding Euler-like equation and vorticity identity.

### 10.3 Projection identities and leakage source terms
Exact projected continuity and momentum leakage formulas, plus:
- kinematic identities for \(\nabla\cdot\mathbf{v}_{\rm brane}\) and \(\nabla\times\mathbf{v}_{\rm brane}\),
- extra stress \(R_{ij}\),
- open-system Euler form and the \(-\mathbf{v}S_\rho\) term,
- operational leakage monitors \(j_{\rm leak}(t)\).

### 10.4 Added mass computations
- General \(d\)-ball coefficient \(\kappa_{\rm add}=1/(d-1)\).
- Reduction of a w-uniform throat to the 3D sphere result.
- Bubble counterfactual giving \(1/3\).
- Assumptions and expected corrections (compressibility, vorticity shedding, w-nonuniformity, etc.).

### 10.5 EIH matching algebra
- Makes the cross-tensor matching explicit and derives the family + invariants.
- Shows minimal parity-even solution \(a_H=0\) corresponds to \(\alpha^2=3/4,\,K_{\rm vec}=2/\pi^2\).

### 10.6 Standing-wave derivations (SR kinematics)
- Explicit operational derivations of time dilation, length contraction, Michelson–Morley null, and universal \(v^4\) coefficient, all from wave-based rods/clocks supported by a massless mode of speed \(c\).

---

## 11) Parameter ledger: fixed vs symbolic

### Fixed (given stated assumptions)
- \(\kappa_{\rm add}=1/2\) for w-uniform throat; \(\kappa_{\rm add}=1/3\) for 4D bubble counterfactual.
- EOS exponent \(n=5\).
- Vector-sector constants: \(\alpha^2=3/4\), \(a_H=0\), \(K_{\rm vec}=2/\pi^2\).
- SR expansion coefficient \(3/8\) in \(\gamma\).
- Exact projection identities: continuity leakage \(S_\rho\), momentum leakage \(S_{J_i}\), extra stress \(R_{ij}\).

### Symbolic / protocol-dependent
- EOS scale \(K_{\rm EOS}\) after choosing \(c_0,\rho_0\) (units normalization).
- Geometry response parameters: stiffness \(K_{ab}\), masses \(M_{ab}\), damping \(C_{ab}\), energy terms \(E_{\rm geom}\).
- \(\kappa_{\rm PV}\) in general (frequency-dependent response), except in the explicit declared adiabatic closure scenario.
- Effective mouth operator \(Z^{\rm eff}_{ij}(\omega)\) and whether a low-\(\omega\) local closure exists.
- Gauge localization integral \(Z_{\rm int}\) and whether \(F_{\mu w}\) is negligible in a given regime.
- Preferred-frame corrections from dispersion/leakage/stress/sector non-universality/dissipation.

---

## 12) Takeaway for downstream reasoning

If you treat this paper as “inputs for the next papers,” the key operational consequences are:

1. **You should not treat \(n,\kappa_{\rm add},\alpha^2,K_{\rm vec}\) as knobs**: they are linked consequences of geometry + optics + thermodynamics + EIH structure.
2. **Any claim about orbital dynamics beyond that** (especially \(\kappa_{\rm PV}\), strong-field effects, dissipation) must declare a response protocol (adiabatic vs dynamical) and/or compute \(Z^{\rm eff}(\omega)\).
3. The brane theory is intrinsically an **open-system projection** of the 4D conservation law. Leakage and extra stress are not optional embellishments; they are where “gravity-like” brane sources and preferred-frame corrections live.
