#!/usr/bin/env python3
"""Exact, conventional symmetric-SM charge response; no model/yield inference.

Run from anywhere: python3 /absolute/path/to/sm_charge_diagnostic.py
Only Python's standard library is required. Outputs are adjacent to this file.
"""
from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPECIES = ("q", "u", "d", "l_e", "l_mu", "l_tau", "e_e", "e_mu", "e_tau", "H")
S = tuple(map(F, (18, 9, 9, 2, 2, 2, 1, 1, 1, 4)))
ZERO = (F(0),) * 10
B = (F(1, 3), F(1, 3), F(1, 3)) + (F(0),) * 7
Y = tuple(map(F, ("1/6", "2/3", "-1/3", "-1/2", "-1/2", "-1/2", "-1", "-1", "-1", "1/2")))
LEPTONS = tuple(tuple(F(int(j == 3 + i or j == 6 + i)) for j in range(10)) for i in range(3))
L = tuple(sum(li[j] for li in LEPTONS) for j in range(10))
Q = tuple(B[j] + L[j] for j in range(10))
DELTAS = tuple(tuple(B[j] / 3 - LEPTONS[i][j] for j in range(10)) for i in range(3))
A = (Y,) + DELTAS


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def weighted(a, b):
    return sum((a[i] * S[i] * b[i] for i in range(10)), F(0))


