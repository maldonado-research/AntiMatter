# Preregistered controls: symmetric-phase SM charge response

Registered before running the calculation script on 2026-10-02 UTC. This is an
independent derivation; it does not read another producer's results.

## Scope and conventions

- Three Standard Model generations, one complex Higgs doublet.
- Symmetric electroweak phase; relativistic, small-chemical-potential linear
  susceptibilities. A Weyl fermion contributes `g T^2/6`; a complex boson
  contributes `g T^2/3`.
- All charged-fermion Yukawas and electroweak sphalerons equilibrated; quark
  flavor mixing equilibrated. Strong-sphaleron equilibrium is included as a
  redundant check.
- Hypercharge neutrality. Each `Delta_i = B/3 - L_i` is conserved and fixed;
  no neutrino-mass or other lepton-flavor-violating reactions are introduced.
- External source `s_a = dot(theta) c_a` enters free energy as `-s^T n`.
  The kinetic chemical potential is `mu_a = n_a/chi_a`; equilibrium requires
  `R (mu - s) = 0`. All source signs below use this convention.
- Integer susceptibility weights `w` factor out the common `T^2/6`.
  Densities printed by the script are normalized by that common factor.

## Required positive controls

1. Exact rational matrix arithmetic recovers `B = (28/79)(B-L)` with no
   external source. Check separate flavor-asymmetric initial charges as well
   as equal `Delta_i`.
2. The reaction matrix has rank 12 on 16 species, and its kernel is precisely
   spanned by hypercharge and the three `Delta_i`. Strong sphalerons add no
   rank after Yukawa equilibrium.
3. For an arbitrary rational source and fixed arbitrary rational charges,
   check all reaction equations, all fixed charges, and hypercharge neutrality.
4. At zero fixed `Delta_i`, a unit source along `B+L` gives normalized baryon
   density `432/79`, along `L` or `B` gives `216/79`, and along `B-L` gives zero.
   Thus the dimensional baryon responses are `(72/79) T^2 dot(theta)` and
   `(36/79) T^2 dot(theta)`, respectively.
5. Adding any conserved-charge vector to a source leaves densities identical
   at fixed conserved charges. Include both `B-L` and flavor-difference
   directions, and the hypercharge direction.
6. The constrained source-response matrix is symmetric, annihilates conserved
   charge vectors, and gives nonnegative quadratic response for a finite
   preregistered rational probe set. This finite positivity check supplements
   the analytic positive-semidefinite construction; it is not a proof by
   itself.

## Negative and convention controls

7. Deliberately replace the Higgs boson weight 4 by the fermion weight 2;
   the no-source conversion must differ from `28/79` (expected `52/145`).
   The production result must retain weight 4.
8. Remove electroweak-sphaleron equilibrium. Baryon and individual lepton
   currents then become conserved, so a source along `B+L` cannot generate
   baryon density from zero fixed baryon/lepton charges.
9. Reverse the external-source sign. Source-induced densities must reverse,
   while the pre-existing-charge contribution remains unchanged.
10. Deliberately omit fixing `B-L`, while preserving zero flavor differences
    and hypercharge neutrality. A pure `B-L` source can then give nonzero
    equilibrium charge. Record this as a *different grand-canonical ensemble*,
    not evidence of closed-system `B-L` generation.
11. Derive the mixed weak and hypercharge anomaly traces in the all-left-handed
    Weyl convention (right-handed particles are charge-conjugated). Per
    generation expect `A_B,WW = A_L,WW = +1/2`,
    `A_B,YY = A_L,YY = -1/2`, and both `B-L` traces zero. Hypercharge's
    weak trace and cubic hypercharge trace vanish. Deliberately omit
    conjugating right-handed fields: the `B-L` hypercharge trace must then
    become nonzero and be detected. With positive topological orientation
    `q_W = g^2 W Wtilde/(32 pi^2)`, expect `Delta(B+L) = +6 Delta N_CS`;
    integration by parts gives `+d(theta) J_(B+L) = -6 theta q_W` for the
    weak part. These signs define a convention, not an independently
    observable absolute orientation.

## Conditional normalization check

Consider the fresh conditional EFT choice `L_bias = c_0 d(theta_0) J_(B+L)`,
with `theta_0 = 2 pi tau_1` and `c_0 = n_det D_d`. This is an assumed
coefficient, not a derived one. The external source would be
`kappa/T = D_d 2 pi n_det dot(tau_1)/T`. Apply the derived response to this
conditional source without identifying `D_d` as a computed Wilson coefficient
or inferring a scalar history. Compare this with the unsuppressed assumption
`c_0 = n_det`; the latter may leave the small-source regime if its source/T is
large. No source histories or fit parameter values have been supplied to
this independent worker, so do not fabricate a numerical cosmological fit.

This non-test explanatory annotation was changed to public site-phase
terminology after the primary run. All reaction controls above and the
implementation are unchanged; `provenance_note.json` records the first hashes.

## Failure policy and interpretation limits

Any failed positive control invalidates the corresponding derivation until
corrected and rerun. Record failures explicitly rather than silently selecting
passing outputs. Matrix checks establish consistency within this idealized
equilibrium model; they do not establish a new operator, a physical scalar
trajectory, CP violation, a cosmological history, or a baryogenesis prediction.
The broken-phase sphaleron freezeout temperature near 131.7 GeV is outside the
massless symmetric-phase approximation used here.
