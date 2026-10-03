# Reproduce the v1.23.2 public package

The complete ZIP has authored release documents at its root and an unchanged public source snapshot in `source/`. Its `SOURCE_MANIFEST.json` records full commit `da472576101a66b1c5c7dc97c01f7124e99076bd` and every input SHA-256. The source's original `CITATION.cff` remains the published v1.23.1 citation; `RELEASE_CITATION.cff` describes v1.23.2 with a **reserved, not yet confirmed published** DOI.

## Verify integrity first

Check downloaded outer hashes with `sha256sum --check AM1232_CHECKSUMS.txt` when all named outer files are present. After extraction, from the archive root:

```bash
set -euo pipefail
python3 - <<'PY'
import hashlib, json
from pathlib import Path
manifest = json.loads(Path('SOURCE_MANIFEST.json').read_text())
for entry in manifest['source_files'] + manifest['generated_documents'] + manifest['copied_release_notices']:
    path = Path(entry['archive_path'])
    assert path.is_file() and not path.is_symlink(), entry['archive_path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], entry['archive_path']
print('All manifest file hashes pass')
PY
(cd source/research/AM1231 && sha256sum --check SHA256SUMS.txt)
(cd source/research/AM1232_CANDIDATE_20261001 && sha256sum --check SHA256SUMS.txt)
(cd source/research/rounds/2026-10-01_transport_gate && sha256sum --check SHA256SUMS.txt)
(cd source/research/rounds/2026-10-02_sm_operator_gate && sha256sum --check SHA256SUMS.txt)
```

The four ledgers have 48, 40, 24, and 60 entries respectively. Their enclosing records include subordinate ledgers. Do not edit a retained file to obtain a pass. The historical operator `producer/ORIGINAL_PORTABILITY_INPUTS/SHA256SUMS` records 15 files in the **original producer context**: archived originals replace amended files, and unchanged parent producer files supply the remaining entries. It is not a standalone ledger for just its preservation subdirectory. Both nested v1.23/v1.22 ZIPs are retained byte for byte; the earlier v1.21 parent needed to rerun all v1.22 physics is not included. Integrity verification does not mean that parent physics was rerun.

## Environment

Use a supplied **Python 3.12.14** interpreter on a supported platform; this guide does not install the interpreter. The pins are the numerical versions validated in the source records. Set `antimatter_public_root` to either the extracted `source/` directory or a verified Git checkout. Set the environment path outside that source tree:

```bash
antimatter_public_root='/absolute/path/to/source-or-checkout'
antimatter_env='/absolute/path/to/new-reproduction-env'
python3.12 -c 'import sys; assert sys.version_info[:3] == (3, 12, 14), sys.version'
python3.12 -m venv "$antimatter_env"
antimatter_python="$antimatter_env/bin/python"
"$antimatter_python" -m pip install \
  -r "$antimatter_public_root/research/AM1231/requirements-replay.txt" \
  -r "$antimatter_public_root/research/rounds/2026-10-02_sm_operator_gate/requirements-operator.txt"
"$antimatter_python" -m pip check
antimatter_replay_root=$(mktemp -d /tmp/antimatter-release-replay.XXXXXXXX)
export XDG_CACHE_HOME="$antimatter_replay_root/cache"
export MPLCONFIGDIR="$antimatter_replay_root/matplotlib"
```

Install the frozen declared dependencies; network access is needed for installation unless they are already available locally. Numerical reproduction itself needs no private references, model execution, literature download, Git push, or publication credential. Never run a producer or reviewer in the retained source directory; outputs and nested review workspaces belong in disposable copies.

## Preferred aggregate runners: a Git checkout

The aggregate scripts call `git rev-parse HEAD`; a plain ZIP extraction intentionally has no `.git` metadata. Use a separate existing clean checkout at the manifest commit, or obtain it with:

```bash
git clone https://github.com/maldonado-research/AntiMatter.git /absolute/path/to/new-checkout
git -C /absolute/path/to/new-checkout checkout --detach da472576101a66b1c5c7dc97c01f7124e99076bd
git -C /absolute/path/to/new-checkout rev-parse HEAD
```

The intended tag URL is <https://github.com/maldonado-research/AntiMatter/tree/v1.23.2>; use the full commit as the authoritative version check. After environment setup with `antimatter_public_root` pointing to that checkout:

```bash
cd "$antimatter_public_root"
"$antimatter_python" scripts/reproduce_candidate.py --output "$antimatter_replay_root/candidate-receipts"
"$antimatter_python" scripts/reproduce_operator_round.py --output "$antimatter_replay_root/operator-receipts"
```

Both must exit zero with `receipt.json` status `passed`. Candidate replay executes seven scripts and compares five producer outputs under the explicit portability policy. Operator replay executes eight checks, requires 15 byte-identical artifacts, and verifies registered control counts. Output directories must be empty and outside the checkout. Transport is a separate numerical workflow step, shown below. A copied snapshot can reproduce the underlying calculations manually without inventing or replacing its recorded source commit.

