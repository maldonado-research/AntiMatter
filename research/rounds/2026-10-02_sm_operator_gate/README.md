# Standard Model charge and source matching gate

Ricardo Maldonado · 2 October 2026 UTC · Prepared with AI assistance

This round makes the inherited baryogenesis scaffold more explicit as a
**conditional EFT comparator**. It does not construct the Wilson model's
microscopic interaction, select a cosmological CP sign, supply an autonomous
reservoir or predict the final matter excess. The charge algebra and methods
are conventional; no mathematical or physical novelty is claimed.

For the trial interaction `L_int=c (partial_mu theta0) J_(B+L)^mu`, define
`kappa=c dot(theta0)`. In a relativistic symmetric Standard Model plasma with
one Higgs doublet, equilibrated quark mixing/Yukawas/weak sphalerons, hypercharge
neutrality and all three fixed `Delta_i=B/3-L_i`, the exact linear response is

`n_B = (28/79) n_(B-L) + (72/79) T^2 kappa`.

This recovers the standard pre-existing B-L conversion and separately specifies
the trial external-source response. A source along an exactly conserved charge
creates no new density on this fixed-charge slice. B and L sources are equivalent
modulo B-L; B+L gives twice either response. These controls distinguish charge
production from a chosen grand-canonical reservoir or symmetric pair production.

The coefficient choice `c=n_det D_d` realizes the public scaffold's source
normalization as an additional assumption. It places D_d **inside** the physical
chemical shift: at the inherited unit-efficiency phase speed,
`kappa/T=52.34302564 D_d` and `max_i |mu_i|/T=33.12849724 |D_d|`.
The hierarchy factor remains formal; it is not inferred from the observed yield
to manufacture a prediction. Choosing `c=n_det` instead would give large
chemical potentials at that same imposed speed and invalidate this linear
comparator. Neither choice derives the Wilson coupling. The field still pays
its own kinetic-energy cost; a small chemical shift does not remove that budget.

With ideal entropy `g_*s=106.75`, the response coefficient is
`C_ideal=6480/(33733 pi^2)=0.0194634710818`, numerically consistent with the
archived rounded `0.0195`. Formally substituting it while freezing all other
energy-frontier inputs moves the one-height continuous threshold from
48.93652273 to 49.02836648: its integer minimum becomes 50 and the n=49
required efficiency becomes 1.000578908. The unit-efficiency full-drop and
strict 1% thresholds remain 35 and 119. This is a sensitivity calculation;
**it is not a correction to the physical response near 131.7 GeV**. Broken-phase
susceptibilities, expansion and finite reaction rates must be computed there.

The anomaly audit uses left-handed Weyl traces with stated topological
orientation: `partial_mu J_(B+L)^mu=6 q_W-6 q_Y` for its mixed-gauge terms.
Conservation of B-L here concerns the selected reaction network. Without
right-handed neutrinos its gravitational trace is nonzero; Majorana/Weinberg
reactions or a dynamical hypermagnetic sector would change the problem.

Small fermionic chemical potentials, positive Higgs thermal mass with
`|mu_H|<m_H(T)`, and equilibration faster than background changes are required.
The prescribed source does not itself close the scalar/bath energy budget.
When sphalerons shut down, charge memory replaces this instantaneous formula.

## Evidence and review depth

- [Producer derivation](producer/DERIVATION.md): 10-species Fraction projection,
  48 primary controls and 36 separately registered conditional sensitivity controls.
- [Independent derivation](independent/DERIVATION.md): 16-species symbolic reaction
  and charge matrices, 24 primary controls, seven post-primary sensitivity checks
  and [11 exact cross-comparisons](independent/comparison_receipt.json).
- [Public operator inventory](inventory/PUBLIC_SAFE_OPERATOR_INVENTORY.md):
  13 exact controls, assumptions and anomaly conventions.
- [Scientific consistency review](reviewer/SCIENTIFIC_REVIEW.md): 35 checks,
  copied-script reproduction and an independent selected-equation literature review.
- [New full-text wall comparator](wall_literature/LITERATURE_NOTE.md): arXiv
  2604.20762v1 supplies local wall motion and finite-rate dynamics under a different
  scalar/Higgs model. Its free susceptibility 13/6 and this constrained 144/79
  require ensemble and kinetic-convention matching; their ratio is not a universal
  yield correction. An anomaly-normalization convention flag remains to be resolved
  before transferring its topological operator.
- [Bounded search receipts](literature/METADATA_RECEIPTS.json): three INSPIRE
  queries, including metadata for Harvey–Turner (1990); this is not full-text
  review of every returned lead or an exhaustive web search.

The independent coefficient message reached the producer after its implementation
was frozen but before its first execution. Both methods derive their results
separately, but execution was **not fully blinded**. Local plans and subsequent
portability amendments preserve their actual ordering. These AI-assisted checks
are not external peer review, experimental confirmation or an independent human
assessment. Private raw files, historical inventory identifiers and third-party
paper PDFs/text/images are excluded.

Read [reproduction instructions](REPRODUCE.md) and [round metadata](ROUND.json).
The predecessor is the [transport gate](../2026-10-01_transport_gate/README.md).
Official release remains v1.23.1; this round is proposed in the existing draft PR.

The next question is to match one allowed Wilson-specific operator and its CP
data, then reconcile constrained susceptibilities and rate conventions across
the electroweak crossover before solving finite-rate, energy-conserving dynamics.
