# Independent symmetric-phase SM source response

This calculation recovers the known Standard Model equilibrium conversion and
derives the linear response to a specified external derivative source. It does
not establish a new baryogenesis operator or a cosmological mechanism. The
primary exact calculation was completed without reading the parallel producer's
code or numerical outputs; 24 registered controls pass.

## Species, reactions, and conserved charges

The ordered 16-species vector is

`(q1,u1,d1,l1,e1,q2,u2,d2,l2,e2,q3,u3,d3,l3,e3,H)`.

Fast gauge interactions equate chemical potentials within each gauge multiplet.
The particles labeled `u,d,e` are physical right-handed fermions. The Higgs is
the complex doublet with hypercharge +1/2. Let `chi = (T^2/6) W`.

| Species | Multiplicity g | W entry | Y | B | L_j | Delta_j = B/3 - L_j |
|---|---:|---:|---:|---:|---:|---:|
| q_i | 6 | 6 | 1/6 | 1/3 | 0 | 1/9 |
| u_i | 3 | 3 | 2/3 | 1/3 | 0 | 1/9 |
| d_i | 3 | 3 | -1/3 | 1/3 | 0 | 1/9 |
| l_i | 2 | 2 | -1/2 | 0 | delta_ij | -delta_ij |
| e_i | 1 | 1 | -1 | 0 | delta_ij | -delta_ij |
| H | 2 | 4 | 1/2 | 0 | 0 | 0 |

The Higgs weight is 4 because a complex boson has susceptibility `g T^2/3`;
the Weyl-fermion susceptibility is `g T^2/6`. Both formulas already describe
particle-minus-antiparticle number at small chemical potential: no additional
particle/antiparticle factor is inserted.

The full reaction matrix has the following 13 rows; unlisted entries are zero.
For each generation i there are three Yukawa rows:

- `q_i + H - u_i`;
- `q_i - H - d_i`;
- `l_i - H - e_i`.

The electroweak-sphaleron row is `sum_i(3 q_i + l_i)`. Two quark-flavor-mixing
rows are `q1-q2` and `q2-q3`. The final strong-sphaleron row is
`sum_i(2 q_i-u_i-d_i)` and is redundant after the Yukawa rows.

The matrix `R` has exact rank 12. Its four-dimensional kernel is spanned by

\[
C=(Y,\Delta_1,\Delta_2,\Delta_3),\qquad RC=0.
\]

The complete explicit matrices, including every row, column, and susceptibility,
are in `matrices.json`. The three independent Delta charges cannot generally
be replaced by a single B-L charge: charged-lepton Yukawa equilibrium does not
equilibrate lepton flavors. We preserve each initial Delta charge. The total
baryon response below depends only on their sum in this ideal regime.
Hypercharge is a gauged charge and its homogeneous density is fixed to zero.

If quark flavor mixing were removed, further flavor charges would need to be
fixed. If neutrino-mass or other lepton-flavor-violating interactions entered
equilibrium, the conserved-charge basis would change.

## External source and the constrained free energy

Specify the interaction sign as

\[
\mathcal L_{\mathrm{bias}}=\partial_\mu\theta\,\sum_a c_a J_a^\mu,
\qquad s_a=\dot\theta c_a.
\]

For a homogeneous external background this lowers the single-particle energy
of species a by `s_a`, and the leading plasma free energy is

\[
F(n)=\frac12 n^T\chi^{-1}n-s^Tn.
\]

The kinetic chemical potential is `mu = chi^{-1} n`. Reaction equilibrium is

\[
R(\mu-s)=0,
\]

with fixed `C^T n = d`, where `d = (0,n_Delta1,n_Delta2,n_Delta3)`.
This gives

\[
\mu=s+C\lambda,\qquad
\lambda=(C^T\chi C)^{-1}(d-C^T\chi s),
\]

\[
n=\chi C(C^T\chi C)^{-1}d+P_\chi s,
\qquad
P_\chi=\chi-\chi C(C^T\chi C)^{-1}C^T\chi.
\]

