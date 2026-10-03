# Conventional action-to-charge diagnostic

This diagnostic supplies a conventional, explicit action and a reproducible
charge-response calculation. It does not supply a matched interaction for the
Wilson replacement, a new law of physics, or a baryogenesis prediction.

## Action, phase normalization, and ensemble

Take a dimensionless phase theta0 and

\[
\mathcal L_{\rm int}=c\,\partial_\mu\theta_0 J_{B+L}^{\mu},\qquad
\kappa=c\dot\theta_0.
\]

The current is normalized so each quark has B = 1/3 and each lepton has L = 1.
For an externally prescribed homogeneous background, the interaction lowers
the matter Hamiltonian by kappa Q_(B+L). This defines the sign convention: a
positive kappa biases positive B+L. Here c is dimensionless and kappa has energy
units. The site-0 public mapping is tau1 = theta0/(2 pi), so

\[
\kappa/T=2\pi c\,\dot\tau_1/T.
\]

Choosing c = 1 fixes a toy normalization. It does not identify c in the Wilson
replacement. The public scaffold uses a phenomenological product
c_sph kappa_dyn (2 pi n_det dot(tau1)/T) D_d. Our **conditional** choice
c = n_det D_d would identify the action bias with that phase-dependent product
before kappa_dyn. The public record does not derive this matching. In particular
n_det = 16 does not determine the operator coefficient, D_d is not proven to
multiply this interaction, and c_sph = 0.0195 is an output-normalization ansatz
rather than a determination of c. No private manuscript or private source path
is needed for this benchmark.

Integration by parts gives -c theta0 partial_mu J^(mu), up to a boundary term.
For conserved charge currents this supplies no reaction bias at fixed charge.
B+L has electroweak anomalies. The weak sphaleron below is the sole anomalous
reaction included. There is no dynamical hypermagnetic background or extra
Abelian sphaleron process in this reaction network. The anomaly traces checked
by the independent calculation do not furnish such a rate or UV matching.

## Symmetric SM thermodynamics and susceptibility projection

Use quark flavor equilibrium and the ten species

\[
(q,u,d,l_e,l_\mu,l_\tau,e_e,e_\mu,e_\tau,H).
\]

In the linear, symmetric-SM approximation let

\[
\chi=(T^2/6)S,\qquad
S=\operatorname{diag}(18,9,9,2,2,2,1,1,1,4),\qquad n=\chi\mu.
\]

The factors count three equilibrated quark generations and the two complex
Higgs components, including the leading bosonic factor. Define A with rows Y,
Delta_e, Delta_mu, Delta_tau, where Delta_i = B/3-L_i. Hypercharge assignments
are (1/6,2/3,-1/3,-1/2,-1/2,-1/2,-1,-1,-1,1/2). Hold Y neutral and each
Delta_i fixed. These assumptions apply in an unbroken symmetric phase where
all relevant Yukawa and sphaleron processes are fast enough to equilibrate.

For n, the strictly convex constrained free energy is

\[
F(n)=\tfrac12 n^T\chi^{-1}n-\kappa Q^Tn,\qquad An=d,
\quad Q=B+L.
\]

Write delta_i = 6 n_(Delta_i)/T^2 and d_tilde = (0,delta_e,delta_mu,delta_tau).
The exact KKT solution and zero-conserved-density source projector are

\[
\mu=\kappa Q+A^T(ASA^T)^{-1}(\widetilde d-\kappa ASQ),
\qquad
P=I-A^T(ASA^T)^{-1}AS.
\]

The Gram matrix is

\[
ASA^T=\begin{pmatrix}
11&8/3&8/3&8/3\\
8/3&31/9&4/9&4/9\\
8/3&4/9&31/9&4/9\\
8/3&4/9&4/9&31/9
\end{pmatrix}.
\]

A has rank four. P is idempotent and S P = P^T S, so this is a susceptibility-
weighted projection rather than an unweighted projection of reaction charges.
Strict positivity of chi guarantees uniqueness. A nonzero allowed reaction
perturbation raises F by its positive quadratic susceptibility cost.

## Reaction affinities and exact source charges

For any reaction row nu, equilibrium is

\[
\nu\cdot(\mu-\kappa Q)=0,
\]

which is an equilibrium condition for the biased Hamiltonian. The intrinsic
chemical potentials need not have zero affinity for a violated source charge.
The explicit rows are

