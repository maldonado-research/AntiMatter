#!/usr/bin/env python3
"""Replay the sensitivity worker using temporary public checkout contexts."""

import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import conditional_normalization_sensitivity as sensitivity


OUT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = sensitivity.resolve_public_source()
    before = json.loads((OUT/"portability_provenance.json").read_text())
    current = json.loads((OUT/"sensitivity_receipt.json").read_text())
    checks = []

    def check(name, passed):
        checks.append({"name": name, "passed": bool(passed)})
        if not passed:
            raise AssertionError(name)

    check("sensitivity_values_unchanged", current["values"] == before["pre_portability_sensitivity_values"])
    check("seven_sensitivity_checks_pass", len(current["checks"]) == 7
          and all(item["passed"] is True for item in current["checks"]))
    check("source_path_repo_relative", current["source_path"] == sensitivity.SOURCE_RELATIVE.as_posix()
          and not Path(current["source_path"]).is_absolute())
    untouched = ("provenance_note.json", "CONTROLS.md", "SENSITIVITY_CONTROLS.md",
                 "sm_charge_response.py", "receipt.json", "matrices.json")
    check("primary_controls_results_and_original_provenance_unchanged",
          all(digest(OUT/name) == before["pre_portability_sha256"][name] for name in untouched))
    actual_versions = {name: version(name) for name in sensitivity.ANALYSIS_DEPENDENCIES}
    check("declared_dependency_versions_match_replay", actual_versions == sensitivity.ANALYSIS_DEPENDENCIES)

    with tempfile.TemporaryDirectory(prefix="antimatter-charge-portability-") as temp:
        tmp = Path(temp)
        checkout = tmp/"public-checkout"
        relocated_source = checkout/sensitivity.SOURCE_RELATIVE
        relocated_source.parent.mkdir(parents=True)
        shutil.copy2(source, relocated_source)
        outside = tmp/"outside-checkout"
        outside.mkdir()
        replay = outside/"independent"
        replay.mkdir()
        for name in ("conditional_normalization_sensitivity.py", "SENSITIVITY_CONTROLS.md"):
            shutil.copy2(OUT/name, replay/name)
        explicit_env = os.environ.copy()
        explicit_env["ANTIMATTER_PUBLIC_REPO"] = str(checkout)
        explicit = subprocess.run([sys.executable, str(replay/"conditional_normalization_sensitivity.py")],
                                  cwd=outside, env=explicit_env, capture_output=True, text=True)
        check("explicit_env_temporary_context_pass", explicit.returncode == 0)
        explicit_receipt = json.loads((replay/"sensitivity_receipt.json").read_text())
        check("temporary_explicit_receipt_identical", explicit_receipt == current)

        nested = checkout/"research"/"temporary-round"/"independent"
        nested.mkdir(parents=True)
        for name in ("conditional_normalization_sensitivity.py", "SENSITIVITY_CONTROLS.md"):
            shutil.copy2(OUT/name, nested/name)
        discovery_env = os.environ.copy()
        discovery_env.pop("ANTIMATTER_PUBLIC_REPO", None)
        discovered = subprocess.run([sys.executable, str(nested/"conditional_normalization_sensitivity.py")],
                                    cwd=outside, env=discovery_env, capture_output=True, text=True)
        check("verified_script_ancestor_context_pass", discovered.returncode == 0)
        discovered_receipt = json.loads((nested/"sensitivity_receipt.json").read_text())
        check("temporary_ancestor_receipt_identical", discovered_receipt == current)

        cwd_discovered = subprocess.run([sys.executable, str(replay/"conditional_normalization_sensitivity.py")],
                                        cwd=nested, env=discovery_env, capture_output=True, text=True)
        check("verified_cwd_ancestor_context_pass", cwd_discovered.returncode == 0)
        check("temporary_cwd_receipt_identical", json.loads((replay/"sensitivity_receipt.json").read_text()) == current)

        invalid_env = explicit_env.copy()
        invalid_env["ANTIMATTER_PUBLIC_REPO"] = str(tmp/"missing-checkout")
        missing = subprocess.run([sys.executable, str(replay/"conditional_normalization_sensitivity.py")],
                                 cwd=outside, env=invalid_env, capture_output=True, text=True)
        check("missing_explicit_context_rejected", missing.returncode != 0
              and "Cannot locate the frozen public source" in missing.stderr)
        relocated_source.write_text(relocated_source.read_text()+"\n# temporary mismatch control\n")
        mismatch = subprocess.run([sys.executable, str(replay/"conditional_normalization_sensitivity.py")],
                                  cwd=outside, env=explicit_env, capture_output=True, text=True)
        check("wrong_public_source_hash_rejected", mismatch.returncode != 0
              and "Public source hash differs" in mismatch.stderr)

    receipt = {
        "status": "PASS", "study_type": "post-run portability replay only",
        "check_count": len(checks), "checks": checks,
        "declared_analysis_dependencies": sensitivity.ANALYSIS_DEPENDENCIES,
        "replay_dependency_versions": actual_versions,
        "replay_code_sha256": digest(Path(__file__)),
        "portable_sensitivity_code_sha256": digest(OUT/"conditional_normalization_sensitivity.py"),
        "portable_sensitivity_receipt_sha256": digest(OUT/"sensitivity_receipt.json"),
        "pre_portability_provenance_sha256": digest(OUT/"portability_provenance.json"),
        "source_sha256": sensitivity.EXPECTED_SOURCE_SHA256,
        "temporary_contexts": "temporary copies only; removed after replay",
        "limitation": "No primary scientific computation, source assumption, or sensitivity value changed.",
    }
    (OUT/"portability_receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps({"status": "PASS", "check_count": len(checks),
                      "sensitivity_numeric_values": "unchanged",
                      "dependency_versions": actual_versions}, indent=2))


if __name__ == "__main__":
    main()
