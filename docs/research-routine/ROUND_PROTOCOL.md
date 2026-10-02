# Repeated Antimatter research rounds

This repository supplies a research prompt, persistent queue and numerical
reproduction workflow. It does not launch a continuous AI researcher.
No recurring AI scheduler was callable in the originating cloud session.
The Codex CLI was present and its non-interactive interface was inspected;
a persistent external host, valid authentication and the requested model mapping
have not been validated. No AI schedule is active.

The first completed round is
[`2026-10-01_transport_gate`](../../research/rounds/2026-10-01_transport_gate/README.md).
It supplies conserved-charge and signed-response controls for an illustrative
network. The physical candidate source and reaction content remain open.

## Each research round

1. Read `routine.json`, the latest completed round and the current Git/PR state.
   Record the baseline full commit SHA. If a prior round is marked running,
   inspect its checkpoint and owner before continuing; do not overlap writers.
2. Choose one ranked question and a bounded deliverable. Record the assumptions,
   input hashes, intended method and controls before a fresh numerical scan.
   Use a new round directory; preserve earlier results and negative findings.
3. Execute, diagnose failures, and independently verify important claims. Record
   numerical checks separately from physical validity and external peer review.
4. Write a result note, code, inputs/provenance, evidence and next test. Check
   privacy and claims before pushing a new public draft or updating a draft PR.
5. Advance the queue and commit the durable record only after evidence review.
   Report blocked, failed and completed outcomes distinctly. A human-reviewed
   merge and authenticated archival publication remain separate events.

Future rounds should use the model preference in `routine.json`: GPT-6.1 Sol
with Ultra reasoning effort. A prompt does not change the active model; the
launcher must select it and confirm availability. Use the existing isolated
checkouts; do not create a Git worktree unless Ricardo explicitly requests one.

## Scheduling

The requested external AI routine is completion-driven: start the next bounded
round after a completed, validated, committed checkpoint, with one active writer.
Failed, blocked, timed-out or incomplete rounds stop the chain for diagnosis.
Each round must checkpoint and return; an indefinite chat turn or background process in an ephemeral cloud task is not
a durable scheduler. The queue and prompt can be resumed manually in any future
authorized session. No research round should recursively launch itself.

To activate actual AI rounds, a persistent Codex task runner must be connected to
this repository, supplied with usable authentication and configured to invoke
ROUND_PROMPT.md using the requested model/effort. Set its concurrency to one and
its bounded runtime to 60 minutes. Its job history must verify a first completed
invocation and a subsequent scheduled invocation before claiming unattended
operation. Choosing a runner, connecting it, and validating that history remain
outside the capabilities verified in this cloud chat.

`scripts/run_ai_round.sh` is a concrete external Linux runner template. Its
shell syntax, the installed Codex CLI interface and 20 mocked checkpoint/stop
scenarios were checked; authenticated model execution, model-ID mapping, and persistence on an external host have
not been tested. It requires Codex, `flock`, `timeout`, a clean checkout, an
already authenticated runner and a persistent state directory outside the
public checkout. Set the non-secret `ANTIMATTER_CODEX_MODEL` to the runner's
verified identifier for GPT-6.1 Sol. The template requests Ultra effort, permits
one active invocation, limits it to 60 minutes, and preserves private logs with
restricted permissions. It installs no cron or service and was not launched.
Do not publish its logs; private references may appear in model events.

First validate one manual invocation on the persistent host:

```bash
bash scripts/run_ai_round.sh /absolute/AntiMatter /absolute/private-run-state
```

After validating authentication, the requested model/effort and that first round,
a persistent host can run successive rounds with:

```bash
while bash scripts/run_ai_round.sh /absolute/AntiMatter /absolute/private-run-state; do :; done
```

The wrapper stops on a concurrent owner, nonzero CLI exit, timeout, missing new
round, non-passing receipt, incorrect predecessor, uncommitted work, history
rewind or nonportable/symlink pointers. A checkpoint must be tracked and descend
from the invocation baseline. Reproduce the mock-only controls with
`python scripts/check_ai_runner.py`; it does not call the actual Codex CLI.
It checks structural evidence and recorded validation; scientific review and remote
publication receipts still require the round's own checks. This loop has not been
launched in the cloud chat and does not survive a host shutdown without a real
service manager.

Unavailable model/effort, unusable authentication, dirty work or timeout must be
diagnosed before enabling repeated execution. Do not silently change the model
or override another round. The scheduler must read the completed scientific
record; a zero CLI exit alone is not a result or publication receipt.

The included GitHub Actions workflow runs **verification only** (public
numerical checks and mocked runner controls): manual and relevant PR triggers, plus `17 */4 * * *` UTC, around six runs per day. GitHub
schedules are approximate and can be delayed. The cron becomes eligible only
after the workflow reaches the default branch and Actions are enabled. An open
draft PR does not activate it. GitHub can disable inactive repository schedules;
check job history rather than assuming uninterrupted 24/7 service.

## Numerical check runner

Install the exact dependencies in `research/AM1231/requirements-replay.txt`, then:

```bash
python scripts/reproduce_candidate.py
```

Use the pinned virtual environment in cloud tasks. The script verifies the 48
baseline and 40 candidate ledger entries, copies only the public candidate to a
new temporary directory, executes its seven reproduction steps, compares five
producer files and writes receipts/logs. [Portable comparisons](PORTABLE_REPRODUCTION.md) distinguish byte equality
from exact structured scientific data and explicitly bounded observations.
Only explicitly listed metadata, spectral/endpoint values and diagnostics can vary under the documented gates, after all original independent comparisons
pass. The documentation identifies new archival portability gates separately
from the original registered criteria. Unexpected differences fail, and every
difference is retained in the receipt. Preserved files are never rewritten.
It does not modify release files, scan the private archive, call AI, search literature, push commits, deploy
the website or publish to Zenodo. The workflow has read-only repository permission
and uses no research/publication credentials. Logs and receipts contain public
calculation evidence; private reference files never enter the artifact upload.

Checksum failure, a failed calculation/comparison, changed producer output or a
timeout is a failed run. Do not alter preserved outputs to make it pass. The
GitHub-hosted numerical and transport execution passed in run
[36972300414](https://github.com/maldonado-research/AntiMatter/actions/runs/36972300414)
at commit `de73cc9e3124ddb2a6d365311a55b8222c1a986f`. Its evidence is separate from
the local replay and any future runtime activation.
The workflow also checks the completed transport round in its own temporary copy:
nine producer tests, 71 independent controls, 11 comparisons and provenance checks.
Its nine/71 checks and all 201 trajectory samples pass in the pinned local
environment and the cited hosted run; check subsequent outcomes in job history.

## Durable round record

Each `research/rounds/<round_id>/` contains a result note, reproducible code,
locally recorded pre-run plan when applicable, result receipt and SHA256SUMS.txt.
The note states the baseline and requested/verified model configuration, the
question, explicit assumptions, input provenance, conclusions and limitations.
Use public source links; private raw references remain in their authorized
archive. Each new ROUND.json names its predecessor, status, next_question and
validation_receipt (a path inside the round, whose JSON has status="passed" or
passed=true). Immutable receipts preserve negative or blocked outcomes; `routine.json` points to the
latest completed record. Scheduler ownership/leases live in the external runner,
not as a pretend active lock in a committed JSON file.

Scientific release v1.23.1 and the v1.23.2 candidate remain distinct. A passing
reproduction job says that the calculation is reproducible; it does not establish
the source/operator, a physical CP mechanism, a final baryon yield or novelty.
