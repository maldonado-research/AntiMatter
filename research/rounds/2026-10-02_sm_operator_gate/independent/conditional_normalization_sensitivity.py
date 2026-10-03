#!/usr/bin/env python3
"""Read historical literals without execution; bounded normalization sensitivity."""

import ast
import hashlib
import json
import os
from pathlib import Path

import sympy as sp


OUT = Path(__file__).resolve().parent
SOURCE_RELATIVE = Path("research/AM1231/v1.23.1/v1.23.1_efficiency_energy_frontier.py")
EXPECTED_SOURCE_SHA256 = "4a2bfece249ef634986256b45b75fc8ab89a147d16673972e5565aeca24fe3a9"
ANALYSIS_DEPENDENCIES = {"sympy": "1.14.0", "mpmath": "1.3.0"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_public_source():
    """Explicit context takes precedence; otherwise verify a checkout ancestor."""
    configured = os.environ.get("ANTIMATTER_PUBLIC_REPO")
    if configured:
        candidates = [Path(configured).expanduser().resolve()]
    else:
        current = Path.cwd().resolve()
        candidates = list(dict.fromkeys([OUT, *OUT.parents, current, *current.parents]))
    for root in candidates:
        source = root / SOURCE_RELATIVE
        if not source.is_file():
            continue
        if digest(source) != EXPECTED_SOURCE_SHA256:
            raise RuntimeError("Public source hash differs from the frozen historical input")
        return source
    raise RuntimeError("Cannot locate the frozen public source; set ANTIMATTER_PUBLIC_REPO to its repository root")


def main():
    controls = OUT / "SENSITIVITY_CONTROLS.md"
    if not controls.exists():
        raise RuntimeError("Missing sensitivity controls")
    source = resolve_public_source()
    raw = source.read_text()
    tree = ast.parse(raw)
    literals = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        try:
            value = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                literals[target.id] = value
            elif isinstance(target, ast.Tuple):
                for subtarget, item in zip(target.elts, value):
                    if isinstance(subtarget, ast.Name):
                        literals[subtarget.id] = item
    rational = lambda x: sp.Rational(str(x))
    ratio_old = rational(literals["FROZEN"]["WE_A_required_over_A"])
    winding0 = rational(literals["N0"])
    c_legacy = rational(literals["C_SPH"])
    entropy_dof = rational(literals["G_STAR"])
    c_ideal = sp.Rational(72, 79)/(2*sp.pi**2*entropy_dof/45)
    response_ratio = c_ideal/c_legacy
    threshold_old = winding0*sp.sqrt(ratio_old)
    threshold_new = threshold_old/response_ratio
    eta_old, eta_new = threshold_old/49, threshold_new/49
    n_old, n_new = int(sp.ceiling(threshold_old)), int(sp.ceiling(threshold_new))

    def energy_ratio(n, eta=1):
        return ratio_old*(winding0/(n*eta*response_ratio))**2

    checks = [
        ("literal_input_values", ratio_old == sp.Rational("9.35462209607388")
         and winding0 == 16 and c_legacy == sp.Rational("0.0195") and entropy_dof == sp.Rational("106.75")),
        ("historical_required_efficiency_rounding", abs(sp.N(eta_old, 40)-sp.Rational("0.9987045454")) < sp.Rational("0.0000000001")),
        ("ideal_coefficient_lower_than_legacy", bool(sp.N(response_ratio, 40) < 1)),
        ("required_efficiency_increases", bool(sp.N(eta_new, 40) > sp.N(eta_old, 40))),
        ("conditional_winding_minimum", n_old == 49 and n_new == 50),
        ("integer_energy_inequality_and_predecessor", bool(sp.N(energy_ratio(n_new), 40) <= 1)
         and bool(sp.N(energy_ratio(n_new-1), 40) > 1)),
        ("boundary_energy_equality", sp.simplify(energy_ratio(49, eta_new)-1) == 0),
    ]
    values = {
        "ideal_response_C_exact": str(c_ideal), "ideal_response_C": str(sp.N(c_ideal, 35)),
        "legacy_response_C": str(c_legacy), "C_ideal_over_C_legacy": str(sp.N(response_ratio, 35)),
        "fractional_response_shift": str(sp.N(response_ratio-1, 35)),
        "old_continuous_one_A_threshold": str(sp.N(threshold_old, 35)),
        "new_continuous_one_A_threshold": str(sp.N(threshold_new, 35)),
        "old_required_eta_at_n49": str(sp.N(eta_old, 35)),
        "new_required_eta_at_n49": str(sp.N(eta_new, 35)),
        "old_minimum_n_at_eta1": n_old, "new_minimum_n_at_eta1": n_new,
        "conditional_new_kinetic_over_A_at_n49_eta1": str(sp.N(energy_ratio(49), 35)),
        "conditional_new_kinetic_over_A_at_n50_eta1": str(sp.N(energy_ratio(50), 35)),
    }
    receipt = {
        "status": "PASS" if all(bool(passed) for _, passed in checks) else "FAILED",
        "study_type": "post-primary conditional normalization sensitivity",
        "source_path": SOURCE_RELATIVE.as_posix(), "source_sha256": digest(source),
        "controls_sha256": digest(controls), "code_sha256": digest(Path(__file__)),
        "declared_analysis_dependencies": ANALYSIS_DEPENDENCIES,
        "arithmetic": "exact symbolic expressions with 40-digit comparisons",
        "checks": [{"name": name, "passed": bool(passed)} for name, passed in checks],
        "values": values,
        "limitation": "Massless symmetric-phase ideal coefficient is not a correction at broken-phase T=131.7 GeV; historic EFT coefficient and scalar history remain assumptions.",
    }
    (OUT / "sensitivity_receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps({"status": receipt["status"], **values}, indent=2))
    if receipt["status"] != "PASS":
        raise AssertionError("Sensitivity control failure")


if __name__ == "__main__":
    main()
