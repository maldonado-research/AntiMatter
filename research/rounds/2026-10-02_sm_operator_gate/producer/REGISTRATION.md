# Pre-computation registration: conventional SM charge diagnostic

Registered 2026-10-02, before the producer solver or tests were run. This file
freezes the questions, assumptions, controls, and reporting boundaries. No
claim of a novel interaction, viable model, or physical baryon yield is made.

## Benchmark and independent computation

Use a dimensionless background phase theta0 and the conventional externally
prescribed derivative interaction

    L_int = c (partial_mu theta0) J_(B+L)^mu,
    kappa = c dot(theta0).

The sign convention is H_int = -kappa Q_(B+L). The coefficient c is unspecified
by the Wilson replacement model; c = 1 is a normalization toy, not UV matching.
If the historical EFT identification is verified in a public source, report
c = n_det D_d as an explicitly conditional assumption, not a derivation.

Producer uses ten particle species q,u,d,l_e,l_mu,l_tau,e_e,e_mu,e_tau,H,
quark flavor equilibrium, and ideal symmetric-phase SM susceptibilities
chi = diag(18,9,9,2,2,2,1,1,1,4) T^2/6. All charged-fermion Yukawa interactions,
strong sphalerons, and weak sphalerons are in equilibrium. Impose hypercharge
neutrality and fix all three Delta_i = B/3-L_i. Use exact fractions and a
susceptibility-weighted KKT minimization; do not infer the source coefficient
from the inherited phenomenological yield formula. The independent agent uses
sixteen separate quark-flavor species and a distinct constraint solver. No
implementation or result exchange occurs until both calculations are done.

## Frozen checks

1. Zero-drive baryon conversion recovers B = (28/79)(B-L).
2. Determine, without a pre-specified expected value, the exact coefficient of
   kappa T^2 in B for a B+L source at fixed zero Delta_i.
3. The effective chemical potentials mu-kappa Q satisfy every reaction;
   weak-sphaleron intrinsic affinity equals kappa times its exact source charge.
4. Hypercharge and individual Delta_i sources are invisible at fixed conserved
   densities; B and L sources give identical density responses, and B+L gives
   twice either response.
5. Equal and opposite conserved flavor asymmetries give zero total B while
   allowing nonzero individual lepton densities.
6. Check rank, uniqueness, charge conservation, source normalization, and the
   relation between susceptibility-weighted projection and reaction constraints.
7. Derive small-mu/T and external-work conditions, with no extrapolation to a
   numerical yield at T = 131.7 GeV, where the symmetric-phase approximation
   is invalid. Recompute all reproducible outputs byte-identically.

## Interpretation limits

The existing n_det = 16, D_d, c_sph = 0.0195, and tau1 = theta0/(2pi)
are historical inputs. Their existence does not independently fix c in the
Wilson replacement or supply its gauge/anomaly matching. Any historical EFT
coefficient identification must be reported conditionally with source provenance.
No coefficient from this diagnostic is inserted into the frozen parent model.
No dynamical phase equation, CP-odd invariant, energy reservoir, finite-rate
sphaleron transport, broken-phase susceptibilities, or freeze-out yield is
established. External drive and autonomous source accounting remain separate.

## Artifacts and provenance

Write a stdlib-only Python solver, exact JSON and CSV outputs, a derivation,
public source path/line/hash provenance, a run receipt, and SHA256 ledger only
under this producer directory. Publication and repository edits are parent tasks.