`P_chi` is symmetric, annihilates every conserved-charge direction, and is
positive semidefinite: write it as `chi^(1/2) (I-Pi) chi^(1/2)`, where Pi is the
orthogonal projector onto the columns of `chi^(1/2) C`.

Two source vectors differing by `C v` give identical densities at fixed d.
Thus the physical external-source class is defined modulo the complete
conserved-charge space. The corresponding multipliers shift by `-v`.

## Closed-form baryon response

For `s = kappa (B+L)`, every Yukawa and mixing row has zero source contraction;
the electroweak-sphaleron contraction is `R_EW s = 6 kappa`.
Write `Q = sum_i mu_qi`, `ell = sum_i mu_li`, and `h = mu_H`. Then

\[
\mu_{u_i}=\mu_{q_i}+h,\quad
\mu_{d_i}=\mu_{q_i}-h,\quad
\mu_{e_i}=\mu_{l_i}-h,
\]

\[
3Q+\ell=6\kappa,\qquad
2Q-2\ell+14h=0.
\]

Define normalized densities `hat(n) = 6 n/T^2` and
`D = hat(n_B-n_L)`. Counting the species gives

\[
\hat n_B=4Q,\qquad \hat n_L=3\ell-3h,
\qquad D=4Q-3\ell+3h.
\]

Consequently

\[
Q=\frac{7D+108\kappa}{79},\qquad
\hat n_B=\frac{28}{79}D+\frac{432}{79}\kappa,
\]

or in physical density units,

\[
\boxed{n_B=\frac{28}{79}(n_B-n_L)+\frac{72}{79}T^2\kappa}
\quad\text{for an external }+\kappa J_{B+L}^0.
\]

The first term is a pre-existing conserved-charge contribution; setting kappa
to zero recovers the usual `28/79` conversion. At zero initial Delta_i the
potential vector for a unit B+L source is, in each generation,

\[
(\mu_q,\mu_u,\mu_d,\mu_l,\mu_e)
  =\frac{\kappa}{79}(36,42,30,50,44),\qquad
\mu_H=\frac{6\kappa}{79}.
\]

Therefore `max_a |mu_a|/|kappa| = 50/79`. Linear susceptibilities require these
chemical potentials small compared with T.

Since `B-L` is conserved here,

\[
B=L+(B-L),\qquad B+L=2L+(B-L).
\]

At zero fixed Delta_i a source along B or L gives
`n_B = (36/79) T^2 kappa`, whereas a pure B-L source gives zero response.
For nonzero fixed Delta_i a B-L source still does not change their equilibrium
densities. It can shift grand-canonical charge potentials if charges are left
unfixed, but that is a different ensemble and does not generate conserved
charge in a closed initially neutral plasma.

The matrix controls also show that no B+L response survives if sphalerons are
removed and B and each lepton number are fixed. This is an equilibrium source
response, not a departure from charge conservation.

## Anomaly convention and the pure B-L qualification

For anomaly traces every fermion must be represented as a left-handed Weyl
field. Hence the physical right-handed `u,d,e` become `u^c,d^c,e^c` with
opposite global and hypercharge assignments. Per generation,

\[
A_{B,WW}=A_{L,WW}=+\frac12,\qquad
A_{B,YY}=A_{L,YY}=-\frac12.
\]

The weak hypercharge trace and the cubic hypercharge anomaly cancel. B-L has
zero mixed weak and hypercharge traces. Define
`q_W = g^2 W^a_mu nu Wtilde^(a mu nu)/(32 pi^2)` and positive topological
orientation `Delta N_CS = integral q_W`. The weak contribution then satisfies

\[
\partial_\mu J_{B+L}^\mu=6q_W,\qquad
\Delta(B+L)=6\Delta N_{CS},
\]

and integration by parts gives

\[
\partial_\mu\theta J_{B+L}^\mu=-6\theta q_W+\text{boundary}
\]

for the weak part. The hypercharge-anomaly contribution is also present in a
complete operator statement; no primordial hypermagnetic field dynamics are
included in this plasma reaction network. Changing the definition of positive
topological orientation reverses both signs together. The anomaly relation
does not determine the magnitude of a Wilson coefficient or its ultraviolet
origin.

