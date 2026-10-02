# Continuous runner: inactive Linux deployment package

This package prepares completion-driven research rounds on a persistent Linux host. Nothing was installed, enabled, or launched on an external host. No host, SSH access, Mac access, scheduler API, or verified model ID is assumed. This cloud workspace is temporary and does not establish 24/7 service.

The requested model remains **GPT-6.1 Sol with Ultra reasoning**. Obtain the exact model ID from the authenticated runner's available configuration and verify that it supports Ultra. The prompt cannot switch models. Do not replace this preference silently or treat the placeholder as an available model.

`scripts/run_ai_continuously.sh` calls the checkout's existing `scripts/run_ai_round.sh` again only after it exits successfully. That wrapper requires a new committed checkpoint, a passed validation receipt, a next question, and a clean checkout. The loop preserves any failing exit status and stops. `MAX_ROUNDS=2` bounds initial validation; `MAX_ROUNDS=0`, the default, continues until a failure or manual stop. `Restart=no` prevents automatic retries within the current user-manager lifecycle; an enabled unit can start again at reboot or user-manager restart.

## Prerequisites on the persistent host

- A Linux account with systemd user services and a persistent filesystem.
- An already authenticated Codex CLI compatible with the checkout's wrapper, the verified requested model/effort, and its required network access.
- Bash, Git, `flock`, GNU `timeout`, and the validated Python 3.12.14
  research environment with the pinned baseline and operator dependencies.
- A clean Antimatter checkout containing the current research routine and `scripts/run_ai_round.sh`.
- One private persistent state directory outside the public checkout. **All runners for this checkout must use the same state directory.** The loop and one-round wrapper locks prevent concurrent work only when this requirement is followed.

Keep authentication on the host through its supported login mechanism. Do not copy credentials into this package, the environment file, the repository, or logs. No tokens or secrets are included here.

## Validate two real invocations before enabling repetition

Transfer this package to the chosen host using your normal secure deployment method. Replace the path placeholders below with persistent absolute paths; these examples use paths without spaces.

```bash
repo_dir='/ABSOLUTE_PATH_TO_CHECKOUT'
package_dir='/ABSOLUTE_PATH_TO_RUNNER_PACKAGE'
state_dir='/ABSOLUTE_PRIVATE_STATE_DIRECTORY'
config_dir='/ABSOLUTE_PRIVATE_CONFIG_DIRECTORY'
install -d -m 700 "$state_dir" "$config_dir"
chmod 700 "$package_dir" "$package_dir/run_ai_continuously.sh"
codex --version
codex login status
git -C "$repo_dir" status --short
export ANTIMATTER_CODEX_MODEL='REPLACE_WITH_VERIFIED_GPT_6_1_SOL_MODEL_ID'
MAX_ROUNDS=2 bash "$package_dir/run_ai_continuously.sh" "$repo_dir" "$state_dir"
```

The wrapper launches real, potentially long running research only when that last command is executed on the configured host. A successful bounded run must produce **two different completed checkpoints**. Inspect the two new private `round.*/checkpoint-guard.json` files and verify different round identifiers and descendant commit hashes. Each invocation's `cli-exit-code.txt` and `exit-code.txt` must be `0`. Review its `final.md`, committed `ROUND.json`, and validation receipt, including the next question and scientific limitations. For a pause after the first invocation, use `MAX_ROUNDS=1`, inspect it, then run the same bounded command again.

If authentication, model selection, scientific validation, cleanliness, or timeout blocks a round, the loop stops with that failure status and retains private evidence. Diagnose and preserve the work before another launch. Wrapper success establishes a structural checkpoint; it does not establish a breakthrough, remote GitHub publication, or Zenodo publication. Continue the repository's review and publication workflow and verify remote changes separately.

## Optional systemd user service

After real bounded validation passes, copy `docs/research-routine/deployment/runner.env.example` to `$config_dir/runner.env` and set its verified model ID, the actual directory containing `codex` in `PATH`, and `MAX_ROUNDS=0`. The file contains configuration only; keep it mode `600`.

Render `docs/research-routine/deployment/antimatter-research.service.in` as `antimatter-research.service`, replacing every `/ABSOLUTE_...` placeholder. Check `/usr/bin/bash` against `command -v bash` and change the unit's executable path if needed. The configured state directory must already exist with mode `700`; stdout/stderr and detailed model events remain private there. Do not publish those logs or private source material.

The following commands are for the configured persistent host; they were **not executed here**. Preserve any existing unit/configuration before installing this unit.

```bash
chmod 600 "$config_dir/runner.env"
systemd-analyze --user verify "$package_dir/antimatter-research.service"
install -d -m 700 "$HOME/.config/systemd/user"
install -m 600 "$package_dir/antimatter-research.service" "$HOME/.config/systemd/user/antimatter-research.service"
systemctl --user daemon-reload
systemctl --user enable --now antimatter-research.service
systemctl --user status antimatter-research.service
```

For operation after logout or reboot, the host owner must configure user lingering, for example `loginctl enable-linger "$(id -un)"` where that host permits it. Verify boot persistence on that host; enabling a unit does not prove persistence. Monitor service status, private checkpoint receipts, authentication, and host availability. Continuous completion is not guaranteed through outages, limits, or scientific blockers.

To stop: `systemctl --user stop antimatter-research.service`. To prevent another boot/user-manager launch while diagnosing a failure, use `systemctl --user disable --now antimatter-research.service`. After reviewing its evidence and resolving the blocker, explicitly enable/start it again. `Restart=no` alone is not a persistent failure latch.

## Validation performed in this workspace

`python scripts/check_continuous_runner.py` passed 12 tests using temporary mock one-round wrappers. They cover two bounded successes, one success, default unbounded continuation until failure, exact failure/signal status propagation, competing loop exclusion, argument/bound/model checks, private file modes, and rejecting private state inside the checkout. No actual Codex invocation occurred. See `MOCK_VALIDATION_RECEIPT.json` for the precise scope and unverified capabilities.

The checkout's one-round checkpoint guard was reviewed separately; these mock tests verify only the added orchestration layer. `BASELINE_RUNNER_REFERENCE.json` identifies the exact existing wrapper observed. Independent review adds orchestration and inactive-unit checks; see `INDEPENDENT_REVIEW_RECEIPT.json`. Authentication, requested model/effort execution, external systemd installation, GitHub/Zenodo publication, and uninterrupted host operation remain untested by this package.

For the repository layout, set the unit runner-package placeholder to the checkout’s `scripts/` directory. The environment PATH must include the checkout’s `.venv/bin` and the real Codex executable directory. Service installation commands are templates for the selected external host, not cloud startup commands.