| Reaction | Row in ten-species basis | Delta B | Delta L | Delta(B+L) |
|---|---|---:|---:|---:|
| Up Yukawa | q + H - u | 0 | 0 | 0 |
| Down Yukawa | q - H - d | 0 | 0 | 0 |
| Charged-lepton Yukawa, each flavor | l_i - H - e_i | 0 | 0 | 0 |
| Strong sphaleron, three generations | 6q - 3u - 3d | 0 | 0 | 0 |
| Weak sphaleron, three generations | 9q + l_e + l_mu + l_tau | 3 | 3 | 6 |

All rows conserve Y and each Delta_i. Their rank is six; the strong-sphaleron
row is redundant when both quark Yukawa rows equilibrate. Thus their kernel is
exactly the four-dimensional space spanned by the rows of A. The weak equation
is 9 mu_q + sum_i mu_l_i = 6 kappa; imposing zero on the left in the presence
of the source would omit the action bias.

## Exact solution and controls

Let D = delta_e + delta_mu + delta_tau. The intrinsic chemical potentials are

\[
\begin{aligned}
\mu_q&=(36/79)\kappa+(7/237)D,\\
\mu_u&=(42/79)\kappa-(5/237)D,\\
\mu_d&=(30/79)\kappa+(19/237)D,\\
\mu_H&=(6/79)\kappa-(4/79)D,\\
\mu_{l_i}&=(50/79)\kappa+(16/711)D-\delta_i/3,\\
\mu_{e_i}&=(44/79)\kappa+(52/711)D-\delta_i/3.
\end{aligned}
\]

Therefore

\[
n_B=\frac{28}{79}\sum_i n_{\Delta_i}+\frac{72}{79}T^2\kappa,
\qquad
n_L=-\frac{51}{79}\sum_i n_{\Delta_i}+\frac{72}{79}T^2\kappa.
\]

At zero drive this recovers 28/79 conversion of B-L. At fixed zero Delta_i,
n_B = n_L, and the response of total B+L is (144/79) T^2 kappa. A B-only or
L-only source gives (36/79) T^2 kappa in B: their difference B-L is conserved.
Their B+L sum gives twice this response. A pure Y source, an individual Delta_i
source, or L_e-L_mu source projects to zero at fixed conserved densities.

Different conserved **densities** can still have a physical flavor asymmetry.
For (delta_e,delta_mu,delta_tau) = (1,-1,0), the solution has mu_l_e = mu_e_e
= -1/3 and mu_l_mu = mu_e_mu = +1/3 in the formal energy units, while all
quark and Higgs chemical potentials vanish. Total B is zero. The distinction
between an invisible conserved source and a nonzero conserved initial density
is checked explicitly.

## Entropy normalization and registered conditional sensitivity

For ideal entropy s = (2 pi^2/45) g_star_s T^3 with g_star_s = 106.75,

\[
\frac{n_B}{s}=C_{\rm SM}\frac{\kappa}{T}
\quad(\Delta_i=0),\qquad
C_{\rm SM}=\frac{1620}{79\pi^2g_{*s}}
=\frac{6480}{33733\pi^2}
\simeq0.0194634710818.
\]

This is numerically consistent with rounding to the inherited 0.0195; it is
not proof of the historical origin of that constant. The ideal coefficient is
0.1873278% smaller. Under our conditional c = n_det D_d identification, the
formal equilibrium expression has the same product as the inherited ansatz,
with kappa_dyn = 1. No transport efficiency is derived.

The registered sensitivity changes only the coefficient in a separate formal
recalculation of the public frontier. Continuous required n_det times relative
efficiency rescales by 0.0195/C_SM = 1.00187679361234; the required kinetic
energy at fixed n and efficiency rescales by its square. At unit relative
efficiency the results are

| Energy allowance | Public continuous threshold | Conditional ideal threshold | Public integer minimum | Conditional integer minimum |
|---|---:|---:|---:|---:|
| One source height | 48.93652273 | 49.02836648 | 49 | 50 |
| Full two-height drop | 34.60334707 | 34.66829041 | 35 | 35 |
| Strictly below 1% radiation | 118.55636407 | 118.77886989 | 119 | 119 |

For n_det = 49 the one-height required relative efficiency changes from
0.998704545445795 to 1.00057890775730. This is a boundary sensitivity of a
frozen algebraic gate, not a physical correction to the model. Remaining
efficiency cases and independent energy inequalities are saved in CSV/JSON.
No ideal coefficient is transplanted into the original data or release.

