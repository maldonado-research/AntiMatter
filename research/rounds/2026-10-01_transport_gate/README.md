# Transport gate: conserved charges and signed response

Ricardo Maldonado · 1 October 2026, Pacific · Prepared with AI assistance

This completed research round adds a reusable **illustrative transport
diagnostic**. It does not supply the Antimatter candidate's microscopic operator,
particle content, thermal rates, physical CP bias or baryon yield. The methods
use standard linear response and linear algebra; no mathematical or scientific
novelty is claimed. The official release remains v1.23.1.

## What this round contributes

The density response depends on susceptibility, active reaction channels,
conserved charges, the full source vector and its signed history. These cannot
be identified from a field speed or a chosen efficiency alone. In the registered
three-species comparator, a source in an exactly conserved-current direction
induces no new charge. A compatible source requires a susceptibility-weighted
projection onto the allowed charge slice. Incompatible reaction biases can
produce externally driven circulation and rate-dependent stationary densities.

Equal positive and negative source intervals need not cancel: their retarded
weights differ. In this comparator, shutting off reactions preserves the signed
residual; keeping reactions active washes out its nonconserved part. Species A
is an illustrative label, not baryon number. Outputs are dimensionless densities
divided by T cubed, not predicted cosmological yields. The fixed-temperature
numerics do not solve expanding cosmology, entropy production or an autonomous
reservoir; the general derivation states the extra terms those extensions need.

## Evidence

- [Derivation and physical gates](producer/DERIVATION.md)
- [Producer results](producer/RESULTS.md), [local pre-run plan](producer/REGISTRATION.md),
  [recorded qualification](producer/AMENDMENTS.md), and [nine-test receipt](producer/validation_receipt.json)
- [Independent derivation and audit](independent/AUDIT.md): 71 controls using
  chemical-potential coordinates and augmented matrix exponentials, without
  importing the producer implementation
- [Comparison receipt](independent/comparison_results.json): 11 comparisons,
  including all 201 signed-history samples; original maximum discrepancy
  4.44e-16 in the specified dimensionless cases
- [Validation-failure checks](independent/validation_failure_checks.json):
  missing/changed provenance and incomplete trajectories are rejected
- [Reproduction](REPRODUCE.md) and [round metadata](ROUND.json)

The producer's symmetric spectral method and internal RK4 cross-check are
separate from the independent implementation. All checks are AI-assisted
computational verification within this session; they are not external scientific
peer review or validation of the underlying hypothesis. A preserved original
registration and receipt document the local ordering, not an external
preregistration service. Its inactive-channel qualification was recorded after
review without changing numerical cases or thresholds.

The context baseline is commit `fadef6b67064eda06b3528a7a73ef959c205d8a2`
and [the prior consistency candidate](../../AM1232_CANDIDATE_20261001/README.md).
Its four registered public-context hashes remain unchanged. Original runs used
NumPy 2.3.5/SciPy 1.17.0; the enclosing pinned-environment replay receipt reports
its own versions. No private raw references, personal documents or chat export
were incorporated.

## Next physical question

Construct an action-derived, rephasing-invariant source and explicit particle/
reaction content for one chosen branch. Match anomaly conventions, gauge and
spectator constraints, susceptibility, rates and initial conserved charges.
Then evolve the source, bath, entropy and expansion through production, washout
and freeze-out. This framework supplies controls for that calculation; it does
not determine those missing physical inputs or explain cosmological sign choice.