## Manual archive replay without Git metadata

These commands use the extracted public `source/` as `antimatter_public_root`, the environment above, and new disposable copies. Exact producer/comparator failure status is preserved by `set -euo pipefail`.

### Kinetic-metric and duration candidate

```bash
cp -R "$antimatter_public_root/research/AM1232_CANDIDATE_20261001" "$antimatter_replay_root/candidate"
cd "$antimatter_replay_root/candidate"
antimatter_baseline="$antimatter_public_root/research/AM1231/v1.23"
"$antimatter_python" wilson-metric/audit.py --source-root "$antimatter_baseline" --output-dir "$PWD/wilson-metric"
"$antimatter_python" wilson-metric-independent/independent.py --source-root "$antimatter_baseline" --output-dir "$PWD/wilson-metric-independent"
"$antimatter_python" wilson-metric-independent/compare.py --source-root "$antimatter_baseline" --producer-dir "$PWD/wilson-metric" --output-dir "$PWD/wilson-metric-independent"
"$antimatter_python" source-duration/audit.py --source-root "$antimatter_baseline" --output-dir "$PWD/source-duration"
"$antimatter_python" source-duration-independent/independent_time_check.py --registered-grid --output "$PWD/source-duration-independent/registered_grid_time_results.json"
"$antimatter_python" source-duration-independent/independent_duration_check.py
"$antimatter_python" source-duration-independent/compare_outputs.py
```

Expect 12 metrics, 36 configurations, 210 Wilson controls, all 30 registered trajectory endpoints, all five duration bounds, and successful comparison receipts. The explicit **post-run portability policy** allows only named metadata and bounded numerical differences, including specified primary floating values and trajectory endpoints, while retaining every difference in receipts. All original producer/independent checks must still pass; policy acceptance does not imply byte equality or external preregistration. See `source/docs/research-routine/PORTABLE_REPRODUCTION.md`. The two comparison scripts check the independent calculations; the aggregate runner adds the five-producer-output portability comparison. Manual success alone is not a substitute for that additional comparison.

### Transport

```bash
cp -R "$antimatter_public_root/research/rounds/2026-10-01_transport_gate" "$antimatter_replay_root/transport"
cd "$antimatter_replay_root/transport"
"$antimatter_python" -m unittest discover -s producer -p test_transport.py -v
(cd producer && "$antimatter_python" run_round.py)
"$antimatter_python" independent/independent_check.py --producer-dir "$PWD/producer"
"$antimatter_python" independent/compare_results.py --producer-dir "$PWD/producer" --repo-root "$antimatter_public_root"
```

Expect nine tests, 71 independent controls, 11 comparisons, and all 201 signed-history samples. Environment metadata and run timestamps describe the new run; original retained receipts describe their own runs.

### Standard Model operator, sensitivity, and wall comparison

```bash
cp -R "$antimatter_public_root/research/rounds/2026-10-02_sm_operator_gate" "$antimatter_replay_root/operator"
cd "$antimatter_replay_root/operator"
export ANTIMATTER_PUBLIC_REPO="$antimatter_public_root"
for antimatter_script in \
  producer/sm_charge_diagnostic.py producer/conditional_sensitivity.py \
  independent/sm_charge_response.py independent/conditional_normalization_sensitivity.py \
  independent/compare_frozen_producer.py inventory/verify_inventory.py \
  wall_literature/compare_susceptibilities.py reviewer/review_checks.py; do
  "$antimatter_python" "$antimatter_script"
done
```

Expect 48 producer primary and 36 sensitivity controls, 24 independent primary and seven sensitivity checks, 11 exact comparisons, 13 inventory checks, and 35 review checks. The aggregate runner additionally compares 15 retained artifacts byte for byte; Python metadata can require the exact patch version. `wall_literature/compare_susceptibilities.py` verifies the free susceptibility sum and its ratio to the imported projected result; it does not rerun the cited paper's wall simulation or independently rederive the projected coefficient.

### Preserved baseline

For baseline integrity run `research/AM1231/verify_release.py` against the extracted files. For a new replay, copy `research/AM1231/` into a separate disposable directory and follow its `README.md` and `REPRODUCIBILITY.md`: the standard-library energy frontier uses the unchanged v1.23 source ZIP, and the v1.23 numerical audit uses the unchanged v1.22 parent ZIP. Original deterministic CSV/JSON comparisons and rendering differences have separate scopes. Retain all newly produced logs/receipts outside the source.

Passing arithmetic, hash, or reproduction checks establishes the stated computational scope. It does not establish physical baryogenesis, scientific novelty, external peer review, a published reserved DOI, or active continuous AI operation.
