# Independent implementation review of the candidate Wilson metric audit

Review date: 2026-10-01, America/Los_Angeles (2026-10-02 UTC). This review concerns a finite family of assumed kinetic
metrics, not a matched loop correction or a baryogenesis mechanism. It is an
independently implemented computational cross-check by another AI agent under
shared inputs. It is not external peer review or experimental validation.

## Registration and derivation

The producer's `../wilson-metric/REGISTRATION.md` correctly identifies the
dimensionless metric G, physical phase kinetic matrix K=f_site²G and mass matrix
H=U/f_site². The generalized problem is H v=m²G v; there is no second factor of
f_site in that problem. Inputs and the finite metric family are fixed in advance.

Write Q with rows e_j−3e_(j+1), e=e_30, and w=(3³⁰,…,1). Exactly Qw=0 and
eᵀw=1. With D=wᵀw=Σ(r=0…30)9ʳ, the family

    G=I+cQᵀQ+b eeᵀ
    F²=f_site² wᵀG w=f_site²(D+b)

has exactly unchanged F for b=0 and any c. For b>0, the relative squared-scale
shift is b/D. These are exact algebraic statements for the stated metric and
kernel winding. They do not depend on a numerical eigenvalue solver. The stable
relative period shift is (b/D)/(sqrt(1+b/D)+1); computing it by subtracting two
ordinary floating-point numbers would erase the change.

For c,b≥0, zᵀGz=||z||²+c||Qz||²+b(eᵀz)²>0 for z≠0. The adjacent-only controls
G=I+aT are positive definite because their eigenvalues are
1+2a cos(kπ/32), k=1,…,31, and |a|=0.04921048547006312<1/2. These controls are
different assumed metrics; they omit the correlated diagonal terms.

With B formed by stacking Q and eᵀ,

    H=Bᵀ diag(k_link,…,k_link,k_endpoint) B.

B is upper triangular with diagonal 1 and superdiagonal −3, hence invertible.
Its inertia proves that the source minimum has no negative eigenvalues, the
source top has exactly one, and source off has precisely one zero direction.
Congruence by a positive kinetic metric cannot change those counts. For b=0,
source off also has the exact nonzero spectrum

    m_l²=k_link μ_l/(1+c μ_l),
    μ_l=10−6cos(lπ/31), l=1,…,30.

The off-diagonal entries of cQᵀQ are −3c. Thus c=epsilon_pub/3 realizes a
negative off-diagonal entry of magnitude epsilon_pub. The published scalar
leading-log proxy does not establish this physical sign or its diagonal
renormalization prescription. The registration correctly states that limitation.

## Independent numerical method and evidence

`independent.py` uses only Python's standard library. It reads the public summary
and reconstructs curvatures from the harmonic formula without importing either
the preserved generator or the producer program. Matrix inputs are promoted from
the frozen floating-point coefficients; extra Decimal digits resolve the linear
algebra, not unknown physical parameter digits.

For the tiny minimum and top roots, it applies H⁻¹G by solving the two triangular
systems from the exact B factorization. Normalized inverse iteration isolates
the eigenvalue of greatest inverse magnitude; a quadratic-form Rayleigh quotient
and the full generalized-equation residual check the answer. This is different
from the producer's registered light-root Sturm calculation. For the smallest
and largest heavy roots, a Decimal LDL inertia bisection supplies high-precision
checks independent of a double-precision generalized eigensolver.

All 12 metrics and all three source states were checked at 80 and 110 Decimal
digits. The largest relative change in the checked eigenvalues/masses between
precisions is 1.63×10⁻⁷⁷. The largest generalized-equation relative residual for
the tiny nonzero eigenvalues is below 5.59×10⁻⁸¹. Source-off zeros follow exactly
from the factorization. Detailed values are in `independent-results.json`.

Selected independently computed source-minimum results:

