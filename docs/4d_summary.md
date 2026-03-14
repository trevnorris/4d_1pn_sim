4d.tex

## 1) What this paper is trying to accomplish

This paper (“Paper 7” in the toy-model sequence) upgrades the toy model to a **fully action-based 4D-spatial bulk theory** and then defines what an embedded **3D “brane observer”** actually measures.

The key deliverables are:

1. **A complete, explicit action** for the coupled system:
   - matter sector: **gauged 4D nonlinear Schrödinger (GNLS)** field with a fixed (“frozen”) stiff polytropic equation of state,
   - electromagnetic sector: **Maxwell theory in 4+1** with a prescribed **localization profile** \(Z(w)\), plus gauge-fixing and explicit **external** sources,
   - geometry closure: two effective, dynamical geometric degrees of freedom \(a(t)\) (radius) and \(L(t)\) (length), including damping and an optional stiff ratio penalty \(L \simeq \alpha a\).

2. **Exact Euler–Lagrange equations** and exact hydrodynamic identities (continuity, Euler-like form, vorticity–gauge identity).

3. **Operational brane observables via projection** with a normalized weight \(W(w)\), and the exact consequence:
   - **projected continuity has a leakage source** \(S_{\rm leak}\) that encodes exchange with the extra direction \(w\).

4. The central “gravity hook”:
   - from projected continuity + Helmholtz decomposition of the **brane velocity**, derive an **exact longitudinal identity**
     \[
       \rho_{\rm brane}\,\nabla_3^2 \varphi
       =
       S_{\rm leak} - \partial_t \rho_{\rm brane} - (\nabla_3\rho_{\rm brane})\cdot(\nabla_3\varphi + \mathbf v_T),
     \]
     which contains a **3D Laplacian** acting on a scalar potential \(\varphi\).
   - In a clearly stated **controlled regime** (quasi-static, weak correction terms, often longitudinal dominance) this becomes a **Poisson equation on the brane** and yields **inverse-square scaling** of the longitudinal velocity field.

5. A separate “EM hook”:
   - under an explicit **zero-mode ansatz** for the gauge field, integrate the localized bulk Maxwell equation over \(w\) to obtain an effective **3+1 Maxwell theory** on the brane with renormalized coupling
     \[
       \mu_0^{\rm eff}=\mu_0/Z_{\rm int},\qquad Z_{\rm int}=\int_{-\infty}^{\infty}Z(w)\,dw.
     \]

Throughout, the paper is careful to classify statements as **(i) exact**, **(ii) controlled reductions**, or **(iii) regime approximations**.

---

## 2) Core objects, geometry, and notation (things you’ll keep using)

### Spacetime and coordinates
- Spacetime is \((4+1)\)-dimensional:  
  \[
    x^M = (t, x, y, z, w),\qquad w \equiv x^4.
  \]
- Spatial bulk coordinate: \(\mathbf X=(x,y,z,w)\in\mathbb R^4\).  
- Brane spatial coordinate: \(\mathbf x=(x,y,z)\in\mathbb R^3\).

### Index sets
- Spacetime indices: \(M,N\in\{0,1,2,3,4\}\) with \(0\equiv t\) and \(4\equiv w\).
- Bulk spatial indices: \(i,j\in\{x,y,z,w\}\).
- Brane spatial indices: \(a,b\in\{x,y,z\}\).

### Metric convention (for Maxwell bookkeeping)
- Flat Minkowski signature:
  \[
    \eta_{MN}=\mathrm{diag}(-1,+1,+1,+1,+1).
  \]
**Important:** the matter field is nonrelativistic (Schrödinger/GNLS); “covariant” in this paper primarily means **gauge-covariant**, not 5D Lorentz-covariant.

### Differential operators
- Bulk (4D spatial) gradient and Laplacian:
  \[
    \nabla_4 = (\partial_x,\partial_y,\partial_z,\partial_w),\qquad
    \nabla_4^2=\partial_x^2+\partial_y^2+\partial_z^2+\partial_w^2.
  \]
