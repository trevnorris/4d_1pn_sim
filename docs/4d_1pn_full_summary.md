4d_1pn_full.tex — Comprehensive summary (full conservative 1PN assembly paper)

## 0) What this paper is doing

This paper is the **end-to-end conservative 1PN assembly** for the 4D toy-model program. It takes the exact/action-based machinery of `4d.tex`, imports the coefficient-fixing logic of the intermediate bridge papers, and then shows that the whole **two-body Einstein–Infeld–Hoffmann (EIH) ledger through order \(c^{-2}\)** can be reproduced in one derivation chain.

The paper’s target is the complete conservative two-body 1PN structure:

1. the free-particle quartic kinetic terms \((v^4)\),
2. the **self-sector** terms proportional to \(\Phi v^2/c^2\),
3. the **cross-sector** velocity tensor proportional to
   \(\mathbf v_A\!\cdot\!\mathbf v_B\) and
   \((\mathbf v_A\!\cdot\!\hat{\mathbf n})(\mathbf v_B\!\cdot\!\hat{\mathbf n})\),
4. the **static nonlinear** term proportional to \(G^2/r^2\), and
5. the test-mass orbit reduction giving the standard **perihelion advance**.

The basic architecture is:

- **Exact 4D parent structure** supplies the bulk fields, projection map, exact projected continuity, leakage, and the exact longitudinal identity.
- A **controlled near-zone Poisson hook** produces the brane-facing Newtonian scalar sector.
- A **coherent-defect / small-body worldtube reduction** gives the Newtonian point-particle limit.
- The **self sector** is fixed by scalar mass dressing + optical/barotropic consistency.
- The **static \(G^2/r^2\)** term comes from local mass scaling plus exact pair counting.
- The **cross sector** comes from a constructive isotropic Fourier-space wake basis.
- Topology and one explicit adiabatic internal-response closure give the familiar ledger
  \[
  \beta_{\rm 1PN}=\kappa_\rho+\kappa_{\rm add}+\kappa_{\rm PV}=3.
  \]
- Once those pieces are combined, the final reduced two-body Lagrangian is **exactly equal** to the standard conservative EIH Lagrangian.

The paper is explicit that this is **not** an assumption-free theorem of the fully solved moving-throat PDE problem in the bulk. It is a **full 1PN derivation within a declared closure hierarchy**.

---

## 1) Claim taxonomy (important for later use)

The paper constantly distinguishes four kinds of statements. This is part of the result, not just rhetoric.

### 1.1 Exact

These are identities that follow directly from the declared action, definitions, or algebraic pair counting.

Examples:
- projected continuity with leakage,
- the exact longitudinal identity,
- local pair counting once the reduced ansatz is declared,
- algebraic assembly of the final EIH Lagrangian once all coefficients are supplied.

### 1.2 Controlled reduction

These require explicit regime assumptions, such as:
- quasi-staticity,
- small-body / smooth-external-field scaling,
- low-Mach exterior potential flow,
- isotropic linear far-field wake response.

Examples:
- the Poisson hook,
- the worldtube-to-point-particle reduction,
- \(\kappa_{\rm add}=1/2\) for the \(w\)-uniform throat,
- the wake overlap tensor derivation.

### 1.3 Protocol closure

These depend on a declared internal-response model and are not claimed as exact consequences of kinematics alone.

The central example is:
\[
\kappa_{\rm PV}=\frac32
\]
for the paper’s chosen **adiabatic one-degree-of-freedom breathing closure**.

### 1.4 Full assembly

Once all earlier ingredients are imported, the final equality
\[
L^{\rm derived}_{\rm 1PN}=L^{\rm EIH}_{\rm 1PN}
\]
is exact algebra. The same is true for the test-mass perihelion coefficient once
\(\beta_{\rm 1PN}=3\) is inserted.

---

## 2) Headline outputs / carry-forward constants

This is the shortest “memory table” for the paper.

### 2.1 Newtonian and scalar sector

Newtonian matching of the reduced scalar-dressed particle action fixes
\[
q=1,
\qquad
\kappa_\rho=1.
\]

### 2.2 Optical/barotropic sector

Weak-field optical consistency fixes the EOS exponent in
\[
P(\rho)=K_{\rm EOS}\rho^n
\]
to
\[
n=5.
\]

### 2.3 Universal free kinematics

The free-particle reduced Lagrangian has the standard relativistic/wave-supported quartic term
\[
L_{\rm free}
=
-mc^2+\frac12 mv^2+\frac18 m\frac{v^4}{c^2}+\cdots.
\]
So the 1PN **Lagrangian** coefficient is
\[
\frac18,
\]
while the corresponding **energy** coefficient is the usual
\[
\frac38.
\]

### 2.4 Self-sector pair coefficient

The self-sector coefficient multiplying \((v_A^2+v_B^2)\) in the pair Lagrangian is
\[
+\frac32.
\]
This is obtained in two independent ways:
- directly from scalar + optical dressing, and
- from the ledger
  \(\beta_{\rm 1PN}=\kappa_\rho+\kappa_{\rm add}+\kappa_{\rm PV}\).

### 2.5 Static nonlinear coefficient

The velocity-independent two-body 1PN term is
\[
L_{\rm stat}^{(AB)}
=
-\frac{G^2m_A m_B(m_A+m_B)}{2c^2 r_{AB}^2},
\]
so the static coefficient is
\[
-\frac12.
\]

### 2.6 Added mass / topology

For the actual \(w\)-uniform throat geometry,
\[
\kappa_{\rm add}=\frac12.
\]
For the counterfactual compact 4D bubble,
\[
\kappa_{\rm add}^{(B^4)}=\frac13.
\]
This is treated as a **topology discriminator**, not a tunable inertial coefficient.

### 2.7 Internal breathing closure (protocol-fixed)

Within the declared adiabatic 1-DOF closure,
\[
\kappa_{\rm PV}=\frac32,
\qquad
E_w:E_f:E_{\rm PV}=11:2:5,
\qquad
\frac{d\ln a_*}{d\ln\rho}=-\frac{57}{64}.
\]
Then
\[
\beta_{\rm 1PN}
=\kappa_\rho+\kappa_{\rm add}+\kappa_{\rm PV}
=1+\frac12+\frac32=3.
\]

### 2.8 Wake / cross sector

The parity-even wake parameters are fixed to
\[
\alpha^2=\frac34,
\qquad
a_H=0,
\qquad
K_{\rm vec}=\frac{2}{\pi^2},
\]
which give the EIH cross coefficients
\[
C_\parallel=-\frac72,
\qquad
C_L=-\frac12.
\]

### 2.9 Final two-body conservative 1PN Lagrangian

The paper’s main final formula is
\[
L_{\rm 1PN}^{\rm derived}
=
\frac12 m_A v_A^2 + \frac12 m_B v_B^2
+ \frac{m_A v_A^4 + m_B v_B^4}{8c^2}
+ \frac{Gm_A m_B}{r_{AB}}
\]
\[
\qquad
+ \frac{Gm_A m_B}{c^2 r_{AB}}
\left[
\frac32(v_A^2+v_B^2)
-\frac72\,\mathbf v_A\!\cdot\!\mathbf v_B
-\frac12(\mathbf v_A\!\cdot\!\hat{\mathbf n})(\mathbf v_B\!\cdot\!\hat{\mathbf n})
\right]
- \frac{G^2m_A m_B(m_A+m_B)}{2c^2 r_{AB}^2}.
\]
The claim is that
\[
L_{\rm 1PN}^{\rm derived}=L_{\rm 1PN}^{\rm EIH}
\]
**exactly**.