def solve(matrix, rhs):
    """Exact full-pivot-row Gaussian elimination; singular matrices fail."""
    size = len(rhs)
    aug = [list(map(F, matrix[i])) + [F(rhs[i])] for i in range(size)]
    for col in range(size):
        pivot = next((r for r in range(col, size) if aug[r][col]), None)
        if pivot is None:
            raise ValueError("singular matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [v / scale for v in aug[col]]
        for row in range(size):
            if row != col:
                scale = aug[row][col]
                aug[row] = [x - scale * y for x, y in zip(aug[row], aug[col])]
    return tuple(aug[i][-1] for i in range(size))


def rank(matrix):
    work = [list(map(F, row)) for row in matrix]
    pivot_row = 0
    for col in range(len(work[0])):
        pivot = next((r for r in range(pivot_row, len(work)) if work[r][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [v / scale for v in work[pivot_row]]
        for row in range(len(work)):
            if row != pivot_row:
                scale = work[row][col]
                work[row] = [x - scale * y for x, y in zip(work[row], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


GRAM = tuple(tuple(weighted(a, b) for b in A) for a in A)


def response(source=Q, kappa=F(1), delta=(F(0), F(0), F(0))):
    """Return intrinsic mu, with delta_i = 6 n_Delta_i/T^2.

    kappa and delta have energy units; values here are exact formal basis units.
    Charge densities are n_a = (T^2/6) * weighted(a, mu).
    """
    target = (F(0),) + tuple(map(F, delta))
    multipliers = solve(GRAM, tuple(target[i] - kappa * weighted(A[i], source) for i in range(4)))
    return tuple(kappa * source[j] + sum(A[i][j] * multipliers[i] for i in range(4)) for j in range(10))


def reaction(**coefficients):
    return tuple(F(coefficients.get(name, 0)) for name in SPECIES)


REACTIONS = {
    "up_Yukawa": reaction(q=1, H=1, u=-1),
    "down_Yukawa": reaction(q=1, H=-1, d=-1),
    "electron_Yukawa": reaction(l_e=1, H=-1, e_e=-1),
    "muon_Yukawa": reaction(l_mu=1, H=-1, e_mu=-1),
    "tau_Yukawa": reaction(l_tau=1, H=-1, e_tau=-1),
    "strong_sphaleron_full_3_generations": reaction(q=6, u=-3, d=-3),
    "weak_sphaleron_full_3_generations": reaction(q=9, l_e=1, l_mu=1, l_tau=1),
}


def rational(value):
    return str(F(value))


def write_json(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def write_csv(name, header, rows):
    with (HERE / name).open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def main():
    tests = []

    def check(name, condition, detail):
        tests.append({"test": name, "passed": bool(condition), "detail": detail})
        if not condition:
            raise AssertionError(name + ": " + str(detail))

    drive = response()
    effective = tuple(drive[j] - Q[j] for j in range(10))
    density = tuple(S[j] * drive[j] for j in range(10))
    basis = tuple(response(kappa=F(0), delta=tuple(F(i == j) for j in range(3))) for i in range(3))
    bcoef = weighted(B, drive)
    lcoef = weighted(L, drive)
    conversion = tuple(weighted(B, v) for v in basis)
    check("conserved_matrix_rank", rank(A) == 4, {"rank": rank(A)})
    check("reaction_matrix_rank", rank(tuple(REACTIONS.values())) == 6, {"rank": rank(tuple(REACTIONS.values()))})
    check("standard_B_minus_L_conversion", conversion == (F(28, 79),) * 3, list(map(rational, conversion)))
    check("zero_drive_zero_charge", response(kappa=F(0)) == ZERO, "mu vanishes")
    check("drive_fixed_conserved_charges", all(weighted(a, drive) == 0 for a in A), "Y and all Delta_i unchanged")
    check("B_and_L_equal_for_zero_Delta", bcoef == lcoef, {"B": rational(bcoef), "L": rational(lcoef)})

    reaction_rows = []
    for name, nu in REACTIONS.items():
        charges = {"B": dot(nu, B), "L": dot(nu, L), "B_plus_L": dot(nu, Q), "Y": dot(nu, Y)}
        charges.update({f"Delta_{i}": dot(nu, DELTAS[j]) for j, i in enumerate(("e", "mu", "tau"))})
        check(name + "_conserved_charges", all(charges[key] == 0 for key in ("Y", "Delta_e", "Delta_mu", "Delta_tau")), {key: rational(value) for key, value in charges.items()})
        check(name + "_effective_affinity", dot(nu, effective) == 0, rational(dot(nu, effective)))
        check(name + "_intrinsic_source_compatibility", dot(nu, drive) == charges["B_plus_L"], rational(dot(nu, drive)))
        reaction_rows.append((name,) + tuple(rational(charges[key]) for key in ("B", "L", "B_plus_L", "Y", "Delta_e", "Delta_mu", "Delta_tau")) + (rational(dot(nu, drive)), rational(dot(nu, effective))))

    check("weak_sphaleron_exact_charge", dot(REACTIONS["weak_sphaleron_full_3_generations"], Q) == 6, "Delta B = 3, Delta L = 3, Delta(B+L) = 6")
    for name, conserved in zip(("hypercharge", "Delta_e", "Delta_mu", "Delta_tau"), A):
        check(name + "_source_invisible", response(conserved) == ZERO, "projection identically zero at fixed conserved charge")
    b_response = response(B)
    l_response = response(L)
    check("B_L_sources_equivalent", b_response == l_response, "B-L is conserved")
    check("B_plus_L_source_twice_B", drive == tuple(2 * v for v in b_response), "linear projection")
    for i in range(3):
        for j in range(i + 1, 3):
            flavor_source = tuple(LEPTONS[i][k] - LEPTONS[j][k] for k in range(10))
            check(f"flavor_source_{i}_{j}_invisible", response(flavor_source) == ZERO, "L_i-L_j is conserved")
    flavor_delta = response(kappa=F(0), delta=(F(1), F(-1), F(0)))
    check("flavor_difference_total_B_zero", weighted(B, flavor_delta) == 0, rational(weighted(B, flavor_delta)))
    check("flavor_difference_is_nontrivial", any(flavor_delta), list(map(rational, flavor_delta)))
    check("flavor_difference_Y_zero", weighted(Y, flavor_delta) == 0, rational(weighted(Y, flavor_delta)))

    # Nonzero conserved-charge/control basis, not only the zero-charge case.
    mixed_delta = (F(2, 7), F(-3, 11), F(5, 13))
    mixed_kappa = F(7, 17)
    mixed = response(kappa=mixed_kappa, delta=mixed_delta)
    check("general_B_response", weighted(B, mixed) == F(28, 79) * sum(mixed_delta) + bcoef * mixed_kappa, rational(weighted(B, mixed)))
    check("general_conserved_values", tuple(weighted(a, mixed) for a in A) == (F(0),) + mixed_delta, list(map(rational, (weighted(a, mixed) for a in A))))
    check("general_reaction_equilibrium", all(dot(nu, tuple(mixed[j] - mixed_kappa * Q[j] for j in range(10))) == 0 for nu in REACTIONS.values()), "all seven reactions")

    # Weighted projector idempotence and reciprocal response are independent
    # algebraic properties of the constrained thermodynamic projection.
    unit_vectors = tuple(tuple(F(i == j) for j in range(10)) for i in range(10))
    projection_columns = tuple(response(v) for v in unit_vectors)
    check("projection_idempotent", all(response(v) == v for v in projection_columns), "P^2 = P")
    check("susceptibility_reciprocity", all(weighted(unit_vectors[i], projection_columns[j]) == weighted(unit_vectors[j], projection_columns[i]) for i in range(10) for j in range(10)), "S P = P^T S")
    effective_basis = tuple(tuple(basis[k][j] for j in range(10)) for k in range(3))
    check("no_drive_equilibrium_for_Delta_basis", all(dot(nu, v) == 0 for v in effective_basis for nu in REACTIONS.values()), "nonzero conserved-density solutions")

    # Thermodynamic positivity for one nonzero allowed perturbation nu.
    nu = REACTIONS["weak_sphaleron_full_3_generations"]
    eps = F(1, 5)
    perturb_mu = tuple(drive[j] + eps * nu[j] / S[j] for j in range(10))
    objective = lambda mu: weighted(mu, mu) / 2 - weighted(Q, mu)
    gap = objective(perturb_mu) - objective(drive)
    expected_gap = eps**2 * sum(nu[j]**2 / S[j] for j in range(10)) / 2
    check("strict_KKT_minimum_allowed_perturbation", gap == expected_gap and gap > 0, rational(gap))

    # Source shift invariance holds even when conserved density is nonzero.
    shifted_source = tuple(Q[j] + 3 * Y[j] - 2 * DELTAS[1][j] for j in range(10))
    check("general_conserved_source_shift", response(shifted_source, mixed_kappa, mixed_delta) == mixed, "Q -> Q + conserved charge changes only a fixed constant")

    results = {
        "benchmark": "conventional external derivative B+L interaction; symmetric unbroken SM",
        "not_a_model_yield": True,
        "units": {"theta0": "dimensionless", "c": "dimensionless", "kappa": "energy", "delta_i": "6 n_Delta_i/T^2 (energy)", "mu_i": "intrinsic chemical potential (energy)"},
        "source_normalization": "L_int=c (partial_mu theta0) J_(B+L)^mu; kappa=c dot(theta0); H_int=-kappa Q_(B+L)",
        "c_status": "unspecified by Wilson replacement; c=1 is a toy normalization",
        "species": list(SPECIES),
        "susceptibility_diagonal_in_T2_over_6": list(map(rational, S)),
        "charge_rows": {"B": list(map(rational, B)), "L": list(map(rational, L)), "B_plus_L": list(map(rational, Q)), "Y": list(map(rational, Y)), **{f"Delta_{i}": list(map(rational, DELTAS[j])) for j, i in enumerate(("e", "mu", "tau"))}},
        "conserved_gram_matrix_A_S_AT": [list(map(rational, row)) for row in GRAM],
        "zero_Delta_B_plus_L_drive": {"mu_over_kappa": list(map(rational, drive)), "scaled_density_over_kappa": list(map(rational, density)), "B_over_kappa_T2_over_6": rational(bcoef), "L_over_kappa_T2_over_6": rational(lcoef), "B_over_kappa_T2": rational(bcoef / 6), "B_plus_L_over_kappa_T2": rational((bcoef + lcoef) / 6), "max_abs_mu_over_kappa": rational(max(map(abs, drive)))},
        "zero_drive_Delta_basis_mu": [list(map(rational, row)) for row in basis],
        "B_minus_L_conversion": list(map(rational, conversion)),
        "flavor_difference_control": {"scaled_Delta": ["1", "-1", "0"], "mu": list(map(rational, flavor_delta)), "scaled_B": rational(weighted(B, flavor_delta)), "scaled_Le": rational(weighted(LEPTONS[0], flavor_delta)), "scaled_Lmu": rational(weighted(LEPTONS[1], flavor_delta))},
        "small_mu_zero_Delta": f"max_i |mu_i|/T = {rational(max(map(abs, drive)))} |kappa|/T << 1",
        "tests": tests,
        "test_count": len(tests),
    }
    write_json("results.json", results)
    write_csv("species_response.csv", ("species", "susceptibility_T2_over_6", "B_charge", "L_charge", "Y_charge", "mu_over_kappa", "scaled_density_over_kappa", "mu_over_kappa_decimal"), ((SPECIES[i], rational(S[i]), rational(B[i]), rational(L[i]), rational(Y[i]), rational(drive[i]), rational(density[i]), format(float(drive[i]), ".17g")) for i in range(10)))
    write_csv("reaction_charges.csv", ("reaction", "Delta_B", "Delta_L", "Delta_B_plus_L", "Delta_Y", "Delta_Delta_e", "Delta_Delta_mu", "Delta_Delta_tau", "intrinsic_affinity_over_kappa", "effective_affinity_over_kappa"), reaction_rows)
    write_csv("conserved_density_basis.csv", ("species", "mu_per_scaled_Delta_e", "mu_per_scaled_Delta_mu", "mu_per_scaled_Delta_tau", "flavor_difference_mu"), ((SPECIES[i],) + tuple(rational(v[i]) for v in basis) + (rational(flavor_delta[i]),) for i in range(10)))
    write_csv("tests.csv", ("test", "passed", "detail"), ((t["test"], str(t["passed"]).lower(), json.dumps(t["detail"], sort_keys=True)) for t in tests))
    print(json.dumps({"tests_passed": len(tests), "B_over_kappa_T2": rational(bcoef / 6), "conversion": rational(conversion[0]), "max_mu_over_kappa": rational(max(map(abs, drive)))}, sort_keys=True))


if __name__ == "__main__":
    main()
