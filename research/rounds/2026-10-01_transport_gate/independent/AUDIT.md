# Independently implemented transport verification

The registered dimensionless comparator passes 71 independently implemented
controls. Eleven producer-output comparisons, including all 201 signed-history
samples, agree within a maximum absolute discrepancy of
`4.440892098500626e-16`. The producer's nine tests were separately rerun:
nine passed, none skipped. This is verification by another automated agent in
the same research session, not external scientific peer review.

No AntiMatter species, physical source operator, reaction coefficient, thermal
susceptibility, or baryon yield has been identified by these checks. The
construction uses standard linear response and linear algebra; it establishes
no scientific novelty, observational agreement, or breakthrough.

## Independence and reproducibility

The reviewer first read `REGISTRATION.md`, derived the constraints and analytic
stationary states, and implemented `independent_check.py` before reading the
producer's implementation or numerical results. No producer code is imported.
The independent implementation evolves chemical potentials using an augmented
matrix exponential (`scipy.linalg.expm`), whereas the producer diagonalizes the
susceptibility-whitened generator and cross-checks ordinary-coordinate RK4.
Independent stationary states come from a charge-constrained linear solve;
source projection comes from weighted least squares in reaction coordinates.

The initial independent environment was Python 3.12.14, NumPy 2.3.5 and
SciPy 1.17.0. No dependency was installed for this review. Any later environment
replay must report its own versions and checks. The machine-readable results
record these versions, all control thresholds, and file digests.

Both scripts accept `--producer-dir`. For an exported artifact with sibling
`producer/` and `independent/` directories, run from the artifact root:

```sh
python independent/independent_check.py --producer-dir producer
python independent/compare_results.py --producer-dir producer --repo-root /path/to/AntiMatter
```

The comparison script repeats the independent controls before comparing outputs.
Without the option, it searches for a sibling `producer/` directory, then the
locally named registered round. The comparator requires the actual context
repository through `--repo-root`, or discovers the nearest ancestor containing
`research/AM1231`. It always maps the original receipt's repository-relative
source paths into that supplied/discovered repository, even if their old
absolute paths remain accessible. It writes only to its own directory.

The final comparator exits nonzero if the original registration or receipt
digest changes, a required context input is absent or has a different digest,
the result embeds another receipt, the trajectory lacks any of its eight
required columns or 201 rows, its time grid differs, or any of the eleven
numerical comparisons fails. The complete trajectory comparison verifies
densities, chemical potentials, and conserved charge. Seven focused validation
checks were executed separately: relocation with matching inputs succeeds;
modified registration, modified receipt, missing trajectory column, missing
trajectory row, missing context repository, and modified context input all
fail cleanly. These are publication-validation checks, not additional physics
controls; their outcomes are in `validation_failure_checks.json`.

## Charge constraints and susceptibility weighting

Write `R=diag(rho)`, `L=S R S^T`, and `W=L C^-1`. For positive rates, a conserved
species charge obeys `S^T q=0`; its value `q^T x` cannot change. The corresponding
right zero mode of W is `C q`, not generally q. With `z=C^-1/2 x`, the generator
`A=C^-1/2 L C^-1/2` is symmetric positive semidefinite and its zero modes are
`C^1/2 ker(S^T)`.

If some rates vanish, all these statements use the active reaction subnetwork.
Its conserved space is `ker(S_active^T)`. The independent controls exercise
conserved-space dimensions one, two, and three under full activity, one active
edge, and complete shutdown. The original registration's first control omitted
the strictly-positive-rate qualification. The producer preserved its original
registration and recorded the correction in `AMENDMENTS.md`; no preselected
input or numerical threshold changed.

For a compatible bias `b=S^T d` and charge-basis columns Q, zero conserved charges
select

```text
x_eq = C d - C Q (Q^T C Q)^-1 Q^T C d.
```

Nonzero initial charges add `C Q (Q^T C Q)^-1 Q^T x_initial`. For the registered
`C=diag(1,2,3)`, `d=(1,0,0)`, and amplitude 0.01, the independent solution is
`(0.008333333333333333,-0.003333333333333333,-0.005)` for both positive rate
choices. A conserved shift `d -> d+Q alpha` changes no bias. The independent
non-diagonal SPD susceptibility case also satisfies the constrained formula.

## Source compatibility, projection, and circulation

Zero affinity on every active edge requires `b_active` in
`image(S_active^T)`, equivalently zero projection onto every reaction-space cycle
in `ker(S_active)`. Reaction cycles and conserved species charges are distinct
null spaces. An arbitrary b cannot be interpreted as an equilibrium chemical
potential shift.

For strictly positive R, the steady affinity is the R-weighted projection

```text
b_star = S^T (S R S^T)^+ S R b.
S R (b-b_star) = 0.
```