- Brane (3D spatial) operators:
  \[
    \nabla_3 = (\partial_x,\partial_y,\partial_z),\qquad
    \nabla_3^2=\partial_x^2+\partial_y^2+\partial_z^2.
  \]

### Field content
1. **Matter/order parameter** (complex scalar):
   \[
     \psi(\mathbf X,t)\in\mathbb C,\qquad \rho(\mathbf X,t)\equiv |\psi|^2.
   \]
   \(\rho\) is interpreted as **number density**; mass density is \(m\rho\) if needed.

2. **Gauge field**:
   \[
     A_M(x)=(A_0,A_i),\qquad F_{MN}=\partial_MA_N-\partial_NA_M.
   \]
   The contraction \(\partial\!\cdot\!A\equiv \partial_M A^M\) appears in gauge fixing.

3. **Localization profile for EM**: a prescribed function \(Z(w)>0\), peaked near \(w=0\) and decaying as \(|w|\to\infty\).

4. **Confinement potential**:
   \[
     V_{\rm conf}(\mathbf X; a,L),
   \]
   which defines the localized tube/throat region and depends on geometry parameters \(a(t)\) and \(L(t)\).

5. **Geometry degrees of freedom (DOFs)**:
   \[
     a(t)\ \text{(effective radius)},\qquad L(t)\ \text{(effective length)}.
   \]

### Minimal coupling (covariant derivatives)
\[
D_t\psi = \partial_t\psi + \frac{i q}{\hbar}A_0\psi,\qquad
D_i\psi = \partial_i\psi - \frac{i q}{\hbar}A_i\psi.
\]

### Matter number current and bulk velocity
\[
j^i \equiv \frac{\hbar}{m}\,\mathrm{Im}\left(\psi^*D_i\psi\right),\qquad
\partial_t\rho+\partial_i j^i=0.
\]
Where \(\rho>0\), define the bulk velocity by
\[
j^i=\rho v^i,\qquad v^i=j^i/\rho.
\]

### Charge current bookkeeping
The paper uses the convention
\[
J_\psi^M = (q\rho,\ q j^i),
\]
and distinguishes this dynamical matter current from **external/background** sources \(J_{\rm ext}^M\).

---

## 3) Critical distinction: “projection” vs “reduction”

The paper uses **two different operations** involving the extra coordinate \(w\):

### (A) Projection = operational definition of brane observables
Given a fixed, normalized weight \(W(w)\ge 0\),
\[
\int_{-\infty}^{\infty}W(w)\,dw=1,
\]
define any brane observable as a weighted average over \(w\):
\[
\langle f\rangle_W(\mathbf x,t)=\int_{-\infty}^{\infty}W(w)\,f(\mathbf x,w,t)\,dw.
\]
This is a **measurement definition**. It is not an approximation.

### (B) Reduction = integrate out \(w\) under a stated ansatz
In controlled limits (e.g. EM zero-mode), one **integrates the bulk equations** over \(w\) to produce an **effective 3+1 theory** with renormalized couplings, e.g.
\[
Z_{\rm int}=\int Z(w)\,dw,\qquad \mu_0^{\rm eff}=\mu_0/Z_{\rm int}.
\]
This is a **controlled reduction** that depends on explicit assumptions (e.g. \(w\)-independence of the fields).

---

## 4) Full model specification (the action)

The total action is
\[
S = S_\psi + S_{\rm EM} + S_{\rm geom}.
\]

### 4.1 Matter sector: gauged 4D GNLS with confinement
Lagrangian density:
\[
\boxed{
\mathcal L_\psi
=
\frac{i\hbar}{2}\left(\psi^*D_t\psi-\psi\,D_t\psi^*\right)
-\frac{\hbar^2}{2m}(D_i\psi)^*(D_i\psi)
- V_{\rm conf}(\mathbf X;a,L)\,\rho
- U(\rho)
}
\]
with \(i\in\{x,y,z,w\}\).

