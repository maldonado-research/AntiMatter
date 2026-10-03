# Post-portability scientific consistency review, 2 October 2026

**Pass within the stated ideal-plasma comparator scope.** The charge algebra,
operator sign, mixed-gauge anomaly traces and conditional sensitivity arithmetic
are consistent. This is an AI-assisted review and reproduction of conventional
equilibrium calculations, not external peer review, a new mathematical result,
a verified Wilson-line interaction or a baryogenesis prediction.

The companion `REVIEW_RECEIPT.json` records the current reviewed public file
hashes and 35 passing reviewer checks: the original 33 consistency/reproduction
checks plus two checks replaying the independent portability harness and its
receipt. `review_checks.py` runs seven copied scripts under `reviewer/replay`
and never executes a solver in its original directory. Fourteen regenerated
output files match their originals byte for byte. The producer, independent,
selected public inventory and public historical inputs remain unchanged by
this reviewer. The separate wall-paper comparison below is outside this tally.

The producer and independent workers amended their software context resolution
after the scientific runs. Both support `ANTIMATTER_PUBLIC_REPO`; the independent
historical input is pinned by SHA256 and its receipt uses a repository-relative
path. Original code/results provenance is preserved in their portability
amendment artifacts. Their primary scientific controls and numerical results
are unchanged. This current review replaces pre-portability software hashes;
the earlier review artifacts remain only in the local review history. It is
not a new preregistration.

The independent portability harness separately reports 13 software controls,
including disposable explicit/ancestor/cwd contexts and rejected missing or
wrong-hash contexts. Producer portability evidence reports an isolated replay
of all 84 scientific controls plus two context-rejection controls. These are
distinct from new scientific evidence. The actual analysis environment uses
SymPy 1.14.0 and mpmath 1.3.0; a public dependency file can pin those versions.

To replay after relocating this package, from its parent directory use
`ANTIMATTER_PUBLIC_REPO=/path/to/AntiMatter python reviewer/review_checks.py`.
Only the public inventory allowlist is read or hashed:
`PUBLIC_SAFE_OPERATOR_INVENTORY.md`, `verify_inventory.py`, and
`EXACT_INVENTORY_CHECKS.json`. Private historical inventory identifiers are
excluded from the current reviewer script and receipt.

## Charge and operator checks

For a prescribed homogeneous background the declared interaction

`L_int = c (partial_mu theta0) J_(B+L)^mu`, `kappa = c dot(theta0)`

has the source convention `H_int = -kappa Q_(B+L)`. The plasma objective is
`F_0(n)-kappa q^T n`; its reaction affinity is `R(mu-kappa q)`.
Thus a positive source produces the stated positive baryon response. The
weak-sphaleron row has `Delta B=3`, `Delta L=3`, `Delta(B+L)=6`, so intrinsic
equilibrium affinity is `R_EW mu=6 kappa`, while its effective affinity vanishes.
For a dynamical scalar, canonical momentum and scalar backreaction must instead
be derived from the full action; the prescribed-source Hamiltonian does not
by itself establish autonomous energy accounting.

The density convention uses physical right-handed `u,d,e` particles. Each Weyl
fermion contributes `g T^2/6`; the two-component complex Higgs contributes
`2 T^2/3`. The aggregated ten-species weights are
`(18,9,9,2,2,2,1,1,1,4) T^2/6`, with no extra antiparticle factor.
The sixteen-species calculation uses three separate copies of quark weights
`(6,3,3)`. Both reduce to exactly the same response.

The conserved basis contains **all three** `Delta_i=B/3-L_i` and hypercharge;
charged-lepton Yukawas do not equilibrate these flavor charges. The respective
reaction ranks are 6 on 10 aggregated species and 12 on 16 resolved species,
leaving the same four-dimensional conserved kernel. Weak sphalerons preserve
each Delta_i, and the strong-sphaleron row is redundant after Yukawa constraints.
The exact, susceptibility-weighted projection satisfies the conserved constraints
and minimizes a strictly convex free energy on the allowed charge space.

The hand-reduced flavor-symmetric Gram matrix is
`[[11,8],[8,13]]` in the `(Y,B-L)` basis and weights `T^2/6`.
It independently gives

`mu_Y/kappa=12/79`, `mu_(B-L)/kappa=23/79`,

`(mu_q,mu_u,mu_d,mu_l,mu_e,mu_H)/kappa=(36,42,30,50,44,6)/79`,

