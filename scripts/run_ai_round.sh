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
round_root = (repo / latest).resolve()
if not round_root.is_relative_to((repo / "research/rounds").resolve()):
    raise SystemExit("Completed round must be inside research/rounds")
record = json.loads((round_root / "ROUND.json").read_text())
if record.get("status") != "completed" or not record.get("next_question", "").strip():
    raise SystemExit("Round is incomplete or lacks a next question")
if record.get("predecessor") != before.get("latest_completed_round"):
    raise SystemExit("Round predecessor does not match the prior checkpoint")
receipt_name = record.get("validation_receipt")
if not isinstance(receipt_name, str):
    raise SystemExit("Round must name its validation receipt")
receipt_path = (round_root / receipt_name).resolve()
if not receipt_path.is_relative_to(round_root):
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
if commit == (run / "baseline-commit.txt").read_text().strip():
    raise SystemExit("No new committed checkpoint")
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