Without right-handed neutrinos, B-L is not free of the mixed gravitational
anomaly (the left-handed B-L charge trace is -1 per generation); it also has
a cubic global B-L anomaly. Therefore this calculation claims conservation
only in the selected flat-plasma SM reaction network. A homogeneous isotropic
FRW background has zero gravitational Pontryagin density and does not activate
that mixed gravitational anomaly by itself. Gravitational-wave helicity or
other extensions would require a different analysis.

## Conditional source normalization

Use a site phase `theta_0 = 2 pi tau_1`. A possible trial EFT source, motivated
by the public frozen linear yield ansatz, is

\[
\mathcal L_{\mathrm{bias}}=c_0\partial_\mu\theta_0 J_{B+L}^\mu,
\qquad c_0=n_{\mathrm{det}}D_d.
\]

This is a fresh conditional coefficient choice, not a derived Wilson
coefficient. It would give the relevant source

\[
\frac{\kappa}{T}=D_d\,2\pi n_{\mathrm{det}}
\frac{\dot\tau_1}{T},
\]

and the ideal entropy-normalized response is

\[
Y_B=\frac{n_B}{s}
=\frac{1620}{79\pi^2 g_{*s}}\frac{\kappa}{T}
\quad\text{at zero initial conserved charges}.
\]

For a separate ideal entropy assumption `g_*s = 106.75`, this coefficient is
`0.01946347108179968455`. This closely matches the frozen `c_sph = 0.0195`
coefficient and gives a possible conditional normalization. It does not prove
that `c_0 = n_det D_d` is the physical Wilson coefficient: an anomaly trace, a
statistical suppression factor, and a scalar coupling coefficient are
different inputs.

If instead `c_0 = n_det`, the source is unsuppressed. For the public frozen
relation `u_0 = K_B/(2 pi c_sph n_0)`, the nominal external source becomes
`kappa/T = K_B/c_sph`, about 52 for the old inputs; the largest kinetic
chemical potential would be about 33 T. The small-chemical-potential
approximation would then be inapplicable. Choosing `c_0 = n_det D_d` gives
`kappa/T = 52.3430256410 D_d`. D_d's public numeric value and physical
derivation have not been supplied to this independent worker; they must be
specified before testing the actual small-source regime. Inferring D_d from
the observed yield and then reinserting it would be a normalization fit,
not an independent prediction. The alternative coefficient `c_0 = 1` gives
a different site-current operator and cannot be used interchangeably with
these two coefficient choices.

## Self-consistent physics and the regime boundary

A prescribed external theta(t) can do work on the plasma. A dynamical scalar
must obey its own equation with current backreaction, scalar kinetic and
potential energies, total conserved charges, and initial conditions. Varying
`(partial theta) J` gives a current-divergence term in the scalar equation;
the scalar conjugate momentum is also shifted by the charge coupling.
One cannot choose kappa independently while simultaneously treating this
scalar as an isolated finite-energy reservoir. A conserved-current derivative
coupling can be a boundary term under exact conservation, but the anomalous
B+L coupling has dynamical content through the nonconserved current. Establishing
a physical source still needs the candidate operator, coefficient, CP/CPT
properties of the background and action, initial conditions, and a transport
history.

Sphaleron equilibration plus a persistent external source supports a biased
thermal charge. A surviving baryon asymmetry requires a source history and
washout/freezeout calculation. Switching the source off while sphalerons remain
equilibrated drives the source-induced B+L charge back toward zero.

The quoted sphaleron freezeout temperature near `131.7 +/- 2.3 GeV` comes from
the broken electroweak phase, e.g. D'Onofrio, Rummukainen, and Tranberg,
*Phys. Rev. Lett.* **113**, 141602 (2014), arXiv:1404.3565,
doi:10.1103/PhysRevLett.113.141602. The unbroken, relativistic susceptibility
weights in this derivation cannot be substituted as an actual correction at
that temperature. Broken-phase gauge-charge neutrality, Higgs expectation,
masses, finite-temperature susceptibilities, and finite sphaleron rates need
their own treatment. High-temperature entropy degrees of freedom must also
be checked rather than inherited uncritically.

