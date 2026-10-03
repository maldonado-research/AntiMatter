# Portable archival comparisons

`scripts/reproduction_policy.py` implements the explicit `candidate-portability-v3`
policy. It compares fresh output to the preserved candidate without editing
either artifact. Byte equality is reported separately from acceptance. Every
content difference is retained in the receipt, with its category and gate.

All seven original producer and independent-comparison commands must succeed
before applying this policy. The existing Wilson independent comparator checks
all 36 CSV/JSON rows, source/code/registration provenance, light roots and period
shifts, heavy masses, mode counts and the producer controls. This policy does
not replace those checks or modify their thresholds.

The only accepted Wilson differences are:

- `runtime.python_executable`: interpreter installation path metadata. Python,
  NumPy and SciPy versions remain exact.
- Named heavy-coordinate and analytic source-off control observations: the
  names, pass statuses and bound strings stay identical; both observations
  must be finite, nonnegative and at most the original `2e-12` bound.
- Named positive source-off heavy-spectrum observations: both remain finite
  and positive, with identical names, null bounds and passing statuses. The
  fresh observation's square root must equal its generated minimum heavy mass.
- JSON result and CSV `heavy_coordinate_relative_error` diagnostics: they
  must satisfy the same original `2e-12` gate, agree with the named control,
  and retain matching row identities. CSV diagnostics must exactly match
  the generated JSON representation.
- Positive finite `heavy_min_GeV` and `heavy_max_GeV`: archival relative drift
  must be strictly below `1e-12`, reusing the existing independent spectral
  comparison criterion. Its original independent comparison must also pass.
- `heavy_min_relative_change` and `heavy_max_relative_change`: each must exactly
  equal the same document's mass divided by its matching baseline mass minus
  one. Both referenced masses must satisfy the same `1e-12` archival gate;
  no absolute tolerance is applied to a near-zero relative change.
- `metric_correction_operator_norm`: both values must be finite and nonnegative,
  and their absolute difference must be at most 64 ULP of their maximum.
  This is a **new display/portability gate**, adopted after reviewing hosted
  machine drift. It was not a preregistered scientific acceptance threshold.
  Every result norm must exactly equal its document's metric-case norm.
  The receipt reports the absolute difference and allowed 64-ULP interval.

The five named primary floating fields may also vary in CSV, only when each
cell exactly matches its same document's JSON representation, retains matching
row identities, and satisfies the corresponding gate above. Observed hosted
differences were confined to these floating fields and the previously listed
diagnostics/installation path. This motivated v2; the archived inputs, data
and registration have not been rewritten.

All other Wilson contents remain exact: inputs and hashes, registered families,
Decimal root and period strings, other metric values and spectral changes,
counts, conventions, versions, CSV columns and
row ordering. Missing/extra fields, nonfinite observations, changed control
bounds or unexpected differences fail. No general floating-point tolerance
is applied outside the named fields. A newly observed difference outside this
allowlist requires an explicit evidence review; it is not silently accepted.

The receipt distinguishes accepted metadata, accepted bounded diagnostics,
accepted primary floating differences (`scientific_differences`), and rejected
scientific or unapproved differences. Accepted primary differences describe
numerical portability under recorded gates, not scientific advancement.
A passing portable
comparison indicates agreement under this policy, not byte-identical files,
physical validity, novelty or external peer review.

## Source-duration semantic comparison

V3 adds a **new portable archival comparator** after observing hardware-dependent
adaptive ODE steps, ledger diagnostics and endpoint rounding. It reuses the
original registered controls and independent proper-time endpoint criteria;
it is not a newly preregistered verification or a change to preserved data.
All original producer and proper-time comparisons must still succeed.

Root parameters, source/code/registration hashes, exact software versions,
scope, dates, status, all 11 named check booleans and all duration bounds remain
exact. The ordered 30 initial temperature/phase/expansion/energy records remain
exact. Missing or additional root, row, control or summary fields fail.

Each archived/fresh row compares exactly the original eight endpoint measures:
absolute phase, momentum, signed site-0 velocity, total scalar fraction and
Hubble ratio; absolute kinetic and potential differences divided by the frozen
amplitude; and relative conditional winding-times-efficiency difference. Every
measure must be strictly below `1e-7`, the original independent comparator's
criterion. The receipt includes all 30 sets of endpoint differences.

Explicit derived fields may vary consistently with those endpoints and the
original energy/radiation ledgers: phase and canonical velocities, total scalar
energy, radiation density, kinetic fraction, integrated Hubble loss and final
ledger residual. Velocity, Hubble and conditional winding expressions are
recomputed from their same-document inputs. Energy/fraction/ledger consistency
uses the original `1e-7` natural-scale criteria and radiation consistency uses
the original `1e-8` criterion. These derived checks add consistency requirements
to the new archival comparator; they do not widen any original tolerance.

Only the explicitly listed solver/error/extremum/count diagnostics may vary:
scalar absolute/relative ledger errors, radiation ledger/analytic errors,
maximum energy ratio, four sampled minima, tight/loose evaluation counts,
two-tolerance endpoint difference and loose scalar-ledger error. Values must
be finite, evaluation counts positive integers, and all original energy,
positivity, ledger, radiation, two-tolerance, stationary, reflection and Bessel
controls are re-evaluated. The Bessel scalar-ledger relative error remains a
reported nonnegative diagnostic with no invented acceptance bound.

Summary extrema must exactly match their generated rows. The largest-sample
record must exactly mirror the generated maximum-energy row and retain the
same initial temperature/phase as the archive. It remains a sampled maximum.

Both source CSVs must retain their exact columns and row order, with every
cell exactly matching its corresponding JSON representation. Trajectory cells
may vary only for the named endpoint/derived/diagnostic fields. Duration-bound
CSV and JSON contents remain exact. All accepted numerical differences are
recorded; passing this semantic comparison does not imply byte equality.
