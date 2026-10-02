# General linear reaction response and physical gates

This is a standard near-equilibrium transport construction, derived here as a
reproducible diagnostic. It specifies neither the AntiMatter branch's source
operator nor its particle content. Natural units use energy for inverse time.

## Species, reactions, and dimensions

Let `n_i` be signed particle asymmetry densities (dimension E^3), `mu_i` their
chemical potentials (E), and `chi_ij(T)=dn_i/dmu_j` the susceptibility matrix
(E^2). Assume chi is symmetric positive definite on independent unconstrained
species coordinates. Gauge neutrality and redundant species should first be
eliminated consistently; a singular susceptibility cannot be inverted as if it
were positive definite. Near equilibrium, `n=chi mu`. Small physical `|mu_i|/T`
is necessary for this linear treatment; the susceptibility must be calculated
for the actual species and phase. An illustrative small amplitude is not a
validity test for the unconstructed candidate.

The column `v_r=S[:,r]` gives the signed changes caused by one forward reaction
event. A physical reaction bias `zeta_r(t)` has dimension E. Its affinity is

    Delta_r = v_r^T mu - zeta_r.

Choose the kinetic normalization by the detailed-balance linearization

    J_r = - gamma_r Delta_r / T,

where reaction progress J_r and positive kinetic coefficient gamma_r have
dimension E^4. For example, a forward/backward rate ratio
`exp(-Delta_r/T)` produces this sign upon linearization. Event multiplicities,
particle-versus-antiparticle conventions and the definition of a sphaleron
diffusion coefficient must be matched before assigning a literature number to
gamma. A measured diffusion rate is not automatically this kinetic coefficient.

For homogeneous species in a cosmological background,

    n_dot + 3 H n = -S Lambda (S^T chi^-1 n - zeta),
    Lambda = diag(gamma_r/T),
    W = S Lambda S^T chi^-1,
    f = S Lambda zeta.

Lambda has dimension E^3, W has E, and f has E^4. Both sides of the density
equation have E^4. Because chi is of order T^2 in a relativistic plasma,
relaxation eigenvalues are of order gamma/T^3 times charge/susceptibility factors.
This is why comparing a dimension-four diffusion rate directly with H is wrong.
Which rate eigenvalue controls a chosen charge is a question about this network,
not a universal numerical sphaleron factor.

At fixed chi and T with no expansion and no source, the free energy density
`F=n^T chi^-1 n/2` satisfies

    F_dot = -(S^T mu)^T Lambda (S^T mu) <= 0.

With a source, `mu^T S Lambda zeta` is the algebraic source contribution to this
quadratic F derivative; it is not the total physical drive power. Write
`a=S^T mu`, `Delta=a-zeta`, and `J=-Lambda Delta`. If the local detailed-balance
description and its biases have been physically matched, the supplied bias power
and dissipative balance at fixed background are

    P_bias = zeta^T J,
    F_dot = P_bias - Delta^T Lambda Delta,
    sigma_reaction = Delta^T Lambda Delta / T >= 0.

Power densities have dimension E^5; reaction entropy production per volume and
time has E^4. A prescribed bias is an external drive; this equation does not
supply an autonomous energy reservoir. For time-dependent chi and expanding
densities, the derivative of the same quadratic F has additional terms
`-mu^T chi_dot mu/2 - 3 H mu^T n`; source-free monotonicity was asserted only
for the stated fixed background. A full receiving-sector thermodynamic energy
ledger requires a matched microscopic model and evolving bath and reservoir.

## Conserved charges and compatibility

For active reactions, charge vectors form the columns of Q with
`S_active^T Q=0`. Then

    d(Q^T n)/dt + 3 H Q^T n = 0.

Thus a network source of the form `S Lambda zeta` cannot inject an exactly
conserved charge. A separate explicit injection would have to appear as a new
term and be physically matched. Inactive reactions enlarge the conserved space.
Initial conserved charges must be specified instead of lost through an inverse
of the singular relaxation matrix.

If a matched derivative-current operator supplied a species chemical shift d,
its compatible reaction bias would be `zeta=S^T d` (d has dimension E here).
Adding an exactly conserved direction `d -> d+Q alpha` changes no reaction bias.
This is an identifiability statement about the transport equations: a source
along an exact conserved current creates no new density from zero initial state.
It does not derive the candidate's operator or determine an anomaly coefficient.

It is possible to set every active affinity to zero if and only if

    zeta_active belongs to image(S_active^T),
    equivalently c^T zeta_active = 0 for all c in ker(S_active).

Here c is a cycle in reaction space, distinct from a conserved charge in species
space. For incompatible sources, setting every reaction term to zero is invalid.
A stationary state can still exist with `S J=0` and circulating nonzero J. Its
densities can depend on the reaction rates; it is externally driven stationarity,
not detailed-balanced equilibrium. Even a compatible bias does not justify an
instantaneous equilibrium approximation unless the active relaxation modes are
fast enough compared with source variation and expansion.