#### Frozen stiff polytropic EOS
- Pressure:
  \[
    P(\rho)=K\rho^5.
  \]
- Internal energy density:
  \[
    U(\rho)=\frac{K}{4}\rho^5.
  \]
- Enthalpy-like potential appearing in the GNLS/Madelung form:
  \[
    h(\rho)=\frac{dU}{d\rho}=\frac{5K}{4}\rho^4.
  \]
- Sound speed:
  \[
    c_s^2(\rho)=\frac{1}{m}\frac{dP}{d\rho}=\frac{5K}{m}\rho^4.
  \]

### 4.2 Electromagnetic sector: localized Maxwell + gauge fixing + external sources
Key bookkeeping rule: because \(\mathcal L_\psi\) uses covariant derivatives, **varying \(S_\psi\) already generates the dynamical matter current \(J_\psi^M\)**.  
Therefore any explicit \(A_MJ^M\) term in \(\mathcal L_{\rm EM}\) must represent **external/background sources only**, denoted \(J_{\rm ext}^M\).

Lagrangian density:
\[
\boxed{
\mathcal L_{\rm EM}
=
-\frac{Z(w)}{4\mu_0}F_{MN}F^{MN}
-\frac{1}{2\xi\mu_0}(\partial\!\cdot\!A)^2
+ A_M J_{\rm ext}^M
}
\]
- \(\xi\): covariant gauge-fixing parameter.
- Total source in Maxwell’s equation:
  \[
    J_{\rm tot}^M = J_\psi^M + J_{\rm ext}^M.
  \]

**Neutralizing background (“jellium”)** is implemented as \(J_{\rm ext}^0\), e.g.
\[
J_{\rm ext}^0=-q\rho_0,\qquad J_{\rm ext}^i=0
\quad\Rightarrow\quad
J_{\rm tot}^0=q(\rho-\rho_0).
\]

### 4.3 Geometry sector: two dynamical DOFs \(a(t),L(t)\)
Baseline effective mechanical Lagrangian:
\[
\boxed{
\mathcal L_{\rm geom}
=
\frac{1}{2}M_a\dot a^2 + \frac{1}{2}M_L\dot L^2
- E_{\rm geom}(a,L) - E_{\rm ratio}(a,L)
}
\]
Optional stiff ratio penalty:
\[
E_{\rm ratio}(a,L)=\frac{\kappa}{2}\big(L-\alpha a\big)^2.
\]
Total conservative energy:
\[
H_{\rm tot}=H_\psi[\psi;a,L] + H_{\rm EM}[A;a,L] + E_{\rm geom}(a,L) + E_{\rm ratio}(a,L).
\]
Generalized geometry forces:
\[
F_a=-\frac{\partial H_{\rm tot}}{\partial a},\qquad
F_L=-\frac{\partial H_{\rm tot}}{\partial L}.
\]
Baseline damped evolution laws:
\[
\boxed{
M_a\ddot a+\Gamma_a\dot a = -\frac{\partial H_{\rm tot}}{\partial a},\qquad
M_L\ddot L+\Gamma_L\dot L = -\frac{\partial H_{\rm tot}}{\partial L}.
}
\]

---

## 5) Exact Euler–Lagrange equations and hydrodynamic identities

### 5.1 Matter equation of motion (gauged 4D GNLS)
Variation of \(S_\psi\) w.r.t. \(\psi^*\):
\[
\boxed{
i\hbar D_t\psi
=
\left[
-\frac{\hbar^2}{2m}D_iD_i + V_{\rm conf}(\mathbf X;a,L) + h(\rho)
\right]\psi.
}
\]

### 5.2 Conserved current and continuity
Number current:
\[
\boxed{
j^i(\mathbf X,t)=\frac{\hbar}{m}\,\mathrm{Im}\left(\psi^*D_i\psi\right),
}
\]
continuity:
\[
\boxed{\partial_t\rho + \partial_i j^i = 0.}
\]

