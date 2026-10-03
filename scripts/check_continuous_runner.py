#!/usr/bin/env python3
"""Exercise orchestration with a fake one-round wrapper; never invoke Codex."""

import fcntl
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parent
LOOP = PACKAGE / "run_ai_continuously.sh"
OUTPUT = Path(tempfile.mkdtemp(prefix="antimatter-continuous-proof."))
MOCK_WRAPPER = """#!/usr/bin/env bash
set -euo pipefail
count_file="$2/mock-invocations.txt"
count=0
if [[ -f "$count_file" ]]; then read -r count < "$count_file"; fi
count=$((count + 1))
printf '%s\\n' "$count" > "$count_file"
if [[ ${MOCK_SIGNAL_ON:-0} -eq $count ]]; then kill -TERM "$BASHPID"; fi
if [[ ${MOCK_FAIL_ON:-0} -eq $count ]]; then exit "${MOCK_EXIT_STATUS:-47}"; fi
printf 'Mock verified checkpoint %s\\n' "$count"
"""


class ContinuousLoopTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="mock-fixture-", dir=OUTPUT)
        self.root = Path(self.temp.name)
        self.repo = self.root / "checkout"
        self.state = self.root / "private-state"
        (self.repo / "scripts").mkdir(parents=True)
        self.state.mkdir(mode=0o700)
        (self.repo / "scripts/run_ai_round.sh").write_text(MOCK_WRAPPER)
        self.env = dict(os.environ)
        self.env.update(ANTIMATTER_CODEX_MODEL="mock-model-not-real", MAX_ROUNDS="2")

    def tearDown(self):
        self.temp.cleanup()

    def invoke(self, *, env=None, state=None, args=None):
        return subprocess.run(
            ["bash", str(LOOP)] + (args if args is not None else [str(self.repo), str(state or self.state)]),
            env=self.env if env is None else env,
            capture_output=True,
            text=True,
            timeout=5,
        )

    def count(self):
        path = self.state / "mock-invocations.txt"
        return int(path.read_text()) if path.exists() else 0

    def test_two_bounded_successful_invocations(self):
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.count(), 2)
        self.assertIn("Bounded validation finished after 2", result.stdout)
        self.assertEqual((self.state / "mock-invocations.txt").stat().st_mode & 0o777, 0o600)
        self.assertEqual((self.state / "continuous.lock").stat().st_mode & 0o777, 0o600)

    def test_one_bounded_successful_invocation(self):
        self.env["MAX_ROUNDS"] = "1"
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.count(), 1)

    def test_first_failure_exit_status_is_preserved(self):
        self.env.update(MOCK_FAIL_ON="1", MOCK_EXIT_STATUS="47")
        result = self.invoke()
        self.assertEqual(result.returncode, 47)
        self.assertEqual(self.count(), 1)
        self.assertIn("halted after 0 completed invocations", result.stderr)

    def test_failure_after_success_is_preserved(self):
        self.env.update(MOCK_FAIL_ON="2", MOCK_EXIT_STATUS="42")
        result = self.invoke()
        self.assertEqual(result.returncode, 42)
        self.assertEqual(self.count(), 2)
        self.assertIn("halted after 1 completed invocations", result.stderr)

    def test_default_unbounded_mode_stops_at_failure(self):
        self.env.pop("MAX_ROUNDS")
        self.env.update(MOCK_FAIL_ON="3", MOCK_EXIT_STATUS="61")
        result = self.invoke()
        self.assertEqual(result.returncode, 61)
        self.assertEqual(self.count(), 3)
        self.assertIn("halted after 2 completed invocations", result.stderr)

    def test_child_signal_status_is_preserved(self):
        self.env["MOCK_SIGNAL_ON"] = "1"
        result = self.invoke()
        self.assertEqual(result.returncode, 143)
        self.assertEqual(self.count(), 1)

    def test_second_continuous_writer_is_rejected(self):
        with (self.state / "continuous.lock").open("w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = self.invoke()
        self.assertEqual(result.returncode, 75)
        self.assertEqual(self.count(), 0)

    def test_invalid_bounds_are_rejected_before_invocation(self):
        for value in ["-1", "2.5", "02", "1000000000", "two"]:
            with self.subTest(value=value):
                self.env["MAX_ROUNDS"] = value
                result = self.invoke()
                self.assertEqual(result.returncode, 2)
                self.assertEqual(self.count(), 0)

    def test_missing_model_is_rejected_before_invocation(self):
        self.env.pop("ANTIMATTER_CODEX_MODEL")
        result = self.invoke()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.count(), 0)

    def test_missing_wrapper_is_rejected(self):
        (self.repo / "scripts/run_ai_round.sh").unlink()
        result = self.invoke()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.count(), 0)

    def test_public_checkout_cannot_hold_private_state(self):
        result = self.invoke(state=self.repo / "private-state")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.count(), 0)

    def test_wrong_argument_count_is_rejected(self):
        for args in [[], [str(self.repo)], [str(self.repo), str(self.state), "extra"]]:
            with self.subTest(args=args):
                result = self.invoke(args=args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(self.count(), 0)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ContinuousLoopTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    receipt = {
        "status": "passed" if result.wasSuccessful() else "failed",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "method": "Temporary Linux fixtures using a mock scripts/run_ai_round.sh",
        "actual_model_invocations": 0,
        "external_host_validated": False,
        "service_installed_or_started": False,
        "scope": "Loop orchestration, exit propagation, bounded repetition, permissions, and lock exclusion",
        "limits": "Mock success does not validate authentication, model availability, checkpoint science, publication, or 24/7 operation",
    }
    (OUTPUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "tests": result.testsRun, "receipt": str(OUTPUT / "receipt.json")}))
    raise SystemExit(0 if result.wasSuccessful() else 1)
