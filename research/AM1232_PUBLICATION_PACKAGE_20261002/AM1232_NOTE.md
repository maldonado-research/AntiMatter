# AntiMatter: Conditional Kinetic, Source-Duration, Transport and Standard Model Charge Audits (v1.23.2)

**Ricardo Maldonado · Publication date prepared as 2 October 2026, Pacific · Prepared with AI assistance**

**Publication status at package preparation:** Zenodo version DOI **10.5281/zenodo.23112808** is reserved for draft record 23112808; publication has **not yet been confirmed**. The existing concept DOI is **10.5281/zenodo.18193771**. The published predecessor is v1.23.1, DOI **10.5281/zenodo.22400470**. Reserving a DOI, preparing these files, or creating a Git tag does not publish a Zenodo record.

This package archives conditional consistency calculations and two completed diagnostic rounds. It does not establish successful baryogenesis, the observed baryon sign or abundance, a matched ultraviolet theory, new mathematics, or physical novelty. Source snapshot: full Git commit `da472576101a66b1c5c7dc97c01f7124e99076bd`; intended tag source URL: <https://github.com/maldonado-research/AntiMatter/tree/v1.23.2>. Exact source bytes and hashes are recorded in `SOURCE_MANIFEST.json`.

## What changed since v1.23.1

The preserved v1.23.1 package contains the earlier symmetry, Wilson-line, energy, and cosmology audit. Its original files, citation, parent archives, and checksum ledger remain unchanged. The present release adds assumed kinetic-metric tests, an expanding source-only duration bound and finite trajectory scan, an illustrative transport diagnostic, an exact ideal Standard Model charge/source comparator, and a bounded comparison with a 2026 electroweak-wall paper. It also contains numerical reproduction scripts and an **inactive** external AI runner template.

The main advance is a more explicit account of dependencies and missing inputs. A field speed, available energy, or selected efficiency alone cannot determine a net charge: operator normalization, susceptibility, reactions, conserved charges, signed source history, washout, and shutdown matter. Each result below holds only in its stated problem.

## 1. Assumed Wilson kinetic metrics

For the public 31-site, q=3 benchmark, let `Q_j=e_j−3e_(j+1)`, `w=(3^30,…,1)`, and `e=e_30`. The audit keeps the bare site scale fixed at `f_site=235.70226039551585 GeV` and solves the generalized spectrum `Hv=m²Gv`, with `H=aQ^TQ+d ee^T`. Its chosen metric family is

`G=I+c Q^TQ+b ee^T`, with nonnegative c and b.

Since `Qw=0` and `e^T w=1`, the winding-trough norm obeys the exact identity

`F²=f_site²(w^T w+b)`, where `w^T w=(9^31−1)/8`.

Link-only corrections therefore preserve this norm exactly at fixed site normalization; endpoint terms retain an extremely small fractional shift. `F` is the scale in `cos(a/F)`, with full repeat `2πF`, and is not an exact light-mass formula. At the nominal link-mixing magnitude, the minimum's smallest heavy mass changes **213.753471 → 207.018544 GeV** and its largest heavy mass changes **425.414884 → 378.697141 GeV**. Adjacent-only comparison metrics shift the period by about +1.63% or −1.65%, demonstrating the role of correlated diagonal terms.

The finite audit has **12 metrics, 36 source/metric configurations, and 210 controls**. Positive metrics preserve Hessian inertia; the source-off mode is zero and a source maximum has one tachyonic direction. A separate high-precision inverse-iteration implementation agrees with the producer's Sturm-root calculation across all 36 configurations.

This is an audit of **assumed matrices**, not a calculation of a physical loop correction. The unsigned leading-log proxy fixes neither its sign nor counterterms, finite terms, thresholds, endpoint matching, or a five-dimensional completion. Large corrections are stress tests without a perturbative error claim. Many reported Decimal digits resolve the mathematical matrix problem; they do not express physical precision for uncomputed matching.

## 2. Source duration and its energy bill