### 5.3 Localized Maxwell equation (exact, with gauge fixing)
Variation of \(S_{\rm EM}\) w.r.t. \(A_N\):
\[
\boxed{
\partial_M\left(Z(w)F^{MN}\right)
+\frac{1}{\xi}\partial^N(\partial\!\cdot\!A)
=
\mu_0\left(J_\psi^N+J_{\rm ext}^N\right).
}
\]

Define bulk “electric” and “magnetic” components:
\[
E_i=-\partial_t A_i-\partial_i A_0,\qquad
B_{ij}=\partial_iA_j-\partial_jA_i=F_{ij}.
\]

### 5.4 Madelung rewrite and Euler-like bulk form
Madelung substitution:
\[
\psi=\sqrt{\rho}\,e^{i\theta}.
\]
Gauge-invariant velocity:
\[
\boxed{
v_i=\frac{\hbar}{m}\left(\partial_i\theta - \frac{q}{\hbar}A_i\right).
}
\]
Quantum potential:
\[
\boxed{
Q(\rho)=-\frac{\hbar^2}{2m}\frac{\nabla_4^2\sqrt{\rho}}{\sqrt{\rho}}.
}
\]
Exact Euler-like equation in bulk:
\[
\boxed{
m(\partial_t+v_j\partial_j)v_i
=
q(E_i+v_jB_{ij})
-\partial_i\left(V_{\rm conf}+h(\rho)+Q(\rho)\right).
}
\]

### 5.5 Vorticity–gauge identity (exact)
Define vorticity 2-form:
\[
\Omega_{ij}=\partial_i v_j-\partial_j v_i.
\]
Then (away from phase singularities),
\[
\boxed{
\Omega_{ij} = -\frac{q}{m}B_{ij} = -\frac{q}{m}F_{ij}.
}
\]
So bulk vorticity is directly tied to the gauge field.

---

## 6) Brane observables via projection (exact identities)

### 6.1 Projection weight and brane fields
Given a normalized brane weight \(W(w)\),
\[
\int W(w)\,dw=1,
\]
define:
\[
\boxed{
\rho_{\rm brane}(\mathbf x,t)=\int W(w)\rho(\mathbf x,w,t)\,dw,
}
\]
\[
\boxed{
\mathbf j_{\rm brane}(\mathbf x,t)=\int W(w)\mathbf j_{xyz}(\mathbf x,w,t)\,dw,
}
\]
where \(\mathbf j_{xyz}=(j^x,j^y,j^z)\).

Brane velocity (kinematic definition):
\[
\boxed{
\mathbf v_{\rm brane}(\mathbf x,t)=\frac{\mathbf j_{\rm brane}}{\rho_{\rm brane}}\quad (\rho_{\rm brane}>0).
}
\]
**Non-commutation reminder:** this is a ratio of averages, not an average of bulk velocities.

### 6.2 Projected continuity with leakage (exact)
Starting from bulk continuity and integrating over \(w\),
\[
\boxed{
\partial_t\rho_{\rm brane} + \nabla_3\cdot \mathbf j_{\rm brane} = S_{\rm leak},
}
\]
with exact leakage source
\[
\boxed{
S_{\rm leak}(\mathbf x,t)
=
-\left[W(w)j^w(\mathbf x,w,t)\right]_{-\infty}^{+\infty}
+
\int_{-\infty}^{\infty} W'(w)\,j^w(\mathbf x,w,t)\,dw.
}
\]
If \(Wj^w\to 0\) as \(|w|\to\infty\), then
\[
\boxed{
S_{\rm leak}(\mathbf x,t)=\int W'(w)\,j^w(\mathbf x,w,t)\,dw.
}
\]

Interpretation: even with exact bulk conservation, projected density can change due to \(w\)-directed flow.

---

## 7) Longitudinal identity and the “Poisson hook”

