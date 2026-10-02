# AntiMatter v1.23.2 candidate: kinetic metrics and source-duration diagnostics

Ricardo Maldonado · 1 October 2026, Pacific · Prepared with AI assistance

**Candidate research checkpoint for review.** The archived scientific release
remains v1.23.1. This package proposes a distinct follow-up; it has no new DOI
and is not an implemented v1.24 thermal or baryogenesis model. It contains two
bounded consistency calculations using public v1.23/v1.23.1 inputs. No private
raw files, chat exports or personal documents were incorporated.

## In More Basic Terms

The field chain's long variation scale survives one assumed family of correlated
kinetic corrections, while its heavier modes change. This tells us which matrix
structure matters, but the actual quantum correction still needs to be derived.

An energy budget also has to last. In the source-only calculation, sustaining the
stipulated motion through expansion requires more energy than an instantaneous
speed check. The familiar full-cosine winding allowance of 35 rises to 45 for
0.1 e-fold and 156 for one e-fold ending at the electroweak benchmark, at unit
response efficiency. An e-fold means the scale factor grows by a factor of e.
These are necessary conditions for the stated speed requirement, not a mechanism
that produces the observed matter excess.

## Results and their scope

| Calculation | Verified result | Assumptions and limits |
|---|---|---|
| Wilson kinetic metric | For `G=I+c Q^T Q+b ee^T`, `Qw=0` gives `F^2=f_site^2(w^T w+b)` exactly. Link-only corrections preserve the winding scale. At the nominal magnitude, the smallest heavy mass changes 213.753471 → 207.018544 GeV. | Fixed bare site scale; chosen charge-correlated metric. The leading-log magnitude does not determine physical sign, counterterms or five-dimensional matching. |
| Source duration | `K_req,*[3 exp(2 Delta N)-2] <= 2A`; unit-efficiency integer minima are 35, 36, 45, 86 and 156 for intervals of 0, 0.01, 0.1, 0.5 and 1 e-fold ending at `T*=131.7 GeV`. | Initially resting fixed cosine, no work or extra dissipation, and a pointwise constant dimensionless threshold `u=abs(dot(tau_1))/T`. The physical speed threshold scales with temperature. A general integrated baryon yield need not require this threshold. |
| Source trajectories | All 30 locally registered source-only trajectories execute with coupled Friedmann expansion and scalar/radiation ledgers. The largest sampled endpoint kinetic energy is 0.483580462 A, implying a conditional final-instant `n eta >= 70.371811944`. | Finite grid, not a global optimum. Changing n only changes the inferred threshold here; it does not change the already computed trajectory. |

`F` is the scale in `cos(a/F)`; the full field repeat is `2 pi F`. The potential
coefficient is A and the ideal full drop is 2A. The source-only cosine uses
`F_eff=3^30*250 GeV`, not 250 GeV. It is a one-field diagnostic, separate from
the generalized multi-field Wilson spectrum. The calculations do not combine
into a completed physical model.

The largest-kinetic sample has total scalar/radiation ratio 0.029584693 and
kinetic/radiation ratio 0.028382607. It exceeds the earlier strict 1% kinetic
target; it is not presented as a viable solution. Residual potential belongs
in Friedmann's equation. Hubble dilution in the scalar ledger is not heat
deposited into the separately conserved radiation sector.

## Evidence and independent implementations

- [Wilson report](wilson-metric/RESULTS.md), [local pre-run plan](wilson-metric/REGISTRATION.md), [code](wilson-metric/audit.py), [JSON](wilson-metric/results.json), [CSV](wilson-metric/results.csv).
- [Wilson independent review](wilson-metric-independent/AUDIT.md) and [comparison receipt](wilson-metric-independent/comparison-results.json): separate high-precision inverse iteration checks the producer's Sturm roots and heavy spectrum. All 36 source/metric combinations agree; all 210 producer controls pass.
- [Source-duration report](source-duration/RESULTS.md), [local pre-run plan](source-duration/REGISTRATION.md), [code](source-duration/audit.py), [JSON](source-duration/results.json), [trajectories](source-duration/trajectories.csv), [duration table](source-duration/duration_bounds.csv).
- [Source-duration independent review](source-duration-independent/AUDIT.md): separate proper-time integration checks the producer's e-fold integration and all 30 registered endpoints.
- [Claims and limitations](CLAIM_REVIEW.md), [reproduction instructions](REPRODUCE.md), and [next tests](NEXT_TESTS.md).

The plans were written locally before the new finite scans, with the published
baseline already known; no external preregistration is claimed. Reviews use
independently implemented calculations with shared public inputs and AI
assistance. They are computational cross-checks, not external peer review,
experimental evidence or independent validation of the underlying hypothesis.

## What remains unresolved

Actual kinetic matching, messenger/anomaly construction, an analytic thermal
potential, a physical CP-odd invariant, autonomous driver and reservoir, transport,
sphaleron freeze-out, washout, spectators, relics and vacuum/defect history remain
open. Selecting an initial rolling sign does not derive CP violation. Particle
pair production alone cannot produce a net matter asymmetry. These diagnostics
predict neither the sign nor the final observed baryon abundance.

The scientific baseline and its public sources are preserved in
[AM1231](../AM1231/). No new literature was retrieved for this checkpoint because
the current runtime rejected external literature requests. No priority or
novelty claim is made. Existing AntiMatter CC BY 4.0 terms apply.