The superscript + denotes the Moore-Penrose inverse. A conserved chemical
potential shift supplies the selected initial-charge slice without changing
`b_star`. The residual generates steady reaction progress `j=R(b-b_star)` in
`ker(S)`. With inactive channels, project only on active reaction coordinates.
An ordinary unweighted compatibility residual correctly diagnoses feasibility,
but does not by itself determine steady response under unequal rates.

For `b=0.01*(1,1,1)`, equal rates give zero densities and nonzero progress
`(0.01,0.01,0.01)`. Rates `(1,2,4)` give the independently verified stationary
density `0.01*(11/21,-8/21,-1/7)` and progress `12*0.01/7` on each edge. This is
externally driven circulation, not detailed-balanced equilibrium or a reservoir
derived from the candidate hypothesis.

## Positivity, detailed balance, and dimensions

For fixed C and zero bias, `F=x^T C^-1 x/2` decreases since
`F'=-a^T R a<=0`, with `a=S^T C^-1 x`. More generally `j=R(b-a)` gives

```text
F' = b^T j - (b-a)^T R (b-a).
```

Thus bias power `b^T j` supplies dissipation. The extra algebraic source term
in `F'=-a^T R a+a^T R b` is not by itself the full drive power. In physical
units, `Delta=S^T mu-zeta`, `Lambda=diag(gamma/T)`, `J=-Lambda Delta`, and

```text
F_dot = zeta^T J - Delta^T Lambda Delta
sigma_reaction = Delta^T Lambda Delta / T >= 0.
```

This entropy-production statement presumes a matched local detailed-balance
normalization and bath/drive accounting. It does not supply an autonomous
source reservoir. The independent controls check the work/dissipation identity
at nine states and both driven steady cycles. Positivity of A is relaxation
stability, not positivity of every signed asymmetry density.

The producer's dimensional assignments are consistent: `[chi]=E^2`,
`[gamma]=E^4`, `[Lambda]=E^3`, `[W]=E`, and `[S Lambda zeta]=E^4`.
The dimensionless rate is `rho=t_ref gamma/T^3`; comparing gamma directly to H
would be dimensionally wrong. Physical reaction/diffusion normalization remains
unmatched. For `s_dot+3Hs=Sigma`, the yield equation
`Y_dot=-(W+(Sigma/s)I)Y+S Lambda zeta/s` follows directly from `Y=n/s`.
Time-dependent chi or an expanding background contributes further terms to a
free-energy derivative; fixed-background monotonicity is correctly limited to
the source-free diagnostic. The registered calculation is not an expanding
cosmological transport solution.

## Signed response and washout

For the compatible constant source, let `E=exp(-W)`. A one-unit positive interval
followed by a one-unit negative interval produces
`x(2)=-(I-E)^2 x_eq`, even though its integrated bias vanishes. The independently
computed equal-rate result is

```text
x(2)=(-0.00685781721761856,0.00329313533484921,0.00356468188276935)
norm(x(2))=0.008401270990108685.
```

Reversing both interval signs reverses the state. Complete reaction shutdown
preserves it. Twenty additional units with active zero-bias reactions erase the
nonconserved component to norm `2.3827050905400872e-14`, comfortably below the
registered `1e-10` threshold. The producer's corresponding norm
`2.3826630547752883e-14` differs only by absolute floating-point roundoff.
Conserved initial charges survive; source timing is weighted by the response
kernel, so a source area or speed threshold cannot determine a final density.

## Provenance and remaining limitations

The originally read registration digest is
`a8cf1c87f1dc5fd0d404a2f5b8a8b56ccf3cfe993aef8daeb08c8e35d4513006`.
It remains unchanged. At initial review, all four input files listed by the
producer's receipt were accessible and their hashes matched. The comparison
output records this check and the audited implementation/result/trajectory
hashes. The unchanged original receipt digest is
`2bbd13f5465735b84968d92384b2633972300ad56d8c678eb1258764ff5a0bba`.
Each comparator rerun validates the immutable original snapshot against the
actual context repository. Missing or mismatched required inputs prevent a
successful provenance result and cause a nonzero exit; an exported comparator
alone is insufficient for this required context validation. The original
registration/receipt remain untouched, and the rerun validation is recorded
separately from the initial review snapshot.
A local pre-run timestamp and receipt demonstrate the session's recorded order,
not an externally immutable preregistration service.

No material numerical or dimensional mismatch was found in the stated toy
scope. The inactive-rate qualification was corrected by a recorded amendment;
the producer also implemented the reviewer's requested separation of algebraic
source contribution, total drive work, and entropy production. Extreme reaction-rate hierarchies,
nonlinear chemical potentials, changing susceptibility, expansion, and a coupled
source bath were not numerically validated. The source/operator, particle
content, physical charge label, susceptibilities, rate conventions, conserved
initial charges, cosmological history, and freeze-out prescription remain
prerequisites for any actual AntiMatter abundance calculation. Literature
references were scoped inputs here; no new exhaustive web or novelty review was
performed by this independent numerical check.