and

`n_B=(28/79)(n_B-n_L)+(72/79) T^2 kappa`.

The full flavor-resolved controls verify that the pre-existing-charge term
depends on `sum_i n_Delta_i`, including unequal or opposite flavor asymmetries.
Pure hypercharge and Delta_i sources create no density change at fixed charges.
B and L sources give equal responses and B+L gives twice either source-induced
response, because their difference is conserved. These are fixed-charge ensemble
statements. Leaving B-L unfixed instead defines a charge-exchanging ensemble;
its nonzero B-L response is not closed-system charge production.

## Anomaly and rephasing checks

For anomaly traces the right-handed fields are conjugated to left-handed Weyl
fields, reversing their global and hypercharges. With `T(2)=1/2`, per generation

`A_B,WW=A_L,WW=+1/2`, `A_B,YY=A_L,YY=-1/2`.

With `q_W=g^2 W Wtilde/(32 pi^2)` and
`q_Y=g'^2 B Btilde/(32 pi^2)`, the three-generation mixed-gauge part is

`partial_mu J_(B+L)^mu = 6 q_W - 6 q_Y`.

The **relative** weak/hypercharge signs are opposite. The orientation of
positive topological charge defines the common overall sign. Integration by
parts transfers the constant-coefficient source to
`-6 c theta0 q_W + 6 c theta0 q_Y`, plus boundary and any further anomaly or
explicit-breaking terms. A matter-field rephasing transfers these terms and
interaction phases; deleting them or counting the rephased and original
descriptions as independent source contributions is incorrect.

B-L has zero mixed weak and hypercharge traces in the stated reaction network,
but its mixed-gravitational charge trace is `-1` per generation without
right-handed neutrinos. Its cubic global anomaly also requires qualification
if B-L is gauged. This comparator claims conservation in the selected minimal
SM plasma network, not cancellation of all possible gravitational or extended
model anomalies. A homogeneous isotropic FRW geometry has zero gravitational
Pontryagin density; curved space alone is not evidence for an activated source.

An exactly conserved total current coupled to a constant scalar gradient gives
only a boundary term in a fixed initial charge sector. B+L escapes that control
only while B+L-changing processes are active. Once they shut down, the conserved
space enlarges and the already established density retains charge memory.
It cannot continue tracking an instantaneous equilibrium formula. Conserved
source-shift equivalence also holds beyond linear response: a shift along a
fixed conserved charge changes the free energy only by a constant. The numerical
linear coefficients themselves need not hold beyond their susceptibility regime.

## Conditional coefficient and threshold comparison

The explicit conditional benchmark identification `I_F=D_d` and
`a/f_a=2 pi n_det tau1`, with `tau1=theta0/(2 pi)`, imply
`c=n_det D_d` **only as an additional EFT assumption**. The public Wilson
replacement supplies no UV matching for that coefficient. The comparator does
not import the older scalar/messenger construction into the Wilson branch.
A real CP-even hierarchy magnitude does not derive a CP-odd invariant, a signed
rolling initial condition, or a physical asymmetry.

The separate ideal entropy assumption `g_*s=106.75` gives

`C_ideal=(72/79)/(2 pi^2 g_*s/45)=6480/(33733 pi^2)`

`=0.01946347108179968455`.

The archived `0.0195` is numerically consistent with rounding this expression
to four decimal places. Agreement alone does not establish its historical
derivation. Entropy `g_*s` and radiation-energy `g_*` are distinct quantities;
their equality is an ideal relativistic SM assumption here.

The unchanged public v1.23.1 input freezes
`rho_kin(16)/A=9.35462209607388`. Therefore its one-A threshold is
`16 sqrt(9.35462209607388)=48.93652272684394`, and the original required
relative efficiency at n=49 is `0.9987045454457947`. It is a **required**
efficiency, not an achieved yield ratio.

Holding the target yield, kinetic normalization and all inherited inputs fixed,
required speed scales as `1/C`, so the purely conditional replacement gives

`threshold_new=threshold_old (0.0195/C_ideal)=49.02836648010788`,

`eta_required_new(n=49)=1.000578907757304`.

At unit relative efficiency the arithmetic minimum changes from 49 to 50.
The separate energy inequalities give `rho_kin/A=1.001158150648799` at 49
and `0.961512287883107` at 50. This is a coefficient-normalization sensitivity
comparator. It is **not a correction of a physical yield at 131.7 GeV**, a
calculated efficiency or a successful higher-winding operator construction.
Printed extra digits identify the numerical boundary; they are not a measure
of physical precision.

