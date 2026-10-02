# B+L source and ideal Standard Model charge comparator

Prepared 2 October 2026 UTC with AI assistance. This is a conditional analytic
comparator, not a completed Wilson-line particle model, a physical baryon-yield
prediction, an experimental result or external peer review. Its inputs and
derivation use public material and conventional Standard Model charges.

## Public source boundary

The public v1.23 generator, `research/AM1231/v1.23/
v1.23_wilson_instanton_cosmology_audit.py`, states a derivative B+L operator
localized at site 0 and the map `τ1=θ0/(2π)` at lines 1155–1167. Its
phenomenological response is

`Y_B = c_sph κ_dyn D_d (2π n_det dot(τ1)/T)`.

A concrete EFT comparator realizing the stipulated chemical shift can be
**assumed**, freshly and explicitly, as

`L_bias = I_F (∂μ a/f_a) J_(B+L)^μ`,

`I_F=D_d`, `a/f_a=2π n_det τ1`,

so `μ_+=D_d 2π n_det dot(τ1)` for a homogeneous background. These are
additional EFT assumptions that reproduce the public scaffold's convention;
they are not a derived Wilson-line coupling. Here `D_d` denotes the real
hierarchy coefficient in the phenomenological relation. The cited local public
v1.23 source does not specify its microscopic Yukawa definition, which is not
needed for the charge projection below. A CP-even hierarchy magnitude alone
does not establish a physical CP-odd invariant or explain the sign of rolling.

Public generator lines 797–811 and 835–850 state that the standalone Wilson
alternative does not inherit the older scalar messenger/anomaly sector and
leave drive, nonlinear anomalies, and the full CP invariant/transport open.
Candidate `research/AM1232_CANDIDATE_20261001/NEXT_TESTS.md` leaves the same
physical matching tasks open. No action-derived source coefficient,
Wilson-specific matter charges, CP-sign selection or autonomous reservoir
is supplied by this comparator.

## Frozen numerical and energy inputs

Generator lines 45–69 specify `q=3`, `N=30`, `Λ=185 GeV`,
`c_X=0.5294026257283574`, `f_site=250 GeV`, `K_B=1.020689`,
`c_sph=0.0195`, `n_det=16`, `T*=131.7 GeV` and `g*=106.75`.
The physical potential coefficient is

`A=c_X Λ⁴ = 620116096.5235525 GeV⁴`.

The much smaller `A/3³⁰=3.011864038119e−6 GeV⁴` is a projected force
normalization, not available source energy; generator lines 282–299.
The diagnostic cosine has `F_eff=3³⁰·250 GeV` and maximum ideal drop `2A`.
The generator's `ETA` at line 58 is unrelated to the v1.23.1 response
efficiency variable.

The frozen v1.23.1 frontier script lines 21–28, 55–69 uses
`u_req=K_B/(2π c_sph n_det)` and the stipulated
`ρ_kin=(2π f_site T* u_req)²/2`. The efficiency extrapolation is conditional
on the same assumed response. These calculations specify an energy gate,
not a value of physical response efficiency or an achieved abundance.
The preserved public release is not changed by the new ideal-plasma comparator.

## Fresh charge derivation

Assume three generations of relativistic Standard Model fermions, one complex
Higgs doublet, fast Yukawa/gauge interactions and zero initial hypercharge and
B−L. This is an ideal unbroken-plasma approximation. The charge and susceptibility
table follows from `n_i−n̄_i=g_i μ_i T²/6` for fermions and `g_i μ_i T²/3`
for complex bosons, as leading zero-chemical-potential susceptibilities in the
relativistic limit. A physical Higgs Bose distribution requires a positive
thermal mass and `abs(μ_H)<m_H(T)`; the linear approximation also requires
`abs(μ_i)/T≪1` and a controlled expansion about zero chemical potentials.
The table's formal relativistic Higgs coefficient does not establish these
conditions for a finite source or compute thermal-mass corrections.

| Species | Aggregate `g` | B | L | Y | `χ_i/T²` |
|---|---:|---:|---:|---:|---:|
| q_L | 18 | 1/3 | 0 | 1/6 | 3 |
| u_R | 9 | 1/3 | 0 | 2/3 | 3/2 |
| d_R | 9 | 1/3 | 0 | −1/3 | 3/2 |
| ℓ_L | 6 | 0 | 1 | −1/2 | 1 |
| e_R | 3 | 0 | 1 | −1 | 1/2 |
| H | 2 bosons | 0 | 0 | 1/2 | 2/3 |

Let `C=χ/T²`, `d=B+L` and `Q=(B−L,Y)`. The stationary charge projection,
for compatible bias and active reactions that equilibrate all other modes, is