| Metric | F/F0−1 | Light mass (eV, ordinary quoted precision) | Smallest heavy mass (GeV) |
|---|---:|---:|---:|
| I | 0 | 0.00045759246742303815 | 213.75347146299057 |
| c=c0,b=0 | 0 exactly | 0.00045759246742303815 | 207.0185441150698 |
| c=c0,b=c0 | 1.71980×10⁻³¹ | 0.00045759246742303815 | 207.01745599958562 |
| c=10c0,b=30c0 | 5.15941×10⁻³⁰ | 0.00045759246742303815 | 165.81749599610953 |
| adjacent +epsilon | +0.01627112048 | 0.0004502661329279424 | 204.00339426167167 |
| adjacent −epsilon | −0.01654028568 | 0.0004652884716689404 | 225.0506376908766 |

Here c0=epsilon_pub/3. The unchanged quoted light mass is not an exact equality:
at c=c0,b=0 its relative shift is −1.66918×10⁻³²; at c=10c0,b=30c0 it is
−4.25235×10⁻³⁰. Exact F invariance and near-invariance of a local light mass are
different statements. Finite endpoint stiffness relaxes the local eigenvector;
the exact low eigenvalue must not be replaced by k_endpoint/(wᵀG w).

## Physical interpretation limits

The vector leading-log magnitude is not a computed five-dimensional A5 kinetic
metric. The phase metric requires a matching prescription, allowed counterterms,
thresholds and boundary conditions; gauge-vector and holonomy effective actions
must not silently be identified across compactification. Unknown permitted
kinetic operators need not have the restricted link-correlated form. Holding
bare site normalization fixed is part of this audit, not a renormalization
prediction. The illustrative b values and c=10c0 stress tests are not loop
estimates. This calculation supplies no messenger/anomaly completion, CP bias,
thermal potential, autonomous driver, baryon yield, or universal stability claim.

## Producer comparison

PASS for all 12 registered metrics and 36 case/state rows. `compare.py` reruns
the independent eigenvalue methods with precisely the producer's retained
frozen coefficient strings. Separately reconstructed curvature coefficients
agree within 2.68×10⁻¹⁶ relative; their small last-bit difference follows the
different order of floating-point arithmetic and is explicitly recorded.

With matched coefficients, maximum differences are:

| Comparison | Maximum difference |
|---|---:|
| Tiny signed mass squared, inverse iteration versus producer Sturm roots | 6.59×10⁻⁸¹ relative |
| Smallest/largest heavy masses, Decimal bisection versus producer double solver | 5.78×10⁻¹⁶ relative |
| Relative period shifts, stable algebra versus producer Decimal result | 3.42×10⁻⁸⁰ relative |
| Relative tiny-mass-squared changes | 1.00×10⁻⁸⁰ absolute |

All 210 producer check flags pass, all 36 CSV rows match their JSON entries,
all 36 inertia/nullity classifications match the exact factorization, and the
referenced public source hashes still match.
`comparison-results.json` preserves the exact producer script/results and
registration hashes reviewed, per-row errors and input differences. The numbers
above establish agreement of implementations for this assumed metric problem;
they are not estimates of physical accuracy.

No blocking mathematical, normalization or numerical issue was found within
the registered scope. Claims of a physically derived Wilson kinetic correction,
loop sign, quantum completion or baryogenesis would exceed this review.
The producer's final `RESULTS.md` was also reviewed: its equations, displayed
tables, sign conventions and stated physical limits agree with the checked data
and derivation. Its use of independently implemented verification does not imply
external scientific validation.

To reproduce this review from any directory, use the supplied scripts and point
`--source-root` to the public release's `research/AM1231/v1.23` directory:

```sh
python3 /path/to/wilson-metric-independent/independent.py \
  --source-root /path/to/AntiMatter/research/AM1231/v1.23 \
  --output-dir /path/to/review-output
python3 /path/to/wilson-metric-independent/compare.py \
  --source-root /path/to/AntiMatter/research/AM1231/v1.23 \
  --producer-dir /path/to/wilson-metric \
  --output-dir /path/to/review-output
```

These review programs use only Python's standard library and write solely in
the selected output directory. Omitting options uses the recorded cloud workspace
source path and each script's own directory for output; the second program looks
for its producer in sibling `wilson-metric/`. The second program requires the
producer results and provenance files to exist. `independent.py` must remain
beside `compare.py` because the latter imports the independent solver.