## Chemical-potential, Higgs, and timescale validity

At zero Delta_i the largest intrinsic |mu_i| is (50/79)|kappa|, so the fermionic
linear-response condition is (50/79)|kappa|/T much less than one. Nonzero Delta_i
must be checked using the full formulas above. The leading Higgs susceptibility
is a formal linear expansion, not a stable massless Bose gas at finite chemical
potential. In a normal symmetric thermal phase the positive thermal Higgs mass
must also satisfy |mu_H| < m_H(T); here |mu_H| = (6/79)|kappa| at zero Delta_i.
Finite thermal masses and interaction corrections change the ideal response.

At the **fixed inherited** speed dot(tau1)/T = 0.5206657041971909, c = 1 gives
kappa/T = 3.27143910 and max |mu_i|/T = 2.07053108, outside the linear regime.
The unsuppressed c = n_det = 16, I_F = 1 choice gives kappa/T = 52.34302564 and
max |mu_i|/T = 33.12849724. These are distinct phase normalizations and are not
solutions recalibrated to a new yield target. Under **our conditional** c =
n_det D_d choice, those latter two values acquire a factor D_d. Thus a tiny
D_d could make the chemical source small while the phase speed and its kinetic
cost remain large. The coefficient choice does not establish D_d or a predicted
yield, and D_d is not fitted to observed Y_B here.

Equilibrium further requires the slowest relevant relaxation rate much larger
than the expansion rate and the inverse timescale on which kappa or the plasma
changes. A finite-rate source, freeze-out, or broken-phase plasma requires a
transport calculation. T = 131.7 GeV is at electroweak sphaleron freeze-out in
the broken-phase region; it cannot be inserted into this ideal symmetric-phase
calculation to claim a physical yield. A freeze-out value from radiation-
dominated SM cosmology does not transfer automatically to the model's energy
budget. No such yield calculation is made.

## External work and autonomous source boundary

The minimization assumes prescribed kappa. It includes the energy bias in the
matter Hamiltonian; it is not an accounting of the reservoir that maintains
phase motion. At fixed temperature and conserved charges, the **intrinsic**
matter free energy F_0 = (1/2) n^T chi^(-1) n satisfies
dF_0 = kappa dQ_(B+L) along a quasistatic reaction at biased equilibrium. The
**biased** stationary objective is F = F_0 - kappa Q_(B+L); along its equilibrium
family, dF = -Q_(B+L) d kappa, which vanishes for fixed kappa. For a
parameter-changing biased Hamiltonian, external work includes
(partial H/partial kappa) d kappa = -Q_(B+L) d kappa. These statements use the
prescribed-background ensemble and do not license unlimited autonomous energy
or a physical drive history.

For illustration only, a homogeneous dynamical phase with kinetic term
(f_theta^2/2) dot(theta0)^2 and the same interaction has canonical momentum

\[
p_\theta=f_\theta^2\dot\theta_0+c n_{B+L},\qquad
\mathcal H_{\theta}=\frac{(p_\theta-c n_{B+L})^2}{2f_\theta^2}+V.
\]

The matter bias follows by differentiating this complete kinetic contribution
at fixed canonical momentum, but kappa is then a self-consistent dynamical
quantity rather than a prescribed parameter. Expansion, the phase potential,
energy transfer, reservoir depletion, finite reaction rates, and decay products
must be evolved together. The positive sign of motion was chosen in this
benchmark; no physical CP-odd invariant or autonomous rolling initial state has
been derived. The small chemical source condition does not remove the existing
phase-energy gate.

## Reproduction and independent comparison

Run `python3 sm_charge_diagnostic.py` and `python3 conditional_sensitivity.py`.
They require Python's standard library. The second script finds the public
AntiMatter v1.23 and v1.23.1 parent artifacts in the current repository ancestry.
The first calculation executes 48 exact rational controls; the conditional
comparison executes 36 decimal/energy-inequality controls. JSON and CSV outputs
are deterministic. A second run must reproduce their SHA256 hashes.

The separate sixteen-species solver uses independently written reaction
constraints and retains distinct quark generations. Its result agrees on
28/79 conversion, 72/79 source response, and each reduced chemical potential.
An independent completion message exposed its coefficient after this producer's
code was written but before the producer's first execution. The producer had
no hardcoded expected source coefficient; the agreement is an independent
implementation check, not fully blinded execution. Registration and source
path/line/hash evidence are recorded in the accompanying provenance and receipt.
