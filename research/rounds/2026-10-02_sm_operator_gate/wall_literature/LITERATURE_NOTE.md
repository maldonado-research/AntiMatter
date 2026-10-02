# Bounded primary-source review: induced electroweak walls

Prepared 2026-10-02 UTC. This note reviews **one** newly retrieved primary
paper in full, including its appendices. It is a targeted comparator, not an
exhaustive literature search, a peer review, or a claim of a new discovery.
No wall calculation from the paper was numerically reproduced here.

**Source:** Miguel Vanvlasselaer and Wen Yin, *Spontaneous Baryogenesis from
Axions on Induced Electroweak Walls*, [arXiv:2604.20762v1](https://arxiv.org/abs/2604.20762v1),
submitted 22 April 2026. INSPIRE currently lists JCAP **09** (2026) 063,
[DOI 10.1088/1475-7516/2026/09/063](https://doi.org/10.1088/1475-7516/2026/09/063).
The reviewed full text is the 31-page **arXiv v1**, not a separately inspected
journal typeset version. The version-pinned and unversioned arXiv PDFs matched
byte for byte at retrieval. Their SHA256 is
`55c4e37de2289f3148830d18827ec6a57dd4e8ddf6ae64593f3b918b20942ca3`.
Retrieval timestamps, URLs, extraction hash, and comparator hashes are in the
accompanying JSON receipts. Source PDFs, extracted text, metadata responses,
and page images remain under `/tmp`; they are excluded from this authored note
and its publication artifacts.

## Mechanism and explicit action

The paper couples a scalar to the Higgs through a field-dependent Higgs mass
parameter, with potential structure
`-m_H^2(phi)|H|^2 + lambda|H|^4 + V_phi(phi)` (Eq. 1, p4). A scalar wall
then separates a region where electroweak sphalerons remain active from a
region where they become suppressed. This differs materially from prescribing
a homogeneous rolling phase without supplying a Higgs profile.

The supplied interaction is
`L_int = -c_(B+L) (partial_mu phi/v) j_(B+L)^mu` (Eq. 12, p7).
Eq. 13 relates it to a scalar coupling to the SU(2) topological density through
the electroweak anomaly. This gives an explicit EFT operator and anomaly route
for **the paper's scalar**, not UV matching for the public Wilson clockwork.
The displayed coefficient in Eq. 13 also needs a normalization reconciliation:
with canonical SU(2) field strengths, integration by parts of Eq. 12 gives
the conventional anomaly coefficient proportional to `N_g`, whereas the
displayed Eq. 13 coefficient contains `1/N_g`. The independent review flags
this as an unresolved convention check; do not import that coefficient into
the Wilson model or infer a paper error without resolving the definitions.
The plasma-frame source is
`mu_(B+L) = -c_(B+L) u^mu partial_mu phi/v` (Appendix A, Eq. A3, p26).
For a translated planar profile `phi(z-beta_w t)`, the source comes from wall
motion: `mu_(B+L)=c_(B+L) beta_w partial_xi phi/v` (Eqs. 15–17, p8).
The short prose after Eq. 14 drops the coefficient; Eq. A3 retains it and is
the unambiguous normalization used here.

The wall background and Higgs adiabatic approximation have conditions. Eqs.
3–6 (pp4–5) require sufficiently small portal backreaction while changing the
Higgs mass enough to separate the phases. A resulting scale condition is
`m_phi^2 v^2 >> v_ew^2 mu_H^2`. In the regime discussed, a scalar wall wider
than the Higgs response scale lets the Higgs track its local minimum (Eq. 7).
Figure 1 compares coupled two-field profiles to that approximation, with
visible degradation as backreaction becomes larger. These conditions must
be tested in a chosen model; the word “wall” alone supplies none of them.

## Finite rates, susceptibility, and validity

The paper evolves a plasma element with the finite relaxation equation
`dn_(B+L)/dt=-Gamma_sph(t)[n_(B+L)-n_(B+L)^eq(t)]` (Eq. 24, p9).
The equilibrium density is linear in the local source and susceptibility
(Eq. 18). Its rate model uses a symmetric-phase rate and an exponential
suppression set by the Higgs-dependent sphaleron energy (Eqs. 19–23, pp8–9),
giving an illustrative symmetric-phase relaxation scale of about `10^-6 T`.
It neglects diffusion and wall-induced plasma bulk motion in this evolution.
It is therefore a reduced finite-rate treatment, not a full species-resolved
reaction, diffusion, and hydrodynamic calculation.

Two distinct timescale restrictions matter. The finite-rate response depends
on `Gamma_sph L_w/beta_w`, while `L_w` in the plasma frame scales as
`1/(gamma_w m_phi)` (Eq. 26). Independently, local equilibrium requires
`gamma_w m_phi << T`, and Eq. 18 also requires `|mu_(B+L)| << T` (p10 and
Appendix A, pp26–27). The prose on p10 gives a broad saturation statement
immediately before stating the microscopic validity bound. A safe comparison
must retain the latter bound; it does not justify extrapolating the reduced
equation to arbitrarily thin or boosted walls. There can be a window
`Gamma_sph << gamma_w m_phi << T` where the schematic yield in Eq. 27 has
reached its plateau while microscopic equilibrium remains applicable, subject
also to the source amplitude and other assumptions. No such window has been
demonstrated for the public clockwork.

The paper explicitly says spectators affect susceptibility (Eq. 18), then
uses `chi_(B+L)=13 T^2/6` as a Standard Model estimate (Eq. 22, p9). This
number equals the unconstrained ideal-gas sum of the squared B+L charges with
their susceptibility weights. This round's separate diagnostic instead fixes
hypercharge neutrality and each `Delta_i=B/3-L_i`, and obtains
`chi_(B+L)=144 T^2/79` under its fully equilibrated symmetric-SM assumptions.
The ratio is `864/1027`, about `0.8413`. The small arithmetic script here
reproduces the unconstrained sum and ratio; it imports the projected result
from that diagnostic and does not independently rederive it.

This is a concrete **ensemble and spectator matching requirement**, not a
conclusion that the paper's yield is wrong. One cannot insert the projected
susceptibility into Eq. 20 while leaving its sphaleron diffusion, anomaly
charge, and relaxation-rate conventions unexplained. Neither symmetric-phase
number establishes a broken-phase response or a yield at 131.7 GeV.
In Eq. 20 the relaxation rate scales inversely with susceptibility, so its
product with the equilibrium density can stay unchanged at fixed kinetic
prefactor. The ratio above alone is not a baryon-yield correction.

## Energy reservoir and surviving sign

Localization reduces the need for a large homogeneous kinetic energy density,
but the paper also tracks substantial energy stored in scalar structures.
Its domain-wall realization uses an axion cosine (Eq. 28, p10), thermal/Higgs
vacuum bias (Eqs. 29–32, pp10–12), and tension `sigma~8 m_phi f_phi^2`
(Eq. 40, p13). Collapse must occur before wall domination under the stated
cosmological conditions. The authors estimate a huge stable axion abundance
after wall collapse (Eq. 42), motivating decay or other energy transfer.
Fermion decays, entropy dilution, and reheating below sphaleron reactivation
are part of their scenario (Eqs. 43–49, pp14–15). These are an identified
reservoir and disposal route, with approximate cosmological accounting;
they are not an independently evolved energy-conserving solution for this
research program.

The shock-wave realization instead invokes scalar potential energy and
potential hilltop-to-bottom configurations (Eqs. 54–58, p18). Its origin can
be low-scale inflation or other dynamics; the paper does not solve the full
generation and reheating problem. It imposes both the reheating temperature
and the **maximum** temperature during reheating below the sphaleron scale,
since a low final temperature alone would not ensure preservation. Late
reheating dilutes the baryon yield (Eq. 59, p19).

Net sign is not automatic. On p14 the authors explain that an ordinary
string-attached wall network can produce statistically equal increasing-phi
and decreasing-phi passages; opposite baryon signs then cancel. Their domain
wall branch needs a preferred collapse direction and walls without the
described string winding. The Higgs bias selects the expanding phase, but
the sign of the anomalous coupling, profile orientation, and initial
population still matter. The numerical illustration chooses `c_(B+L)=-1`
(p10, Fig. 2). This is not a derivation of the observed sign from the public
clockwork's microscopic parameters.

The domain branch assigns different Higgs behavior to scalar values separated
by an axion period. The portal must therefore distinguish these domains.
The later wall-chain discussion explicitly invokes a periodicity-breaking
portal (Eq. 52 and footnote 5, p17). A port to compact Wilson holonomies must
explain the allowed portal and its global/branch structure; the polynomial
portal cannot simply be appended while retaining all previous periodicity
and gauge assumptions.

## Constraints and useful next work

The domain branch illustrates GeV-scale axions with roughly `10^9–10^10 GeV`
decay constants. Its charm-decay example requires a mass above the charm-pair
threshold and enough reheating to avoid excessive dilution (pp14–16,
Fig. 3); these are scenario-dependent conditions, not universal exclusions.
The authors discuss baryon inhomogeneity and deuterium constraints, which
can remain significant even with an early collapse. Their wall-chain and
subhorizon shock realizations are proposed mitigations (pp15–17, p20).
For shock waves, Fig. 4 overlays supernova constraints and **projected** SHiP
sensitivity. The plots were inspected as illustrations, without independently
checking their external exclusion data or extracting new bounds. The appendix
quotes older ACME limits for its separate conventional EWBG comparator;
that discussion is not a current comprehensive EDM bound review for the
axion operator. Gravitational-wave predictions in Section IV are broad
estimates with entropy dilution and foreground qualifications, not a precise
detectability forecast validated here.

The public v1.23 note already identifies the homogeneous constant-cosine
energy, sign, shutdown, and relic problems. A localized wall is a plausible
**different dynamical branch to investigate**, not a counterexample to its
fixed homogeneous no-driver budget. It adds spatial gradient energy,
Higgs-dependent thermal dynamics, wall formation/topology, decay and entropy
evolution. The v1.23 wall-bias proxies do not establish any of those ingredients.
The new B+L projection supplies a transparent ideal charge response to an
external action; this paper gives a concrete example of the next dynamical
ingredients, without supplying their matching to the clockwork.

The next bounded task would be to register a spatial scalar/Higgs action,
match its allowed anomaly and Higgs couplings, reconcile the susceptibility
ensemble and finite-rate conventions, and test **opposite wall orientations**
as a cancellation control. Any subsequent yield calculation must evolve
wall/field energy, washout, and maximum reheating temperature together with
the charge response. This review changes the research agenda and identifies
controls; it does not establish a viable extension, a new law, or a Nobel-level
result.

## Reproduction and scope

Run `python compare_susceptibilities.py` in this folder to regenerate
`SUSCEPTIBILITY_COMPARISON.json` byte for byte. `PDF_RECEIPT.json` pins the
reviewed source and extraction. `BIBLIOGRAPHIC_METADATA.json` and
`METADATA_RECEIPTS.json` record the selected public bibliographic information
and live-source retrievals. `COMPARISON_RECEIPT.json` pins the public v1.23
note and the newly authored operator diagnostic used for comparison.
Independent reviewers can inspect the source at the version-pinned arXiv URL;
selected equations were visually checked on printed pp7–10, 14, 18 and 26.
The published journal text, numerical wall curves, external constraints,
and wider cited literature have not been independently reproduced or fully
reviewed in this bounded task.
