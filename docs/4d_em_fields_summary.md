4d_em_fields.tex

## 1) What this paper is trying to accomplish

This paper (“Paper VIII” in the toy-model sequence) isolates the **electromagnetic / gauge-field sector** of the unified brane–bulk toy model and shows how ordinary **3+1 Maxwell theory on the brane** arises from a **localized 4+1 Maxwell action**.

It is explicitly designed to answer the referee-style question left open by the earlier “EM-from-flow dictionary” papers:

> Where do the **inhomogeneous** Maxwell equations (and the correct propagator / retarded structure) come from, *dynamically*, without postulating them by hand?

### Core deliverables (as stated/derived)

1. **Bulk dynamics (exact):** starting from a localized 4+1 action, derive the bulk Euler–Lagrange equations
   \[
   \partial_M\big(Z(w)F^{MN}\big) + \frac{1}{\xi}\,\partial^N(\partial\!\cdot\!A) = \mu_0 J^N,
   \]
   plus the Bianchi identities and a divergence consistency identity tying the gauge condition to current conservation.

2. **Controlled brane reduction (Maxwell limit):** under explicit reduction assumptions (axial gauge, zero-mode dominance, brane-localized sources), integrate over the transverse direction and obtain standard 3+1 Maxwell on the brane with a computable effective coupling
   \[
   \mu_0^{\rm eff} = \frac{\mu_0}{Z_{\rm int}},
   \qquad
   Z_{\rm int}=\int_{-\infty}^{\infty}Z(w)\,dw.
   \]
   For a Gaussian profile \(Z(w)=e^{-w^2/\lambda^2}\), this becomes \(\mu_0^{\rm eff}=\mu_0/(\lambda\sqrt\pi)\).

3. **KK corrections (quantitative, falsifiable):** for Gaussian localization, solve the transverse Sturm–Liouville problem in closed form. The result is a discrete KK tower with a **rigid** mass/coupling pattern that yields **Yukawa-suppressed** departures from Coulomb’s law. The leading correction is fixed:
   \[
   A_0(r)
   = \frac{\mu_0^{\rm eff}q}{4\pi r}
     \Big[1+\tfrac12 e^{-2r/\lambda}+\cdots\Big].
   \]

4. **Moving sources (causal + brane-Lorentz covariant):** each KK mode propagates with a covariant retarded Green function. Massive modes produce causal “tails” inside the light cone; summing the tower preserves causality and depends on brane momenta only through the Lorentz scalar \(k^2\).

5. **Source consistency (derived, not imposed):** a minimal brane matter model with local \(U(1)\) phase symmetry produces a conserved Noether current, which supplies the conserved source required by the Maxwell divergence identity (closing the gauge symmetry ↔ current conservation ↔ Maxwell consistency loop).


## 2) Frozen conventions, objects, and notation (the bookkeeping you must keep consistent)

### 2.1 Coordinates, indices, and metric

Bulk coordinates:
\[
x^M=(t,x,y,z,w),
\qquad
M,N\in\{0,1,2,3,4\}.
\]

Brane indices:
\[
\mu,\nu\in\{0,1,2,3\},
\qquad
x^\mu=(t,x,y,z).
\]

Brane spatial indices:
\[
i,j\in\{1,2,3\}.
\]

Flat bulk metric (“mostly plus”):
\[
\eta_{MN}=\mathrm{diag}(-1,1,1,1,1),
\qquad
\eta^{MN}=(\eta_{MN})^{-1}.
\]

Bulk d’Alembertian:
\[
\Box \equiv \eta^{MN}\partial_M\partial_N
= -\partial_t^2 + \nabla^2 + \partial_w^2,
\]
with \(\nabla\) the 3D gradient in \((x,y,z)\). Units take the brane light-cone speed to be 1 (restore \(c\) by \(t\mapsto ct\)).

### 2.2 Localization profile

A nonnegative localization profile \(Z(w)\) multiplies the Maxwell kinetic term. This paper chooses a Gaussian:
\[
Z(w)=\exp\!\left(-\frac{w^2}{\lambda^2}\right),
\]
with finite integral
\[
Z_{\rm int}=\int_{-\infty}^{\infty}Z(w)\,dw = \lambda\sqrt\pi.
\]

All integrations by parts in \(w\) assume the relevant boundary terms vanish as \(|w|\to\infty\) (true for the localized configurations considered, and checked in the symbolic suite).

