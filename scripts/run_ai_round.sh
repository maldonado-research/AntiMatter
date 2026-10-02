#!/usr/bin/env bash
# External persistent Linux runner template. No schedule is installed here.
set -euo pipefail
umask 077

antimatter_repo_root=$(cd "${1:?Pass the Antimatter checkout path}" && pwd -P)
antimatter_state_root=${2:?Pass a persistent state directory outside the checkout}
antimatter_model_id=${ANTIMATTER_CODEX_MODEL:?Set a verified runner model ID for GPT-6.1 Sol}
command -v codex >/dev/null
command -v flock >/dev/null
command -v timeout >/dev/null
command -v python3 >/dev/null
mkdir -p "$antimatter_state_root"
antimatter_state_root=$(cd "$antimatter_state_root" && pwd -P)
case "$antimatter_state_root/" in
  "$antimatter_repo_root/"*) echo 'State directory must be outside the public checkout' >&2; exit 2 ;;
esac
exec 9> "$antimatter_state_root/round.lock"
if ! flock -n 9; then
  echo 'Another research round owns the runner; stop before overlapping invocations.' >&2
  exit 75
fi
if [[ -n $(git -C "$antimatter_repo_root" status --porcelain) ]]; then
  echo 'Checkout has existing work; preserve or finish it before starting a new scheduled round.' >&2
  exit 2
fi
antimatter_run_dir=$(mktemp -d "$antimatter_state_root/round.XXXXXXXX")
git -C "$antimatter_repo_root" rev-parse HEAD > "$antimatter_run_dir/baseline-commit.txt"
cp "$antimatter_repo_root/docs/research-routine/routine.json" "$antimatter_run_dir/before-routine.json"
date -u +'%Y-%m-%dT%H:%M:%SZ' > "$antimatter_run_dir/started-utc.txt"
set +e
timeout --kill-after=30s 60m codex --no-daemon exec --ephemeral \
  --approve-for-me --model "$antimatter_model_id" \
  -c 'model_reasoning_effort="ultra"' \
  --cd "$antimatter_repo_root" --json \
  --output-last-message "$antimatter_run_dir/final.md" - \
  < "$antimatter_repo_root/docs/research-routine/ROUND_PROMPT.md" \
  > "$antimatter_run_dir/events.jsonl" 2> "$antimatter_run_dir/stderr.log"
antimatter_exit_code=$?
set -e
printf '%s\n' "$antimatter_exit_code" > "$antimatter_run_dir/cli-exit-code.txt"
date -u +'%Y-%m-%dT%H:%M:%SZ' > "$antimatter_run_dir/ended-utc.txt"
echo "Research invocation ended with status $antimatter_exit_code; private runner logs: $antimatter_run_dir"
if [[ "$antimatter_exit_code" -ne 0 ]]; then
  printf '%s\n' "$antimatter_exit_code" > "$antimatter_run_dir/exit-code.txt"
  exit "$antimatter_exit_code"
fi
# Continue only after a new, validated, committed checkpoint. This structural
# guard does not replace scientific review or verify remote publication.
set +e
python3 - "$antimatter_repo_root" "$antimatter_run_dir" <<'PY'
import json
import pathlib
import subprocess
import sys

repo, run = map(pathlib.Path, sys.argv[1:])
before = json.loads((run / "before-routine.json").read_text())
after = json.loads((repo / "docs/research-routine/routine.json").read_text())
latest = after.get("latest_completed_round")
if not isinstance(latest, str) or latest == before.get("latest_completed_round"):
    raise SystemExit("No new completed round: stop for checkpoint review")
latest_path = pathlib.Path(latest)
if latest_path.is_absolute() or latest_path.parts[:2] != ("research", "rounds") or ".." in latest_path.parts:
    raise SystemExit("Round pointer must be a portable relative path under research/rounds")
round_path = repo / latest_path
round_root = round_path.resolve()
if round_path != round_root:
    raise SystemExit("Round pointer must not traverse symlinks")
if not round_root.is_relative_to((repo / "research/rounds").resolve()):
    raise SystemExit("Completed round must be inside research/rounds")
record_path = round_root / "ROUND.json"
if record_path.is_symlink() or not record_path.is_file():
    raise SystemExit("Round record must be a regular file inside the round")
record = json.loads(record_path.read_text())
if record.get("status") != "completed" or not record.get("next_question", "").strip():
    raise SystemExit("Round is incomplete or lacks a next question")
if record.get("predecessor") != before.get("latest_completed_round"):
    raise SystemExit("Round predecessor does not match the prior checkpoint")
receipt_name = record.get("validation_receipt")
if not isinstance(receipt_name, str):
    raise SystemExit("Round must name its validation receipt")
receipt_relative = pathlib.Path(receipt_name)
if receipt_relative.is_absolute() or ".." in receipt_relative.parts:
    raise SystemExit("Validation receipt must use a portable relative path inside the round")
receipt_file = round_root / receipt_relative
receipt_path = receipt_file.resolve()
if receipt_file != receipt_path or not receipt_path.is_file() or not receipt_path.is_relative_to(round_root):
    raise SystemExit("Validation receipt must stay inside the round")
receipt = json.loads(receipt_path.read_text())
if receipt.get("status") != "passed" and receipt.get("passed") is not True:
    raise SystemExit("Round validation did not pass")
if subprocess.check_output(["git", "-C", str(repo), "status", "--porcelain"], text=True).strip():
    raise SystemExit("Uncommitted work remains: stop for preservation and review")
for item in [round_root / "ROUND.json", receipt_path, repo / "docs/research-routine/routine.json"]:
    subprocess.run(["git", "-C", str(repo), "ls-files", "--error-unmatch", str(item.relative_to(repo))],
                   check=True, stdout=subprocess.DEVNULL)
commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
baseline = (run / "baseline-commit.txt").read_text().strip()
if commit == baseline:
    raise SystemExit("No new committed checkpoint")
if subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", baseline, commit]).returncode:
    raise SystemExit("New checkpoint must descend from the invocation baseline")
summary = {"status": "completed_checkpoint_verified", "round": latest,
           "validation_receipt": receipt_name,
           "commit": commit}
(run / "checkpoint-guard.json").write_text(json.dumps(summary, indent=2) + "\n")
print("Completed checkpoint verified:", latest)
PY
antimatter_guard_exit=$?
set -e
printf '%s\n' "$antimatter_guard_exit" > "$antimatter_run_dir/exit-code.txt"
exit "$antimatter_guard_exit"