## Regime limits and literature spotcheck

No unresolved algebraic bug was found. The following qualifications determine
whether the conditional comparator is used correctly:

- Linear response requires all actual occupation chemical potentials to be
  small relative to T. With zero Delta_i the maximum is
  `(50/79)|kappa|/T`. At large fermion chemical potential the massless ideal
  response acquires `mu^3` terms; one cannot extend the linear coefficient by
  rescaling it. For the Higgs normal thermal phase one also needs
  `|mu_H|<m_H(T)` and a controlled expansion about zero chemical potential.
  A strictly massless boson gas at finite nonzero chemical potential is not
  justified by its formal susceptibility at zero.
- Setting the assumed `I_F` to 1 while retaining the inherited target-speed
  normalization gives `kappa/T=K_B/0.0195`, about 52.34, and a formal maximum
  `|mu|/T` about 33.13. This deliberately unsuppressed toy is outside the
  linear domain. Even fixed `c=1` at the inherited phase speed gives a formal
  maximum above T. Neither toy supplies a nonlinear calculation.
- A quasistatic response needs the relevant relaxation rates large compared
  with H and the source-evolution scale. At sphaleron freezeout this condition
  fails by construction. Switching off a source while sphalerons still act
  removes its charge response through relaxation; survival needs a kinetic
  history. Independently driven reaction sources can also be incompatible
  with simultaneous zero affinities, in which case rates determine a driven
  stationary state instead of this thermodynamic minimum.
- The quoted `T_*=131.7 +/- 2.3 GeV` belongs to the minimal SM broken phase
  with radiation-dominated expansion. A new reservoir, substantial extra
  energy density or changed thermal species modifies H and the freezeout
  criterion. Symmetric massless weights, high-temperature entropy, actual
  spectator equilibration and physical near-freezeout susceptibilities need
  separate control.

The cached public fulltexts were spotchecked, with line numbers referring to
the local text extraction, not journal pagination:

