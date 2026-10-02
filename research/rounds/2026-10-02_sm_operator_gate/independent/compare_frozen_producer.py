#!/usr/bin/env python3
"""Post-completion strict-schema comparison of reduced and full outputs.

This is a cross-check after both primary implementations were frozen and run.
It is not part of the blinded independent primary calculation.
"""

import hashlib
import json
from pathlib import Path
import re

import sympy as sp


OUT = Path(__file__).resolve().parent
PRODUCER = OUT.parent / "producer" / "results.json"
EXPECTED_FULL = [f"{a}{i}" for i in range(1, 4) for a in ("q", "u", "d", "l", "e")]+["H"]
EXPECTED_REDUCED = ["q", "u", "d", "l_e", "l_mu", "l_tau", "e_e", "e_mu", "e_tau", "H"]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rat(value):
    if isinstance(value, int) and not isinstance(value, bool):
        return sp.Rational(value)
    if not isinstance(value, str) or re.fullmatch(r"-?\d+(?:/[1-9]\d*)?", value) is None:
        raise ValueError("Expected an integer or strict rational string")
    parts = value.split("/")
    return sp.Rational(int(parts[0]), int(parts[1]) if len(parts) == 2 else 1)


def mat(value, rows, cols):
    if not isinstance(value, list) or len(value) != rows or any(not isinstance(row, list) or len(row) != cols for row in value):
        raise ValueError(f"Expected a {rows} x {cols} matrix")
    return sp.Matrix([[rat(cell) for cell in row] for row in value])


def vec(value, length):
    if not isinstance(value, list) or len(value) != length:
        raise ValueError(f"Expected a length-{length} list")
    return sp.Matrix([rat(cell) for cell in value])