### 2.10 Orbit/perihelion output

In the test-mass limit, the perihelion shift is
\[
\Delta\phi_{\rm model}
=
\frac{2\pi\beta_{\rm 1PN}\mu}{c^2 a(1-e^2)}.
\]
With \(\beta_{\rm 1PN}=3\),
\[
\Delta\phi_{\rm model}
=
\frac{6\pi\mu}{c^2 a(1-e^2)}
=
\Delta\phi_{\rm GR}.
\]

---

## 3) Notation and bookkeeping you must keep straight

### 3.1 Coordinates and projection language

Bulk coordinates:
\[
X^M=(t,x,y,z,w),
\qquad
\mathbf X=(x,y,z,w)\in\mathbb R^4,
\qquad
\mathbf x=(x,y,z)\in\mathbb R^3.
\]

What a brane observer measures is defined by a **projection kernel** \(W(w)\), not by stitched boundary conditions:
\[
\mathcal P_W[Q](t,\mathbf x)
=
\int_{-\infty}^{\infty}W(w)\,Q(t,\mathbf x,w)\,dw,
\qquad
\int W(w)\,dw=1.
\]

### 3.2 Projection versus reduction

This distinction is structural:

- **Projection** = operational definition of a brane observable.
- **Reduction** = integrating over \(w\) under additional assumptions to obtain an effective brane theory.

The paper insists on keeping these separate.

### 3.3 Brane density, current, velocity

Projected density and brane current:
\[
\mathcal P_W[\rho](t,\mathbf x),
\qquad
\mathbf J_{\rm br}(t,\mathbf x)
=
\int W(w)\,\mathbf j_{xyz}(t,\mathbf x,w)\,dw.
\]

Brane velocity:
\[
\mathbf v_{\rm br}
=
\frac{\mathbf J_{\rm br}}{\mathcal P_W[\rho]}.
\]
This is a ratio of projected quantities, **not** the projection of the bulk velocity.

### 3.4 EOS/gauge/geometry ingredients carried forward

Matter sector:
\[
\rho=|\psi|^2,
\qquad
P(\rho)=K_{\rm EOS}\rho^n.
\]

Localized Maxwell sector (when retained):
\[
\partial_M\big(Z(w)F^{MN}\big)+\frac1\xi\partial^N(\partial\!\cdot\!A)
=
\mu_0\big(J_\psi^N+J_{\rm ext}^N\big).
\]

Geometry sector carries effective throat variables
\[
a(t),\qquad L(t).
\]
These become important later in the adiabatic breathing-response closure.

### 3.5 Notation warning: two different \(K\)’s

The paper distinguishes:
\[
P(\rho)=K_{\rm EOS}\rho^n
\]
from
\[
K_{\rm vec},
\]
the dimensionless wake-overlap normalization in the vector/cross sector.

Only \(n\) and \(K_{\rm vec}\) are fixed by the 1PN derivation chain; \(K_{\rm EOS}\) remains a dimensional normalization parameter.

---

## 4) Exact projected continuity, leakage, and the Poisson hook

### 4.1 Exact projected continuity

Bulk continuity is exact:
\[
\partial_t\rho+\partial_i j^i=0,
\qquad i\in\{x,y,z,w\}.
\]
Projecting gives the exact open-system brane continuity law:
\[
\partial_t\mathcal P_W[\rho]+\nabla_3\!\cdot\!\mathbf J_{\rm br}=S_{\rm leak},
\]
with leakage source
\[
S_{\rm leak}
=
-\big[W(w)j^w\big]_{-\infty}^{+\infty}
+\int_{-\infty}^{\infty}W'(w)j^w\,dw.
\]
Under fast decay, this simplifies to
\[
S_{\rm leak}=
\int_{-\infty}^{\infty}W'(w)j^w\,dw.
\]

**Meaning:** even if bulk matter evolution is conservative, the brane subsystem is generically **open**.

### 4.2 Helmholtz decomposition and exact longitudinal identity

Decompose the brane velocity as
\[
\mathbf v_{\rm br}=
\nabla_3\phi_{\rm br}+\mathbf v_T,
\qquad
\nabla_3\!\cdot\!\mathbf v_T=0.
\]
Then projected continuity implies the exact identity
\[
\boxed{
\mathcal P_W[\rho]\,\nabla_3^2\phi_{\rm br}
=
S_{\rm leak}
-\partial_t\mathcal P_W[\rho]
-(\nabla_3\mathcal P_W[\rho])\!\cdot\!(\nabla_3\phi_{\rm br}+\mathbf v_T).
}
\]
This is the paper’s exact **longitudinal identity**.

### 4.3 Controlled Poisson hook

A Poisson equation appears only in a controlled regime. If:
- \(\mathcal P_W[\rho]\approx \rho_0\) is slowly varying,
- \(\partial_t\mathcal P_W[\rho]\) is quasi-static,
- the advective correction is subleading,
- the transverse sector is negligible or perturbative,

then
\[
\nabla_3^2\phi_{\rm br}
\simeq
\frac{S_{\rm eff}}{\rho_0},
\]
with \(S_{\rm eff}\) the retained slow source term(s).

For a localized source,
\[
S_{\rm eff}(\mathbf x)\sim \mathcal S\,\delta^{(3)}(\mathbf x),
\]
so
\[
\phi_{\rm br}(\mathbf x)
\sim
-\frac{\mathcal S}{4\pi\rho_0}\frac1r,
\qquad
\nabla_3\phi_{\rm br}\sim \frac1{r^2}.
\]

This is the route by which inverse-square longitudinal behavior appears on the brane.

### 4.4 Newtonian potential definition

The paper then defines the measured Newtonian potential by normalizing this scalar channel:
\[
\Phi_N(\mathbf x,t)=\lambda_\Phi\,\phi_{\rm br}(\mathbf x,t).
\]
For an isolated compact source \(B\), the near-zone exterior solution is
\[
\Phi_B(\mathbf x,t)
=
-\frac{Gm_B}{|\mathbf x-\mathbf X_B(t)|}
+O\!\left(\frac{Gm_B a_B^2}{|\mathbf x-\mathbf X_B|^3}\right).
\]

That is the scalar potential imported into the particle Lagrangian later.

---

## 5) Newtonian point-particle limit from the worldtube reduction

### 5.1 Controlled assumptions

The worldtube-to-particle reduction uses:
- compact defect of size \(a\ll r\),
- smooth external field across the support,
- negligible worldtube boundary fluxes at retained order,
- defect-centered coordinates with vanishing dipole,
- quasi-static near-zone validity of the Poisson hook,
- conservative sector only.

### 5.2 Coherent-defect closure