| Public source | Checked content |
|---|---|
| [arXiv:2504.03506](https://arxiv.org/abs/2504.03506), lines 148-166, 318-328, 343-366 | Derivative sources move under rephasings into interactions/anomalies; kinetic equilibrium and small mu/T are required; physical reaction-source combinations must be retained. |
| Same source, lines 557-600, 644-655 | Incompatible driven affinities produce a rate-dependent stationary solution; hypercharge neutrality and freezeout/entropy assumptions matter. Its left-handed conjugate convention must be translated before comparing right-handed-particle density vectors. |
| [arXiv:2609.05605](https://arxiv.org/abs/2609.05605), lines 252-289, 363-384, 647-674 | The same anomalous rotation produces derivative/topological terms; an effective bias is distinguished from plasma response and evolved with a reaction network. |
| Same source, lines 690-700, 790-794, 950-965 | Flavor quantum kinetics can be needed and a nonzero source with a negligible reaction rate need not generate an appreciable charge. |
| [arXiv:1404.3565](https://arxiv.org/abs/1404.3565), lines 278-283, 319-337 | Rates can enter Boltzmann equations; the quoted freezeout uses `Gamma/T^3=alpha H`, `alpha~0.1015`, radiation domination and `g_*=106.75`. |

No numerical fit, external peer-review acceptance, newly established source
sector or private raw manuscript is supplied by this review.

## Separate selected-equation review of the wall proposal

The public fulltext of [arXiv:2604.20762](https://arxiv.org/abs/2604.20762)
was checked at Eqs. 12, 14, 17, 18, 20, 22, 24 and Appendix A Eq. A3;
Eq. 13 was also inspected directly in the PDF. This is a literature comparison
with the conditional comparator, separate from its registered computations
and reviewer-check tally. It does not establish a wall/portal sector in the
Wilson-line candidate or transfer the paper's numerical yield into that model.

The source sign is consistent after translating conventions:
`delta L=-c_(B+L) (partial_mu phi/v) j_(B+L)^mu` gives
`mu_external=-c_(B+L) u^mu partial_mu phi/v`. For
`xi=z-beta_w t`, this becomes `+c_(B+L) beta_w phi'(xi)/v`, agreeing
with Eq. 17. Appendix A retains the coefficient that the generic-frame
sentence following Eq. 14 suppresses.

Eq. 22 uses `chi_(B+L)=13 T^2/6`. This equals the **free**, unprojected Weyl
sum `sum_a g_a (B_a+L_a)^2 T^2/6`. That ensemble sets
`mu_a=(B_a+L_a) mu_external` and has cross-susceptibilities
`chi_(Y,B+L)=-2 T^2/3` and `chi_(B-L,B+L)=-5 T^2/6`.
It therefore does not impose the fixed neutral/conserved charges used here.
Our projected `chi_(B+L)=144 T^2/79` has ratio `864/1027` to that free value,
approximately 0.841285. Eq. 18 acknowledges dependence on spectator processes;
the displayed Eq. 22 does not provide the same full constraint derivation as
this packet. This is an ensemble/normalization distinction to resolve before
comparing predictions, not grounds to claim the paper implements our spectators
or that its physical conclusions have been disproved.

Eq. 24 is a linear relaxation equation. For a given kinetic prefactor,
Eq. 20's damping varies as `1/chi`, while the equilibrium source density varies
as `chi`. Thus replacing chi changes both; their drive product remains fixed.
The ratio `864/1027` alone is not a universal correction to its surviving
baryon yield. More generally, if Chern-Simons diffusion is defined as
`Gamma_CS=lim <(Delta N_CS)^2>/(V t)`, detailed balance for charge steps
`Delta(B+L)=2N_g` gives the relaxation coefficient
`(2N_g)^2 Gamma_CS/(2 chi T)`, or `18 Gamma_CS/(chi T)` at N_g=3.
A one-direction event-rate convention instead carries 36 times that event
density. The paper's phenomenological kinetic prefactor must be mapped to
the chosen rate convention before applying either factor.

There is also an unresolved topological normalization difference. Eq. 13
displays `c_(B+L) alpha_2 phi/(8 pi N_g v) W Wtilde`.
With the ordinary quark/lepton B+L current and our component convention
`W^a Wtilde^a`, integration by parts of Eq. 12 instead gives
`c_(B+L) N_g alpha_2 phi/(4 pi v) W^a Wtilde^a` for the weak part.
At N_g=3 the displayed coefficients differ by 18 in that convention.
Gauge-matrix trace and current normalizations need explicit reconciliation;
we flag the mismatch and do not import Eq. 13 as a matched coefficient or
declare a convention-independent paper error. A complete B+L operator identity
also contains the hypercharge anomaly absent from this weak-only comparison.

Finally, the paper explicitly notes cancellation between opposite winding
directions in a string-attached collapsing-wall population (text extraction
lines 660-668). In Eq. 24, with identical damping/initial charges, reversing
the source reverses the solution; equal opposite-source histories therefore
cancel by linearity. A net yield requires a specified directional population
bias or a demonstrated asymmetry in the histories. Spatial localization alone
does not select the baryon sign. Local treatment additionally requires a
microscopically slow wall (`gamma_w m_phi << T`); thin/ultrarelativistic walls,
diffusion and induced plasma flow can require full transport rather than the
displayed density-only equation (lines 371-372, 431-438, Appendix A).

## Independence disclosure and publication boundary

The producer ten-species implementation and original registered controls were
frozen before the independent agent's coefficient message. That message arrived
before the producer's first execution. The code has no hardcoded expected source
coefficient and was not revised to match the message. This establishes agreement
between two independently implemented methods; **execution was not fully
blinded**. The threshold sensitivity is a separately disclosed post-primary
extension whose exploratory eta interpretation was corrected before its final
receipt. It must not be presented as preregistered primary evidence.

The independent primary controls' non-test source annotation was reworded after
the primary run in public site-phase terminology, without changing the reaction
tests or implementation. `independent/provenance_note.json` preserves the first
controls/code/receipt/matrix hashes and the current receipt pins current hashes.
The separate eleven-control post-completion comparison intentionally reads both
completed outputs; it is not independent primary evidence.

For any public package use the newly authored
`inventory/PUBLIC_SAFE_OPERATOR_INVENTORY.md` and public-parent provenance.
The full local historical inventory and private provenance remain local and
are not read or hashed by the current review. `reviewer/replay` and
`reviewer/LOCAL_REVIEW_HISTORY` are local working/preservation directories;
exclude both from publication. Do not publish private source files or raw excerpts. This
review does not publish or authorize a Zenodo release;
its claim scope is a bounded conventional comparator and reproducibility check.