### 7.1 Helmholtz decomposition on the brane
On \(\mathbb R^3\), decompose brane velocity:
\[
\boxed{
\mathbf v_{\rm brane} = \nabla_3\varphi + \mathbf v_T,\qquad \nabla_3\cdot \mathbf v_T = 0.
}
\]
\(\varphi\) is the **brane velocity potential** (not the EM scalar potential).

### 7.2 Exact longitudinal identity (from projected continuity)
Use \(\mathbf j_{\rm brane}=\rho_{\rm brane}\mathbf v_{\rm brane}\) and \(\nabla_3\cdot \mathbf v_{\rm brane}=\nabla_3^2\varphi\) to rewrite projected continuity as:
\[
\boxed{
\rho_{\rm brane}\,\nabla_3^2\varphi
=
S_{\rm leak}
-\partial_t\rho_{\rm brane}
-(\nabla_3\rho_{\rm brane})\cdot(\nabla_3\varphi+\mathbf v_T).
}
\]
This is an **identity** (no approximation), given the definitions of projection and Helmholtz decomposition.

### 7.3 Poisson regime (controlled approximation)
A standard Poisson **equation** emerges when:
1. **Quasi-static brane density:** \(\partial_t\rho_{\rm brane}\) small.
2. **Weak density-gradient/advection correction:** \((\nabla_3\rho_{\rm brane})\cdot(\nabla_3\varphi+\mathbf v_T)\) small.
3. Often: **longitudinal dominance:** \(\mathbf v_T\) small/slow.

Then:
\[
\rho_{\rm brane}\,\nabla_3^2\varphi \approx S_{\rm eff},
\]
and if \(\rho_{\rm brane}\approx \rho_0\) is approximately constant:
\[
\boxed{
\nabla_3^2\varphi \approx \frac{1}{\rho_0}S_{\rm eff}.
}
\]

### 7.4 Inverse-square scaling
For a localized effective source \(S_{\rm eff}\approx \mathcal S\,\delta^{(3)}(\mathbf x)\),
\[
\varphi(\mathbf x)\sim -\frac{\mathcal S}{4\pi\rho_0}\frac{1}{r},\qquad r=|\mathbf x|.
\]
If \(\mathbf v_{\rm brane}\approx \nabla_3\varphi\), then the longitudinal field scales as
\[
\boxed{
\mathbf v_L(\mathbf x)=\nabla_3\varphi(\mathbf x)\sim \frac{\mathcal S}{4\pi\rho_0}\frac{1}{r^2}\,\hat{\mathbf r}.
}
\]
**Interpretational boundary:** the paper derives inverse-square scaling for \(\mathbf v_L\). Any identification of \(\mathbf v_L\) with “Newtonian gravity felt by test bodies” is an additional constitutive step beyond this kinematic derivation.

---

## 8) Controlled EM localization reduction to an effective brane Maxwell theory

This is not “projection.” It is a **reduction** under a zero-mode ansatz.

### 8.1 Zero-mode assumptions
Start from exact localized Maxwell:
\[
\partial_M(ZF^{MN})+\frac{1}{\xi}\partial^N(\partial\!\cdot\!A)=\mu_0(J_\psi^N+J_{\rm ext}^N).
\]
Assume:
\[
\boxed{
A_w=0,\qquad \partial_w A_\mu = 0\ (\mu\in\{0,1,2,3\}),
}
\]
and for presentation adopt Lorenz gauge \(\partial\!\cdot\!A=0\) during reduction.

Consistency of the \(N=w\) component then requires
\[
0=\mu_0(J_\psi^w+J_{\rm ext}^w),
\]
so a strict zero-mode sector is consistent only when the **total \(w\)-directed charge current is negligible**.

### 8.2 Localization integral and effective coupling
Define
\[
\boxed{
Z_{\rm int}=\int_{-\infty}^{\infty}Z(w)\,dw.
}
\]
Under the zero-mode ansatz, integrate the \(\nu\in\{0,1,2,3\}\) components over \(w\) to get:
\[
\boxed{
\partial_\mu F^{\mu\nu} = \mu_0^{\rm eff} J_{\rm eff}^\nu,\qquad
\mu_0^{\rm eff}=\frac{\mu_0}{Z_{\rm int}},
}
\]
with effective source
\[
\boxed{
J_{\rm eff}^\nu(\mathbf x,t)=\int_{-\infty}^{\infty}\big(J_\psi^\nu(\mathbf x,w,t)+J_{\rm ext}^\nu(\mathbf x,w,t)\big)\,dw.
}
\]