Introduce the center of mass \(\mathbf X_{\rm cm}(t)\) and defect-centered coordinates
\[
\boldsymbol\xi=\mathbf x-\mathbf X_{\rm cm}(t).
\]
A representative isotropic Gaussian closure is
\[
\rho_{\rm def}(\boldsymbol\xi)
=
\frac{M}{\pi^{3/2}a^3}
\exp\!\left(-\frac{\xi^2+\eta^2+\zeta^2}{a^2}\right).
\]
The key moments are
\[
\int \rho_{\rm def}\,d^3\xi=M,
\qquad
\int \rho_{\rm def}\,\xi_i\,d^3\xi=0,
\qquad
\int \rho_{\rm def}\,\xi_i\xi_j\,d^3\xi=Q_{ij}.
\]
For the isotropic Gaussian,
\[
Q_{ij}=\frac{Ma^2}{2}\,\delta_{ij}.
\]

The vanishing dipole is the important part: it kills the dipole force correction, so the first finite-size term is quadrupolar.

### 5.3 Momentum and kinetic-energy split

Decompose the defect velocity into coherent translation plus internal flow:
\[
\mathbf v(\boldsymbol\xi,t)=\dot{\mathbf X}_{\rm cm}(t)+\mathbf u_{\rm int}(\boldsymbol\xi,t).
\]
With the coherent-translation closure
\[
\int \rho_{\rm def}\,\mathbf u_{\rm int}\,d^3\xi=0,
\]
one gets
\[
\mathbf P=\int \rho_{\rm def}\mathbf v\,d^3\xi=M\dot{\mathbf X}_{\rm cm},
\]
and
\[
T
=
\frac12M\dot{\mathbf X}_{\rm cm}^{\,2}
+\frac12\int \rho_{\rm def}|\mathbf u_{\rm int}|^2\,d^3\xi.
\]
So at Newtonian order the center-of-mass kinetic term is controlled by the same monopole mass \(M\) that couples to the external scalar field.

### 5.4 Monopole force law and quadrupole suppression

The worldtube force in a smooth external potential is
\[
\mathbf F_{\rm ext}
=
-\int \rho_{\rm def}(\boldsymbol\xi,t)
\nabla_3\Phi_N(\mathbf X_{\rm cm}+\boldsymbol\xi,t)
\,d^3\xi
+\mathbf F_{\partial W}.
\]
Taylor expanding about the center gives
\[
F_i
=
-M\,\partial_i\Phi_N(\mathbf X_{\rm cm},t)
-\frac12Q_{jk}\,\partial_j\partial_k\partial_i\Phi_N(\mathbf X_{\rm cm},t)
+\cdots.
\]
Thus the leading force is
\[
\mathbf F_{\rm ext}
=
-M\nabla_3\Phi_N(\mathbf X_{\rm cm},t)
+O(Q\,\nabla^3\Phi_N).
\]
For \(\Phi_N\sim Gm/r\), the quadrupole correction is suppressed by
\[
\frac{|\mathbf F_{\rm quad}|}{|\mathbf F_{\rm mono}|}=O\!\left(\frac{a^2}{r^2}\right).
\]

### 5.5 Newtonian point-particle Lagrangian

So the center-of-mass equation is
\[
M\ddot{\mathbf X}_{\rm cm}
=
-M\nabla_3\Phi_N(\mathbf X_{\rm cm},t)+O\!\left(M\frac{a^2}{r^2}\frac{\Phi_N}{r}\right),
\]
which is equivalent to the Newtonian point-particle Lagrangian
\[
L_N=\frac12M\dot{\mathbf X}_{\rm cm}^{\,2}-M\Phi_N(\mathbf X_{\rm cm},t).
\]
For two compact defects, pair counting gives
\[
L_N^{(2)}=
\frac12m_Av_A^2+\frac12m_Bv_B^2+\frac{Gm_A m_B}{r_{AB}}.
\]

This is the baseline on top of which the 1PN sectors are added.

---

## 6) Self sector from scalar + optical dressing

This section fixes the pair coefficient of \((v_A^2+v_B^2)\). It is explicitly **not** the wake/cross sector.

### 6.1 Reduced scalar/optical worldline ansatz

The key one-body ansatz is
\[
L_{\rm sc}
=
-M_0(1+q\,\epsilon_\Phi)c^2
\sqrt{1-\frac{\epsilon_v^2}{1+(n-1)\epsilon_\Phi}},
\]
with
\[
\epsilon_\Phi\equiv \frac{\Phi_N}{c^2},
\qquad
\epsilon_v^2\equiv \frac{v^2}{c^2}.
\]
Interpretation:
- \(1+q\epsilon_\Phi\) = scalar mass dressing,
- \(1+(n-1)\epsilon_\Phi\) in the denominator = optical/barotropic renormalization of the local propagation speed.

### 6.2 Expansion and Newtonian matching

Expanding to first order in \(\Phi_N/c^2\) and quartic order in \(v/c\):
\[
L_{\rm sc}
=
-M_0c^2-qM_0\Phi_N+\frac12M_0v^2+\frac18M_0\frac{v^4}{c^2}
+M_0\left(\frac q2-\frac{n-1}{2}\right)\frac{\Phi_N v^2}{c^2}+\cdots.
\]
Comparing with the Newtonian point-particle Lagrangian
\[
L_N=\frac12M_0v^2-M_0\Phi_N
\]
fixes
\[
q=1.
\]

### 6.3 Optical consistency fixes \(n=5\)

For
\[
P(\rho)=K_{\rm EOS}\rho^n,
\qquad
c_s^2(\rho)=\frac{dP}{d\rho}=nK_{\rm EOS}\rho^{n-1},
\]
linearization around \(\rho_0\) gives
\[
\frac{\Delta c_s}{c}\simeq \frac{n-1}{2}\,\delta,
\qquad
N(\rho)\equiv \frac{c}{c_s(\rho)}\simeq 1-\frac{n-1}{2}\,\delta.
\]
Using the weak-field relation
\[
\delta\simeq \frac{\Phi_N}{c^2},
\qquad
\Phi_N(r)=-\frac{GM}{r},
\]
we get
\[
N(r)
\simeq
1+\alpha_n\frac{GM}{c^2r},
\qquad
\alpha_n\equiv \frac{n-1}{2}.
\]
The weak-field optical sector requires
\[
\alpha_n=2,
\]
so
\[
\boxed{n=5.}
\]

### 6.4 Self coefficient

The mixed coefficient is
\[
\mathcal C_{\rm self}=\frac q2-\frac{n-1}{2}.
\]
Using \(q=1\) and \(n=5\):
\[
\mathcal C_{\rm self}=\frac12-2=-\frac32.
\]
For body \(A\) in the field of body \(B\),
\[
\Phi_B(\mathbf X_A)=-\frac{Gm_B}{r_{AB}},
\]
so the pair contribution becomes
\[
L_{\rm self}^{(AB)}
=
\frac{Gm_A m_B}{c^2 r_{AB}}
\bigl(-\mathcal C_{\rm self}\bigr)(v_A^2+v_B^2).
\]
Hence
\[
-\mathcal C_{\rm self}=+\frac32,
\]
and the self-sector pair term is
\[
\boxed{
L_{\rm self}^{(AB)}
=
\frac{Gm_A m_B}{c^2r_{AB}}\,\frac32\,(v_A^2+v_B^2).
}
\]

