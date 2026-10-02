# Conditional Wilson kinetic-matrix audit

2026-10-01, America/Los_Angeles. Candidate calculation outside the protected
v1.23 release. **All 210 registered numerical/algebraic controls pass.**
The finite family contains 12 metrics and 36 source configurations. This result
does not compute or match the physical five-dimensional kinetic correction.

The assumed charge-correlated link metric changes heavy masses while leaving the
compact winding period exactly unchanged at fixed site normalization. The nominal
link-only correction moves the source-minimum heavy gap from **213.753471 GeV to
207.018544 GeV** and its largest heavy mass from **425.414884 GeV to 378.697141
GeV**. Arbitrary adjacent-only controls shift the period by approximately +1.63%
or −1.65%, illustrating why the correlated diagonal terms matter.

## Definition and assumptions

Use the public 31-site q=3 Wilson benchmark with rows
`Q_j=e_j−3e_(j+1)`, endpoint `e=e_30` and integer winding
`w=(3^30,…,1)`. The public mass Hessian is already divided by the site scale:

\[
H=aQ^TQ+d ee^T,\qquad Hv=m^2Gv,
\quad K=f_{site}^2G,\quad U_{\theta\theta}=f_{site}^2H.
\]

The reconstructed, float-derived coefficients promoted to Decimal are
`a=11332.575353119271 GeV²`,
`d_min=11221.904286491297 GeV²`, and
`d_top=−11103.289358269605 GeV²`.
The physical site scale stays fixed at the published
`f_site=235.70226039551585 GeV`.

The structural family is **assumed** to have
`G=I+c Q^TQ+b ee^T`, with nonnegative c and b. Its diagonal is
`(1+c,1+10c,…,1+10c,1+9c+b)` and adjacent entries are `−3c`.
The published unsigned mixing proxy is `epsilon=0.04921048547006312`;
`c0=epsilon/3=0.016403495156687706…` matches that off-diagonal magnitude.
The sign choice, complete loop normalization, matching scale, threshold terms,
counterterms and finite pieces remain unspecified. Endpoint values `b=0,c,3c`
are illustrative; they are not an endpoint loop estimate.

The arbitrary controls `G=I±epsilon A`, with A the path adjacency matrix,
are sensitivity tests. They are not physical loop calculations. A site-scale
redefinition that keeps diagonal entries fixed would change the physical K and
the quoted period; this audit instead holds the original f_site fixed. Any pure
coordinate change must transform both H and G together.

## Exact statements and finite numerical results

Write `S=w^T w=(9^31−1)/8=47690053059618228953581237351`.
Integer arithmetic gives `Qw=0` and `e^T w=1`. Therefore

\[
F^2=w^TKw=f_{site}^2(S+b),\qquad
\frac{F^2-F_0^2}{F_0^2}=\frac bS.
\]

The link term cancels exactly, independently of c. For b>0 the period shift is
retained as a high-precision decimal; rounding F/F0 to an ordinary float would
hide it. F here is the winding-trough norm. The finite endpoint curvature changes
the local eigenvector, so `m_light²=d/(S+b)` is not an exact mass formula.

All masses in the following table are in GeV. “Top” means the endpoint source
maximum with the links still at their minima. Machine-readable files contain all
other observables and full precision.

| Metric | F/F0 − 1 | Heavy gap: off | Heavy gap: minimum | Heavy gap: top | Largest heavy: minimum |
|---|---:|---:|---:|---:|---:|
| Baseline | 0 | 213.726845 | 213.753471 | 213.657854 | 425.414884 |
| c=c0, b=0 | 0 exactly | 206.993278 | 207.018544 | 206.922776 | 378.697141 |
| c=c0, b=c | 1.719803e−31 | 206.990858 | 207.017456 | 206.913861 | 378.695425 |
| c=c0, b=3c | 5.159408e−31 | 206.985534 | 207.015137 | 206.892508 | 378.692722 |
| c=3c0, b=0 | 0 exactly | 195.238739 | 195.261642 | 195.164044 | 318.340559 |
| c=3c0, b=c | 5.159408e−31 | 195.232241 | 195.259009 | 195.131438 | 318.336848 |
| c=3c0, b=3c | 1.547822e−30 | 195.214421 | 195.252608 | 194.993865 | 318.333104 |
| c=10c0, b=0 | 0 exactly | 165.824803 | 165.841921 | 165.715680 | 223.622295 |
| c=10c0, b=c | 1.719803e−30 | 165.807538 | 165.837182 | 165.166130 | 223.605765 |
| c=10c0, b=3c | 5.159408e−30 | 165.565661 | 165.817496 | 160.068067 | 223.603344 |
| Adjacent +epsilon | +0.01627112048 | 203.978520 | 204.003394 | 203.919438 | 447.912155 |
| Adjacent −epsilon | −0.01654028568 | 225.021690 | 225.050638 | 224.935904 | 405.999572 |

Every metric is positive definite: the structural family obeys `G≥I`, while
both adjacent controls have minimum metric eigenvalue
`1−2|epsilon| cos(pi/32)=0.902052952936…`.
The link-only correction has operator norm approximately 0.262 at c0, 0.786 at
3c0 and 2.620 at 10c0. The last points are stress tests; the calculation solves
the assumed metric exactly and makes no perturbative truncation-error claim.

The source-off mode is exactly zero in every case. Positive G preserves the
Hessian inertia, so each minimum has 31 positive modes and each top has exactly
one tachyon and 30 positive heavy modes. The baseline tiny roots are

