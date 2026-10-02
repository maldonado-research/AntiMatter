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
mkdir -p "$antimatter_state_root"
antimatter_state_root=$(cd "$antimatter_state_root" && pwd -P)
case "$antimatter_state_root/" in
  "$antimatter_repo_root/"*) echo 'State directory must be outside the public checkout' >&2; exit 2 ;;
esac
exec 9> "$antimatter_state_root/round.lock"
if ! flock -n 9; then
  echo 'Another research round owns the runner; this invocation is skipped.'
  exit 0
fi
if [[ -n $(git -C "$antimatter_repo_root" status --porcelain) ]]; then
  echo 'Checkout has existing work; preserve or finish it before starting a new scheduled round.' >&2
  exit 2
fi
antimatter_run_dir=$(mktemp -d "$antimatter_state_root/round.XXXXXXXX")
git -C "$antimatter_repo_root" rev-parse HEAD > "$antimatter_run_dir/baseline-commit.txt"
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
printf '%s\n' "$antimatter_exit_code" > "$antimatter_run_dir/exit-code.txt"
date -u +'%Y-%m-%dT%H:%M:%SZ' > "$antimatter_run_dir/ended-utc.txt"
echo "Research invocation ended with status $antimatter_exit_code; private runner logs: $antimatter_run_dir"
# Successful model termination is not proof of a scientific advance. Check its
# durable round record, independent evidence, publication status and next action.
exit "$antimatter_exit_code"