### 6.5 Universal free quartic term

Setting \(\Phi_N=0\),
\[
L_{\rm free}
=
-M_0c^2\sqrt{1-\frac{v^2}{c^2}}
=
-M_0c^2+\frac12M_0v^2+\frac18M_0\frac{v^4}{c^2}+\cdots.
\]
Again: \(1/8\) is the Lagrangian coefficient, while \(3/8\) is the energy coefficient.

### 6.6 What to remember

This section fixes
\[
q=1,
\qquad
n=5,
\qquad
\mathcal C_{\rm self}=-\frac32,
\qquad
\text{pair self coefficient}=+\frac32.
\]

---

## 7) Static nonlinear sector from local mass scaling

This is the velocity-independent \(1\)PN piece. It vanishes in neither the self-sector limit nor the wake/cross limit.

### 7.1 Local mass scaling ansatz

Define the local Newtonian potential at body \(A\) due to all the others:
\[
\Phi_A^{\rm loc}(\mathbf X_A)
=
-\sum_{C\neq A}\frac{Gm_C}{r_{AC}}.
\]
Then the reduced mass-dressing ansatz is
\[
m_A^{\rm eff}
=
m_A\left(1+\kappa_\rho\frac{\Phi_A^{\rm loc}}{c^2}\right)+O(c^{-4}).
\]
In this paper,
\[
\kappa_\rho=q=1.
\]

### 7.2 Pair-counted potential and compact many-body formula

Write the pair-counted interaction as
\[
L_{\rm pot}
=
-\frac12\sum_A m_A^{\rm eff}\,\Phi_A^{\rm loc}.
\]
Expanding gives
\[
L_{\rm pot}
=
-\frac12\sum_A m_A\Phi_A^{\rm loc}
-\frac{\kappa_\rho}{2c^2}\sum_A m_A(\Phi_A^{\rm loc})^2+O(c^{-4}).
\]
So the full static nonlinear sector is
\[
L_{\rm stat}
=
-\frac{\kappa_\rho G^2}{2c^2}
\sum_A m_A\left(\sum_{C\neq A}\frac{m_C}{r_{AC}}\right)^2.
\]
This is the key compact formula.

### 7.3 Two-body result

For two bodies,
\[
\Phi_A^{\rm loc}=-\frac{Gm_B}{r_{AB}},
\qquad
\Phi_B^{\rm loc}=-\frac{Gm_A}{r_{AB}},
\]
so
\[
L_{\rm stat}^{(AB)}
=
-\frac{\kappa_\rho G^2m_A m_B(m_A+m_B)}{2c^2r_{AB}^2}.
\]
With \(\kappa_\rho=1\),
\[
\boxed{
L_{\rm stat}^{(AB)}
=
-\frac{G^2m_A m_B(m_A+m_B)}{2c^2r_{AB}^2}.
}
\]
So the coefficient is exactly
\[
-\frac12.
\]

### 7.4 Three-body pattern

For three bodies, this mechanism automatically produces both pair-collapsed \(r^{-2}\) pieces and genuine triplet terms:
\[
L_{\rm stat}^{(ABC)}
=
-\frac{\kappa_\rho G^2}{2c^2}
\left[
\frac{m_A m_B(m_A+m_B)}{r_{AB}^2}
+\frac{m_A m_C(m_A+m_C)}{r_{AC}^2}
+\frac{m_B m_C(m_B+m_C)}{r_{BC}^2}
\right]
\]
\[
\qquad
-\frac{\kappa_\rho G^2m_A m_B m_C}{c^2}
\left[
\frac1{r_{AB}r_{AC}}+\frac1{r_{AB}r_{BC}}+\frac1{r_{AC}r_{BC}}
\right].
\]
So the “gravity gravitates” sector extends consistently to the many-body case.

---

## 8) Topology + internal response ledger

This section rederives the self-sector/precession bookkeeping in the familiar split
\[
\beta_{\rm 1PN}=\kappa_\rho+\kappa_{\rm add}+\kappa_{\rm PV}.
\]

### 8.1 Scalar part

Already fixed:
\[
\kappa_\rho=q=1.
\]

### 8.2 Added mass as a topology discriminator

The exterior added-mass problem is treated in the low-Mach, quasi-static, irrotational potential-flow regime:
\[
\mathbf v_{\rm ext}=\nabla\phi,
\qquad
\nabla^2\phi=0
\quad\text{outside the excluded region.}
\]
The exterior kinetic energy defines \(M_{\rm add}\):
\[
T_{\rm ext}=\frac12\rho_0\int_{\rm ext}|\nabla\phi|^2dV=\frac12M_{\rm add}U^2.
\]
With displaced mass
\[
M_{\rm disp}=\rho_0V_{\rm exc},
\qquad
M_{\rm add}=\kappa_{\rm add}M_{\rm disp},
\]
a translating \(d_{\rm eff}\)-dimensional ball gives
\[
\kappa_{\rm add}(d_{\rm eff})=\frac1{d_{\rm eff}-1}.
\]
So:
\[
\kappa_{\rm add}(3)=\frac12,
\qquad
\kappa_{\rm add}(4)=\frac13.
\]

For the actual defect in this paper, the exterior rearrangement is taken to be **uniform in \(w\)**:
\[
\phi(x,y,z,w)=\phi_3(x,y,z),
\qquad
\nabla_4^2\phi=\nabla_3^2\phi_3.
\]
Thus the effective exterior-flow dimension is
\[
d_{\rm eff}=3,
\]
and therefore
\[
\boxed{\kappa_{\rm add}=\frac12.}
\]
If the defect were instead a compact 4D bubble, one would get
\[
\kappa_{\rm add}^{(B^4)}=\frac13.
\]

### 8.3 Adiabatic 1-DOF breathing closure for \(\kappa_{\rm PV}\)

This is the only clearly protocol-level part of the 1PN ledger.

#### Declared protocol

- control parameter = ambient density \(\rho\) at defect location,
- use weak-field relation \(\delta\rho/\rho_0\simeq \Phi_N/c^2\),
- reduce geometry to one breathing variable \(a\),
- fix aspect ratio
  \[
  L=\Lambda a,
  \]
- for each \(\rho\), choose \(a_*(\rho)\) by minimizing an effective energy.

#### Reduced equilibrium energy

The paper uses
\[
F(a,\rho)=E_w+E_f+E_{\rm PV},
\]
with scalings
\[
E_w=\frac{\mathcal C_w c_s(\rho)}{a},
\qquad
E_f=\frac{\mathcal C_f}{\rho a^2},
\qquad
E_{\rm PV}=\mathcal C_{\rm PV}P(\rho)V(a).
\]
Using
\[
P(\rho)=K_{\rm EOS}\rho^n,
\qquad
c_s(\rho)\propto \rho^{(n-1)/2},
\qquad
V(a)=\pi\Lambda a^3,
\]
the \(a\)-powers are
\[
(-1,-2,+3).
\]

#### Virial identity

