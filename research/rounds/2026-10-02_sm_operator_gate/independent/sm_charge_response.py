#!/usr/bin/env python3
"""Independent exact SM equilibrium charge/source response.

Only SymPy and the Python standard library are used. No repository or other
producer output is read. Run from any directory with Python 3 and SymPy.
"""

import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


OUT = Path(__file__).resolve().parent
NAMES = [f"{a}{i}" for i in range(1, 4) for a in ("q", "u", "d", "l", "e")] + ["H"]
INDEX = {name: i for i, name in enumerate(NAMES)}
N = len(NAMES)
RAT = sp.Rational


def vector(values):
    result = sp.zeros(N, 1)
    for name, value in values.items():
        result[INDEX[name]] = value
    return result


def row(values):
    return vector(values).T


WEIGHTS = [value for _ in range(3) for value in (6, 3, 3, 2, 1)] + [4]
W = sp.diag(*WEIGHTS)
Y = vector({**{f"{a}{i}": y for i in range(1, 4) for a, y in
                   (("q", RAT(1, 6)), ("u", RAT(2, 3)), ("d", RAT(-1, 3)),
                    ("l", RAT(-1, 2)), ("e", -1))}, "H": RAT(1, 2)})
B = vector({f"{a}{i}": RAT(1, 3) for i in range(1, 4) for a in ("q", "u", "d")})
LS = [vector({f"l{i}": 1, f"e{i}": 1}) for i in range(1, 4)]
L = sum(LS, sp.zeros(N, 1))
DELTAS = [B / 3 - li for li in LS]
C = sp.Matrix.hstack(Y, *DELTAS)

REACTION_NAMES = []
REACTIONS = []
for i in range(1, 4):
    for name, values in (
        (f"up_yukawa_{i}", {f"q{i}": 1, "H": 1, f"u{i}": -1}),
        (f"down_yukawa_{i}", {f"q{i}": 1, "H": -1, f"d{i}": -1}),
        (f"charged_lepton_yukawa_{i}", {f"l{i}": 1, "H": -1, f"e{i}": -1}),
    ):
        REACTION_NAMES.append(name)
        REACTIONS.append(row(values))
EW_ROW = len(REACTIONS)
REACTION_NAMES.append("electroweak_sphaleron")
REACTIONS.append(row({f"{a}{i}": m for i in range(1, 4) for a, m in (("q", 3), ("l", 1))}))
for i in (1, 2):
    REACTION_NAMES.append(f"quark_flavor_mixing_{i}_{i+1}")
    REACTIONS.append(row({f"q{i}": 1, f"q{i+1}": -1}))
REACTION_NAMES.append("strong_sphaleron_redundant")
REACTIONS.append(row({f"{a}{i}": m for i in range(1, 4) for a, m in
                      (("q", 2), ("u", -1), ("d", -1))}))
R = sp.Matrix.vstack(*REACTIONS)


def project_response(weight_matrix, charges):
    gram = charges.T * weight_matrix * charges
    inverse = gram.inv()
    response = weight_matrix - weight_matrix * charges * inverse * charges.T * weight_matrix
    return gram, inverse, response


G, GINV, P = project_response(W, C)


def solve(source, delta=(0, 0, 0), weight_matrix=W, charges=C):
    fixed = sp.Matrix([0, *delta])
    gram, inverse, response = project_response(weight_matrix, charges)
    lagrange = inverse * (fixed - charges.T * weight_matrix * source)
    mu = source + charges * lagrange
    density = weight_matrix * mu
    return density, mu, lagrange


def scalar(expr):
    return sp.factor(expr[0] if isinstance(expr, sp.MatrixBase) else expr)