### 8.3 Source profile matching (important subtlety)
Because the bulk equation is pointwise in \(w\), a strictly \(w\)-independent \(F^{\mu\nu}(\mathbf x,t)\) solves it for all \(w\) only if the total source matches the localization profile:
\[
\boxed{
J_\psi^\nu(\mathbf x,w,t)+J_{\rm ext}^\nu(\mathbf x,w,t)
=
\frac{Z(w)}{Z_{\rm int}}\,J_{\rm eff}^\nu(\mathbf x,t).
}
\]
Otherwise, higher \(w\)-modes are excited; \(\partial_\mu F^{\mu\nu}=\mu_0^{\rm eff}J_{\rm eff}^\nu\) should then be read as the **leading zero-mode equation**.

### 8.4 Effective action viewpoint
Under \(\partial_w A_\mu=0\), \(A_w=0\), the Maxwell term reduces as
\[
\int dt\int d^4X\left(-\frac{Z(w)}{4\mu_0}F_{MN}F^{MN}\right)
\to
\left(\int Z(w)\,dw\right)\int dt\int d^3x\left(-\frac{1}{4\mu_0}F_{\mu\nu}F^{\mu\nu}\right),
\]
which is equivalent to renormalizing \(\mu_0\to\mu_0^{\rm eff}=\mu_0/Z_{\rm int}\).

### 8.5 Electrostatic brane limit
If time-independent and \(\mathbf E=-\nabla_3\Phi_{\rm EM}\), then
\[
\boxed{
\nabla_3^2\Phi_{\rm EM} = -\mu_0^{\rm eff}J_{\rm eff}^0.
}
\]
This provides a consistency check: both the “gravity Poisson hook” and reduced electrostatics lead to Poisson operators on the brane, via different controlled limits.

---

## 9) Geometry forces and consistency ledger

### 9.1 Ledger identity (non-negotiable bookkeeping)
Define
\[
H_{\rm tot} = H_\psi + H_{\rm EM} + E_{\rm geom}+E_{\rm ratio},
\]
then
\[
\boxed{
F_a=-\partial_a H_{\rm tot},\qquad F_L=-\partial_L H_{\rm tot}.
}
\]

### 9.2 Matter contribution to geometry forces (Hellmann–Feynman form)
If geometry dependence enters matter primarily via \(V_{\rm conf}(\mathbf X;a,L)\), then
\[
\boxed{
F_a^{(\psi)}=-\frac{\partial H_\psi}{\partial a}
=
-\int d^4X\ \rho(\mathbf X,t)\,\partial_a V_{\rm conf}(\mathbf X;a,L),
}
\]
\[
\boxed{
F_L^{(\psi)}=-\frac{\partial H_\psi}{\partial L}
=
-\int d^4X\ \rho(\mathbf X,t)\,\partial_L V_{\rm conf}(\mathbf X;a,L).
}
\]

### 9.3 Ratio penalty forces
From \(E_{\rm ratio}=\frac{\kappa}{2}(L-\alpha a)^2\),
\[
\boxed{
F_a^{(\rm ratio)}=+\kappa\alpha(L-\alpha a),\qquad
F_L^{(\rm ratio)}=-\kappa(L-\alpha a).
}
\]