The source-only problem uses an initially resting, fixed cosine with coefficient A, ideal available drop `2A`, no autonomous work input, and no extra dissipative channel. Coupled Friedmann evolution includes residual potential and separately conserved radiation. Its imposed pointwise dimensionless speed is `u=abs(dot(tau_1))/T`, so the physical speed threshold scales with temperature.

For a required interval ΔN ending at `T*=131.7 GeV`, the necessary budget condition is

`K_req,*[3 exp(2ΔN)−2] <= 2A`.

At unit response efficiency, the integer winding minima are **35, 36, 45, 86, and 156** for ΔN=0, 0.01, 0.1, 0.5, and 1. The single-field diagnostic uses `F_eff=3^30×250 GeV`; it is separate from the generalized Wilson spectrum and does not join the two calculations into a physical model.

All **30 locally registered trajectories** were computed and checked against a separate proper-time implementation of the producer's e-fold integration. The largest sampled endpoint kinetic energy is **0.483580462 A**, corresponding to the conditional final-instant bound `n eta >= 70.371811944`. Its kinetic/radiation ratio is **0.028382607** and total scalar/radiation ratio **0.029584693**. It exceeds the inherited strict 1% kinetic target and is not a viable solution.

The finite grid is not a global optimum. Changing n here changes an inferred threshold rather than an already computed trajectory. A general integrated baryon yield need not require this pointwise speed history. Hubble dilution of scalar energy is not heat deposited into the separately conserved radiation sector. These necessary source-only bounds predict no baryon yield and exclude no different model with spatial gradients, additional work, or energy transfer.

## 3. Illustrative transport and signed history

The three-species, fixed-temperature transport round projects the response onto the allowed susceptibility-weighted charge slice. A source along an exactly conserved current creates no new density. Incompatible reaction biases can instead sustain externally driven circulation and rate-dependent stationary densities.

Equal positive and negative source intervals need not cancel because their retarded weights differ. Shutting off reactions preserves the signed residual in the comparator; keeping reactions active washes out its nonconserved component. Species A is a label, **not baryon number**; the dimensionless densities divided by T cubed are not cosmological yields.

Evidence includes **nine producer tests, 71 independent controls, 11 comparisons, and all 201 signed-history samples**. The independent implementation uses chemical-potential coordinates and augmented matrix exponentials without importing the producer implementation; the recorded maximum discrepancy was 4.44e−16 in the specified dimensionless cases. This fixed-temperature test supplies neither the candidate's operator/rates/CP data nor an expanding, energy-conserving source and bath.

## 4. Exact conditional Standard Model response

For the **trial external** interaction `L_int=c (partial_mu theta0) J_(B+L)^mu`, define `kappa=c dot(theta0)`. In the relativistic symmetric Standard Model with one Higgs doublet, equilibrated quark mixing, Yukawas and weak sphalerons, hypercharge neutrality, and each fixed `Delta_i=B/3−L_i`, exact linear algebra gives

`n_B=(28/79)n_(B−L)+(72/79)T² kappa`.

The familiar B−L conversion and the imposed-source response are distinct terms. An exactly conserved-charge source induces no new density on this fixed-charge slice. B and L sources are equivalent modulo B−L; B+L gives twice either response. This conventional charge calculation does **not** derive a Wilson-specific coupling or supply a grand-canonical reservoir.

Choosing `c=n_det D_d` places the inherited hierarchy factor inside the chemical shift as an additional assumption. At the inherited unit-efficiency phase speed, `kappa/T=52.34302564 D_d` and `max_i |mu_i|/T=33.12849724 |D_d|`. D_d is formal, not fitted to the observed yield. Choosing `c=n_det` would instead produce chemical potentials too large for this linear comparator. Neither normalization derives the physical interaction, and a small chemical shift does not erase the field's kinetic cost.

With ideal entropy `g_*s=106.75`, `C_ideal=6480/(33733π²)=0.0194634710818`, consistent with the archived rounded 0.0195. Freezing all other inherited inputs, this substitution moves the **one-height continuous threshold** 48.93652273 → 49.02836648, giving integer minimum 50 and n=49 efficiency requirement 1.000578908. Full-drop and strict 1% unit-efficiency thresholds remain 35 and 119. This is a conditional sensitivity calculation, **not** a correction to the physical response near 131.7 GeV.