def strings(matrix):
    return [[str(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def anomaly_traces(conjugate_right_handed=True):
    """Per generation; charge-conjugation flips X and Y, not Y squared."""
    # name, total internal multiplicity, color copies for SU(2), Dynkin index,
    # particle hypercharge, particle B, particle L, chirality
    fields = [
        ("q", 6, 3, RAT(1, 2), RAT(1, 6), RAT(1, 3), 0, "L"),
        ("u", 3, 3, 0, RAT(2, 3), RAT(1, 3), 0, "R"),
        ("d", 3, 3, 0, RAT(-1, 3), RAT(1, 3), 0, "R"),
        ("l", 2, 1, RAT(1, 2), RAT(-1, 2), 0, 1, "L"),
        ("e", 1, 1, 0, -1, 0, 1, "R"),
    ]
    output = {"B_WW": 0, "L_WW": 0, "B_YY": 0, "L_YY": 0,
              "Y_WW": 0, "Y_cubed": 0}
    transformed = []
    for name, multiplicity, color, dynkin, y, b, li, chirality in fields:
        sign = -1 if chirality == "R" and conjugate_right_handed else 1
        yl, bl, ll = sign*y, sign*b, sign*li
        transformed.append({"field": name if sign == 1 else name+"^c", "multiplicity": multiplicity,
                            "left_handed_Y": str(yl), "left_handed_B": str(bl), "left_handed_L": str(ll)})
        output["B_WW"] += color*dynkin*bl
        output["L_WW"] += color*dynkin*ll
        output["B_YY"] += multiplicity*bl*yl**2
        output["L_YY"] += multiplicity*ll*yl**2
        output["Y_WW"] += color*dynkin*yl
        output["Y_cubed"] += multiplicity*yl**3
    output["B_minus_L_WW"] = output["B_WW"]-output["L_WW"]
    output["B_minus_L_YY"] = output["B_YY"]-output["L_YY"]
    return output, transformed


def main():
    controls = OUT / "CONTROLS.md"
    if not controls.exists():
        raise RuntimeError("Missing preregistration: CONTROLS.md must exist before tests")
    results = []

    def check(name, condition, details):
        passed = bool(condition)
        results.append({"name": name, "passed": passed, "details": details})
        if not passed:
            receipt = {"status": "FAILED", "checks": results}
            (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
            raise AssertionError(name)

    zero = sp.zeros(N, 1)
    z, m, _ = solve(zero, (RAT(1, 3), RAT(1, 3), RAT(1, 3)))
    check("no_source_28_over_79_equal_flavors", scalar(B.T * z) == RAT(28, 79),
          {"B": str(scalar(B.T * z)), "B_minus_L": str(scalar((B-L).T * z))})
    flavor_delta = (RAT(2, 5), RAT(-3, 7), RAT(5, 11))
    z, m, _ = solve(zero, flavor_delta)
    check("no_source_28_over_79_unequal_flavors", scalar(B.T * z) == RAT(28, 79)*sum(flavor_delta),
          {"Delta_i": list(map(str, flavor_delta)), "B": str(scalar(B.T * z))})
    check("reaction_kernel", R.rank() == 12 and C.rank() == 4 and R*C == sp.zeros(R.rows, C.cols),
          {"reaction_rank": R.rank(), "species_count": N, "conserved_basis_rank": C.rank()})
    check("strong_sphaleron_redundant", R[:-1, :].rank() == R.rank(),
          {"rank_with_strong_sphaleron": R.rank(), "rank_without_strong_sphaleron": R[:-1, :].rank()})

    arbitrary = sp.Matrix([RAT((k % 7)-3, k+2) for k in range(N)])
    z, m, _ = solve(arbitrary, flavor_delta)
    check("all_constraints_arbitrary_source", R*(m-arbitrary) == sp.zeros(R.rows, 1)
          and C.T*z == sp.Matrix([0, *flavor_delta]),
          {"reaction_residual": strings(R*(m-arbitrary)), "fixed_charge_residual": strings(C.T*z-sp.Matrix([0, *flavor_delta]))})

    source_values = {}
    expected = {"B_plus_L": RAT(432, 79), "L": RAT(216, 79), "B": RAT(216, 79), "B_minus_L": 0}
    for name, source in (("B_plus_L", B+L), ("L", L), ("B", B), ("B_minus_L", B-L)):
        density, mu, multipliers = solve(source)
        response = scalar(B.T*density)
        source_values[name] = {"B_normalized": str(response), "L_normalized": str(scalar(L.T*density)),
                               "B_dimensional_coefficient_T2_source": str(response/6),
                               "density_vector": [str(x) for x in density], "mu_vector": [str(x) for x in mu]}
        check(f"source_{name}", response == expected[name], source_values[name])

    additions = [Y, B-L, DELTAS[0]-DELTAS[1], DELTAS[1]-DELTAS[2],
                 C*sp.Matrix([RAT(-2, 3), RAT(4, 5), RAT(7, 9), RAT(-11, 13)])]
    for i, addition in enumerate(additions):
        shifted, _, _ = solve(arbitrary+addition, flavor_delta)
        check(f"conserved_source_equivalence_{i}", shifted == z, {"difference": strings(shifted-z)})
    check("response_symmetry_and_charge_annihilation", P == P.T and P*C == sp.zeros(N, C.cols)
          and C.T*P == sp.zeros(C.cols, N), {"symmetric": P == P.T, "P_C_zero": P*C == sp.zeros(N, C.cols)})
    probes = [sp.eye(N)[:, k] for k in range(N)] + [arbitrary, B+L, B-L,
              sp.Matrix([RAT((-1)**k, k+1) for k in range(N)])]
    values = [scalar(probe.T*P*probe) for probe in probes]
    check("response_nonnegative_preregistered_probes", all(value >= 0 for value in values),
          {"quadratic_values": list(map(str, values)), "probe_count": len(probes)})

    wrong_weights = sp.diag(*(WEIGHTS[:-1]+[2]))
    wrong_density, _, _ = solve(zero, (RAT(1, 3),)*3, weight_matrix=wrong_weights)
    wrong_ratio = scalar(B.T*wrong_density)
    check("wrong_Higgs_statistics_detected", wrong_ratio == RAT(52, 145) and wrong_ratio != RAT(28, 79),
          {"incorrect_ratio": str(wrong_ratio), "correct_ratio": "28/79"})

    without_ew = R.copy()
    without_ew.row_del(EW_ROW)
    c_without_ew = sp.Matrix.hstack(Y, B, *LS)
    g0, inv0, p0 = project_response(W, c_without_ew)
    no_ew_density = p0*(B+L)
    check("remove_sphalerons_conserves_B_and_L", without_ew.rank() == 11
          and without_ew*c_without_ew == sp.zeros(without_ew.rows, 5)
          and no_ew_density == zero,
          {"rank_without_EW_sphaleron": without_ew.rank(), "B_plus_L_source_density": strings(no_ew_density)})

    positive, _, _ = solve(arbitrary, flavor_delta)
    negative, _, _ = solve(-arbitrary, flavor_delta)
    baseline, _, _ = solve(zero, flavor_delta)
    check("source_sign_reversal", positive+negative == 2*baseline,
          {"residual": strings(positive+negative-2*baseline)})

    grand_canonical_constraints = sp.Matrix.hstack(Y, DELTAS[0]-DELTAS[1], DELTAS[1]-DELTAS[2])
    _, _, grand_response = project_response(W, grand_canonical_constraints)
    grand_density = grand_response*(B-L)
    grand_delta = scalar((B-L).T*grand_density)
    check("unfixed_B_minus_L_changes_ensemble", grand_delta > 0,
          {"grand_canonical_B_minus_L_normalized": str(grand_delta), "B_normalized": str(scalar(B.T*grand_density)),
           "closed_fixed_charge_B_minus_L_source_B": "0"})

    d1, d2, d3, a = sp.symbols("d1 d2 d3 a")
    symbolic_density, symbolic_mu, _ = solve(a*(B+L), (d1, d2, d3))
    symbolic_b = scalar(B.T*symbolic_density)
    check("symbolic_general_B_plus_L_result", sp.simplify(symbolic_b-
          (RAT(28, 79)*(d1+d2+d3)+RAT(432, 79)*a)) == 0,
          {"B_normalized": str(symbolic_b)})

    anomalies, lh_fields = anomaly_traces(True)
    expected_anomalies = {"B_WW": RAT(1, 2), "L_WW": RAT(1, 2),
                         "B_YY": RAT(-1, 2), "L_YY": RAT(-1, 2),
                         "Y_WW": 0, "Y_cubed": 0, "B_minus_L_WW": 0, "B_minus_L_YY": 0}
    check("left_handed_SM_anomaly_traces", anomalies == expected_anomalies,
          {key: str(value) for key, value in anomalies.items()})
    wrong_anomalies, _ = anomaly_traces(False)
    check("wrong_right_handed_anomaly_sign_detected", wrong_anomalies["B_minus_L_YY"] != 0
          and wrong_anomalies["Y_cubed"] != 0,
          {key: str(value) for key, value in wrong_anomalies.items()})
    weak_topological_B_plus_L = 2*3*(anomalies["B_WW"]+anomalies["L_WW"])
    check("EW_source_and_anomaly_sign_consistent", weak_topological_B_plus_L == 6
          and scalar(R[EW_ROW, :]*(B+L)) == weak_topological_B_plus_L,
          {"Delta_B_plus_L_per_positive_Delta_N_CS": str(weak_topological_B_plus_L),
           "integrated_by_parts_weak_theta_qW_coefficient": str(-weak_topological_B_plus_L),
           "EW_reaction_source_contraction": str(scalar(R[EW_ROW, :]*(B+L)))})

    matrices = {
        "species_order": NAMES, "reaction_row_order": REACTION_NAMES,
        "susceptibility_weights_T2_over_6": WEIGHTS, "reaction_matrix": strings(R),
        "charge_columns": ["Y", "Delta_1", "Delta_2", "Delta_3"],
        "charge_matrix": strings(C), "charge_gram_matrix": strings(G),
        "constrained_response_matrix": strings(P),
        "B_vector": strings(B), "L_vector": strings(L),
        "source_response_examples": source_values,
        "symbolic_B_plus_L_mu_vector": [str(sp.factor(x)) for x in symbolic_mu],
        "all_left_handed_fields_one_generation": lh_fields,
        "anomaly_traces_one_generation": {key: str(value) for key, value in anomalies.items()},
    }
    matrix_path = OUT / "matrices.json"
    matrix_path.write_text(json.dumps(matrices, indent=2) + "\n")
    receipt = {
        "status": "PASS", "arithmetic": "exact rational/symbolic SymPy",
        "python_version": sys.version.split()[0], "sympy_version": sp.__version__,
        "controls_sha256": sha256(controls), "code_sha256": sha256(Path(__file__)),
        "matrices_sha256": sha256(matrix_path), "check_count": len(results),
        "checks": results,
        "interpretation": "Equilibrium consistency checks only; no candidate operator, CP mechanism, scalar backreaction, rate history, or broken-phase prediction established.",
    }
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "check_count": len(results),
                      "no_source_conversion": "28/79", "B_plus_L_B_T2_source": "72/79",
                      "L_B_T2_source": "36/79", "B_minus_L_B_T2_source": "0",
                      "receipt": str(OUT / "receipt.json")}, indent=2))


if __name__ == "__main__":
    main()