### 9.4 Minimal geometry energy model used in this paper
Baseline closure:
\[
\boxed{
E_{\rm geom}(a,L)=P_{\rm vac}V(a,L)+\sigma A(a,L),
}
\]
interpreting \(V\) and \(A\) as 4D “tube” measures for \(B^3(a)\times[0,L]\):
\[
V(a,L)=\frac{4\pi}{3}a^3 L,
\]
\[
A(a,L)=4\pi a^2L + 2\cdot\frac{4\pi}{3}a^3
\quad\text{(side hyperarea + two endcaps)}.
\]
Derivatives:
\[
\frac{\partial V}{\partial a}=4\pi a^2L,\qquad
\frac{\partial V}{\partial L}=\frac{4\pi}{3}a^3,
\]
\[
\frac{\partial A}{\partial a}=8\pi a L + 8\pi a^2,\qquad
\frac{\partial A}{\partial L}=4\pi a^2.
\]

### 9.5 Dynamic geometry equations and quasi-static limits
Baseline:
\[
M_a\ddot a+\Gamma_a\dot a=-\partial_a H_{\rm tot},\qquad
M_L\ddot L+\Gamma_L\dot L=-\partial_L H_{\rm tot}.
\]
Controlled quasi-static reductions:
- **Overdamped**: neglect \(\ddot a,\ddot L\) → first-order relaxation.
- **Instantaneous minimization**: \(\partial_a H_{\rm tot}\approx 0\), \(\partial_L H_{\rm tot}\approx 0\).

Interpretation: this closure provides explicit energy exchange + ringing/relaxation, but does not claim to be a microscopic wall theory.

---

## 10) Projected brane momentum (appendix): what extra terms appear

The main text mostly uses continuity + kinematics; the appendix records the momentum projection structure.

### 10.1 Bulk momentum balance (brane components)
Let
\[
\Pi\equiv V_{\rm conf}+h(\rho)+Q(\rho).
\]
From the Euler-like equation, the brane component satisfies the exact bulk balance:
\[
\boxed{
\partial_t(\rho v_a) + \partial_j(\rho v_a v_j)
=
\frac{q}{m}\rho(E_a+v_jB_{aj}) - \frac{1}{m}\rho\,\partial_a\Pi,
}
\]
with \(j\in\{x,y,z,w\}\).

### 10.2 Projected brane momentum identity (exact)
Define projected momentum density:
\[
p_{{\rm brane},a}(\mathbf x,t)=\langle \rho v_a\rangle_W.
\]
Then:
\[
\boxed{
\partial_t p_{{\rm brane},a}
+
\partial_b\langle \rho v_a v_b\rangle_W
=
\mathcal S^{(\rm mom)}_a + \mathcal L^{(\rm mom)}_a,
}
\]
where the projected force/source is
\[
\boxed{
\mathcal S^{(\rm mom)}_a
=
\left\langle
\frac{q}{m}\rho(E_a+v_jB_{aj})
-\frac{1}{m}\rho\,\partial_a\Pi
\right\rangle_W,
}
\]
and momentum leakage is
\[
\boxed{
\mathcal L^{(\rm mom)}_a
=
-\left[W\rho v_a v_w\right]_{-\infty}^{+\infty}
+
\int W'(w)\rho v_a v_w\,dw.
}
\]
With fast decay so the boundary term vanishes,
\[
\mathcal L^{(\rm mom)}_a=\int W'(w)\rho v_a v_w\,dw.
\]

### 10.3 Stress / non-commutation correction tensor
Decompose
\[
\langle \rho v_a v_b\rangle_W
=
\rho_{\rm brane}v_{{\rm brane},a}v_{{\rm brane},b}+\tau_{ab},
\]
defining
\[
\boxed{
\tau_{ab}=
\langle \rho v_a v_b\rangle_W
-
\rho_{\rm brane}v_{{\rm brane},a}v_{{\rm brane},b}.
}
\]
Then the projected momentum equation becomes
\[
\boxed{
\partial_t(\rho_{\rm brane}v_{{\rm brane},a})
+
\partial_b(\rho_{\rm brane}v_{{\rm brane},a}v_{{\rm brane},b})
=
\mathcal S^{(\rm mom)}_a + \mathcal L^{(\rm mom)}_a - \partial_b\tau_{ab}.
}
\]
So **any** attempt to write a closed 3D Euler system on the brane requires modeling or bounding \(\tau_{ab}\) and \(\mathcal L_a^{(\rm mom)}\).

