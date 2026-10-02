# Registered bounded Wilson metric audit

Written 2026-10-02 before any new metric-family spectral calculation. The published
v1.23 note, generator, benchmark CSV, summary JSON and Hessian CSV have been read;
their diagonal-metric baseline and adjacent estimate are known. No new scan has
been seen. This is a candidate research calculation outside the protected release,
not a publication, novelty claim or matched five-dimensional loop computation.

## Fixed inputs and scope

Use the public `/workspace/AntiMatter/research/AM1231/v1.23/` generator's 31-site
q=3 Wilson benchmark and pinned `/workspace/AntiMatter/.venv/bin/python`.
Keep its source curvature (including the harmonic sums), f_site, potential, charge
basis, threshold convention and all other inputs fixed. Reconstruct its baseline
using the same float inputs, then promote the resulting k_link and k_endpoint
to Decimal; high precision resolves the matrix problem, not unknown input digits.
Source provenance hashes are recorded, without importing or executing the release
generator and without reading raw private source material.

Let Q have rows e_j-3e_(j+1), e=e_30 and w=(3^30,...,1).
The dimensionless metric is G, physical kinetic matrix K=f_site^2 G and physical
phase Hessian is U=f_site^2 H, with
H=k_link Q^T Q+k_endpoint ee^T in GeV^2. Solve H v=lambda G v.
Thus no extra factor f_site is inserted into the generalized mass problem.

Structural assumption: G=I+c Q^T Q+b ee^T with c,b>=0, an assumed local,
charge-correlated kinetic correction. This is NOT a full computed or matched 5D
loop. Define c0=epsilon_pub/3, where epsilon_pub is the full published summary
JSON estimate (~0.04921048547006312); Q^T Q has off-diagonal -3, so the assumed
off-diagonal magnitude is 3c0. Neither the physical sign nor the renormalized
diagonal terms, finite thresholds, counterterms or matching scheme are supplied
by this magnitude. Baseline bare site normalization is held fixed. Redefining it
to match diagonal entries would give a different period and must not be confused
with this convention.

Finite structural family: c/c0 in {0,1,3,10}. At c=0 take only b=0; at each
positive c take b in {0,c,3c}. These b values are illustrative, not an endpoint
leading-log prediction. This gives 10 structural cases including the baseline.
The 10c0 cases are stress tests and need not be perturbative.
Two sensitivity controls use G=I+epsilon A with A the unweighted path adjacency
matrix and epsilon=+epsilon_pub or -epsilon_pub. They are arbitrary adjacent-only
metrics, not physical loop corrections. No adaptive parameter expansion.

## Registered observables, controls and interpretation

For every case report metric positivity, F/F0 where F^2=w^T K w, and the
source-off/minimum/top light signed mass-squared and signed sqrt(|m^2|) convention,
plus the smallest/largest heavy masses. Exact Qw=0 entails w^T G w=w^Tw+b for
the structural family, so link corrections leave F exactly unchanged and endpoint
terms shift F^2 by f_site^2 b. This is an algebraic check, not a new dynamics claim.

Resolve the tiny minimum and top eigenvalues by a Decimal tridiagonal generalized
Sturm/inertia bisection (or independent robust high-precision method), never by
double-precision light eigenvalues. Check 60,90,110-digit convergence for every
nonzero light root. Use float symmetric generalized solvers for heavy modes only.

Required controls: reproduce all baseline Hessian CSV values to relative 1e-10;
prove integer Qw=0 and structural period identity; source off has one exact zero;
minimum has zero tachyons and top exactly one for every positive metric; require
converged Decimal light roots within 1e-24 relative between 60 and 110 digits and
1e-50 between 90 and 110 digits (or flag precision failure without hiding it).
Check analytic source-off spectrum k_link mu/(1+c mu) when b=0, where
mu=10-6cos(l*pi/31), l=1,...,30. Check generalized heavy masses against an
independent Cholesky coordinate transformation. Include an analytic/perturbative
light-mode consistency check if well posed; label its accuracy separately from
exact numerical root convergence. Report relative spectral changes and finite
perturbation sizes, without declaring a universal perturbative error bound.

On any failure retain evidence, diagnose and amend the implementation openly;
do not tune family points or criteria to get a desired result. Machine-readable
outputs must retain all registered cases and controls. Re-run deterministically.

## Deliverables and exclusions

Write executable `audit.py`, `results.json`, `results.csv`, `RESULTS.md` and this
registration under `/workspace/research-progress/antimatter/wilson-metric/` only.
The results should distinguish exact algebra, verified numerics, assumptions and
open physics. Cite only verified repository anchors. No new web/literature
priority statements, physical baryogenesis success, WGC conclusions, messenger
port, finite-temperature dynamics, or UV completion is claimed. Protected release
files remain untouched and are not publicly committed.

Date clarification appended before the first decisive run: the initial
2026-10-02 date used the host's UTC calendar. The user's local date is
2026-10-01 in America/Los_Angeles; subsequent result/report dates use that date.
