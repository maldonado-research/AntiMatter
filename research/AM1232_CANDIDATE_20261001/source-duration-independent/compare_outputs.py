"""Read-only comparison of independently integrated and producer outputs."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRODUCER = HERE.parent / "source-duration"


def main():
    prod = json.loads((PRODUCER / "results.json").read_text())
    independent = json.loads((HERE / "registered_grid_time_results.json").read_text())
    bounds = json.loads((HERE / "independent_duration_bounds.json").read_text())
    index = {(r["T_i_GeV"], r["theta_i"]): r for r in independent["rows"]}
    differences = []
    for row in prod["trajectories"]:
        ind = index[(row["T_i_GeV"], row["theta_i_rad"])]
        delta = {
            "T_i_GeV": row["T_i_GeV"], "theta_i": row["theta_i_rad"],
            "theta_absolute": abs(row["theta_star_rad"] - ind["theta_star"]),
            "p_absolute": abs(row["p_star"] - ind["q_star"]),
            "K_over_A_absolute": abs(row["K_star_GeV4"] / independent["A_GeV4"] - ind["K_star_over_A"]),
            "V_over_A_absolute": abs(row["V_star_GeV4"] / independent["A_GeV4"] - ind["V_star_over_A"]),
            "u_signed_absolute": abs(row["u_site0_star_signed"] - ind["u_star"]),
            "total_scalar_fraction_absolute": abs(row["rho_phi_over_rho_rad_star"] - ind["total_scalar_over_radiation"]),
            "H_ratio_absolute": abs(row["H_star_over_H_radiation_star"] - ind["H_over_H_rad"]),
            "n_eta_required_relative": abs(row["conditional_n_eta_for_final_instant"] / ind["n_eta_required"] - 1),
        }
        differences.append(delta)
    assert len(differences) == 30
    delta_bounds = []
    for p, ind in zip(prod["duration_bounds"], bounds["bounds"]):
        assert p["Delta_N_ending_at_T_star"] == float(ind["Delta_N"])
        assert p["minimum_integer_n_at_eta_1"] == ind["minimum_n_eta1"]
        delta_bounds.append(abs(p["bound_n_eta_ge"] - float(ind["n_eta_lower_bound"])))
    maximum = {k: max(r[k] for r in differences) for k in differences[0]
               if k not in ("T_i_GeV", "theta_i")}
    assert all(v < 1e-7 for v in maximum.values())
    output = {
        "scope": "Independent implementation/proper-time cross-check, not independent human peer review or physical validation",
        "producer_result_sha256": hashlib.sha256((PRODUCER / "results.json").read_bytes()).hexdigest(),
        "producer_audit_py_sha256": hashlib.sha256((PRODUCER / "audit.py").read_bytes()).hexdigest(),
        "producer_registration_sha256": hashlib.sha256((PRODUCER / "REGISTRATION.md").read_bytes()).hexdigest(),
        "number_of_compared_trajectories": len(differences),
        "maximum_differences": maximum,
        "maximum_duration_bound_absolute_difference": max(delta_bounds),
        "identical_integer_minima": [r["minimum_n_eta1"] for r in bounds["bounds"]],
        "per_trajectory_differences": differences,
        "producer_controls": prod["controls"],
    }
    (HERE / "comparison_results.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "per_trajectory_differences"}, indent=2))


if __name__ == "__main__":
    main()
