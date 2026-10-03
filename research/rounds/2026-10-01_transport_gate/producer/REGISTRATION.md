# Registered transport diagnostic

Registered locally before numerical execution, 2 October 2026 UTC. This is a
bounded diagnostic/comparator round, not the candidate's particle model.

## Question and fixed scope

Can a susceptibility-weighted linear reaction network distinguish a real
charge-changing response from a source along an exactly conserved current,
enforce operator/source compatibility, and integrate signed production and
washout without replacing them by a pointwise speed or chosen efficiency?

Inputs read: public v1.23 source constants and matter-over-antimatter scaffold;
candidate `NEXT_TESTS.md`, `CLAIM_REVIEW.md`, and 1 October literature addendum.
Those files and all tracked repository files remain unchanged. No frozen
`c_sph=0.0195`, `n_det=16`, `T*=131.7 GeV`, or response efficiency is used as a
microscopic source, susceptibility, or reaction rate. Their operator matching
remains open. No candidate baryon abundance will be computed or claimed.

## Model and preselected cases

Natural units. For species densities n, positive definite susceptibility chi,
stoichiometry S (columns are reaction changes), reaction density gamma_r >= 0
with mass dimension four, and physical reaction bias zeta_r of dimension one:

    n_dot + 3 H n = -S diag(gamma/T) (S^T chi^-1 n - zeta).

Gamma normalization must be matched to a chosen microscopic convention. The
diagnostic uses constant temperature, constant susceptibility, no expansion,
and dimensionless x=n/T^3, C=chi/T^2, b=zeta/T,
rho_r=t_ref gamma_r/T^3, tau=t/t_ref:

    x' = -S diag(rho) (S^T C^-1 x - b).

The three illustrative species are A, B, C, with conversion columns
(-1,1,0), (0,-1,1), (1,0,-1). C=diag(1,2,3), x(0)=0,
a=0.01, and rates either (1,1,1), (1,2,4), or all zero. All amplitudes and
times are dimensionless; none denotes a physical baryon yield or thermal
freeze-out temperature. The charge q=(1,1,1) is conserved; the reaction cycle
c=(1,1,1) obeys S c=0.

Predicted controls, fixed before numerical execution:

1. The symmetric susceptibility-whitened relaxation matrix is positive
   semidefinite and its zero modes coincide with C^(1/2) ker(S^T).
2. A compatible bias b=S^T d a with d=(1,0,0) has zero cycle sum.
   Stationary x=(5/6,-1/3,-1/2) a on the zero-charge slice, independently of
   positive reaction rates.
3. Adding any alpha*q to d has no effect; d=q gives b=0 and no density response.
4. The cycle bias b=a*(1,1,1) is incompatible with setting every affinity to
   zero. Equal rates give x=0 but a stationary reaction cycle; rates (1,2,4)
   give x=(11/21,-8/21,-1/7) a and cycle progress 12 a/7. A stationary state
   need not be detailed-balanced equilibrium.
5. A +a interval on [0,1], followed by -a on [1,2], has zero integrated bias
   but generally nonzero x(2)=-[I-exp(-W)]^2 x_eq. Reversing the source sign
   reverses x. The response stays fixed when all reactions turn off at tau=2.
6. The same source history followed by twenty units of zero-bias active rates
   erases the nonconserved component to absolute norm below 1e-10.
7. Initial exactly conserved charges survive reactions. With b=0, the
   fixed-temperature quadratic free energy is nonincreasing.
8. A non-diagonal SPD susceptibility is also exercised; invalid non-SPD
   susceptibility and negative rates are rejected. Reaction-rate shutdown
   enlarges the conserved space and must be treated without inverting W.

## Numerical procedure and pass criteria

Exact constant-segment propagation uses the eigendecomposition of the symmetric
matrix A=C^-1/2 S diag(rho) S^T C^-1/2, including zero-mode integration.
An independent ordinary-coordinate RK4 integrator uses 32, 64 and 128 steps per
unit-time segment; final-state error at 128 must be below 2e-10, with convergence
decreasing across the grid. Algebraic identity controls use absolute tolerance
2e-12, stationary analytic comparisons 2e-12, and charge drift 2e-12. Distinct
outputs, including circulating flux, source compatibility residuals and maximum
|mu_i/T|, are recorded. Source-induced steady circulating flux is externally
driven in this comparator; no autonomous reservoir is implied.

The general physical derivation will additionally show entropy production in
yield variables and dimensional conversion of gamma/T^3 into a relaxation rate.
Numerical cases stay constant-temperature and are not promoted to an expanding
cosmology solver. Failure triggers correction and a recorded amendment, never
retuning to infer the desired candidate abundance.

## Outcome boundary

This can provide a reusable transport test framework and a precise list of
missing identifiability inputs. It cannot establish a physical CP-odd invariant,
candidate species content, electroweak susceptibility, sphaleron matching,
autonomous drive, novelty, observational agreement, or successful baryogenesis.