### 2.3 Gauge field and field strength

Bulk gauge potential \(A_M(x)\) is treated as a **covector** (one-form). Field strength:
\[
F_{MN}=\partial_M A_N-\partial_N A_M,
\qquad
F^{MN}=\eta^{MP}\eta^{NQ}F_{PQ}.
\]

Divergence:
\[
\partial\!\cdot\!A \equiv \partial_M A^M,
\qquad
A^M\equiv \eta^{MN}A_N.
\]

### 2.4 Gauge fixing parameter

A Lorenz-type gauge-fixing term is included with parameter \(\xi\) (called \(\xi_{\rm gf}\) in the paper). \(\xi\) labels equivalent gauge-fixed descriptions; gauge-invariant observables do not depend on \(\xi\) when the source is conserved.

### 2.5 Source/current bookkeeping (critical sign + index conventions)

The source is a contravariant bulk current \(J^M(x)\) (a vector field). The coupling sign convention is fixed as:
\[
\mathcal L_{\rm int}=-A_M J^M.
\]

This convention ensures the gauge-variation of the interaction term makes the conservation requirement explicit (see §4 below). It is also explicitly flagged as a major historical source of sign/placement mistakes in symbolic checks.


## 3) Full localized 4+1 Maxwell sector (the action)

The localized Maxwell action (in flat bulk) is
\[
S_{\rm EM}[A;Z]
=\int dt\,d^3x\,dw\;
\left[
-\frac{Z(w)}{4\mu_0}F_{MN}F^{MN}
-\frac{1}{2\xi\mu_0}(\partial\!\cdot\!A)^2
- A_M J^M
\right].
\]

Notes:

* Only the Maxwell kinetic term is multiplied by \(Z(w)\). The gauge-fixing term is not weighted by \(Z\) in this presentation.
* \(\mu_0\) is the “bare” 4+1 coupling parameter; the brane sees \(\mu_0^{\rm eff}=\mu_0/Z_{\rm int}\) in the controlled Maxwell limit (§5).


## 4) Exact Euler–Lagrange equations and identities (bulk statements)

Everything in this section is **exact** (no brane reduction assumptions yet).

### 4.1 Bulk Maxwell equations (with localization + gauge fixing)

Varying \(A_N\) gives:
\[
\partial_M\big(Z(w)F^{MN}\big)
+\frac{1}{\xi}\,\partial^N(\partial\!\cdot\!A)
= \mu_0 J^N.
\]
Define the “Maxwell operator”
\[
\mathcal M^N[A]\equiv
\partial_M\big(ZF^{MN}\big)
+\frac{1}{\xi}\,\partial^N(\partial\!\cdot\!A),
\qquad
\mathcal M^N[A]=\mu_0 J^N.
\]

### 4.2 Bianchi identities (homogeneous Maxwell)

From the definition of \(F\):
\[
\partial_{[L}F_{MN]}=0
\quad\Leftrightarrow\quad
\partial_LF_{MN}+\partial_MF_{NL}+\partial_NF_{LM}=0.
\]
These are off-shell identities (hold for any smooth \(A_M\)).

### 4.3 Divergence consistency identity (Maxwell consistency ↔ current conservation)

Taking \(\partial_N\) of the EOM, the “double divergence” term vanishes because \(ZF^{MN}\) is antisymmetric:
\[
\partial_N\partial_M(ZF^{MN})=0.
\]
So one obtains the exact identity
\[
\partial_N(\mathcal M^N[A]-\mu_0 J^N)
=
\frac{1}{\xi}\,\Box(\partial\!\cdot\!A) - \mu_0\,\partial_N J^N.
\]

Consequences:

* In **Lorenz gauge** \(\partial\!\cdot\!A=0\), the Maxwell equations enforce bulk current conservation:
  \[
  \partial_N J^N=0.
  \]
* Conversely, if \(\partial_N J^N=0\), the gauge-fixing term can be understood as selecting a representative in the gauge orbit without affecting gauge-invariant observables.


## 5) Gauge structure and brane Lorentz covariance

### 5.1 Gauge transformations

Infinitesimal gauge transformation:
\[
\delta_\chi A_M = \partial_M\chi.
\]

