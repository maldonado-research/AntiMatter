# AntiMatter: bounded primary-literature review

Prepared 1 October 2026, Pacific; retrieved 2 October 2026 UTC. This is a literature addendum to the public v1.23 baseline and v1.23.2 candidate diagnostics, not a new model, discovery claim, or external peer review. Five open arXiv papers received targeted full-text review, including the September 2026 flavor comparator. Five bounded INSPIRE searches covered recent 2024–2026 material; search results and abstracts were used only to identify further reading.

The literature supports the candidate's decision to withhold a baryogenesis claim. It supplies concrete requirements for operator matching, transport, energy accounting and ultraviolet completion. None of the papers derives the candidate's charge assignments, kinetic coefficients, autonomous source, or final baryon yield.

## Verified sources and access depth

| Reference | Verified bibliographic identity | Material inspected |
|---|---|---|
| [1404.3565v1](https://arxiv.org/abs/1404.3565v1) | Michela D'Onofrio, Kari Rummukainen and Anders Tranberg, **The Sphaleron Rate in the Minimal Standard Model** (2014); DOI [10.1103/PhysRevLett.113.141602](https://doi.org/10.1103/PhysRevLett.113.141602). | Full PDF, especially Eqs. (3), (7)–(9) and the freeze-out discussion. |
| [1605.00670v2](https://arxiv.org/abs/1605.00670v2) | Andrea De Simone and Takeshi Kobayashi, **Cosmological Aspects of Spontaneous Baryogenesis** (2016); DOI [10.1088/1475-7516/2016/08/052](https://doi.org/10.1088/1475-7516/2016/08/052). | Full PDF, targeted Sections 2–5 and Appendix A. This is the exact title associated with this ID. |
| [2504.03506v2](https://arxiv.org/abs/2504.03506v2) | Mateusz Duch, Alessandro Strumia and Arsenii Titov, **Baryogenesis from cosmological CP breaking**; submitted 4 April 2025, revised 2 October 2025. | Full PDF, targeted Sections 2, 3.1–3.4, 4 and 4.1. Existing CSV title and identifier are correct. |
| [2606.02728v1](https://arxiv.org/abs/2606.02728v1) | Shihwen Hor, Yuichiro Nakai, Motoo Suzuki and Junxuan Xu, **Deconstructing the Extra-Dimensional Axion**, 1 June 2026. | Full PDF, targeted introduction, Section 3.1, Sections 5.1–5.2 and conclusions. Existing CSV title and identifier are correct. |
| [2609.05605v1](https://arxiv.org/abs/2609.05605v1) | Martin A. Mojahed and Alfredo Stanzione, **Minimal spontaneous baryogenesis from flavor**, 4 September 2026. | Full PDF, targeted Sections 2.1–2.3, 3–3.2 and 4–4.1, Tables 1–2 and the stated Appendix A consistency requirements. |
| [2604.08700](https://arxiv.org/abs/2604.08700) | **Axion Quality in Warped Extra-Dimension**; submitted 9 April 2026, revised 28 May 2026 (v2). | Authoritative arXiv landing metadata and abstract only. The existing CSV's “Axion Quality in Warped Extra Dimensions” is a title mismatch; the identifier is correct. No full-text result from this paper is used below. |

Bibliographic verification establishes publication identity; model validity requires its own checks.

## September 2026 flavor comparator: what it establishes and what it leaves open

[Mojahed and Stanzione, 2609.05605v1](https://arxiv.org/abs/2609.05605v1) already give an explicit link between flavor hierarchies and spontaneous baryogenesis. Their mechanism is substantially more specified than an empirical Yukawa-product relation: a **global** horizontal U(1) symmetry, a charged flavon, heavy vector-like messengers and charge-selected powers of the flavon generate the Yukawas, Eqs. (2.1)–(2.4). A field redefinition yields a derivative coupling to the full generation-dependent flavor current, Eqs. (2.6)–(2.9). The dimension-five Weinberg operator supplies B−L violation, with its heavy mediators assumed non-dynamical throughout the relevant thermal history.

Their driving is ordinary initial misalignment in an approximately quadratic, temperature-independent potential during radiation domination: Eqs. (2.11)–(2.17). The initial angle is a free parameter selected by the assumed inflationary history. This is not a derived moving-minimum driver or an unlimited work reservoir. They neglect plasma backreaction under stated smallness assumptions (footnote 5). Their standard-misalignment benchmark result requires oscillation temperatures roughly above \(4\times10^{11}\) GeV and flavon scales roughly \(7\times10^{13}\)–\(2\times10^{17}\) GeV (Section 4.1). It does not establish a 131.7 GeV realization; lower scales are discussed as extensions requiring changed physics.

The most useful concrete comparison is that **the flavor hierarchy does not uniquely fix the source**. Tables 1–2 give two charge assignments compatible with the charged-fermion flavor textures; universal shifts preserve the charged-fermion charge differences but change the weak anomaly coefficient from 16 to 22, while the strong coefficient remains 23. Transport sources depend on the complete charge vectors and anomalies, Eqs. (3.1)–(3.3), not merely a determinant power. The occurrence of 16 in their first weak-anomaly benchmark does not identify it with the candidate's \(n_{\rm det}=16\). That would require an explicit operator and anomaly match. No such match is performed in this review.

The paper supplies explicit coupled equations, Eqs. (3.8)–(3.14), and checks its use of small \(\mu_i/T\), but “complete” is relative to its chosen high-temperature species and reaction set. It explicitly drops sizable off-diagonal lepton coherences, approximates the flavor basis and defers a quantum kinetic treatment around flavor transitions (Section 3, footnotes 7–8). Its late dilution uses an instantaneous-decay approximation; footnote 11 calls for coupled scalar and radiation energy equations for a more refined treatment. These limitations make it a useful comparator and starting reference, not a finished transport solver to transplant into AntiMatter. A future implementation should compare source vectors, reactions, validity ranges and conserved-charge null spaces before comparing yields. This existing flavor–baryogenesis connection also prevents treating that broad conceptual connection itself as a new discovery of the candidate.

## Five concrete consequences for the next model calculation

### 1. Match the physical source and check its approximation before inferring an asymmetry

De Simone and Kobayashi derive the effective chemical potential from a specified derivative-current operator, then expand the fermion density for small chemical potential: Eqs. (2.1), (2.9)–(2.12). Their linear abundance expression, Eq. (2.14), assumes rapid baryon-violating reactions, appropriate thermal distributions, and no additional charge constraints in that simplified derivation. It is not a universal conversion factor for an arbitrary rolling phase.

Duch, Strumia and Titov give a stronger matching prescription: Yukawa phases, derivative-current couplings and anomalous theta angles transform together under field rephasings. The physical source combinations are their Eqs. (19)–(21), derived from the action and transformations in Eqs. (1)–(4). A single phase removable by a field or gauge transformation does not by itself establish a physical CP-breaking parameter; their Sections 2.2–2.3 explain the distinction. A CP-odd cosmological state and its sign-selection history also have to be specified.

For the public frozen relation

\[
Y_B=c_{\rm sph}\kappa_{\rm dyn}(2\pi n\dot\tau_1/T)D_d,
\]

the quoted target implies \(2\pi n|\dot\tau_1|/T\simeq52.34\) at unit response efficiency. **Only if this entire unsuppressed combination were identified as a physical \(|\mu|/T\)** would it violate the small-chemical-potential assumption. The derivative operator and the placement of \(D_d\) within the microscopic source or response are not established, so this is a missing validity check, not a demonstrated exclusion. A small final \(Y_B\) does not on its own establish small individual chemical potentials. Derive the species-dependent sources, conserved-charge constraints and susceptibility matrix before using linear response.

### 2. Compute a signed transport history instead of identifying a speed crossing with baryogenesis

The 2025 paper's species equations, Eqs. (23)–(27), explicitly combine Yukawa reactions, strong and weak sphalerons and lepton-number violation. Section 3.3 shows that setting every reaction term separately to zero can even be inconsistent when the sources are incompatible; the stationary result can depend on reaction rates. Its Eq. (41) is a reduced equation under stated fast-reaction assumptions, not a general replacement for the network.

De Simone and Kobayashi, Section 3 and Eq. (3.1), explain how rapid sign-changing scalar oscillations suppress the simple equilibrium mechanism if reactions cannot follow the source. This is a warning about time scales and cancellation, not a no-go theorem for all nonequilibrium oscillatory models. Integrate the signed source through production and washout, and report the final charge after the source and relevant reactions freeze out. The candidate's pointwise speed and duration diagnostics cannot provide that result.

Ordinary particle–antiparticle pair production contributes zero net baryon charge when the production interaction conserves it. A matter excess requires an explicitly modeled charge-violating process and a physical bias, followed by survival against washout. Choosing the initial rolling sign predicts neither its cosmological selection nor the observed abundance. A useful control is to reverse all CP-odd data and verify the corresponding transformation of the computed asymmetry.

The successful examples in the 2025 paper employ a different setting, including Majorana-neutrino lepton-number violation and typically temperatures around \(10^{11}\) GeV; see Sections 3.5 and 4.1. They do not validate an electroweak-temperature realization of the candidate.

### 3. Recompute sphaleron freeze-out using the actual expansion history

The lattice result in 1404.3565 supplies a thermal Standard Model diffusion rate. Its broken-phase fit, Eq. (7), was fitted over approximately 140–155 GeV and extended by the authors down to approximately 130 GeV after comparison with the perturbative result; the abstract gives the broader 130 GeV to crossover characterization. The logarithm is natural. The familiar \(T_*=(131.7\pm2.3)\) GeV follows from Eq. (9),

\[
\Gamma(T_*)/T_*^3=\alpha H(T_*),\qquad\alpha\simeq0.1015,
\]

using radiation domination and \(g_*=106.75\). The diffusion rate has mass dimension four; it must be converted with the relevant susceptibilities into the charge-relaxation equations. Equating \(\Gamma\) itself to \(H\) is dimensionally wrong.

The candidate's largest-kinetic sample reports total scalar/radiation energy near 0.0296, while the inherited frozen benchmark has a substantially larger kinetic fraction. These facts call for recalculating \(H(T)\), cooling and washout in the completed model. They do not retrospectively invalidate the candidate's explicitly fixed-temperature diagnostic. If the new fields appreciably change electroweak thermodynamics, importing the minimal-Standard-Model rate also needs justification. A finite temperature fit and a freeze-out benchmark are not a computed response efficiency \(\kappa_{\rm dyn}\).

### 4. Close both the driver energy ledger and the late cosmology

De Simone and Kobayashi retain the current backreaction in the scalar equation, Eq. (3.2), and derive the conditions for neglecting it in Section 3.2, Eqs. (3.11)–(3.12). Their radiation-era slow-varying attractor has \(5H\dot\phi\simeq-V'\), Eq. (3.5), rather than the inflationary \(3H\) approximation. These results have explicit assumptions and must be rederived if the candidate's source, metric or bath differs.

Their Sections 4–5 connect the residual scalar energy to domination, entropy dilution, decay and baryon isocurvature. The 2025 paper likewise evolves a reheating reservoir with energy-transfer equations, Eqs. (36)–(40), and tests late scalar decay and isocurvature in Section 4. It still uses an approximate scalar potential and stated simplifications; it is not a completed reservoir calculation for AntiMatter.

An autonomous drive can perform work beyond the source-only \(2A\) budget, but that work must appear as energy lost by a dynamical reservoir. Dissipation must enter the receiving sector. Thermal potentials, field backreaction, decay products, entropy and the Friedmann equation must be evolved consistently. Hubble dilution of an isolated scalar is not automatically deposited as radiation heat. These are requirements for extending the candidate, not new numerical results or modifications of its registered source-only bounds.

### 5. Match the topology, anomalous coupling and ultraviolet completion before importing Wilson-line protection

Hor et al. provide an explicit orbifold deconstruction with charge assignments and a gauged Wess–Zumino–Witten counterpart of the five-dimensional Chern–Simons coupling. Their Sections 3–4 illustrate the construction needed to connect a Wilson mode to a physical anomalous operator. They do not calculate the candidate's 31-holonomy clockwork metric or the coefficient and sign of its chosen \(G=I+cQ^TQ+bee^T\) family. The candidate's exact \(Qw=0\) identity remains a structural result under the assumed metric, not a matched quantum correction.

Two distinctions directly affect the proposed next steps. First, the orbifold model differs from a circle: in the minimal charged-scalar sector, holonomy dependence can be rotated out, and a potential from that charged-scalar sector requires boundary shift-symmetry breaking; see the introduction and Section 5.2. Separate QCD/instanton contributions remain possible. An orbifold prescription used to remove unwanted vector zero modes cannot simply inherit the candidate's circle winding-loop potential without a fresh calculation. Second, Section 5.1.2, Eqs. (5.40)–(5.42), finds suppression of site-localized instantons in the controlled five-dimensional regime, but warns that it can disappear for sufficiently small instantons probing the deconstructed ultraviolet theory. The authors leave a detailed analysis of that region for future work. Their “fractional” instantons are site configurations, explicitly distinguished in footnote 8 from those of a quotient gauge group.

Thus neither nonlocality nor an infrared suppression factor alone closes the charge-lattice and instanton audit. Specify the compact topology, boundary operators, charged spectrum, anomalous coupling and renormalization conditions; then compute the kinetic matrix and all allowed potential terms in that same model. This paper does not repair the original gauged-character obstruction by citation.

## Recent leads with metadata-level evidence only

Five INSPIRE searches, sorted by most recent date and limited to at most 15 hits each, identified the following useful follow-ups. The broad searches were truncated; this is not an exhaustive novelty search.

| Lead | Why it may matter; current limit |
|---|---|
| [2604.20762, Spontaneous baryogenesis from axions on induced electroweak walls](https://inspirehep.net/literature/3148095) and [2604.27376, Electroweak Baryogenesis from Collapsing Domain Walls](https://inspirehep.net/literature/3150589) | Electroweak-temperature comparators, but spatial wall sources differ from homogeneous rolling. Metadata only. |
| [2411.13494, DW-genesis: baryon number from domain wall network collapse](https://inspirehep.net/literature/2850224) | Metadata flags opposite-wall cancellation and the timing of charge-violating decoupling. Relevant if a wall-based branch is proposed. |
| [2504.08868, Spontaneous baryogenesis with large misalignment](https://inspirehep.net/literature/2911626) | Possible comparator for nonlocal fermion backreaction and local-response approximations. Its derivation was not checked. |
| [2512.11011, Spontaneous baryosynthesis with large initial phase](https://inspirehep.net/literature/3092531) and [2512.18516, Comment on “Spontaneous baryosynthesis with large initial phase”](https://inspirehep.net/literature/3094745) | A later comment alleges a technical problem. Read both before relying on that large-angle result; this review does not adjudicate the dispute or extend the criticism to a different paper. |
| [2511.15794, Axiverse Baryogenesis](https://inspirehep.net/literature/3085073) | Metadata identifies kinetic misalignment, axion quality, abundance tension and dissipation. No transfer of that model's conclusions to this candidate is established. |

## Evidence files and scope

- `source_metadata.json`: normalized bibliographic identities, version and review-depth labels, and full-text retrieval receipts.
- `full_text_retrieval_receipts.json`: requested URLs, HTTP results, UTC retrieval times, byte counts and SHA-256 hashes for the five PDFs.
- `initial_retrieval_receipts.json`: arXiv landing-page receipts for the first three full-text sources and the additional September 2026 flavor paper.
- `recent_metadata.json`: authoritative recent-title checks, the exact five INSPIRE query URLs, retained bibliographic results and search limits.

Requests succeeded with HTTP 200 over HTTPS with normal certificate verification. No blocked destination was bypassed. PDFs and extracted paper text remain only under `/tmp/antimatter-papers`; they are not included in this addendum. Saved metadata omits verbatim abstracts. The summaries above are independently written and cite source sections and equations. Preserved release files and registered numerical results remain unchanged. This addendum corrects the warped-paper title without changing the preserved release and follows the registered numerical audits.