The Higgs bosonic susceptibility is a formal leading linear response around
zero chemical potential. A physical thermal plasma needs a positive Higgs
thermal mass and `|mu_H| < m_H(T)` to avoid Bose condensation; `|mu_H| << T`
alone does not guarantee this. This calculation does not posit finite
chemical potential for a strictly massless equilibrium boson. The quoted
Standard Model freezeout estimate also assumes its stated expansion history;
it cannot be transferred directly to a cosmology with a substantial new
scalar or reservoir energy density.

## Bounded rounding sensitivity

The separate `conditional_normalization_sensitivity.py` reads only literals
from the historical public v1.23.1 script, without executing it. It holds all
other inherited assumptions fixed and explores replacing the rounded 0.0195
by the ideal coefficient above. This is a post-primary sensitivity extension,
not a finite-temperature correction.

The ideal/legacy response ratio is `0.9981267221435735667`, a decrease of about
0.18733%. Because required phase speed scales as the inverse response, the
historical one-A threshold `16 sqrt(9.35462209607388)` shifts from
`48.93652272684394` to `49.02836648010788`. The required relative efficiency
at n=49 shifts from `0.998704545445795` to `1.000578907757304`. Holding the
relative efficiency at 1, the conditional minimum integer therefore changes
from 49 to 50. The independently recomputed kinetic-energy ratios are
`rho_kin/A = 1.001158150648799` at 49 and `0.961512287883107` at 50.

This demonstrates how a tight integer threshold can depend on a coefficient's
rounding precision. It does not establish the correct physical coefficient
at the old broken-phase temperature, or validate the assumed source operator.
The complete separate sensitivity receipt records all seven passing checks,
historical source hash, and the corrected interpretation of eta.

## Reproduction and receipts

From this `independent` directory, run:

```sh
python sm_charge_response.py
python conditional_normalization_sensitivity.py
python compare_frozen_producer.py
```

When this directory is outside the public checkout, set
`ANTIMATTER_PUBLIC_REPO=/path/to/checkout` for the sensitivity command.

Python 3 and SymPy suffice; no dependencies or lockfiles were changed. The
primary `receipt.json` records 24 passing exact controls and hashes of controls,
code, and matrices. `sensitivity_receipt.json` separately records the seven
post-primary checks and the hash of the unchanged historical input.
`comparison_receipt.json` records 11 passing exact matrix comparisons with
the completed 10-species producer, including strict rational schemas, the
species-collapse map, and both outputs' hashes. This final comparison
intentionally reads the completed producer output; it is separate from the
independent primary derivation. The producer reported receiving the coefficient
after its code was frozen but before its first execution, so the computation
phase was not fully blinded. `provenance_note.json` records the primary first
hashes before the non-test source annotation was clarified in public site-phase
terminology. No GitHub or Zenodo publication was performed by this independent
worker.

## Post-run portability amendment

The sensitivity script now resolves its historical input through the task-specific
`ANTIMATTER_PUBLIC_REPO` environment variable, or by discovering a checkout
ancestor of the script or current directory. In both cases it verifies the
frozen public source SHA-256 before reading literals. Its receipt records the
repository-relative source path, so replay does not require the original
checkout location. For a script outside that checkout, run with
`ANTIMATTER_PUBLIC_REPO=/path/to/checkout`.

Declared analysis dependencies are SymPy 1.14.0 and mpmath 1.3.0. This amendment
changes context handling and metadata only. `portability_provenance.json`
preserves hashes of the pre-amendment sensitivity script, receipt, and original
provenance note, plus the original numeric values. The primary solver,
registered controls, primary receipt, and matrices are unchanged. Seven
sensitivity checks and the eleven producer comparisons are replayed after
the amendment; portability is also tested against a separate temporary
checkout context. This amendment adds no finite-temperature physics or new
source assumptions.

`portability_replay.py` records 13 passing checks, including identical
receipts across explicit-environment, script-ancestor, and current-directory
ancestor contexts, unchanged numeric values and primary hashes, and rejection
of missing or altered historical inputs.
