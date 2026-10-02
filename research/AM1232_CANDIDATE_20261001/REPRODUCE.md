# Reproduce the candidate checkpoint

Use Python 3.12 and the exact dependencies in `research/AM1231/requirements-replay.txt`.
The producer runs used Python 3.12.14, NumPy 2.5.2 and SciPy 1.17.1. The independent
proper-time run used the machine's supplied NumPy 2.3.5 and SciPy 1.17.0; the
separate algorithms also pass comparisons when run in the producer's pinned
environment. Differences in independent output bytes across versions are not
claims of physical uncertainty or failure.

From the AntiMatter repository root, create an isolated output copy. This keeps
all preserved research records unchanged and retains relative sibling paths
used by the comparison scripts:

```bash
set -euo pipefail
source .venv/bin/activate
export XDG_CACHE_HOME=/workspace/.cache
export MPLCONFIGDIR=/workspace/.cache/matplotlib
antimatter_source_root="$PWD/research/AM1231/v1.23"
antimatter_check_dir=$(mktemp -d /tmp/antimatter-candidate.XXXXXX)
cp -R research/AM1232_CANDIDATE_20261001 "$antimatter_check_dir/checkpoint"
cd "$antimatter_check_dir/checkpoint"
python wilson-metric/audit.py --source-root "$antimatter_source_root" --output-dir "$PWD/wilson-metric"
python wilson-metric-independent/independent.py --source-root "$antimatter_source_root" --output-dir "$PWD/wilson-metric-independent"
python wilson-metric-independent/compare.py --source-root "$antimatter_source_root" --producer-dir "$PWD/wilson-metric" --output-dir "$PWD/wilson-metric-independent"
python source-duration/audit.py --source-root "$antimatter_source_root" --output-dir "$PWD/source-duration"
python source-duration-independent/independent_time_check.py --registered-grid --output "$PWD/source-duration-independent/registered_grid_time_results.json"
python source-duration-independent/independent_duration_check.py
python source-duration-independent/compare_outputs.py
```

Expected producer results: Wilson PASS, 12 metrics, 36 configurations and 210
controls; source duration PASS, 30 trajectories and all registered checks.
Both comparison scripts must exit successfully. Independent Wilson comparison
checks script and registration provenance as well as JSON/CSV rows. Independent
source comparison checks all 30 endpoints and all five duration bounds.

Producer JSON and CSV are deterministic in the pinned environment. Their source,
code and registration hashes are recorded. Report Markdown source links were
adapted for GitHub readability during packaging; regenerating those reports can
restore local source links without changing scientific JSON/CSV results. Results
files contain many Decimal digits to resolve the mathematical matrix problem;
these are not precision claims about uncomputed physical corrections.

The release checksum ledger is `SHA256SUMS.txt`. Validate it from this directory
with `sha256sum --check SHA256SUMS.txt`. The enclosing ZIP has a separate external
checksum. No raw private references or original chat export are required.