\[
m^2_{min}=+2.093908662423041576\times10^{-25}\ {\rm GeV}^2,
\quad
m^2_{top}=-2.653153307216788740\times10^{-25}\ {\rm GeV}^2.
\]

Their signed square-root conventions are `+0.000457592467423038… eV` and
`−0.000515087692263831… eV`, respectively. The negative sign labels tachyonic
mass squared, not a negative real particle mass. At nominal c0,b=0 the relative
changes in mass squared are `−3.33835e−32` at the minimum and `−5.35971e−32` at
the top; these require the 90/110-digit calculation to distinguish. Across the
registered structural family their magnitudes change by at most `1.394e−29`
relative. These digits describe this mathematical pencil at fixed rounded inputs;
they are not physical precision on uncomputed quantum corrections.

For the adjacent controls the minimum masses are `0.000450266132928 eV`
(+epsilon) and `0.000465288471669 eV` (−epsilon). Their mass-squared shifts are
approximately −3.17649% and +3.39198%. The exact period formula is
`F/F0=sqrt(1+(2epsilon/3)(1−1/S))` with signed epsilon.

## Verification and reproduction

Decimal tridiagonal LDL/Sturm inertia counts certify the light-root brackets;
bisection is performed separately at 60, 90 and 110 digits. The largest relative
60-versus-110 discrepancy is `6.418e−31`; 90-versus-110 gives `6.890e−61`.
Double precision is used only for heavy eigenvalues and approximate metric
extrema. An independent Cholesky coordinate transformation reproduces the heavy
eigenvalues within `1.877e−15` relative. The analytic source-off spectrum at b=0,
`a mu/(1+c mu)` with `mu=10−6cos(l*pi/31)`, also passes. All published baseline
Hessian CSV entries agree within `2.255e−12` relative (registered bound 1e−10).

A separate exact inverse-trace identity checks finite endpoint relaxation.
For nonzero d, put `T=(S−31)/8`; then

\[
\operatorname{tr}(H^{-1}G)=\frac{S+b}{d}+\frac{T+30c}{a}
=\sum_i\lambda_i^{-1}.
\]

For adjacent controls replace the numerator pair by
`S+(2epsilon/3)(S−1)` and `T+epsilon(S−271)/12`.
The inverse of this trace approximates the tiny root, with the heavy reciprocal
sum supplying the correction. Its largest observed relative error is
`2.050e−28`; this approximate control is not substituted for the converged root.

Run from any directory, selecting a fresh output directory:

```sh
/workspace/AntiMatter/.venv/bin/python /workspace/research-progress/antimatter/wilson-metric/audit.py \
  --source-root /workspace/AntiMatter/research/AM1231/v1.23 \
  --output-dir /tmp/wilson-metric-replay
```

Expected summary: `PASS`, 12 cases, 36 configurations, 210 checks, no failures.
The pinned runtime is Python 3.12.14, NumPy 2.5.2 and SciPy 1.17.1. Two complete
runs, including a fresh output directory, produced byte-identical JSON and CSV;
[reproduction.json](reproduction.json) records both SHA-256 pairs. The code writes
into the selected output directory; without flags it defaults to its own. Public
source hashes before/after the audit match and are included in
[results.json](results.json), together with the code and registration hashes.

The pre-run [registration](REGISTRATION.md) fixes the finite family and controls.
[audit.py](audit.py) is executable; [results.csv](results.csv) contains one row
per case/source configuration. No private raw research inputs were used.

An independent review using charge-factor inverse iteration for tiny roots and
Decimal Sturm bisection for heavy roots agrees across all 36 rows: relative errors
are at most `6.59e−81` for tiny mass squared and `5.78e−16` for heavy masses.
The exact period shifts agree within `3.42e−80`. The separate
[independent audit](../wilson-metric-independent/AUDIT.md) records its algorithm,
comparisons and limitations.

## Verified source anchors and remaining uncertainty

The only source inputs are the checked local public release:

- [v1.23 note, Wilson benchmark and open kinetic-matrix requirement](https://github.com/maldonado-research/AntiMatter/blob/main/research/AM1231/v1.23/v1.23_wilson_instanton_cosmology_audit_note.md#L70).
- [Public generator, harmonic curvature](https://github.com/maldonado-research/AntiMatter/blob/main/research/AM1231/v1.23/v1.23_wilson_instanton_cosmology_audit.py#L204) and [Hessian normalization/proxy](https://github.com/maldonado-research/AntiMatter/blob/main/research/AM1231/v1.23/v1.23_wilson_instanton_cosmology_audit.py#L427).
- [Preserved Hessian CSV](https://github.com/maldonado-research/AntiMatter/blob/main/research/AM1231/v1.23/v1.23_wilson_hessian.csv), [benchmark CSV](https://github.com/maldonado-research/AntiMatter/blob/main/research/AM1231/v1.23/v1.23_wilson_benchmark.csv), and [full-precision summary](https://github.com/maldonado-research/AntiMatter/blob/main/research/AM1231/v1.23/v1.23_summary.json).

This establishes a conditional spectral replay and exposes the importance of
charge-correlated diagonal corrections. Physical loop matching, allowed finite
counterterms, UV thresholds, messenger/anomaly port, radion stabilization and
thermal/driver/cosmological dynamics remain open. No physical baryogenesis,
general WGC conclusion, priority or novelty claim follows. No external papers
were retrieved or verified for this bounded audit, and the protected release
was not edited or committed.
