# Reproduce in an isolated copy

Use Python 3.12 and the pinned dependencies in
`research/AM1231/requirements-replay.txt`. Activate the repository virtual
environment first. From the AntiMatter repository root:

```bash
set -euo pipefail
antimatter_repo_root="$PWD"
antimatter_round_copy=$(mktemp -d /tmp/antimatter-transport.XXXXXX)
cp -R research/rounds/2026-10-01_transport_gate "$antimatter_round_copy/round"
cd "$antimatter_round_copy/round"
sha256sum --check SHA256SUMS.txt
python -m unittest discover -s producer -p test_transport.py -v
(cd producer && python run_round.py)
python independent/independent_check.py --producer-dir "$PWD/producer"
python independent/compare_results.py --producer-dir "$PWD/producer" --repo-root "$antimatter_repo_root"
```

The producer must execute nine tests without failure or skips. The independent
implementation must pass all 71 controls. The comparator must pass 11 numerical
comparisons and the registration/receipt/input checks, including 201 trajectory
rows. It rejects modified pre-run documents and receipts, missing or changed
public-context inputs, missing columns/rows, invalid grids and numerical mismatch.
Supply the actual repository root; it maps the preserved recorded paths without
assuming a `/workspace/AntiMatter` checkout on another machine.

Run in the copy: result scripts regenerate JSON/CSV and change run timestamps
and environment metadata. The stored original receipts and checksum ledgers
refer to their preserved runs, not those new output bytes. Controls use explicit
numerical tolerances; many printed digits are not physical precision claims.
Keep each new receipt separate from the original evidence.

The fixed-temperature, dimensionless comparator is a numerical test framework.
A passing run does not derive the physical Antimatter source or final abundance.