Then \(\delta_\chi F_{MN}=0\), so the kinetic term is invariant. The interaction term varies as:
\[
\delta_\chi\mathcal L_{\rm int}
=-(\partial_M\chi)J^M
= -\partial_M(\chi J^M)+\chi\,\partial_M J^M.
\]
So (dropping boundary terms) gauge invariance of the coupling is equivalent to \(\partial_M J^M=0\).

Gauge fixing breaks gauge invariance in the standard way because
\[
\delta_\chi(\partial\!\cdot\!A)=\Box\chi.
\]

### 5.2 Brane Lorentz symmetry + transformation types (important implementation detail)

Because \(Z(w)\) depends only on \(w\), the theory preserves exact **3+1 Poincaré symmetry** along the brane.

A key bookkeeping rule:

* \(A_\mu\) transforms as a **covector** (one-form) on the brane.
* \(J^\mu\) transforms as a **vector** on the brane.

Under a brane Lorentz transform \(x'^\mu=\Lambda^\mu{}_{\nu}x^\nu\):
\[
A'_\mu(x')=(\Lambda^{-1})^\nu{}_{\mu}A_\nu(x),
\qquad
J'^\mu(x')=\Lambda^\mu{}_{\nu}J^\nu(x).
\]
With these transformation types, \(A_\mu J^\mu\) is a scalar and \(F_{\mu\nu}F^{\mu\nu}\) is invariant.

### 5.3 “Propagator depends only on \(k^2\)” statement

Fourier transforming along the brane, \(\partial_\mu\to i k_\mu\), the brane momentum enters only through
\[
k^2\equiv\eta^{\mu\nu}k_\mu k_\nu=-\omega^2+\mathbf k^2.
\]
The brane-to-brane response kernel becomes a KK sum of the schematic form
\[
D_{\rm eff}(k^2)\sim\sum_n\frac{c_n}{k^2-m_n^2+i\epsilon},
\]
so brane Lorentz covariance is manifest.


## 6) Controlled brane reduction and the effective coupling \(\mu_0^{\rm eff}\)

Everything here is **controlled**: it requires explicit reduction assumptions.

### 6.1 Axial gauge reachability and residual 3+1 gauge freedom

