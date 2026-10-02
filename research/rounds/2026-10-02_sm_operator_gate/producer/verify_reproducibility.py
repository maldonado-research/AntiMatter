#!/usr/bin/env python3
"""Rerun diagnostics, require identical output bytes, and write receipt/ledger."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUTS = (
    "results.json", "species_response.csv", "reaction_charges.csv",
    "conserved_density_basis.csv", "tests.csv", "conditional_sensitivity.json",
    "conditional_sensitivity.csv", "PROVENANCE.json",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script):
    result = subprocess.run([sys.executable, str(HERE / script)], cwd=HERE, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"{script} failed ({result.returncode}): {result.stderr}")
    return {"script": script, "exit_code": result.returncode, "stdout": result.stdout.strip()}


def main():
    # Refresh outputs once, including provenance hashes of final registrations.
    first = [run("sm_charge_diagnostic.py"), run("conditional_sensitivity.py")]
    hashes_before = {name: digest(HERE / name) for name in OUTPUTS}
    second = [run("sm_charge_diagnostic.py"), run("conditional_sensitivity.py")]
    hashes_after = {name: digest(HERE / name) for name in OUTPUTS}
    if hashes_before != hashes_after:
        raise AssertionError("scientific/provenance output bytes changed between identical runs")
    result = json.loads((HERE / "results.json").read_text())
    sensitivity = json.loads((HERE / "conditional_sensitivity.json").read_text())
    if not all(test["passed"] for test in result["tests"] + sensitivity["tests"]):
        raise AssertionError("failed registered control")
    receipt = {
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "dependencies": "Python standard library only; no dependency or repository edits",
        "first_verification_runs": first,
        "second_verification_runs": second,
        "registered_primary_controls_passed": result["test_count"],
        "registered_conditional_controls_passed": sensitivity["test_count"],
        "total_controls_passed": result["test_count"] + sensitivity["test_count"],
        "reproduced_output_sha256": hashes_after,
        "byte_identical_second_run": True,
        "resolved_initial_attempt": "conditional_sensitivity first run used wrong ancestor index and failed with FileNotFoundError; replaced with public-parent ancestor discovery; all subsequent checks pass",
        "independent_comparison": "separate 16-species solver agrees on exact source coefficient and reduced chemical potentials; structured cross-comparison is retained under independent/",
        "independence_limit": "independent coefficient message arrived after producer implementation but before producer first execution; not fully blinded execution",
        "scientific_limits": [
            "conventional symmetric-SM equilibrium benchmark with explicitly assumed coefficient",
            "no Wilson operator or UV matching derivation",
            "no physical yield at 131.7 GeV or frozen-model coefficient replacement",
            "small fermionic chemical potentials, Higgs thermal stability, and rapid relaxation required",
            "no autonomous driver, physical CP-odd invariant, or hypermagnetic transport derived",
        ],
    }
    (HERE / "RECEIPT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    entries = sorted(p for p in HERE.rglob("*") if p.is_file() and p != HERE / "SHA256SUMS")
    (HERE / "SHA256SUMS").write_text("".join(f"{digest(path)}  {path.relative_to(HERE).as_posix()}\n" for path in entries))
    print(json.dumps({"controls_passed": receipt["total_controls_passed"], "byte_identical_output_files": len(OUTPUTS), "ledger_files": len(entries)}, sort_keys=True))


if __name__ == "__main__":
    main()