---

## 11) Gauge choices and source bookkeeping (appendix)

### 11.1 Gauge transformations
\[
A_M\mapsto A_M+\partial_M\chi,\qquad
\psi\mapsto e^{iq\chi/\hbar}\psi.
\]
Then \(D_M\psi\) transforms covariantly and \(F_{MN}\) is gauge invariant.

### 11.2 Gauge fixing (\(\xi\))
The gauge-fixing term is
\[
-\frac{1}{2\xi\mu_0}(\partial\!\cdot\!A)^2.
\]
Lorenz gauge \(\partial\!\cdot\!A=0\) is used as a convenient presentation choice and in the EM reduction.

### 11.3 Single-source bookkeeping rule
- \(J_\psi\) is generated automatically by varying \(S_\psi\).
- Any explicit \(A_MJ^M\) term in \(\mathcal L_{\rm EM}\) must use \(J_{\rm ext}\) (external/background only).
- Neutralizing background implemented via \(J_{\rm ext}^0\).

A practical checklist in the appendix emphasizes avoiding double counting.

---

## 12) Claim taxonomy (appendix): exact vs controlled vs regime

### Exact (no approximations)
- EOM from the declared action: GNLS, localized Maxwell, geometry force definitions/closure.
- Conservation and hydrodynamic identities: current, continuity, Madelung velocity, quantum potential, Euler-like form, vorticity–gauge identity.
- Projection identities: brane observables, projected continuity + exact leakage, Helmholtz identity, exact longitudinal identity.
- Geometry ledger identities: force definitions and force decompositions.

### Controlled reductions (explicit assumptions)
- EM localization reduction to brane Maxwell: requires zero-mode ansatz (and usually Lorenz gauge during reduction).
- Electrostatic limit of reduced EM.
- Quasi-static geometry limits (overdamped or fast-relaxation).
- Boundary-term suppression in leakage formulas.

### Regime statements (approximate; must be validated)
- Poisson equation as a reduction of the longitudinal identity requires smallness of time-variation and density-gradient/advection corrections (and often small transverse part).
- Inverse-square scaling additionally requires localized sources and appropriate domain/boundary conditions.

---

## 13) How to use this framework in practice (paper’s recommended workflow)

1. **Fix model inputs**: choose \(V_{\rm conf}\), \(Z(w)\), projection weight \(W(w)\), external sources \(J_{\rm ext}\), and geometry parameters \((M_a,M_L,\Gamma_a,\Gamma_L,\kappa,\alpha)\).
2. **Solve/analyze bulk EOMs**: GNLS + localized Maxwell + geometry ODEs.
3. **Construct brane observables**: compute \(\rho_{\rm brane}\), \(\mathbf j_{\rm brane}\), and leakage \(S_{\rm leak}\).
4. **Diagnose Poisson regime**: evaluate the explicit correction terms in the exact longitudinal identity and compare them to the source term.
5. **Use controlled reductions** where appropriate: EM zero-mode reduction, quasi-static geometry, etc.

---

## 14) High-level conceptual map (what depends on what)

- **Bulk dynamics** is always governed by the action → GNLS + localized Maxwell + geometry closure.
- **Brane “gravity” structure** comes from:
  - *definitions*: projection \(W(w)\), brane velocity, Helmholtz decomposition,
  - *identity*: projected continuity → longitudinal identity,
  - *regime*: Poisson limit → inverse-square scaling for \(\nabla_3\varphi\).
- **Brane electromagnetism** comes from:
  - *controlled reduction*: zero-mode + integrating over \(w\) → effective Maxwell with \(\mu_0^{\rm eff}\).

This paper’s main philosophical move is: **operators like \(\nabla_3^2\)** on the brane are not assumed; they appear as consequences of what the brane observer measures, plus mathematically inevitable decompositions in 3D.

