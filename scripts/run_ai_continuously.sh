#!/usr/bin/env bash
# External Linux host template. This file installs or enables no service.
set -euo pipefail
umask 077

if [[ $# -ne 2 ]]; then
  echo 'Usage: run_ai_continuously.sh /absolute/checkout /absolute/private-state' >&2
  exit 2
fi
if [[ -z ${ANTIMATTER_CODEX_MODEL:-} ]]; then
  echo 'Set ANTIMATTER_CODEX_MODEL to the verified GPT-6.1 Sol model ID.' >&2
  exit 2
fi
antimatter_max_rounds=${MAX_ROUNDS:-0}
if [[ ! $antimatter_max_rounds =~ ^(0|[1-9][0-9]{0,8})$ ]]; then
  echo 'MAX_ROUNDS must be 0 (unbounded) or an integer from 1 to 999999999.' >&2
  exit 2
fi
command -v flock >/dev/null
antimatter_repo_root=$(cd "$1" && pwd -P)
antimatter_state_root=$2
mkdir -p "$antimatter_state_root"
antimatter_state_root=$(cd "$antimatter_state_root" && pwd -P)
case "$antimatter_state_root/" in
  "$antimatter_repo_root/"*)
    echo 'State directory must be outside the public checkout.' >&2
    exit 2
    ;;
esac
antimatter_round_runner="$antimatter_repo_root/scripts/run_ai_round.sh"
if [[ ! -f "$antimatter_round_runner" ]]; then
  echo 'The checkout must contain scripts/run_ai_round.sh.' >&2
  exit 2
fi

# Every invocation for this checkout must use this same private state root.
# The existing one-round wrapper separately holds round.lock while working.
exec 8> "$antimatter_state_root/continuous.lock"
if ! flock -n 8; then
  echo 'Another continuous runner owns this state directory.' >&2
  exit 75
fi

antimatter_completed_rounds=0
while :; do
  set +e
  # The child must not retain the continuous lock if its parent exits.
  bash "$antimatter_round_runner" "$antimatter_repo_root" "$antimatter_state_root" 8>&-
  antimatter_round_exit=$?
  set -e
  if [[ $antimatter_round_exit -ne 0 ]]; then
    printf 'Continuous runner halted after %s completed invocations; round exit status: %s.\n' \
      "$antimatter_completed_rounds" "$antimatter_round_exit" >&2
    exit "$antimatter_round_exit"
  fi
  antimatter_completed_rounds=$((antimatter_completed_rounds + 1))
  printf 'Verified completed invocation: %s.\n' "$antimatter_completed_rounds"
  if [[ $antimatter_max_rounds -gt 0 && $antimatter_completed_rounds -ge $antimatter_max_rounds ]]; then
    printf 'Bounded validation finished after %s completed invocations.\n' "$antimatter_completed_rounds"
    exit 0
  fi
done
