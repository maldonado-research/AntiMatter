# Portable archival comparisons

`scripts/reproduction_policy.py` implements the explicit `wilson-portability-v1`
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

All other contents remain exact: inputs and hashes, registered families,
Decimal root and period strings, metric values, heavy masses and spectral
changes, counts, conventions, versions, source-duration data, CSV columns and
row ordering. Missing/extra fields, nonfinite observations, changed control
bounds or unexpected differences fail. No general floating-point tolerance
is applied to primary results. A newly observed difference outside this
allowlist requires an explicit evidence review; it is not silently accepted.

The receipt distinguishes accepted metadata, accepted bounded diagnostics,
and rejected scientific or unapproved differences. A passing portable
comparison indicates agreement under this policy, not byte-identical files,
physical validity, novelty or external peer review.