Equilibrium \(\partial_aF=0\) implies
\[
E_w+2E_f=3E_{\rm PV}.
\]
Define
\[
x\equiv \frac{E_f}{E_w}.
\]
Then
\[
\frac{E_{\rm PV}}{E_w}=\frac{1+2x}{3},
\qquad
F=E_w\frac{4+5x}{3}.
\]

#### Density-slope formula

By the envelope theorem,
\[
\frac{d\ln F_{\rm eq}}{d\ln\rho}
=
\frac{\left(\frac{n-1}{2}\right)E_w+(-1)E_f+nE_{\rm PV}}{F}.
\]
Substituting the virial relations gives
\[
\frac{d\ln F_{\rm eq}}{d\ln\rho}
=
\frac{\frac{5n-3}{2}+(2n-3)x}{4+5x}.
\]
For the already-fixed \(n=5\),
\[
\frac{d\ln F_{\rm eq}}{d\ln\rho}
=
\frac{11+7x}{4+5x}.
\]

#### Mapping to \(\kappa_{\rm PV}\)

In the paper’s adiabatic estimator,
\[
\kappa_{\rm PV}
\equiv
\frac{d\ln F_{\rm eq}}{d\ln\rho}-\kappa_\rho.
\]
Since \(\kappa_\rho=1\), the target \(\kappa_{\rm PV}=3/2\) corresponds to
\[
\frac{d\ln F_{\rm eq}}{d\ln\rho}=\frac52.
\]
Applying this to the \(n=5\) slope formula yields
\[
\frac{11+7x}{4+5x}=\frac52
\qquad\Longrightarrow\qquad
x=\frac{2}{11}.
\]
Therefore the closure gives
\[
\boxed{\kappa_{\rm PV}=\frac32.}
\]

#### Internal partition and breathing slope

The same solution implies
\[
E_w:E_f:E_{\rm PV}=11:2:5,
\]
that is,
\[
(f_w,f_f,f_{\rm PV})=
\left(\frac{11}{18},\frac{2}{18},\frac{5}{18}\right).
\]
It also predicts
\[
\frac{d\ln a_*}{d\ln\rho}=-\frac{57}{64}\approx -0.890625.
\]

### 8.4 Final ledger

Combining the three pieces gives
\[
\beta_{\rm 1PN}=\kappa_\rho+\kappa_{\rm add}+\kappa_{\rm PV}
=1+\frac12+\frac32=3.
\]
This means the one-body self coefficient is
\[
-\frac{\beta_{\rm 1PN}}{2}=-\frac32,
\]
which matches the direct scalar/optical route exactly, and the pair self coefficient is
\[
+\frac{\beta_{\rm 1PN}}{2}=+\frac32.
\]

**Key conceptual point:** the coefficient \(+3/2\) in the pair Lagrangian is reproduced by two independent routes:
- scalar + optical worldline expansion,
- topology + response ledger.

---

## 9) Constructive wake derivation of the EIH cross terms

This section is **only** about the bilinear cross tensor. It does not generate the self-sector terms.

### 9.1 Target cross structure

For two bodies,
\[
\mathbf r_{AB}=\mathbf X_A-\mathbf X_B,
\qquad
r_{AB}=|\mathbf r_{AB}|,
\qquad
\hat{\mathbf n}_{AB}=\frac{\mathbf r_{AB}}{r_{AB}},
\]
the most general rotationally invariant parity-even bilinear cross sector is
\[
L_{\rm vec}^{(AB)}
=
\frac{Gm_A m_B}{c^2r_{AB}}
\left[
C_\parallel\,\mathbf v_A\!\cdot\!\mathbf v_B
+
C_L(\mathbf v_A\!\cdot\!\hat{\mathbf n}_{AB})(\mathbf v_B\!\cdot\!\hat{\mathbf n}_{AB})
\right].
\]
The EIH target is
\[
C_\parallel=-\frac72,
\qquad
C_L=-\frac12.
\]

### 9.2 Isotropic Fourier-space wake basis

The far-field disturbance of a moving defect is written as
\[
\mathbf u(\mathbf k;\mathbf v)=\mathbf u_T+\mathbf u_H+\mathbf u_L,
\]
with
\[
\mathbf u_T(\mathbf k;\mathbf v)
=
i a_T\frac{\mathbf P_T(\hat{\mathbf k})\mathbf v}{k},
\qquad
\mathbf P_T(\hat{\mathbf k})=\mathbf I-\hat{\mathbf k}\hat{\mathbf k},
\qquad a_T\equiv 1,
\]
\[
\mathbf u_H(\mathbf k;\mathbf v)
=
i a_H\frac{\mathbf k\times \mathbf v}{k^2},
\]
\[
\mathbf u_L(\mathbf k;\mathbf v)
=
i a_L\frac{\mathbf k(\mathbf k\!\cdot\!\mathbf v)}{k^3}.
\]
Interpretation:
- \(u_T\): transverse/shear translation response,
- \(u_H\): helical transverse response,
- \(u_L\): longitudinal/compressible response.

### 9.3 Bilinear overlap and tensor decomposition

The pair overlap kernel is
\[
I_{AB}(r_{AB})
\propto
\int d^3k\;\mathbf u(\mathbf k;\mathbf v_A)\!\cdot\!\mathbf u(-\mathbf k;\mathbf v_B)
\,e^{i\mathbf k\cdot\mathbf r_{AB}}.
\]
Isotropy implies
\[
I_{AB}(r_{AB})
=
\frac1{r_{AB}}
\left[
\mathcal S_\parallel\,\mathbf v_A\!\cdot\!\mathbf v_B
+
\mathcal S_L(\mathbf v_A\!\cdot\!\hat{\mathbf n}_{AB})(\mathbf v_B\!\cdot\!\hat{\mathbf n}_{AB})
\right].
\]
The explicit evaluation gives
\[
\mathcal S_\parallel=\pi^2(-1+a_H^2-a_L^2),
\qquad
\mathcal S_L=\pi^2(-1+a_H^2+a_L^2).
\]
Define
\[
\alpha^2\equiv a_L^2.
\]
With overall normalization \(K_{\rm vec}\), the cross coefficients are
\[
C_\parallel=K_{\rm vec}\pi^2(-1+a_H^2-\alpha^2),
\qquad
C_L=K_{\rm vec}\pi^2(-1+a_H^2+\alpha^2).
\]

This is the core wake formula to remember.

### 9.4 EIH matching gives a one-parameter family

Imposing the EIH targets gives the invariants
\[
K_{\rm vec}\alpha^2=\frac{3}{2\pi^2},
\qquad
K_{\rm vec}(1-a_H^2)=\frac{2}{\pi^2}.
\]
Equivalently,
\[
\alpha^2(a_H^2)=\frac34(1-a_H^2),
\qquad
K_{\rm vec}(a_H^2)=\frac{2}{\pi^2(1-a_H^2)},
\qquad
0\le a_H^2<1.
\]
So EIH matching alone leaves a one-parameter family.

### 9.5 Thermodynamic closure from the already-fixed EOS exponent

