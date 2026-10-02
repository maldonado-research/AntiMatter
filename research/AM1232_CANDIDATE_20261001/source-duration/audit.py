#!/usr/bin/env python3
"""Registered fixed-cosine source-only audit; reads public inputs, writes elsewhere."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import sys

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
from scipy.special import jv, jvp, yv, yvp

T_STAR = 131.7
G_STAR = 106.75
MPL = 2.435e18
F_ALPHA = 250.0
K_B = 1.020689
C_SPH = 0.0195
PHASES = [0.0001, 0.01, 0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, math.pi-0.01]
TEMPERATURES = [200.0, 500.0, 2000.0]
DURATIONS = [0.0, 0.01, 0.1, 0.5, 1.0]
TOLS = [(1e-9, 1e-11), (1e-11, 1e-13)]
SOURCE_NAMES = [
    "research/AM1231/v1.23/v1.23_summary.json",
    "research/AM1231/v1.23/v1.23_source_normalization.csv",
    "research/AM1231/v1.23/v1.23_misalignment.csv",
    "research/AM1231/v1.23/v1.23_wilson_instanton_cosmology_audit_note.md",
    "research/AM1231/v1.23/v1.23_wilson_instanton_cosmology_audit.py",
    "research/AM1231/v1.23.1/v1.23.1_efficiency_energy_frontier.md",
    "research/AM1231/v1.23.1/v1.23.1_efficiency_energy_frontier.py",
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_csv(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


class Model:
    def __init__(self, source):
        self.A = source["physical_source_height_GeV4"]
        self.F = source["desired_endpoint_period_GeV"]
        self.qN = source["q_to_N"]
        self.m = math.sqrt(self.A)/self.F
        self.C = self.F**2/(3*MPL**2)
        self.K16 = self.A*source["WE_A_required_over_A"]
        self.rhostar = self.rho_rad(T_STAR)

    @staticmethod
    def rho_rad(T):
        return math.pi**2*G_STAR*T**4/30

    def integrate(self, theta_i, Ti, tol, *, linear=False, radiation_only=False):
        r_i = self.rho_rad(Ti)/self.A
        initial_v = theta_i**2/2 if linear else 2*math.sin(theta_i/2)**2
        span = math.log(Ti/T_STAR)

        def rhs(x, y):
            th, p, loss, r, rloss = y
            v = th**2/2 if linear else 2*math.sin(th/2)**2
            force = th if linear else math.sin(th)
            # Declared exact stationary controls represent mathematical 0,+/-pi.
            # Do not turn libm's sin(pi) roundoff into a fictitious physical seed.
            if not linear and th in (0.0, math.pi, -math.pi) and p == 0.0:
                force = 0.0
            h = math.sqrt(self.C*(r if radiation_only else r+p*p/2+v))
            return [p/h, -3*p-force/h, 3*p*p, -4*r, 4*r]

        sol = solve_ivp(rhs, (0,span), [theta_i,0,0,r_i,0], method="DOP853",
                        rtol=tol[0], atol=tol[1], max_step=0.02, dense_output=True)
        if not sol.success:
            raise RuntimeError(sol.message)
        grid = np.linspace(0,span,1001)
        theta,p,loss,r,rloss = sol.sol(grid)
        v = theta**2/2 if linear else 2*np.sin(theta/2)**2
        k = p*p/2
        e = k+v
        ledger = e+loss-initial_v
        radiation_analytic_error = np.max(np.abs(r/(r_i*np.exp(-4*grid))-1))
        rad_ledger = np.max(np.abs(r+rloss-r_i))/r_i
        ef, kf, vf = (float(x[-1]) for x in (e,k,v))
        pf, thf, lossf, rf = (float(x[-1]) for x in (p,theta,loss,r))
        h2 = self.C*(r if radiation_only else r+e)
        n_eta = 16*math.sqrt(self.K16/(self.A*kf)) if kf>0 else None
        row = {
            "T_i_GeV": Ti, "theta_i_rad": theta_i, "Delta_N_total": span,
            "theta_star_rad": thf, "p_star": pf,
            "theta_dot_star_GeV": self.m*pf,
            "a_field_dot_star_GeV2": math.sqrt(self.A)*pf,
            "u_site0_star_signed": self.qN*self.m*pf/(2*math.pi*T_STAR),
            "K_star_GeV4": self.A*kf, "V_star_GeV4": self.A*vf,
            "E_phi_star_GeV4": self.A*ef, "rho_rad_star_GeV4": self.A*rf,
            "rho_phi_over_rho_rad_star": ef/rf,
            "rho_kin_over_rho_rad_star": kf/rf,
            "H_star_over_H_radiation_star": math.sqrt(1+ef/rf),
            "initial_E_phi_GeV4": self.A*initial_v,
            "integrated_Hubble_loss_GeV4": self.A*lossf,
            "final_scalar_ledger_residual_GeV4": self.A*(ef+lossf-initial_v),
            "max_scalar_ledger_abs_error_over_A": float(np.max(np.abs(ledger))),
            "max_scalar_ledger_rel_initial_error": float(np.max(np.abs(ledger))/initial_v) if initial_v else 0.0,
            "max_radiation_ledger_rel_initial_error": float(rad_ledger),
            "max_radiation_analytic_rel_error": float(radiation_analytic_error),
            "max_scalar_energy_over_initial": float(np.max(e)/initial_v) if initial_v else 1.0,
            "min_K_over_A": float(np.min(k)), "min_V_over_A": float(np.min(v)),
            "min_radiation_over_A": float(np.min(r)),
            "min_H2_over_m2": float(np.min(h2)),
            "conditional_n_eta_for_final_instant": n_eta,
            "nfev": sol.nfev,
        }
        return row, sol, grid

    def analytic_linear(self, Ti, theta_i, grid):
        # Radiation domination H=1/(2t), z=m t; theta=z^-1/4(C_J J_1/4+C_Y Y_1/4).
        zi = 1/(2*math.sqrt(self.C*self.rho_rad(Ti)/self.A))
        z = zi*np.exp(2*grid)
        def basis(z):
            pref = z**(-0.25)
            b = np.array([pref*jv(0.25,z), pref*yv(0.25,z)])
            bp = np.array([pref*(jvp(0.25,z)-jv(0.25,z)/(4*z)),
                           pref*(yvp(0.25,z)-yv(0.25,z)/(4*z))])
            return b,bp
        b0,bp0 = basis(zi)
        constants = np.linalg.solve(np.array([b0,bp0]), np.array([theta_i,0.0]))
        b,bp = basis(z)
        return constants@b, constants@bp


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path("/workspace/AntiMatter/research/AM1231/v1.23"),
                        help="Public AM1231/v1.23 directory (or repository root)")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    source_root = args.source_root.resolve()
    if (source_root/"v1.23_summary.json").is_file():
        source_root = source_root.parents[2]
    if output == source_root or source_root in output.parents:
        raise ValueError("Outputs must be outside the immutable public checkout")
    output.mkdir(parents=True, exist_ok=True)
    sources = {name: sha(source_root/name) for name in SOURCE_NAMES}
    public = json.loads((source_root/SOURCE_NAMES[0]).read_text())
    model = Model(public)
    u = K_B/(2*math.pi*C_SPH*16)
    K16_independent = 0.5*(2*math.pi*F_ALPHA*T_STAR*u)**2
    assert math.isclose(model.F, model.qN*F_ALPHA, rel_tol=2e-15)
    assert math.isclose(model.K16, K16_independent, rel_tol=2e-14)
    assert math.isclose(model.K16/model.rhostar, public["WE_kinetic_over_radiation_n16"], rel_tol=2e-14)

    bounds = []
    for delta in DURATIONS:
        factor = 3*math.exp(2*delta)-2
        integral = quad(lambda x: 6*math.exp(-2*x), -delta, 0, epsabs=1e-12)[0]+1
        threshold = 16*math.sqrt(model.K16/(2*model.A)*factor)
        minimum = math.ceil(threshold)
        assert (model.K16*(16/minimum)**2*factor<=2*model.A and
                model.K16*(16/(minimum-1))**2*factor>2*model.A)
        bounds.append({"Delta_N_ending_at_T_star": delta,
                       "T_interval_start_GeV": T_STAR*math.exp(delta),
                       "energy_factor": factor,
                       "bound_n_eta_ge": threshold,
                       "minimum_integer_n_at_eta_1": minimum,
                       "factor_quadrature_abs_error": abs(factor-integral)})

    rows=[]
    for Ti in TEMPERATURES:
        for theta in PHASES:
            low,_,_ = model.integrate(theta,Ti,TOLS[0])
            high,_,_ = model.integrate(theta,Ti,TOLS[1])
            changes = [abs(low[k]-high[k]) for k in ["theta_star_rad","p_star"]]
            changes.extend(abs(low[k]-high[k])/model.A for k in ["K_star_GeV4","V_star_GeV4"])
            high["tolerance_endpoint_max_natural_scale_difference"] = max(changes)
            high["loose_nfev"] = low["nfev"]
            high["loose_max_scalar_ledger_abs_error_over_A"] = low["max_scalar_ledger_abs_error_over_A"]
            rows.append(high)

    controls={}
    for label,theta in [("bottom",0.0),("hilltop",math.pi)]:
        row,sol,grid = model.integrate(theta,2000,TOLS[1])
        controls[label] = {"max_abs_phase_departure": float(np.max(np.abs(sol.sol(grid)[0]-theta))),
                           "max_abs_p":float(np.max(np.abs(sol.sol(grid)[1]))),
                           "scalar_ledger_error_over_A":row["max_scalar_ledger_abs_error_over_A"]}
    positive,_,_=model.integrate(1.5,500,TOLS[1])
    negative,_,_=model.integrate(-1.5,500,TOLS[1])
    controls["reflection"] = {"endpoint_phase_sum":positive["theta_star_rad"]+negative["theta_star_rad"],
                              "endpoint_velocity_sum":positive["p_star"]+negative["p_star"],
                              "endpoint_energy_difference_over_A":(positive["E_phi_star_GeV4"]-negative["E_phi_star_GeV4"])/model.A}
    for label,linear,rad_only in [("linear_radiation_Bessel",True,True),
                                  ("full_small_angle_Bessel",False,False)]:
        theta_i=1e-5
        row,sol,grid=model.integrate(theta_i,2000,TOLS[1],linear=linear,radiation_only=rad_only)
        analytical=np.array(model.analytic_linear(2000,theta_i,grid))
        errors=np.max(np.abs(sol.sol(grid)[:2]-analytical),axis=1)/theta_i
        controls[label]={"max_phase_abs_error_over_initial_phase":float(errors[0]),
                         "max_p_abs_error_over_initial_phase":float(errors[1]),
                         "max_scalar_ledger_rel_initial_error":row["max_scalar_ledger_rel_initial_error"]}

    checks = {
        "all_initial_energies_at_most_2A": all(0<=r["initial_E_phi_GeV4"]<=2*model.A for r in rows),
        "all_sampled_energies_nonnegative_and_H_positive": all(r["min_K_over_A"]>=0 and r["min_V_over_A"]>=0 and r["min_radiation_over_A"]>0 and r["min_H2_over_m2"]>0 for r in rows),
        "scalar_ledger_below_1e_minus_7_A": all(r["max_scalar_ledger_abs_error_over_A"]<1e-7 and r["loose_max_scalar_ledger_abs_error_over_A"]<1e-7 for r in rows),
        "no_scalar_energy_above_initial_beyond_1e_minus_7_relative": all(r["max_scalar_energy_over_initial"]<1+1e-7 for r in rows),
        "radiation_analytic_error_below_1e_minus_8": all(r["max_radiation_analytic_rel_error"]<1e-8 for r in rows),
        "radiation_ledger_error_below_1e_minus_8": all(r["max_radiation_ledger_rel_initial_error"]<1e-8 for r in rows),
        "two_tolerance_endpoint_agreement_below_1e_minus_7": all(r["tolerance_endpoint_max_natural_scale_difference"]<1e-7 for r in rows),
        "bottom_and_hilltop_at_rest": all(controls[k][q]<1e-7 for k in ["bottom","hilltop"] for q in ["max_abs_phase_departure","max_abs_p"]),
        "reflection_below_1e_minus_7": all(abs(v)<1e-7 for v in controls["reflection"].values()),
        "Bessel_controls_below_3e_minus_7": all(controls[k][q]<3e-7 for k in ["linear_radiation_Bessel","full_small_angle_Bessel"] for q in ["max_phase_abs_error_over_initial_phase","max_p_abs_error_over_initial_phase"]),
        "public_inputs_unchanged": sources=={name:sha(source_root/name) for name in SOURCE_NAMES},
    }
    result={
        "date_user_facing":"2026-10-01 America/Los_Angeles", "host_date":"2026-10-02 UTC",
        "status":"PASS" if all(checks.values()) else "CHECK_FAILURE",
        "scope":"Fixed single cosine plus radiation only; pointwise velocity threshold, not integrated baryon yield",
        "software":{"python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__},
        "registration_sha256":sha(Path(__file__).with_name("REGISTRATION.md")),
        "audit_py_sha256":sha(__file__), "public_source_sha256":sources,
        "parameters":{"A_GeV4":model.A,"F_eff_GeV":model.F,"F_alpha_GeV":F_ALPHA,
                      "q_to_N":model.qN,"reduced_Mpl_GeV":MPL,"m_GeV":model.m,
                      "T_star_GeV":T_STAR,"g_star":G_STAR,"K_B":K_B,"c_sph":C_SPH,
                      "rho_kin_16_GeV4":model.K16,"rho_kin_16_independent_GeV4":K16_independent,
                      "rho_rad_star_GeV4":model.rhostar,"phases":PHASES,"initial_temperatures_GeV":TEMPERATURES,
                      "tolerances":[{"rtol":r,"atol":a} for r,a in TOLS],"max_step_N":0.02,"dense_check_samples":1001},
        "duration_bounds":bounds,"trajectories":rows,"controls":controls,"checks":checks,
        "largest_sampled_endpoint_K":max(rows,key=lambda r:r["K_star_GeV4"]),
        "summaries":{"max_scalar_ledger_error_over_A":max(r["max_scalar_ledger_abs_error_over_A"] for r in rows),
                     "max_scalar_ledger_rel_initial_error":max(r["max_scalar_ledger_rel_initial_error"] for r in rows),
                     "max_radiation_analytic_rel_error":max(r["max_radiation_analytic_rel_error"] for r in rows),
                     "max_radiation_ledger_rel_initial_error":max(r["max_radiation_ledger_rel_initial_error"] for r in rows),
                     "max_tolerance_endpoint_natural_scale_difference":max(r["tolerance_endpoint_max_natural_scale_difference"] for r in rows),
                     "max_scalar_energy_over_initial":max(r["max_scalar_energy_over_initial"] for r in rows)},
    }
    (output/"results.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    write_csv(output/"trajectories.csv",rows)
    write_csv(output/"duration_bounds.csv",bounds)
    (output/"RESULTS.md").write_text(report(result,source_root))
    print(json.dumps({"status":result["status"],"checks":checks,"summaries":result["summaries"],
                      "duration_bounds":bounds,"largest_sampled_endpoint_K":result["largest_sampled_endpoint_K"],"controls":controls},indent=2))
    return 0 if all(checks.values()) else 1


def report(r, source_root):
    p=r["parameters"]
    best=r["largest_sampled_endpoint_K"]
    s=r["summaries"]
    lines=["# Source-only duration bound and autonomous fixed-cosine trajectories", "",
        "Date: October 1, 2026 Pacific (host date October 2 UTC). Candidate computation outside the public checkpoint.","",
        "The new result is a conditional **duration-dependent necessary energy bound**. Maintaining the frozen phenomenological speed threshold for 0.1 e-fold before T_* requires n eta >= %.9f (n >= %d at eta=1), strengthening the instantaneous n>=35 allowance. This is not a baryogenesis calculation." % (r["duration_bounds"][2]["bound_n_eta_ge"],r["duration_bounds"][2]["minimum_integer_n_at_eta_1"]),"",
        "## Model and canonical normalization", "",
        "Use V=A[1-cos(theta)] and a_field=F_eff theta, with A=%.12g GeV^4 and F_eff=%.12g GeV = 3^30 * 250 GeV. The endpoint cosine is cos(a_field/F_eff). The conditional site-0 identification is theta_0=3^30 theta, tau_1=theta_0/(2 pi), so K=0.5(F_eff theta_dot)^2. The potential's full height is 2A." % (p["A_GeV4"],p["F_eff_GeV"]),"",
        "Flat expanding homogeneous FRW contains separately conserved radiation and this scalar only. g_*=106.75 is constant, T=T_i exp[-(N-N_i)], rho_rad=pi^2 g_* T^4/30, and 3 Mbar_Pl^2 H^2=rho_rad+K+V with Mbar_Pl=2.435e18 GeV. The potential is fixed; there is no driver work or dissipation beyond expansion.","",
        "With p=F_eff theta_dot/sqrt(A), r=rho_rad/A, h=H/(sqrt(A)/F_eff), the dimensionless equations are theta'=p/h, p'=-3p-sin(theta)/h, r'=-4r and h^2=F_eff^2(r+p^2/2+1-cos(theta))/(3 Mbar_Pl^2). The integrated ledgers are L_phi'=3p^2 and L_rad'=4r. The scalar ledger measures cosmological dilution by expansion, not energy deposited into radiation.","",
        "## Analytic duration bound", "",
        "The inherited linear relation supplies u=|dot(tau_1)|/T, with rho_kin(16,1)=%.12g GeV^4. Keeping the required u fixed at given n and relative efficiency eta implies K_req(N)=K_req,* exp[-2(N-N_*)], where K_req,*=rho_kin(16,1)[16/(n eta)]^2. This pointwise threshold is an additional imposed requirement. An integrated baryon yield need not require this profile." % p["rho_kin_16_GeV4"],"",
        "For any qualifying interval [N_*-Delta N,N_*], scalar conservation gives E_start=E_end+6 integral K dN. If it began from rest in the same fixed source at or before this interval, E_start<=2A. Since V>=0 and K>=K_req pointwise,", "",
        "    2A >= E_start >= K_req,* + 6 integral_{-Delta N}^0 K_req,* exp(-2x) dx", 
        "       = K_req,* [3 exp(2 Delta N)-2]", "",
        "    n eta >= 16 sqrt{rho_kin(16,1)/(2A) [3 exp(2 Delta N)-2]}.","",
        "| Delta N ending at T_* | Interval start T (GeV) | Required n eta | Minimum n at eta=1 |",
        "|---:|---:|---:|---:|"]
    for b in r["duration_bounds"]:
        lines.append("| %.2f | %.6f | %.9f | %d |" % (b["Delta_N_ending_at_T_star"],b["T_interval_start_GeV"],b["bound_n_eta_ge"],b["minimum_integer_n_at_eta_1"]))
    lines += ["", "At Delta N=0 this recovers the public full-drop value 34.603347068 and integer 35. A positive threshold cannot hold at the release instant when the field is at rest; a qualifying interval must start later. Equality in this optimistic budget is not guaranteed attainable. A hilltop initially exactly at rest remains at rest. Initial potential below 2A, prior Hubble losses, residual potential, and additional dissipation strengthen the bound; initial kinetic energy or external work changes the budget.","",
        "This formula applies only to intervals ending at T_*. For an interval extending from N_*-a to N_*+b, the analogous necessary budget is K_req,*[3 exp(2a)-2 exp(-2b)]<=E_cap. Substituting its total width a+b into the endpoint table is unjustified. For a known smaller energy cap one may replace 2A by E_cap. Eta is a relative yield-law parameter, not an energy-conversion fraction.","",
        "## Registered trajectory sample", "",
        "DOP853 integrates the fixed 10 phases at T_i=200,500,2000 GeV, initially at rest, to T_*=131.7 GeV, twice at (rtol,atol)=(1e-9,1e-11) and (1e-11,1e-13), max_step=0.02. Each dense solution is checked at 1001 fixed points. The grid was registered before integration and was not refined. The CSV reports all 30 cases; the table gives the largest endpoint K among the 10 registered phases for each T_i.","",
        "| T_i (GeV) | Sampled theta_i | K_* (GeV^4) | V_* (GeV^4) | rho_phi/rho_rad | Conditional n eta |",
        "|---:|---:|---:|---:|---:|---:|"]
    for Ti in TEMPERATURES:
        x=max((x for x in r["trajectories"] if x["T_i_GeV"]==Ti),key=lambda x:x["K_star_GeV4"])
        lines.append("| %.0f | %.9f | %.9g | %.9g | %.9g | %.9f |" % (Ti,x["theta_i_rad"],x["K_star_GeV4"],x["V_star_GeV4"],x["rho_phi_over_rho_rad_star"],x["conditional_n_eta_for_final_instant"]))
    lines += ["", "The largest sampled endpoint K is %.12g GeV^4 (%.9f A), at T_i=%.0f GeV and theta_i=%.9f. Its conditional final-instant requirement is n eta >= %.9f. This is a sampled endpoint value, not an optimized trajectory or an integrated yield. Increasing n or changing eta only changes that inferred threshold in this computation; it does not reduce the actual scalar energy of an already fixed trajectory." % (best["K_star_GeV4"],best["K_star_GeV4"]/p["A_GeV4"],best["T_i_GeV"],best["theta_i_rad"],best["conditional_n_eta_for_final_instant"]),"",
        "For that sampled case, the scalar ledger (GeV^4) is E_initial = %.12g, E_final = %.12g, integrated 6K dN = %.12g, residual = %.6g. Its total scalar/radiation ratio is %.9g, while its kinetic/radiation ratio is %.9g; both components enter Friedmann." % (best["initial_E_phi_GeV4"],best["E_phi_star_GeV4"],best["integrated_Hubble_loss_GeV4"],best["final_scalar_ledger_residual_GeV4"],best["rho_phi_over_rho_rad_star"],best["rho_kin_over_rho_rad_star"]),"",
        "## Verification", "",
        "All registered checks: **%s**. The worst tight-run scalar-ledger error is %.3g A (worst relative to initial scalar energy %.3g). Radiation is checked separately: worst analytic-scaling relative error %.3g and ledger relative error %.3g. Maximum endpoint difference across the two tolerances, using theta,p and K/A,V/A natural scales, is %.3g. Sampled K and V are nonnegative, radiation and H^2 are positive, and no sampled scalar energy exceeds its initial value beyond the stated tolerance." % (r["status"],s["max_scalar_ledger_error_over_A"],s["max_scalar_ledger_rel_initial_error"],s["max_radiation_analytic_rel_error"],s["max_radiation_ledger_rel_initial_error"],s["max_tolerance_endpoint_natural_scale_difference"]),"",
        "The small-angle control uses the exact prescribed-radiation solution theta=z^(-1/4)[C_J J_(1/4)(z)+C_Y Y_(1/4)(z)], z=mt=m/(2H_rad), with theta_i=1e-5 and zero initial velocity. The constants are fixed at T_i=2000 GeV. This independently checks the linear damping normalization; full nonlinear small-angle evolution approaches it because scalar backreaction and anharmonicity vanish with amplitude.","",
        "| Control | Max phase error / theta_i | Max p error / theta_i |", "|---|---:|---:|"]
    for name in ["linear_radiation_Bessel","full_small_angle_Bessel"]:
        c=r["controls"][name]
        lines.append("| %s | %.3g | %.3g |" % (name,c["max_phase_abs_error_over_initial_phase"],c["max_p_abs_error_over_initial_phase"]))
    lines += ["", "Bottom and exact hilltop controls remain exactly at rest. For these declared mathematical stationary points, the RHS returns zero force when theta is exactly 0 or +/-pi and p=0; floating-point sin(pi) is not treated as a physical seed. Reflection theta_i -> -theta_i reverses the velocity and preserves scalar energy. Thus selecting a rolling sign here does not derive a physical CP-odd bias.","",
        "## Limits and provenance", "",
        "This source-only model omits the analytic finite-temperature potential, autonomous driver/reservoir, CP-odd invariant, sphaleron/washout/spectator transport, and odd-relic evolution requested by the public next-step program. It is not the full Wilson or inherited scalar model. The public misalignment estimate uses relaxed curvature 0.918434 A; this explicit single-cosine diagnostic instead uses A/F_eff^2 and stops at T_*. It makes no new late-time relic prediction. Pair production is not a matter-antimatter asymmetry. No physical asymmetry success, operator construction, or scientific novelty is claimed.","",
        "Public source anchors (SHA-256 values are in results.json):"]
    for name in SOURCE_NAMES:
        lines.append("- [%s](%s)" % (Path(name).name,source_root/name))
    lines += ["", "The public source files were hashed before and after the run and remained unchanged. Only candidate outputs outside the checkout were written. The exact benchmark densities were independently recomputed from F_alpha,T_*,K_B,c_sph,g_* and agree with the published ratios within 2e-14 relative tolerance. Duration factors also agree with independent numerical quadrature, and every reported integer passes while its predecessor fails.","",
        "Reproduce using existing dependencies:","", "```bash", "cd /workspace/research-progress/antimatter/source-duration", 
        "/workspace/AntiMatter/.venv/bin/python audit.py", "# Independent output folder:",
        "/workspace/AntiMatter/.venv/bin/python audit.py --output-dir /tmp/antimatter-source-duration-replay", "```", "",
        "Software: Python %s, NumPy %s, SciPy %s. See [REGISTRATION.md](REGISTRATION.md), [audit.py](audit.py), [results.json](results.json), [trajectories.csv](trajectories.csv), and [duration_bounds.csv](duration_bounds.csv)." % (r["software"]["python"],r["software"]["numpy"],r["software"]["scipy"]),"",
        "Implementation correction before the final rerun: the exact stationary control explicitly returns zero force, removing the artificial sin(pi) floating-point seed. The first run had already passed its registered tolerance; no scan phase, physical parameter, target, tolerance, or threshold was changed. This correction implements the registered exact-rest control rather than treating numerical roundoff as dynamics.",""]
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