The mixed-gauge Weyl trace, with the recorded topological orientation, gives `partial_mu J_(B+L)^mu=6 q_W−6 q_Y`. B−L conservation here belongs to the selected reaction network; its gravitational trace without right-handed neutrinos, Majorana/Weinberg reactions, and a dynamical hypermagnetic sector require separate treatment. Small fermionic chemical potentials, `|mu_H|<m_H(T)` with positive Higgs thermal mass, and equilibration faster than background changes are necessary. Broken-phase susceptibilities, finite rates, and memory after sphaleron shutdown are absent.

The producer has **48 primary controls and 36 conditional sensitivity controls**; the separate 16-species symbolic implementation has **24 primary controls, seven sensitivity checks, and 11 exact comparisons**. The public operator inventory has 13 checks and the scientific consistency review 35. Producer implementation was frozen before the independent coefficient arrived, but that message arrived **before first execution**: execution was not fully blinded.

## 5. A 2026 electroweak-wall comparator

Vanvlasselaer and Yin's *Spontaneous Baryogenesis from Axions on Induced Electroweak Walls*, **arXiv:2604.20762v1**, was reviewed in full, including its appendices. The 31-page arXiv v1, rather than a separately inspected journal typeset text, is pinned by retrieval hashes. Bibliographic metadata identifies JCAP 09 (2026) 063, DOI **10.1088/1475-7516/2026/09/063**. This is one targeted comparator, not an exhaustive search or a reproduced wall calculation.

The paper supplies a scalar/Higgs action, local wall-motion chemical shift, finite sphaleron relaxation, and scenarios for wall energy, decay, reheating, and entropy dilution. Those are additional dynamical ingredients, not ultraviolet matching or a reservoir for the public Wilson clockwork. Its treatment neglects diffusion and wall-induced bulk plasma motion; source smallness and microscopic local-equilibrium conditions remain essential.

The unconstrained ideal-gas sum `chi_(B+L)=13T²/6` differs from this release's fixed-charge, hypercharge-neutral result `144T²/79`. Their ratio is **864/1027 ≈ 0.8413**. This identifies an ensemble/spectator and rate-convention matching task; it is **not a universal yield correction**. Changing susceptibility also changes a relaxation convention, and neither symmetric-phase number establishes a response at the electroweak crossover. An anomaly-normalization convention flag in the paper's topological rewriting remains unresolved; no paper error is inferred and that coefficient must not be transferred before reconciliation.

Opposite wall orientations can cancel the net sign. Allowed Higgs portals and compact periodicity, wall formation and population, maximum reheating temperature, washout, relic disposal, and energy transfer must all be matched. A localized wall is a different branch to investigate, not a counterexample to the fixed homogeneous no-driver budget. The paper's numerical wall curves, external constraints, journal text, and wider cited literature were not independently reproduced in this bounded review.

## Independence, provenance, privacy, and automation

All new work uses public inputs. Local plans were recorded before the finite scans with the existing baseline known; these are not external preregistrations. Independent implementations share public data and were prepared with AI assistance. They provide computational cross-checks, not independent human peer review, experimental confirmation, or validation of the physical hypothesis. Post-run portability amendments preserve original scripts and receipts and disclose their actual ordering.

The complete archive preserves the **48-entry baseline, 40-entry candidate, 24-entry transport, and 60-entry operator ledgers** byte for byte, plus their subordinate ledgers and original archives. `SOURCE_MANIFEST.json` binds every copied source file to the specified commit. No private raw references, personal files, historical private inventory identifiers, chat exports, credentials, publication-private state, detailed private AI logs, or third-party paper PDFs/extracted text/page images are packaged. Authored literature notes, source links, bibliographic metadata, and retrieval hash receipts are included; third-party publications retain their own rights.

The GitHub workflow performs numerical checks only. The completion-driven AI wrapper/loop and systemd user unit are **inactive templates**: no authenticated external model execution, installed service, persistent host, or uninterrupted 24/7 research operation is established by this archive. Mock orchestration success does not establish scientific completion or external publication. GitHub and Zenodo publication states require separate verified receipts.

