"""Independent proper-time integration of the frozen one-cosine benchmark.

No producer modules are imported. x = sqrt(A)/F_eff * (t - t_i),
q = dtheta/dx, R = rho_rad/A, L = dissipated scalar energy/A.
All parameters are frozen public AM123/AM1231 values.
"""
from __future__ import annotations

import argparse
import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp

A = 620116096.5235525
F_ALPHA = 250.0
F_EFF = 3**30 * F_ALPHA
M_PL = 2.435e18
G_STAR = 106.75
T_STAR = 131.7
KB = 1.020689
C_SPH = 0.0195
MASS = math.sqrt(A) / F_EFF
R_STAR = (math.pi**2 / 30) * G_STAR * T_STAR**4 / A
H_FACTOR = F_EFF / (math.sqrt(3) * M_PL)
K16 = 0.5 * (F_ALPHA * T_STAR * KB / (16 * C_SPH)) ** 2


def evolve(theta_i, t_initial, rtol=2e-11, atol=2e-13):
    """Integrate with physical time, stopping at radiation temperature T_STAR."""
    r_initial = R_STAR * (t_initial / T_STAR) ** 4
    initial_energy = 2 * math.sin(theta_i / 2) ** 2
    exact_equilibrium = theta_i in (0.0, math.pi, -math.pi)

    def rhs(x, state):
        theta, q, r, loss, efolds = state
        potential = 2 * math.sin(theta / 2) ** 2
        energy = 0.5 * q * q + potential
        h = H_FACTOR * math.sqrt(max(0, r + energy))
        force = 0.0 if exact_equilibrium else math.sin(theta)
        return [q, -3 * h * q - force, -4 * h * r, 3 * h * q * q, h]

    def endpoint(x, state):
        return state[2] - R_STAR

    endpoint.terminal = True
    endpoint.direction = -1
    # Radiation-only gives the longest cooling time because scalar energy >= 0.
    xmax = 1.01 / (2 * H_FACTOR * math.sqrt(R_STAR))
    sol = solve_ivp(rhs, [0, xmax], [theta_i, 0, r_initial, 0, 0],
                    method="DOP853", rtol=rtol,
                    atol=[atol, atol, atol, atol, atol],
                    events=endpoint, dense_output=True, max_step=0.03)
    if not sol.success or not len(sol.t_events[0]):
        raise RuntimeError((sol.message, sol.y[:, -1].tolist()))
    theta, q, r, loss, efolds = sol.y_events[0][0]
    k = 0.5 * q * q
    v = 2 * math.sin(theta / 2) ** 2
    energy = k + v
    sampled = sol.sol(np.linspace(0, sol.t_events[0][0], 5001))
    energies = 0.5 * sampled[1]**2 + 2 * np.sin(sampled[0] / 2)**2
    ledger_residual = float(np.max(np.abs(energies + sampled[3] - initial_energy)))
    entropy_residual = float(np.max(np.abs(np.log(sampled[2] / r_initial) + 4 * sampled[4])))
    u = 3**30 * MASS * q / (2 * math.pi * T_STAR)
    return {
        "theta_i": theta_i,
        "T_i_GeV": t_initial,
        "theta_star": float(theta),
        "q_star": float(q),
        "u_star": float(u),
        "x_elapsed": float(sol.t_events[0][0]),
        "N_elapsed": float(efolds),
        "K_star_over_A": float(k),
        "V_star_over_A": float(v),
        "K_star_over_radiation": float(k / r),
        "total_scalar_over_radiation": float(energy / r),
        "H_over_H_rad": float(math.sqrt(1 + energy / r)),
        "n_eta_required": float(16 * math.sqrt(K16 / (A * k))) if k else None,
        "max_energy_ledger_error_over_A": ledger_residual,
        "max_radiation_entropy_log_error": entropy_residual,
        "endpoint_entropy_error": float(efolds - math.log(t_initial / T_STAR)),
        "function_evaluations": sol.nfev,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--registered-grid", action="store_true")
    parser.add_argument("--theta", type=float, action="append")
    parser.add_argument("--temperature", type=float, action="append")
    args = parser.parse_args()
    default_angles = ([0.0001, 0.01, 0.1, 0.5, 1, 1.5, 2, 2.5, 3, math.pi - 0.01]
                      if args.registered_grid else
                      [0.0, 0.25, 1.0, 2.0, 3.0, math.pi - 0.01, math.pi - 1e-4, math.pi])
    angles = args.theta or default_angles
    temperatures = args.temperature or ([200, 500, 2000] if args.registered_grid else [1e3, 1e4])
    target = args.output or Path(__file__).with_name(
        "registered_grid_time_results.json" if args.registered_grid else "proper_time_results.json")
    rows = []
    for temp in temperatures:
        for theta in angles:
            row = evolve(theta, temp)
            refined = evolve(theta, temp, rtol=2e-12, atol=2e-14)
            row["refinement_K_over_A_absolute_change"] = abs(row["K_star_over_A"] - refined["K_star_over_A"])
            row["refinement_theta_absolute_change"] = abs(row["theta_star"] - refined["theta_star"])
            rows.append(row)
    output = {
        "model": "Conditional homogeneous fixed-cosine benchmark; no driver, no extra damping, constant g_star; initial rest",
        "software": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "coordinates": "Proper time x=m(t-t_i), q=dtheta/dx, R=rho_rad/A, L=(E_i-E)/A, N=ln(a/a_i)",
        "A_GeV4": A, "F_eff_GeV": F_EFF, "m_GeV": MASS,
        "T_star_GeV": T_STAR, "R_star": R_STAR, "rho_kin_16_GeV4": K16,
        "rows": rows,
    }
    target.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"output": str(target), "rows": len(rows),
                      "max_energy_ledger_error_over_A": max(r["max_energy_ledger_error_over_A"] for r in rows),
                      "max_refinement_K_over_A_change": max(r["refinement_K_over_A_absolute_change"] for r in rows)}, indent=2))


if __name__ == "__main__":
    main()
