# Portable archival comparisons

`scripts/reproduction_policy.py` implements the explicit `wilson-portability-v2`
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

All other contents remain exact: inputs and hashes, registered families,
Decimal root and period strings, other metric values and spectral changes,
counts, conventions, versions, source-duration data, CSV columns and
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