The extra input comes from the barotropic identity
\[
P=\rho h-U.
\]
For a polytrope \(P=K_{\rm EOS}\rho^n\),
\[
U(\rho)=\frac{K_{\rm EOS}}{n-1}\rho^n,
\qquad
\frac{U}{P}=\frac1{n-1}.
\]
The paper’s minimal thermodynamic wake closure is
\[
\alpha_{\rm thermo}^2
\equiv
1-\frac{U}{P}
=
1-\frac1{n-1}.
\]
Since the optical sector already fixed \(n=5\),
\[
\boxed{\alpha^2=\alpha_{\rm thermo}^2=\frac34.}
\]

### 9.6 Collapse to the unique parity-even point

Substitute \(\alpha^2=3/4\) into the family:
\[
\frac34=\frac34(1-a_H^2)
\qquad\Longrightarrow\qquad
a_H^2=0.
\]
So the minimal real parity-even solution is
\[
a_H=0,
\qquad
K_{\rm vec}=\frac{2}{\pi^2}.
\]
Then back-substitution yields
\[
C_\parallel=-\frac72,
\qquad
C_L=-\frac12.
\]

**Important division of labor:**
- wake overlap exhausts the parity-even **cross tensor**,
- self terms belong to the scalar/optical and topology/response sectors,
- no extra scalar offset should be added to \(C_L\) or \(C_\parallel\).

---

## 10) Full two-body 1PN Lagrangian and exact EIH match

### 10.1 Assembly pieces

The final derived Lagrangian is written as
\[
L_{\rm 1PN}^{\rm derived}
=
L_N^{(AB)}+L_{v^4}^{(AB)}+L_{\rm self}^{(AB)}+L_{\rm cross}^{(AB)}+L_{\rm stat}^{(AB)}.
\]
The ingredients are:

Newtonian sector:
\[
L_N^{(AB)}=
\frac12m_Av_A^2+\frac12m_Bv_B^2+\frac{Gm_A m_B}{r_{AB}}.
\]

Universal quartic term:
\[
L_{v^4}^{(AB)}=
\frac{m_Av_A^4+m_Bv_B^4}{8c^2}.
\]

Self sector:
\[
L_{\rm self}^{(AB)}=
\frac{Gm_A m_B}{c^2r_{AB}}\,\frac32(v_A^2+v_B^2).
\]

Cross sector:
\[
L_{\rm cross}^{(AB)}
=
\frac{Gm_A m_B}{c^2r_{AB}}
\left[-\frac72\,\mathbf v_A\!\cdot\!\mathbf v_B
-\frac12(\mathbf v_A\!\cdot\!\hat{\mathbf n})(\mathbf v_B\!\cdot\!\hat{\mathbf n})\right].
\]

Static sector:
\[
L_{\rm stat}^{(AB)}=
-\frac{G^2m_A m_B(m_A+m_B)}{2c^2r_{AB}^2}.
\]

### 10.2 Final assembled result

Putting those together gives
\[
L_{\rm 1PN}^{\rm derived}
=
\frac12 m_A v_A^2 + \frac12 m_B v_B^2
+ \frac{m_A v_A^4 + m_B v_B^4}{8c^2}
+ \frac{Gm_A m_B}{r_{AB}}
\]
\[
\qquad
+ \frac{Gm_A m_B}{c^2 r_{AB}}
\left[
\frac32(v_A^2+v_B^2)
-\frac72\,\mathbf v_A\!\cdot\!\mathbf v_B
-\frac12(\mathbf v_A\!\cdot\!\hat{\mathbf n})(\mathbf v_B\!\cdot\!\hat{\mathbf n})
\right]
- \frac{G^2m_A m_B(m_A+m_B)}{2c^2 r_{AB}^2}.
\]

The standard conservative EIH target in the same convention has **exactly the same form**, so
\[
\Delta L
\equiv
L_{\rm 1PN}^{\rm derived}-L_{\rm 1PN}^{\rm EIH}=0.
\]

### 10.3 Coefficient provenance

The paper emphasizes that every final coefficient has a named source:

- \(1/8\) in \(v^4\): wave-supported / relativistic kinematics,
- \(+3/2\) in \(v_A^2+v_B^2\): scalar+optical route and independently the \(\beta_{\rm 1PN}\) ledger,
- \((-7/2,-1/2)\) in the cross tensor: constructive wake derivation,
- \(-1/2\) in the static \(G^2/r^2\) term: local mass scaling + pair counting.

So the final result is a true **assembly of independent derivation channels**, not a repackaged single ansatz.

---

## 11) Test-mass orbit reduction and perihelion shift

### 11.1 Test-mass limit of the full 1PN Lagrangian

Take body \(A\) as a light test mass \(m\), body \(B\) as a heavy central mass \(M\), with
\[
m\ll M,
\qquad
\mu\equiv GM,
\qquad
\mathbf X_B=0,
\qquad
\mathbf v_B=0,
\qquad
r=|\mathbf X_A|.
\]
Dividing the full two-body Lagrangian by the test mass and dropping higher powers of \(m/M\) gives
\[
\mathcal L_{\rm test}
=
\frac12v^2+\frac\mu r
+\frac1{c^2}\left[
\frac18v^4+\frac32\frac\mu r\,v^2-\frac12\frac{\mu^2}{r^2}
\right],
\]
with
\[
v^2=\dot r^2+r^2\dot\phi^2.
\]

### 11.2 Why only the kinetic-prefactor part matters for precession

Introduce the Newtonian specific energy
\[
\mathcal E_N=\frac12v^2-\frac\mu r.
\]
Then
\[
\frac18v^4-\frac12\frac{\mu^2}{r^2}
=
\frac12\mathcal E_N^2+\mathcal E_N\frac\mu r.
\]
At the retained order these terms only renormalize the Kepler energy / semimajor-axis bookkeeping; they do not by themselves generate precession.

The precession-relevant piece is the velocity-coupled correction. Package it as a position-dependent inertia:
\[
\mathcal L_{\rm orb}
=
\frac12\bigl(1+\sigma(r)\bigr)(\dot r^2+r^2\dot\phi^2)+\frac\mu r,
\]
with
\[
\sigma(r)=\frac{\beta_{\rm 1PN}\mu}{c^2r}.
\]
For this paper,
\[
\beta_{\rm 1PN}=3,
\qquad
\sigma(r)=\frac{3\mu}{c^2r}.
\]

This is precisely the orbit-level form used earlier in the series, now derived from the full 1PN assembly.

### 11.3 Conserved angular momentum and energy

Since \(\phi\) is cyclic,
\[
\ell
=\frac{\partial\mathcal L_{\rm orb}}{\partial\dot\phi}
=(1+\sigma(r))r^2\dot\phi
\]
is conserved.

The specific energy is
\[
\mathcal E
=
\frac12(1+\sigma(r))(\dot r^2+r^2\dot\phi^2)-\frac\mu r.
\]

### 11.4 Binet equation and perihelion coefficient