def main():
    independent_path = OUT / "matrices.json"
    independent_receipt_path = OUT / "receipt.json"
    full = json.loads(independent_path.read_text())
    producer = json.loads(PRODUCER.read_text())
    receipt = json.loads(independent_receipt_path.read_text())
    if full["species_order"] != EXPECTED_FULL or producer["species"] != EXPECTED_REDUCED:
        raise ValueError("Unexpected species schema/order")
    if full["charge_columns"] != ["Y", "Delta_1", "Delta_2", "Delta_3"]:
        raise ValueError("Unexpected independent charge-column schema")
    for key in ("Y", "Delta_e", "Delta_mu", "Delta_tau", "B", "L", "B_plus_L"):
        if key not in producer["charge_rows"]:
            raise ValueError("Missing producer charge row")
    if receipt["status"] != "PASS" or receipt["check_count"] != 24:
        raise ValueError("Independent primary receipt not passed")
    for key, path in (("controls_sha256", OUT/"CONTROLS.md"),
                      ("code_sha256", OUT/"sm_charge_response.py"),
                      ("matrices_sha256", independent_path)):
        if receipt[key] != sha256(path):
            raise ValueError("Independent artifact hash mismatch")
    producer_tests = producer["tests"]
    if not isinstance(producer_tests, list) or producer["test_count"] != len(producer_tests):
        raise ValueError("Producer test-count schema mismatch")
    if any(not isinstance(test, dict) or not isinstance(test.get("test"), str)
           or test.get("passed") is not True for test in producer_tests):
        raise ValueError("Producer tests contain a failed or malformed check")
    if len({test["test"] for test in producer_tests}) != len(producer_tests):
        raise ValueError("Producer tests contain duplicate names")

    w16 = sp.diag(*vec(full["susceptibility_weights_T2_over_6"], 16))
    w10 = sp.diag(*vec(producer["susceptibility_diagonal_in_T2_over_6"], 10))
    c16 = mat(full["charge_matrix"], 16, 4)
    c10 = sp.Matrix.hstack(*(vec(producer["charge_rows"][key], 10) for key in
                           ("Y", "Delta_e", "Delta_mu", "Delta_tau")))
    e = sp.zeros(16, 10)
    reduced_index = {name: k for k, name in enumerate(EXPECTED_REDUCED)}
    flavors = {1: "e", 2: "mu", 3: "tau"}
    for k, name in enumerate(EXPECTED_FULL):
        if name == "H":
            reduced_name = "H"
        elif name[0] in ("q", "u", "d"):
            reduced_name = name[0]
        else:
            reduced_name = name[0]+"_"+flavors[int(name[1])]
        e[k, reduced_index[reduced_name]] = 1

    checks = []

    def check(name, passed):
        checks.append({"name": name, "passed": bool(passed)})
        if not passed:
            raise AssertionError(name)

    check("susceptibilities_reduce_exactly", e.T*w16*e == w10)
    check("charge_vectors_lift_exactly", e*c10 == c16)
    g16 = mat(full["charge_gram_matrix"], 4, 4)
    g10 = mat(producer["conserved_gram_matrix_A_S_AT"], 4, 4)
    check("conserved_Gram_matrices_identical", g16 == g10 == c10.T*w10*c10)
    p16 = mat(full["constrained_response_matrix"], 16, 16)
    p10 = w10-w10*c10*g10.inv()*c10.T*w10
    check("response_projection_reduces_exactly", e.T*p16*e == p10)
    b16 = mat(full["B_vector"], 16, 1)
    l16 = mat(full["L_vector"], 16, 1)
    b10 = vec(producer["charge_rows"]["B"], 10)
    l10 = vec(producer["charge_rows"]["L"], 10)
    check("baryon_lepton_vectors_lift_exactly", e*b10 == b16 and e*l10 == l16)
    independent_unit_mu = vec(full["source_response_examples"]["B_plus_L"]["mu_vector"], 16)
    producer_drive = producer["zero_Delta_B_plus_L_drive"]
    producer_unit_mu = vec(producer_drive["mu_over_kappa"], 10)
    check("chemical_potentials_lift_exactly", e*producer_unit_mu == independent_unit_mu)
    check("unit_drive_densities_reduce_exactly", e.T*w16*independent_unit_mu
          == vec(producer_drive["scaled_density_over_kappa"], 10))
    check("baryon_coefficients_agree", rat(producer_drive["B_over_kappa_T2"]) == sp.Rational(72, 79)
          and rat(producer_drive["B_over_kappa_T2_over_6"]) == (b16.T*w16*independent_unit_mu)[0])
    check("maximum_chemical_potential_agrees", rat(producer_drive["max_abs_mu_over_kappa"])
          == max(abs(x) for x in independent_unit_mu) == sp.Rational(50, 79))
    check("no_source_conversion_agrees", vec(producer["B_minus_L_conversion"], 3)
          == sp.ones(3, 1)*sp.Rational(28, 79))
    trial = sp.Matrix([sp.Rational((k % 4)-2, k+3) for k in range(10)])
    check("arbitrary_reduced_source_response_agrees", e.T*p16*e*trial == p10*trial)
    out = {
        "status": "PASS", "phase": "post-completion cross-comparison", "schema": "strict expected species/order and rational matrix dimensions",
        "arithmetic": "exact rational SymPy", "checks": checks,
        "inputs": {"independent_matrices_sha256": sha256(independent_path),
                   "independent_primary_receipt_sha256": sha256(independent_receipt_path),
                   "producer_results_sha256": sha256(PRODUCER), "producer_reported_test_count": producer["test_count"]},
        "comparison_code_sha256": sha256(Path(__file__)),
        "independence_limit": "Primary16-species calculation did not import producer implementation/output; this comparison intentionally reads both completed outputs. Producer reported learning the coefficient after its codefreeze but before first execution.",
        "conclusion": "Full16-species and reduced10-species matrices/responses agree exactly under equilibrated quarkflavor mixing, all3fixed leptonDelta, and the shared external-source convention.",
    }
    (OUT/"comparison_receipt.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({"status": out["status"], "check_count": len(checks), "producer_results_sha256": sha256(PRODUCER)}, indent=2))


if __name__ == "__main__":
    main()