## Entropy, susceptibility changes, and the signed retarded response

Let entropy density s obey `s_dot+3 H s=Sigma`, where Sigma has dimension E^4,
and set `Y=n/s`. The general yield equation is

    Y_dot = -(W + D I) Y + S Lambda zeta/s,
    D = Sigma/s.

The expansion terms cancel; entropy production dilutes Y. In particular,
`(Q^T Y)_dot=-D Q^T Y`. Cooling, chi(T), all reaction rates, the actual H(T),
species thresholds and source shutdown remain time dependent. Evolving n or Y
uses the instantaneous chi inside W. If instead one evolves chemical potentials,
`n=chi mu` implies an additional `chi_dot mu` term; it cannot be discarded during
a changing thermal history.

Let `U(t,t')` solve `dU/dt=-(W(t)+D(t)I)U`, with `U(t',t')=I`.
The signed solution is

    Y(t_f) = U(t_f,t_i)Y(t_i)
           + integral_[t_i,t_f] U(t_f,t') S Lambda(t') zeta(t')/s(t') dt'.

For a physical measured charge b_phys, the abundance is `b_phys^T Y(t_f)`.
This retarded weighting accounts for production, sign changes, spectators,
washout and entropy. Equal positive and negative source areas need not cancel
because their transport weights differ. A trajectory's maximum speed and time
above a fixed speed cannot substitute for the signed integral. Conversely an
oscillating source is not automatically excluded: its outcome depends on the
rates and freeze-out history. Reversing all CP-odd biases and initial CP-odd
densities changes the sign of this linear solution if the CP-even coefficients
are held fixed. This algebraic control does not explain cosmological sign choice.

## Stable constant-segment dimensionless solution

The numerical comparator holds T and chi constant and has H=D=0. It uses

    x=n/T^3, C=chi/T^2, b=zeta/T,
    tau=t/t_ref, rho_r=t_ref gamma_r/T^3,
    x'=-S R(S^T C^-1 x-b), R=diag(rho_r).

Define `z=C^-1/2 x` and

    A=C^-1/2 S R S^T C^-1/2,
    g=C^-1/2 S R b,
    z'=-A z+g.

A is symmetric positive semidefinite. For strictly positive rates its null space
is `C^1/2 ker(S^T)`; for arbitrary nonnegative rates replace S by S_active.
Because the network source is orthogonal to these null modes, zero-charge
source-driven solutions exist without inverting A or W.

For `A=V diag(lambda) V^T`, each modal coordinate evolves over duration h as

    z_k(h)=exp(-lambda_k h) z_k(0)
           + (1-exp(-lambda_k h))/lambda_k * g_k,

with the continuous lambda=0 limit `z_k(h)=z_k(0)+h g_k`. The implementation
uses `expm1` for the small positive eigenvalues, and tracks the actual zero-mode
coordinates through reaction shutdown. No inverse of the singular W is taken.

Numerical zero-mode classification uses a relative 64-machine-epsilon threshold.
The registered rate ratios are mild. Arbitrarily ill-conditioned susceptibilities
or rate hierarchies are not validated; a microscopic calculation must resolve
slow modes rather than treating positive rates below numerical resolution as
physical conservation laws.

For a compatible constant b=S^T d, positive rates and zero conserved charges,

    x_eq = C d - C Q (Q^T C Q)^-1 Q^T C d.

For nonzero initial conserved q0=Q^T x(0), add
`C Q (Q^T C Q)^-1 q0`. This explicitly includes susceptibility and charge
constraints. The result is independent of positive reaction rates only for a
compatible steady source, not an arbitrary time-dependent source or network.

## Literature connection and limit

The candidate's verified 1 October addendum motivates this gate through the
rate-dependent stationary-source discussion in Duch, Strumia and Titov,
[arXiv:2504.03506v2](https://arxiv.org/abs/2504.03506), Section 3.3; the physical
source invariants are treated there in Eqs. (19)-(21). De Simone and Kobayashi,
[arXiv:1605.00670v2](https://arxiv.org/abs/1605.00670), Section 3, discuss
source oscillation and response. Mojahed and Stanzione,
[arXiv:2609.05605v1](https://arxiv.org/abs/2609.05605), give a concrete flavor
comparator with complete source vectors and chosen transport reactions. The
Standard Model sphaleron calculation of D'Onofrio, Rummukainen and Tranberg,
[arXiv:1404.3565v1](https://arxiv.org/abs/1404.3565), provides a diffusion-rate
benchmark, requiring a matching convention and cosmology before use here.

These are scoped references from the supplied addendum, not a fresh comprehensive
literature or novelty search. None specifies this candidate's S, chi, zeta,
reaction coefficients, conserved initial charges, thermal history or final yield.