Set
\[
u(\phi)\equiv \frac1{r(\phi)},
\qquad
\epsilon\equiv \frac{\beta_{\rm 1PN}\mu}{c^2}.
\]
Then
\[
1+\sigma(r)=1+\epsilon u,
\qquad
\dot\phi=\frac{\ell u^2}{1+\epsilon u},
\qquad
\dot r=-\frac{\ell u'}{1+\epsilon u}.
\]
Substituting into the energy integral and expanding to 1PN order gives
\[
u''+u
=
\frac\mu{\ell^2}+\frac{\epsilon\mathcal E}{\ell^2}+\frac{2\epsilon\mu}{\ell^2}u+O(c^{-4}).
\]
Rewriting the constant term as a renormalized semilatus rectum gives
\[
u''+
\left(1-\frac{2\beta_{\rm 1PN}\mu^2}{c^2\ell^2}\right)u
=
\frac1{p_{\rm eff}}+O(c^{-4}).
\]
So the orbit is a slightly detuned Kepler ellipse,
\[
u(\phi)=\frac1{p_{\rm eff}}\bigl[1+e\cos(\omega\phi)\bigr],
\]
with
\[
\omega^2=1-\frac{2\beta_{\rm 1PN}\mu^2}{c^2\ell^2},
\qquad
\omega=1-\frac{\beta_{\rm 1PN}\mu^2}{c^2\ell^2}+O(c^{-4}).
\]
Therefore the perihelion shift per orbit is
\[
\Delta\phi_{\rm model}
=
2\pi\left(\frac1\omega-1\right)
=
\frac{2\pi\beta_{\rm 1PN}\mu^2}{c^2\ell^2}+O(c^{-4}).
\]
Using the Newtonian relation
\[
\ell^2=\mu a(1-e^2),
\]
one obtains the compact result
\[
\boxed{
\Delta\phi_{\rm model}
=
\frac{2\pi\beta_{\rm 1PN}\mu}{c^2a(1-e^2)}.
}
\]
With \(\beta_{\rm 1PN}=3\),
\[
\boxed{
\Delta\phi_{\rm model}
=
\frac{6\pi\mu}{c^2a(1-e^2)}
=\Delta\phi_{\rm GR}.
}
\]

So the perihelion result is the orbit-level manifestation of the already-derived self-sector ledger.

---

## 12) Fixed versus symbolic quantities

This section is important because it tells you what future papers are allowed to treat as carry-forward constants versus what must remain symbolic.

### 12.1 Fixed by the derivation chain

These should be treated as **derived, not tunable** within the paper’s closure hierarchy:

- \(q=1\), \(\kappa_\rho=1\),
- \(n=5\),
- free-particle quartic Lagrangian coefficient \(1/8\),
- static coefficient \(-1/2\),
- \(\kappa_{\rm add}=1/2\) for the actual throat,
- \(\alpha^2=3/4\), \(a_H=0\), \(K_{\rm vec}=2/\pi^2\),
- cross coefficients \((C_\parallel,C_L)=(-7/2,-1/2)\),
- full conservative two-body 1PN Lagrangian,
- exact equality to the conservative EIH target.

### 12.2 Fixed only within the declared protocol

These are **protocol-fixed**, not universal theorems:

- \(\kappa_{\rm PV}=3/2\) in the adiabatic 1-DOF closure,
- \(\beta_{\rm 1PN}=3\) once that \(\kappa_{\rm PV}\) is adopted,
- internal partition \(E_w:E_f:E_{\rm PV}=11:2:5\),
- breathing slope \(d\ln a_*/d\ln\rho=-57/64\).

### 12.3 What remains symbolic

The paper is explicit that the following remain unresolved / symbolic:

#### Absolute normalization

In
\[
P(\rho)=K_{\rm EOS}\rho^n,
\qquad n=5,
\]
the exponent is fixed but the dimensional constant \(K_{\rm EOS}\) is not.

Likewise, \(G\) and \(c\) appear as effective measured constants on the brane; the paper fixes the dimensionless coefficient ledger, not their first-principles absolute numerical values.

#### Projection and localization profiles

The detailed shapes of
\[
W(w),
\qquad
Z(w)
\]
remain symbolic. The 1PN derivation uses only their structural properties.

#### Finite-size / higher multipoles

Objects like
\[
Q_{ij}=\int \rho_{\rm def}\,\xi_i\xi_j\,d^3\xi
\]
remain profile-dependent and enter only beyond the monopole small-body limit.

#### General response beyond the adiabatic closure

Outside the paper’s specific protocol, one should expect a more general response object such as
\[
\kappa_{\rm PV}\to \kappa_{\rm PV}(\omega,\text{protocol}),
\]
plus possible damping, phase lag, multi-mode coupling, etc.

#### Open-system dynamics beyond the quasi-static reduction

The parent 4D model has exact open-system objects such as
\[
S_{\rm leak},
\qquad
R_{ab},
\qquad
\mathbf F_{\partial W},
\]
but the present 1PN derivation only uses them in the quasi-static reduction regime.

#### Beyond-conservative-1PN sectors

The paper leaves unresolved:
\[
\text{radiation reaction},\quad
\text{dissipative leakage},\quad
\text{spin couplings},\quad
\text{higher-PN terms},\quad
\text{strong-field corrections}.
\]

#### Fully solved moving-throat bulk dynamics

The paper does **not** solve the full moving-throat PDE problem in the 4D bulk; the particle limit remains a controlled reduction, not a first-principles theorem from a numerically completed defect solution.

---

## 13) Verification / reproducibility ledger

The analytic derivation is backed by a Wolfram Language referee suite. These scripts are not presented as black-box derivations; they are used to check algebraic identities, coefficient matches, and end-to-end assembly.

### 13.1 Main scripts

#### `4d_gravity_1pn_master_harness.wl`

Role:
- projection normalization,
- leakage split,
- exact longitudinal identity,
- Poisson-hook reduction,
- Newtonian coupling \(q=1\),
- optical coefficient and \(n=5\),
- added mass,
- vector-family invariants,
- adiabatic \(\kappa_{\rm PV}\) closure,
- \(\beta_{\rm 1PN}=3\),
- orbit/perihelion bookkeeping.

Reported summary:
\[
\texttt{PASS count = 60},
\qquad
\texttt{FAIL count = 0}.
\]

#### `vector_wake_rebuild.wl`

Role:
- self-contained constructive wake module,
- overlap shapes,
- EIH ratio constraint,
- selection of real wake,
- normalization fixing.

Reported output:
\[
a_H=0,
\qquad
a_L=\pm\frac{\sqrt3}{2},
\qquad
K_{\rm vec}=\frac{2}{\pi^2},
\]
with recovered targets
\[
C_\parallel=-\frac72,
\qquad
C_L=-\frac12.
\]

#### `4d_full_1pn_derivation_with_vectorwake.wl`

Role:
- coherent-defect / small-body worldtube reduction,
- scalar/self sector,
- static nonlinear term,
- topology and response ledger,
- full two-body EIH equality,
- perihelion reduction.

Reported summary:
\[
\texttt{Passes: 37},
\qquad
\texttt{Fails: 0},
\qquad
\texttt{Skips: 0}.
\]

### 13.2 What the suite is checking

The checks fall into four groups:

1. **Exact symbolic identities**
   - projection normalization,
   - leakage split,
   - exact longitudinal identity,
   - pair-counted Newtonian interaction,
   - local-mass-scaling algebra,
   - virial identities inside the adiabatic closure.

2. **Controlled reductions**
   - Poisson hook,
   - small-body / monopole worldtube reduction,
   - \((a/r)^2\) finite-size suppression,
   - \(\kappa_{\rm add}=1/2\) vs \(1/3\),
   - optical coefficient \(\alpha_n=(n-1)/2\) and \(n=5\),
   - isotropic wake basis and EIH family.

3. **Protocol-level closures**
   - \(x=2/11\),
   - \(\kappa_{\rm PV}=3/2\),
   - \(\beta_{\rm 1PN}=3\),
   - \(d\ln a_*/d\ln\rho=-57/64\).

4. **Full assembly checks**
   - wake module reproduces EIH cross coefficients,
   - scalar/optical and \(\beta_{\rm 1PN}\)-ledger routes agree on the self coefficient,
   - full two-body 1PN Lagrangian matches EIH exactly,
   - test-mass orbit reduction reproduces the canonical perihelion coefficient.

### 13.3 Scope limits of the verification suite

The scripts do **not** verify:
- a fully dynamical moving-throat PDE solution in the parent 4D bulk,
- dissipative leakage,
- radiation reaction,
- spin couplings,
- higher-PN terms,
- non-adiabatic internal response.

So the suite verifies the paper **as stated**, not a stronger claim.

---

## 14) Minimal “keep this in RAM” cache

If I only keep the most load-bearing equations and facts from `4d_1pn_full.tex`, they are these:

1. **Exact projected continuity + leakage**
   \[
   \partial_t\mathcal P_W[\rho]+\nabla_3\!\cdot\!\mathbf J_{\rm br}=S_{\rm leak}.
   \]

2. **Exact longitudinal identity**
   \[
   \mathcal P_W[\rho]\,\nabla_3^2\phi_{\rm br}
   =
   S_{\rm leak}-\partial_t\mathcal P_W[\rho]
   -(\nabla_3\mathcal P_W[\rho])\!\cdot\!(\nabla_3\phi_{\rm br}+\mathbf v_T).
   \]

3. **Controlled Poisson hook / Newtonian potential**
   \[
   \nabla_3^2\phi_{\rm br}\simeq \frac{S_{\rm eff}}{\rho_0},
   \qquad
   \Phi_N=\lambda_\Phi\phi_{\rm br},
   \qquad
   \Phi_B\simeq -\frac{Gm_B}{r}.
   \]

4. **Newtonian two-body baseline**
   \[
   L_N^{(2)}
   =
   \frac12m_Av_A^2+\frac12m_Bv_B^2+\frac{Gm_A m_B}{r_{AB}}.
   \]

5. **Scalar/optical self route**
   \[
   L_{\rm sc}
   =
   -M_0(1+q\Phi_N/c^2)c^2
   \sqrt{1-\frac{v^2/c^2}{1+(n-1)\Phi_N/c^2}}.
   \]
   Newtonian matching fixes \(q=1\); weak-field optics fixes \(n=5\); therefore
   \[
   \mathcal C_{\rm self}=\frac q2-\frac{n-1}{2}=-\frac32,
   \]
   so the pair self coefficient is \(+3/2\).

6. **Universal free quartic coefficient**
   \[
   L_{\rm free}=-mc^2+\frac12mv^2+\frac18m\frac{v^4}{c^2}+\cdots.
   \]

7. **Static nonlinear term from local mass scaling**
   \[
   m_A^{\rm eff}=m_A\left(1+\kappa_\rho\frac{\Phi_A^{\rm loc}}{c^2}\right),
   \qquad \kappa_\rho=1,
   \]
   
   \[
   L_{\rm stat}
   =
   -\frac{\kappa_\rho G^2}{2c^2}\sum_A m_A\left(\sum_{C\neq A}\frac{m_C}{r_{AC}}\right)^2,
   \]
   hence for two bodies
   \[
   L_{\rm stat}^{(AB)}=-\frac{G^2m_A m_B(m_A+m_B)}{2c^2r_{AB}^2}.
   \]

8. **Topology/response ledger**
   \[
   \beta_{\rm 1PN}=\kappa_\rho+\kappa_{\rm add}+\kappa_{\rm PV},
   \qquad
   \kappa_\rho=1,
   \qquad
   \kappa_{\rm add}=\frac12,
   \qquad
   \kappa_{\rm PV}=\frac32\ \text{(protocol-fixed)}.
   \]
   Therefore
   \[
   \beta_{\rm 1PN}=3.
   \]

9. **Wake/cross tensor formulas**
   \[
   C_\parallel=K_{\rm vec}\pi^2(-1+a_H^2-\alpha^2),
   \qquad
   C_L=K_{\rm vec}\pi^2(-1+a_H^2+\alpha^2).
   \]
   EIH + thermodynamic closure + \(n=5\) give
   \[
   \alpha^2=\frac34,
   \qquad
a_H=0,
   \qquad
   K_{\rm vec}=\frac{2}{\pi^2},
   \qquad
   C_\parallel=-\frac72,
   \qquad
   C_L=-\frac12.
   \]

10. **Final conservative two-body 1PN result**
    \[
    L_{\rm 1PN}^{\rm derived}=L_{\rm 1PN}^{\rm EIH}
    \]
    with
    \[
    L_{\rm 1PN}^{\rm derived}
    =
    \frac12 m_A v_A^2 + \frac12 m_B v_B^2
    + \frac{m_A v_A^4 + m_B v_B^4}{8c^2}
    + \frac{Gm_A m_B}{r_{AB}}
    \]
    \[
    \qquad
    + \frac{Gm_A m_B}{c^2 r_{AB}}
    \left[
    \frac32(v_A^2+v_B^2)
    -\frac72\,\mathbf v_A\!\cdot\!\mathbf v_B
    -\frac12(\mathbf v_A\!\cdot\!\hat{\mathbf n})(\mathbf v_B\!\cdot\!\hat{\mathbf n})
    \right]
    - \frac{G^2m_A m_B(m_A+m_B)}{2c^2 r_{AB}^2}.
    \]

11. **Orbit reduction / perihelion**
    \[
    \mathcal L_{\rm orb}
    =
    \frac12(1+\sigma(r))(\dot r^2+r^2\dot\phi^2)+\frac\mu r,
    \qquad
    \sigma(r)=\frac{\beta_{\rm 1PN}\mu}{c^2r},
    \]
    so
    \[
    \Delta\phi_{\rm model}
    =
    \frac{2\pi\beta_{\rm 1PN}\mu}{c^2a(1-e^2)}.
    \]
    With \(\beta_{\rm 1PN}=3\),
    \[
    \Delta\phi_{\rm model}=\frac{6\pi\mu}{c^2a(1-e^2)}=\Delta\phi_{\rm GR}.
    \]

---

## 15) One-sentence bottom line

Within the declared closure hierarchy, `4d_1pn_full.tex` turns the 4D projection-based toy model into a **fully fixed conservative two-body 1PN theory** whose reduced Lagrangian is **exactly the standard EIH result**, with the only clearly protocol-level ingredient being the adiabatic closure used to set \(\kappa_{\rm PV}=3/2\).