`x_eq = [C−C Q(Qᵀ C Q)^(-1)Qᵀ C]d (μ_+/T)`, `x=n/T³`.

Equivalently `μ_i=d_i μ_+ +(B−L)_i μ_- +Y_i μ_Y` gives the constraints

`11 μ_Y +8 μ_- −4 μ_+ =0`,

`8 μ_Y +13 μ_- −5 μ_+ =0`.

Therefore `μ_Y/μ_+=12/79`, `μ_-/μ_+=23/79` and, in table order,

`μ_i/μ_+=(36,42,30,50,44,6)/79`,

`n_i/(μ_+ T²)=(108,63,45,50,22,4)/79`.

The baryon charge contraction yields `n_B/(μ_+ T²)=72/79`. Dividing by
`s=(2π²/45)g_*s T³` gives

`c_ideal=[45/(2π² g_*s)](72/79)=0.019463471081799685`

for the comparator assumption `g_*s=106.75`. Entropy degrees of freedom
`g_*s` are distinct from the energy-density `g*` in the archived energy
calculation; their equality is assumed only in this ideal relativistic plasma.
The frozen `0.0195` exceeds this ideal expression by `0.18767936123416096%`
and is numerically consistent with rounding it to four decimal places. This
comparison does not establish the historical derivation of the archived input.
The new ideal expression and the frozen benchmark should be identified separately.

This coefficient is a susceptibility divided by entropy, not a diffusion
rate or a calculated susceptibility across the electroweak crossover. Broken
symmetry, thermal masses, interaction corrections, additional light species
and the pattern of spectator equilibration require a new calculation.
The ideal unbroken-plasma approximation is not a validated description of
the broken-regime plasma at the archived `T*=131.7 GeV` benchmark. The actual
finite reaction rates and thermal history must establish whether any
stationary response is attained; this algebra does not establish that history.
Flavor-resolved charges `B/3−L_α` can be tracked instead of aggregate B−L;
for equal generation-independent bias and zero initial flavor charges they
recover the aggregate ideal result. Arbitrary flavor sources require that
reduction to be checked.

## Electroweak anomaly and conserved-current controls

In left-handed Weyl convention, right-handed particles contribute as charge
conjugates to anomaly traces. With `T(2)=1/2`, the per-generation SU(2)
B+L trace is `3(1/3)(1/2)+(1)(1/2)=1`. The three-generation trace is 3.
In normalization `g² Wᵃ_μν W̃ᵃμν/(32π²)`, the anomaly coefficient is 6.
Sphaleron transitions change `B+L` by `6 ∆N_CS`.

The per-generation hypercharge trace is

`6(1/3)(1/6)²−3(1/3)(2/3)²−3(1/3)(1/3)²
 +2(1)(1/2)²−(1)(1)²=−1`.

In the matching `g'² B_μν B̃μν/(32π²)` normalization its coefficient is
−6 across three generations. The SU(2) and U(1) terms have opposite relative
signs; an overall anomaly sign depends on chirality and epsilon conventions.
No dynamical hypermagnetic sector is assumed in the ideal comparator.

B−L has zero SU(2) and hypercharge mixed-gauge traces. It is conserved by
the stated minimal renormalizable SM Yukawa and sphaleron reaction network.
Without right-handed neutrinos, its mixed-gravitational trace is −1 per
generation; the statement here is about the chosen plasma reaction network,
not all possible curved-space effects. Majorana masses or Weinberg operators
also break lepton number and require additional reaction columns.

For a constant-coefficient coupling `∂μ θ J_Q^μ`, integration by parts
gives `−θ ∂μ J_Q^μ` and a boundary term. If the total current is exactly
conserved, a pure gradient cannot create a new charge population in a fixed
initial charge sector. For stoichiometry S with `Sᵀ Q=0`, the reaction bias
from a species shift d is `ζ=Sᵀ d`; adding a conserved direction `Qα`
changes no bias. The susceptibility projector above annihilates Q exactly.
Consequently `d=B−L` and `d=Y` provide zero-response controls.

B+L is different because active sphalerons satisfy `dᵀ v_sph=6` and its
SU(2) anomaly is nonzero. After all B+L-changing reactions shut down,
its charge is also conserved by the remaining network. An imposed bias
cannot then create a new population from zero initial density; the previous
density instead retains its conserved-charge memory. A stationary formula
must not be applied after its required active reactions have disappeared.

Externally set grand-canonical chemical potentials and charge-exchanging
reservoirs change the ensemble and must be modeled explicitly. If an operator
has a field-dependent coefficient involving independent fields, its one-form
need not be an exact gradient; its action and reaction bias require separate
matching. This comparator supplies neither that extension nor a physical
CP-odd invariant, finite sphaleron rates, reservoir or cosmological yield.
