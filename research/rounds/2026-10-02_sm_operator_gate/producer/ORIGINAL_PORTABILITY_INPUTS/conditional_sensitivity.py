#!/usr/bin/env python3
"""Registered conditional entropy/energy sensitivity; never a model correction.

No parent files are imported or modified. AST literals and public CSV are read.
Decimal arithmetic isolates the nearby integer boundary from float rounding.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import json
from decimal import Decimal as D, localcontext, ROUND_CEILING, ROUND_FLOOR
from pathlib import Path

HERE = Path(__file__).resolve().parent


def public_repository():
    for ancestor in HERE.parents:
        for candidate in (ancestor / "AntiMatter", ancestor):
            if (candidate / "research/AM1231/v1.23.1/v1.23.1_efficiency_energy_frontier.py").is_file():
                return candidate
    raise FileNotFoundError("public AntiMatter parent artifacts not found in ancestor repositories")


PUBLIC_REPO = public_repository()
FRONTIER = PUBLIC_REPO / "research/AM1231/v1.23.1/v1.23.1_efficiency_energy_frontier.py"
FRONTIER_CSV = FRONTIER.with_suffix(".csv")
GENERATOR = PUBLIC_REPO / "research/AM1231/v1.23/v1.23_wilson_instanton_cosmology_audit.py"


def pi_decimal():
    """Machin formula with series truncation below working precision."""
    def atan_inverse(integer):
        x = D(1) / D(integer)
        x2 = x * x
        term = x
        result = term
        for k in range(1, 10000):
            term *= -x2
            contribution = term / (2 * k + 1)
            new = result + contribution
            if new == result:
                return result
            result = new
        raise RuntimeError("arctan did not converge")
    return 16 * atan_inverse(5) - 4 * atan_inverse(239)


def public_literals(path):
    tree = ast.parse(path.read_text())
    for statement in tree.body:
        if isinstance(statement, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "FROZEN" for t in statement.targets):
            # Preserve original decimal tokens rather than binary float casts.
            return {ast.literal_eval(k): D(ast.get_source_segment(path.read_text(), v)) for k, v in zip(statement.value.keys, statement.value.values)}
    raise ValueError("public FROZEN literal not found")


def text(value):
    return format(value, ".28g")


def provenance_entry(path, ranges):
    raw = path.read_bytes()
    lines = raw.splitlines(keepends=True)
    return {
        "repository": "AntiMatter",
        "path": path.relative_to(PUBLIC_REPO).as_posix(),
        "file_sha256": hashlib.sha256(raw).hexdigest(),
        "ranges": [{"first_line": start, "last_line": end, "excerpt_sha256": hashlib.sha256(b"".join(lines[start - 1:end])).hexdigest()} for start, end in ranges],
        "status": "public parent artifact; no private manuscript source",
    }


def main():
    with localcontext() as context:
        context.prec = 75
        pi = pi_decimal()
        exact_entropy_prefactor = D(6480) / D(33733)
        c_ideal = exact_entropy_prefactor / pi**2
        c_old = D("0.0195")
        rescale = c_old / c_ideal
        frozen = public_literals(FRONTIER)
        thresholds = {
            "one_A": 16 * frozen["WE_A_required_over_A"].sqrt(),
            "two_A": 16 * (frozen["WE_A_required_over_A"] / 2).sqrt(),
            "strict_1pct_radiation": 16 * (frozen["WE_kinetic_over_radiation_n16"] / D("0.01")).sqrt(),
        }
        checks = []

        def check(name, condition):
            checks.append({"test": name, "passed": bool(condition)})
            if not condition:
                raise AssertionError(name)

        with FRONTIER_CSV.open(newline="") as handle:
            original_rows = list(csv.DictReader(handle))
        columns = {"one_A": "n_continuous_one_A", "two_A": "n_continuous_two_A", "strict_1pct_radiation": "n_continuous_strict_1pct_radiation"}
        for original in original_rows:
            eta = D(original["eta_relative_efficiency"])
            for budget, value in thresholds.items():
                check("public_csv_baseline_" + budget + "_eta_" + str(eta), abs(value / eta - D(original[columns[budget]])) < D("1e-12"))

        rows = []
        for eta in (D(1), D("0.75"), D("0.5"), D("0.25")):
            for budget, original in thresholds.items():
                corrected = original * rescale / eta
                old = original / eta
                strict = budget == "strict_1pct_radiation"
                n_new = int(corrected.to_integral_value(rounding=ROUND_FLOOR)) + 1 if strict else int(corrected.to_integral_value(rounding=ROUND_CEILING))
                n_old = int(old.to_integral_value(rounding=ROUND_FLOOR)) + 1 if strict else int(old.to_integral_value(rounding=ROUND_CEILING))
                # Separate energy-squared inequalities validate integer rounding.
                energy_at_min = (corrected / D(n_new))**2
                energy_at_previous = (corrected / D(n_new - 1))**2
                check("conditional_minimum_" + budget + "_eta_" + str(eta), energy_at_min < 1 if strict else energy_at_min <= 1)
                check("conditional_previous_fails_" + budget + "_eta_" + str(eta), energy_at_previous >= 1 if strict else energy_at_previous > 1)
                rows.append({"eta_relative_efficiency": text(eta), "budget": budget, "original_continuous_n": text(old), "conditional_ideal_continuous_n": text(corrected), "original_integer_minimum": n_old, "conditional_ideal_integer_minimum": n_new, "conditional_energy_fraction_at_minimum": text(energy_at_min)})

        eta49_old = thresholds["one_A"] / 49
        eta49_ideal = eta49_old * rescale
        u_old = frozen["WE_u_required_exact_KB"]
        toy_kappa = 2 * pi * u_old
        mu_max = D(50) / 79
        data = {
            "status": "formal conditional comparison; ideal symmetric SM not applicable at inherited T*=131.7 GeV",
            "c_sph_ideal_exact": "6480/(33733*pi^2) for g_star_s=106.75",
            "c_sph_ideal": text(c_ideal),
            "c_sph_inherited": text(c_old),
            "ideal_over_inherited": text(c_ideal / c_old),
            "ideal_minus_inherited_percent": text((c_ideal / c_old - 1) * 100),
            "continuous_threshold_rescaling_inherited_over_ideal": text(rescale),
            "n49_single_height_required_eta_inherited": text(eta49_old),
            "n49_single_height_required_eta_conditional_ideal": text(eta49_ideal),
            "n49_passes_at_eta1_conditional_ideal": eta49_ideal <= 1,
            "conditional_EFT_normalization": {
                "coefficient_assumption": "our conditional choice c=n_det D_d motivated by public yield ansatz; no public operator/UV matching derivation",
                "physical_kappa_over_T": "2*pi*n_det*D_d*(dot_tau1/T)",
                "inherited_unit_efficiency_kappa_over_T_per_Dd": text(16 * toy_kappa),
                "inherited_unit_efficiency_max_mu_over_T_per_Dd": text(16 * toy_kappa * mu_max),
                "ideal_unit_efficiency_kappa_over_T_per_Dd": text(D("1.020689") / c_ideal),
                "ideal_unit_efficiency_max_mu_over_T_per_Dd": text(D("1.020689") / c_ideal * mu_max),
            },
            "fixed_c1_toy_at_inherited_phase_speed": {"kappa_over_T": text(toy_kappa), "max_mu_over_T": text(toy_kappa * mu_max), "linear_response_consistent": False},
            "fixed_c_n_det_toy_at_inherited_phase_speed": {"n_det": 16, "I_F": 1, "kappa_over_T": text(16 * toy_kappa), "max_mu_over_T": text(16 * toy_kappa * mu_max), "linear_response_consistent": False},
            "precision_boundary": "75 decimal arithmetic digits are computational precision; public input decimals and physical assumptions carry no such accuracy",
            "rows": rows,
            "tests": checks,
            "test_count": len(checks),
        }
        (HERE / "conditional_sensitivity.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        with (HERE / "conditional_sensitivity.csv").open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        provenance = {
            "sources": [provenance_entry(GENERATOR, ((63, 69), (582, 585), (1147, 1177))), provenance_entry(FRONTIER, ((19, 28), (65, 83), (188, 204))), provenance_entry(FRONTIER_CSV, ((1, 5),))],
            "registration_sha256": hashlib.sha256((HERE / "REGISTRATION.md").read_bytes()).hexdigest(),
            "addendum_sha256": hashlib.sha256((HERE / "REGISTRATION_ADDENDUM.md").read_bytes()).hexdigest(),
            "coefficient_identification_status": "c=n_det D_d is a fresh conditional EFT normalization assumption; public phenomenological scaffold does not derive it",
            "independence_timing": "independently written solver; independent result message received before producer execution; not fully blinded execution",
        }
        (HERE / "PROVENANCE.json").write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")
        print(json.dumps({"tests_passed": len(checks), "c_sph_ideal": text(c_ideal), "n49_eta_ideal": text(eta49_ideal), "eta1_integer_minima": {row["budget"]: row["conditional_ideal_integer_minimum"] for row in rows if row["eta_relative_efficiency"] == "1"}}, sort_keys=True))


if __name__ == "__main__":
    main()