## Reproduce and inspect

Extract `AM1232_COMPLETE.zip` and use its `source/` directory as the repository root. It preserves the original relative research and script paths. Start by verifying the four enclosing ledgers:

```bash
(cd source/research/AM1231 && sha256sum --check SHA256SUMS.txt)
(cd source/research/AM1232_CANDIDATE_20261001 && sha256sum --check SHA256SUMS.txt)
(cd source/research/rounds/2026-10-01_transport_gate && sha256sum --check SHA256SUMS.txt)
(cd source/research/rounds/2026-10-02_sm_operator_gate && sha256sum --check SHA256SUMS.txt)
```

Use **Python 3.12.14** in an isolated virtual environment with the exact baseline pins and the operator's SymPy/mpmath pins. The aggregate runners require Git metadata and therefore need a checkout of the fixed source commit, rather than a plain extracted `source/` directory. Run from that checkout, with receipts in a separate output directory:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r research/AM1231/requirements-replay.txt \
  -r research/rounds/2026-10-02_sm_operator_gate/requirements-operator.txt
.venv/bin/python -m pip check
.venv/bin/python scripts/reproduce_candidate.py --output /absolute/new-candidate-checks
.venv/bin/python scripts/reproduce_operator_round.py --output /absolute/new-operator-checks
```

Check the interpreter patch version; archived metadata can require it. These commands do numerical work without invoking AI. The runners validate provenance, copy public inputs into disposable directories, and preserve source records. **Package-level `REPRODUCTION.md` supplies both pinned-checkout commands and manual replay directly from the archive without Git.** The candidate's explicit **post-run portability policy** allows only named metadata and bounded numerical differences, including specified primary floating values and trajectory endpoints; every difference is retained in receipts and all original producer/independent checks must still pass. It does not imply byte equality or a newly preregistered acceptance policy. Do not rewrite an original output to force agreement. Follow the included candidate, transport, and operator `REPRODUCE.md` notes for full controls; transport replay is also specified in the numerical workflow. Network literature retrieval is separate from numerical replay.

The historical `producer/ORIGINAL_PORTABILITY_INPUTS/SHA256SUMS` records an earlier producer context. Its parent-relative entries are preserved historical provenance; checking it naively within that archival subdirectory is not a current full-workflow verification. Use the current enclosing ledger and documented portability checks.

`AM1232_ALL.txt` concatenates the authored release note and included Markdown documents with source headings. `AM1232_PHONE.zip` provides lighter reading copies; `AM1232_COMPLETE.zip` contains the reproducible source. Outer SHA-256 hashes are in `AM1232_CHECKSUMS.txt`. The original v1.23.1 `source/CITATION.cff` cites the predecessor; use `RELEASE_CITATION.cff` for this version after its reserved DOI is confirmed published.

## Selected references and next test

- Preserved v1.23.1 publication: <https://doi.org/10.5281/zenodo.22400470>.
- Harvey and Turner, *Cosmological baryon and lepton number in the presence of electroweak fermion-number violation*, Phys. Rev. D 42 (1990) 3344: <https://doi.org/10.1103/PhysRevD.42.3344>.
- Vanvlasselaer and Yin, version actually reviewed: <https://arxiv.org/abs/2604.20762v1>; journal metadata: <https://doi.org/10.1088/1475-7516/2026/09/063>.
- Source-version references and bounded retrieval scopes appear in the candidate literature review, operator derivations/inventory, and `wall_literature/LITERATURE_NOTE.md`.

The next bounded physical test is to select **one allowed Wilson-specific operator**, match its couplings and rephasing-invariant CP data, reconcile spectator/susceptibility and rate conventions across the electroweak crossover, and register an energy-conserving source/bath evolution. A wall branch additionally needs an allowed scalar/Higgs action and opposite-orientation cancellation controls. No final baryon yield, physical CP sign, novelty, or viable cosmology follows before those gates are met.

Copyright © 2026 Ricardo Maldonado. The author's material is supplied under **CC BY 4.0**; retain attribution, the original predecessor citation, license notices, and this description of the new release. Referenced third-party publications are not relicensed.