Under \(\delta A_M=\partial_M\chi\), the transverse component shifts as
\(A_w\mapsto A_w+\partial_w\chi\). One may reach **axial gauge** \(A_w=0\) by choosing
\[
\chi_{\rm Ax}(x^\mu,w)\equiv-\int_0^w A_w(x^\mu,w')\,dw',
\]
so that \(\partial_w\chi_{\rm Ax}=-A_w\).

Residual gauge freedom in axial gauge satisfies \(\partial_w\chi=0\), hence
\[
\chi(x^\mu,w)=\chi_b(x^\mu),
\]
which is precisely ordinary 3+1 gauge freedom on the brane.

In axial gauge, \(\partial\!\cdot\!A=\partial_\mu A^\mu\) once one restricts to configurations with negligible \(w\)-dependence in \(A_\mu\).

### 6.2 Brane-localized sources

A conserved brane source is modeled as
\[
J^\mu(x,w)=J_b^\mu(x)\,\delta(w),
\qquad
J^w(x,w)=0.
\]
Then \(\partial_M J^M=0\) reduces to \(\partial_\mu J_b^\mu=0\) distributionally.

Define the integrated current
\[
J_{\rm eff}^\mu(x)\equiv\int_{-\infty}^{\infty}J^\mu(x,w)\,dw,
\]
so for \(\delta(w)\) sources, \(J_{\rm eff}^\mu=J_b^\mu\).

### 6.3 Exact integrated brane equation (before taking the zero-mode limit)

Write the brane components of the EOM as (\(\nu\in\{0,1,2,3\}\)):
\[
\partial_M\big(ZF^{M\nu}\big)
+\frac{1}{\xi}\,\partial^\nu(\partial\!\cdot\!A)
=\mu_0 J^\nu.
\]
Integrate over \(w\):
\[
\partial_\mu\Big(\int Z F^{\mu\nu}dw\Big)
+\Big[ZF^{w\nu}\Big]_{-\infty}^{+\infty}
+\frac{1}{\xi}\,\partial^\nu\Big(\int (\partial\!\cdot\!A)dw\Big)
=\mu_0 J_{\rm eff}^\nu.
\]
For localized fields, the boundary term vanishes. Define the **weighted brane field strength**
\[
\bar F^{\mu\nu}(x)\equiv \frac{1}{Z_{\rm int}}\int Z(w)F^{\mu\nu}(x,w)\,dw.
\]
Then the exact integrated equation becomes
\[
\partial_\mu\bar F^{\mu\nu}
+\frac{1}{\xi Z_{\rm int}}\,\partial^\nu\Big(\int (\partial\!\cdot\!A)dw\Big)
=\frac{\mu_0}{Z_{\rm int}}\,J_{\rm eff}^\nu.
\]
This is exact but not yet standard Maxwell because \(\bar F\) is a weighted bulk average and the gauge-fixing term retains an explicit \(w\)-integral.

### 6.4 Zero-mode (Maxwell) limit and \(\mu_0^{\rm eff}\)

Impose the controlled “zero-mode dominance” ansatz (in axial gauge):
\[
A_\mu(x,w)\simeq a_\mu(x),
\qquad
\partial_w A_\mu\simeq 0,
\qquad
A_w=0.
\]
Then
\[
F^{\mu\nu}(x,w)\simeq f^{\mu\nu}(x),
\qquad
f_{\mu\nu}\equiv\partial_\mu a_\nu-\partial_\nu a_\mu,
\]
and \(\int(\partial\!\cdot\!A)dw\simeq Z_{\rm int}(\partial_\mu a^\mu)\). The integrated equation reduces to the standard gauge-fixed 3+1 Maxwell form:
\[
\partial_\mu f^{\mu\nu}
+\frac{1}{\xi}\,\partial^\nu(\partial_\mu a^\mu)
=\mu_0^{\rm eff}\,J_b^\nu,
\qquad
\mu_0^{\rm eff}\equiv\frac{\mu_0}{Z_{\rm int}}.
\]
For Gaussian \(Z\):
\[
\mu_0^{\rm eff}=\frac{\mu_0}{\lambda\sqrt\pi}.
\]
In brane Lorenz gauge \(\partial_\mu a^\mu=0\), this becomes \(\partial_\mu f^{\mu\nu}=\mu_0^{\rm eff}J_b^\nu\).

### 6.5 Consistency of the \(N=w\) equation

The \(N=w\) component of the bulk EOM is
\[
\partial_M\big(ZF^{Mw}\big)
+\frac{1}{\xi}\,\partial^w(\partial\!\cdot\!A)
=\mu_0 J^w.
\]
In axial gauge \(A_w=0\) and the zero-mode ansatz, \(F^{\mu w}=-\partial^w A^\mu\simeq 0\) and \(\partial^w(\partial\!\cdot\!A)\simeq 0\), so consistency requires \(J^w\simeq 0\). This is why the brane source model sets \(J^w=0\).

### 6.6 What causes deviations from 3+1 Maxwell?

The exact integrated equation shows deviations appear when any of the following fail:

1. \(A_\mu\) has significant \(w\)-dependence (KK excitations): \(\bar F^{\mu\nu}\neq f^{\mu\nu}\).
2. \(ZF^{w\nu}\) does not decay fast enough to drop boundary terms.
3. \(J^w\neq 0\) (transverse current / charge leakage).


## 7) Gaussian KK tower and corrections to Coulomb (static sector)

### 7.1 KK mode expansion and transverse Sturm–Liouville problem

In axial gauge and (for simplicity) Lorenz gauge for brane components, expand
\[
A_\mu(x,w)=\sum_{n\ge0} a_\mu^{(n)}(x)\,f_n(w).
\]
The transverse profiles solve the weighted Sturm–Liouville problem
\[
-\frac{d}{dw}\Big(Z(w)\frac{df_n}{dw}\Big)=m_n^2 Z(w) f_n(w).
\]
The natural inner product is weighted:
\[
\langle f,g\rangle=\int_{-\infty}^{\infty}Z(w)f(w)g(w)\,dw.
\]

### 7.2 Closed-form solution for Gaussian localization

For \(Z(w)=e^{-w^2/\lambda^2}\), with \(y=w/\lambda\), the SL equation becomes the Hermite equation, giving:
\[
f_n(w)=H_n\!\left(\frac{w}{\lambda}\right),
\qquad
m_n^2=\frac{2n}{\lambda^2},
\qquad
n=0,1,2,\ldots
\]
So:

* \(n=0\) is the massless Maxwell zero mode.
* \(n\ge1\) are massive 3+1 Proca-like modes.

Mode norms:
\[
\|f_n\|^2\equiv\int Z f_n^2 dw
= \lambda\sqrt\pi\,2^n n!.
\]

### 7.3 Brane couplings and parity selection rule

A brane \(\delta(w)\) source excites each KK mode proportional to its value at \(w=0\). Define the brane coupling weights
\[
c_n\equiv\frac{f_n(0)^2}{\|f_n\|^2}.
\]

Hermite parity implies:

* \(H_n(0)=0\) for odd \(n\) → **odd modes decouple from brane sources**
  \[
  c_{2m+1}=0.
  \]

For even \(n=2m\),
\[
c_{2m}
=\frac{1}{\lambda\sqrt\pi}\,\frac{1}{4^m}\binom{2m}{m}.
\]
In particular,
\[
c_0=\frac{1}{\lambda\sqrt\pi}=\frac{1}{Z_{\rm int}},
\]
matching \(\mu_0^{\rm eff}=\mu_0c_0\).

The coefficient ratios are therefore rigid:
\[
\frac{c_{2m}}{c_0}=\frac{1}{4^m}\binom{2m}{m}
=1,\ \frac12,\ \frac{3}{8},\ \frac{5}{16},\ldots\quad(m=0,1,2,3,\ldots).
\]

### 7.4 Effective brane propagator (momentum space)

The brane-to-brane propagator becomes
\[
D_{\rm eff}(k^2)=\sum_{n\ge0}\frac{c_n}{k^2-m_n^2+i\epsilon},
\qquad
m_n^2=\frac{2n}{\lambda^2}.
\]

### 7.5 Coulomb + Yukawa potential for a static point charge

For a brane point charge \(q\) with \(J_b^0=q\delta^{(3)}(\mathbf x)\), the brane scalar potential is
\[
A_0(r)
=\frac{\mu_0 q}{4\pi r}\sum_{n\ge0} c_n e^{-m_n r}.
\]
Separating the zero mode,
\[
A_0(r)
=\frac{\mu_0^{\rm eff} q}{4\pi r}
\left[
1+\sum_{m\ge1}\frac{c_{2m}}{c_0}e^{-m_{2m}r}
\right],
\qquad
m_{2m}=\frac{2\sqrt m}{\lambda}.
\]

Leading correction at large \(r\):
\[
A_0(r)
=\frac{\mu_0^{\rm eff} q}{4\pi r}
\left[
1+\frac12 e^{-2r/\lambda}
+\mathcal O\!\left(e^{-2\sqrt2\,r/\lambda}\right)
\right].
\]
The radial electric field is \(E_r=-\partial_r A_0\).

Interpretation: \(\lambda\) sets the crossover scale; for \(r\gg\lambda\) the theory is extremely close to Maxwell, while at \(r\sim\lambda\) specific departures appear.


## 8) Moving sources and retarded structure (time-dependent sector)

### 8.1 Mode-by-mode brane equations

For conserved brane sources, each KK mode amplitude satisfies
\[
(\square_4+m_n^2)a_\mu^{(n)}(x)=\mu_0 c_n J_{b\,\mu}(x),
\qquad
\square_4\equiv \partial_t^2-\nabla^2.
\]
(Zero mode is massless; massive modes are covariant massive vector excitations.)

### 8.2 Retarded Green functions and effective retarded kernel

Let \(G^{(m)}_{\rm ret}\) solve
\[
(\square_4+m^2)G^{(m)}_{\rm ret}(x-x')=\delta^{(4)}(x-x'),
\qquad
G^{(m)}_{\rm ret}=0\ \text{for}\ t<t'.
\]
Then
\[
a_\mu^{(n)}(x)=\mu_0 c_n\int d^4x'\,G^{(m_n)}_{\rm ret}(x-x')\,J_{b\,\mu}(x').
\]

Fourier form (retarded prescription):
\[
G^{(m)}_{\rm ret}(x)
=\int\frac{d^4k}{(2\pi)^4}\,
\frac{e^{-ik\cdot x}}{k^2+m^2+i\epsilon k^0},
\qquad
k^2=-\omega^2+\mathbf k^2.
\]

Define the KK-summed effective retarded kernel:
\[
G^{\rm eff}_{\rm ret}(x)=\sum_{n\ge0} c_n G^{(m_n)}_{\rm ret}(x),
\]
so
\[
a_\mu(x)=\mu_0\int d^4x'\,G^{\rm eff}_{\rm ret}(x-x')\,J_{b\,\mu}(x').
\]
In momentum space,
\[
D^{\rm eff}_{\rm ret}(k)=\sum_{n\ge0}\frac{c_n}{k^2+m_n^2+i\epsilon k^0}.
\]
This depends on brane momentum only through \(k^2\) (plus the standard retarded prescription), making brane Lorentz covariance manifest.

### 8.3 Explicit causal support: light-cone + tail

In 3+1:

* Massless retarded Green function (support on the light cone):
  \[
  G^{(0)}_{\rm ret}(t,r)=\theta(t)\frac{\delta(t-r)}{4\pi r}.
  \]

* Massive retarded Green function (support on and inside the light cone):
  \[
  G^{(m)}_{\rm ret}(t,r)
  =\theta(t)\left[
  \frac{\delta(t-r)}{4\pi r}
  -\theta(t-r)\frac{m}{4\pi}
  \frac{J_1\!\left(m\sqrt{t^2-r^2}\right)}{\sqrt{t^2-r^2}}
  \right].
  \]
Thus massive modes add a **causal tail** inside the forward light cone.

### 8.4 Moving point charge worldline

A point charge \(q\) on a brane worldline \(z^\mu(\tau)\) has conserved current
\[
J_b^\mu(x)=q\int d\tau\,u^\mu(\tau)\,\delta^{(4)}(x-z(\tau)),
\qquad
u^\mu\equiv \frac{dz^\mu}{d\tau}.
\]
Then the brane potential is
\[
a_\mu(x)
=\mu_0 q\sum_{n\ge0} c_n\int d\tau\,
u_\mu(\tau)\,G^{(m_n)}_{\rm ret}\big(x-z(\tau)\big).
\]
The \(n=0\) term reproduces the usual Liénard–Wiechert structure; \(n\ge1\) add Yukawa/tail corrections (suppressed for \(r\gg\lambda\)).


## 9) Matter current conservation and Maxwell consistency (how the source is justified)

The Maxwell sector requires a conserved source for compatibility with the divergence identity. This paper supplies that source from a minimal brane matter model.

### 9.1 Minimal brane matter model (representative form)

A complex brane field \(\psi(t,\mathbf x)\) with Schrödinger / Gross–Pitaevskii-type Lagrangian and minimal coupling:
\[
\mathcal L_\psi
=
\frac{i\hbar}{2}\left(\psi^* D_t\psi-\psi(D_t\psi)^*\right)
-\frac{\hbar^2}{2m}(D_i\psi)^*(D_i\psi)
-U(|\psi|^2),
\]
with covariant derivatives
\[
D_t=\partial_t+\frac{i q}{\hbar}A_0,
\qquad
D_i=\partial_i+\frac{i q}{\hbar}A_i.
\]

Gauge symmetry:
\[
\psi\mapsto e^{-i q\chi/\hbar}\psi,
\qquad
A_\mu\mapsto A_\mu+\partial_\mu\chi.
\]

### 9.2 Noether current and charge current

From local phase variation, the brane Noether current is
\[
j^0=|\psi|^2,
\]
\[
j^i=\frac{\hbar}{2mi}\big(\psi^* D^i\psi-(D^i\psi)^*\psi\big)
=\frac{\hbar}{m}\,\mathrm{Im}(\psi^* D^i\psi).
\]
Define the charge current:
\[
J_\psi^\mu\equiv q\,j^\mu.
\]

### 9.3 Off-shell identity and on-shell conservation

Let \(\mathrm{EL}_\psi\) and \(\mathrm{EL}_{\psi^*}\) be the matter Euler–Lagrange expressions. The phase symmetry implies the **off-shell Noether identity**
\[
\partial_\mu j^\mu
+\frac{i}{\hbar}\big(\psi^*\mathrm{EL}_{\psi^*}-\psi\,\mathrm{EL}_\psi\big)=0.
\]
On shell, \(\mathrm{EL}_\psi=\mathrm{EL}_{\psi^*}=0\), hence
\[
\partial_\mu j^\mu=0
\quad\Leftrightarrow\quad
\partial_\mu J_\psi^\mu=0.
\]

### 9.4 Embedding as a bulk source and closing the consistency loop

Use the brane-localized bulk current model
\[
J^\mu(x,w)=J_\psi^\mu(x)\,\delta(w),
\qquad
J^w(x,w)=0.
\]
Then
\[
\partial_M J^M
=\partial_\mu(J_\psi^\mu\delta(w))=\delta(w)\,\partial_\mu J_\psi^\mu.
\]
So brane on-shell conservation implies bulk conservation, exactly the condition required by Maxwell consistency (divergence identity + Lorenz gauge).


## 10) Validity regime, leading deviations, and falsifiable tests

### 10.1 When the 3+1 Maxwell limit holds

A sufficient set of conditions:

1. **Zero-mode dominance:** \(A_\mu(x,w)\approx a_\mu(x)\) over the support of \(Z\), with \(\partial_w A_\mu\approx0\). Operationally:
   \[
   r\gg\lambda,
   \qquad
   \omega\ll\frac{2}{\lambda},
   \]
   so KK excitations are not efficiently sourced / remain evanescent.

2. **No transverse flux:** \(J^w=0\).

3. **Localized boundary behavior:** \(Z(w)F^{w\nu}\to0\) fast enough to drop the \([ZF^{w\nu}]_{\pm\infty}\) term.

4. **Conserved brane current:** \(\partial_\mu J_b^\mu=0\) (derived from matter symmetry).

Then brane gauge-invariant observables match Maxwell to high accuracy and the effective coupling is \(\mu_0^{\rm eff}=\mu_0/Z_{\rm int}\).

### 10.2 Leading deviation structure (Gaussian profile)

Static potential:
\[
A_0(r)=\frac{\mu_0^{\rm eff}q}{4\pi r}\left[1+\tfrac12 e^{-2r/\lambda}+\cdots\right].
\]
Two emphasized “rigidity” points:

* The **range** is fixed by the first brane-coupled mass \(m_2=2/\lambda\).
* The **amplitude** of the leading Yukawa term is also fixed (\(1/2\)) by the Gaussian mode structure.

### 10.3 Time-dependent thresholds and dispersion

Each coupled KK mode has dispersion
\[
\omega^2=k^2+m_n^2,
\]
so massive modes have subluminal group velocity. The first brane-coupled threshold is at \(\omega=m_2=2/\lambda\):

* \(\omega<m_2\): KK contributions are evanescent / near-field corrections.
* \(\omega>m_2\): additional propagating channels open (frequency-dependent response).

### 10.4 Tail signatures

Massive modes add causal tails inside the light cone. Time-domain pulse experiments constrain (or potentially detect) this after-response.

### 10.5 Charge leakage / transverse current

The Maxwell regime assumes \(J^w=0\). The framework does not “forbid” \(J^w\neq0\), but it moves one outside the controlled Maxwell limit and implies modifications governed by the \(N=w\) equation.

### 10.6 Profile-shape dependence

All KK predictions depend on \(Z(w)\) only through the Sturm–Liouville problem and the resulting \(\{m_n,c_n\}\). Gaussian \(Z\) is chosen for analytic control; other profiles give other discrete patterns.


## 11) Referee verification suite and common pitfalls (what was checked, and how)

### 11.1 Wolfram Language (WL) referee suite (scripts and their purpose)

The paper includes WL scripts intended to verify every nontrivial identity by checking that the **residual simplifies to zero**, under the frozen conventions:

* Metric \(\eta_{MN}=\mathrm{diag}(-1,1,1,1,1)\).
* \(F_{MN}=\partial_M A_N-\partial_N A_M\).
* Coupling \(\mathcal L_{\rm int}=-A_M J^M\) with \(A_M\) covariant and \(J^M\) contravariant.
* Gaussian \(Z(w)=e^{-w^2/\lambda^2}\).

Scripts summarized in the paper include:

(A) `maxwell_from_4d.wl` — vary action, derive EOM for all components, check Bianchi, divergence identity, and brane reduction \(\mu_0^{\rm eff}=\mu_0/(\lambda\sqrt\pi)\).

(B) `maxwell_symmetry_checks.wl` — check gauge variation of the interaction term and the shift of \(\partial\!\cdot\!A\); verify brane Lorentz invariance with correct transformation types (\(A_\mu\) covector, \(J^\mu\) vector).

(C) `maxwell_kk_coulomb_propagator.wl` — solve SL problem for Gaussian \(Z\), verify Hermite spectrum, norms, coupling weights \(c_n\), parity rule, Coulomb+Yukawa, and the \(k^2\)-only dependence of (truncated) propagators.

(D) `maxwell_axial_gauge_brane_sources.wl` — verify axial gauge reachability, residual 3+1 gauge, \(\delta(w)\) sources, integrated equations, and \(N=w\) consistency.

(E) `maxwell_moving_charges_propagator.wl` — check Lorentz invariance of \(k^2\) and retarded prescriptions; validate that moving sources do not induce preferred-frame artifacts.

(F) `matter_current_conservation.wl` — derive Noether current from phase variation, check explicit \(j^0\), \(j^i\), and verify the off-shell identity.

### 11.2 Common pitfalls explicitly flagged

1. **Treating \(A_\mu\) as a vector instead of a covector** breaks Lorentz invariance checks.
2. **Mixing covariant/contravariant components** without explicit \(\eta_{MN}\) raises/lowers leads to sign errors.
3. **EulerEquations output formatting** in WL (often returns `lhs == rhs`) should be converted to residual expressions before simplifying.
4. **Noether identity sign convention**: the identity has a definite sign; flipping it yields spurious “failures.”
5. **Symbolic Hermite norms**: use spot-checks for integer \(n\) and validated closed forms; pure symbolic integration can return indeterminate.


## 12) Minimal cache for future work (the “what do I keep in RAM?” list)

If you want to build on this paper without re-reading it, the minimal “working set” is:

1. **Action**
   \[
   S=\int d^5x\left[-\frac{Z}{4\mu_0}F_{MN}F^{MN}-\frac{1}{2\xi\mu_0}(\partial\!\cdot\!A)^2-A_MJ^M\right].
   \]

2. **Bulk EOM + divergence identity**
   \[
   \partial_M(ZF^{MN})+\xi^{-1}\partial^N(\partial\!\cdot\!A)=\mu_0J^N,
   \qquad
   \partial_N\partial_M(ZF^{MN})=0
   \Rightarrow
   \xi^{-1}\Box(\partial\!\cdot\!A)=\mu_0\partial_NJ^N.
   \]

3. **Controlled brane Maxwell limit**
   * axial gauge: \(A_w=0\), residual \(\chi=\chi_b(x)\),
   * brane source: \(J^\mu=J_b^\mu\delta(w)\), \(J^w=0\),
   * zero mode: \(\partial_wA_\mu\approx0\),
   giving
   \[
   \partial_\mu f^{\mu\nu}=\mu_0^{\rm eff}J_b^\nu,
   \qquad
   \mu_0^{\rm eff}=\mu_0/Z_{\rm int}=\mu_0/(\lambda\sqrt\pi).
   \]

4. **Gaussian KK data**
   \[
   m_n^2=2n/\lambda^2,\quad
   c_{2m+1}=0,\quad
   c_{2m}=\frac{1}{\lambda\sqrt\pi}\,\frac{1}{4^m}\binom{2m}{m}.
   \]
   Static potential:
   \[
   A_0(r)=\frac{\mu_0 q}{4\pi r}\sum_n c_ne^{-m_nr}
   =\frac{\mu_0^{\rm eff}q}{4\pi r}\left[1+\frac12 e^{-2r/\lambda}+\cdots\right].
   \]

5. **Time-dependent structure**
   \[
   (\square_4+m_n^2)a_\mu^{(n)}=\mu_0c_nJ_{b\mu},
   \quad
   G^{(m)}_{\rm ret}(t,r)=\theta(t)\left[\frac{\delta(t-r)}{4\pi r}-\theta(t-r)\frac{m}{4\pi}\frac{J_1(m\sqrt{t^2-r^2})}{\sqrt{t^2-r^2}}\right].
   \]

6. **Matter current source**
   \[
   j^0=|\psi|^2,
   \quad
   j^i=\frac{\hbar}{m}\,\mathrm{Im}(\psi^*D^i\psi),
   \quad
   \partial_\mu j^\mu + \frac{i}{\hbar}(\psi^*\mathrm{EL}_{\psi^*}-\psi\,\mathrm{EL}_\psi)=0.
   \]
   Embed as \(J^\mu= q j^\mu\delta(w)\), \(J^w=0\).

That set is enough to re-derive: the Maxwell brane limit, the effective coupling, the Yukawa correction pattern, the causal retarded structure for moving sources, and the link between matter symmetry and Maxwell consistency.
