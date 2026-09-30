#!/usr/bin/env python3
"""Deterministic v1.23 audit/release generator.

This script extends the verified v1.22 antimatter-hypothesis benchmark with:
  * an exact compact-character obstruction for the gauged q=3 scalar moose;
  * nonlocal-instanton normalization, harmonic, and shortcut tests;
  * a standalone 31-holonomy Wilson-line replacement benchmark;
  * the site mapping and energy budget of the WE-DWSB scaffold;
  * source misalignment, discrete-wall, and stable-odd-relic diagnostics.

It deliberately does not claim a UV completion or successful baryogenesis.
"""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal, getcontext
import hashlib
import io
import json
import math
import os
from pathlib import Path
import shutil
import sys
import zipfile

os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl-v123")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq
from scipy.special import kn, zeta


VERSION = "v1.23"
TITLE = "Wilson-line, nonlocal-instanton, baryogenesis-energy, and cosmology audit"
EXPECTED_PARENT_SHA256 = "44e5e29bb345e3da82d1dbddcc662b1e6c852f99bf951a3a6f5038da4bb8b807"
FIXED_ZIP_TIME = (2026, 8, 17, 12, 0, 0)

# Frozen v1.22 benchmark.
Q = 3
N = 30
QN = Q**N
LAMBDA = 185.0
C_X = 0.5294026257283574
A_LOCAL = C_X * LAMBDA**4
DRIVE_PROJECTED = A_LOCAL / QN
F_ALPHA = 250.0
S_INV = sum(Q ** (-2 * j) for j in range(N + 1))
F_EFF = QN * F_ALPHA
STRESS_PARENT = 0.0062067040170963395
PURITY_TARGET = 0.01
PURITY_REMAINING = PURITY_TARGET - STRESS_PARENT
ETA = 0.0594611917745775
ZETA_30 = 0.6370331362040969
M_SIGMA = 0.6540921655418205
M_SOURCE_RELAXED_GEV = 4.63642e-13

# WE-DWSB inherited/frozen phenomenology.
K_B_EXACT = 1.020689
K_B_ROUNDED = 1.03
C_SPH = 0.0195
N_DET_PARENT = 16
T_SPH = 131.7
G_STAR_EW = 106.75

# Cosmology conventions.
MPL_REDUCED = 2.435e18
MPL_UNREDUCED = 1.22089e19
S0_CM3 = 2891.2
RHO_CRIT_H2_GEV_CM3 = 1.05375e-5
OMEGA_DM_H2 = 0.12


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        if value == 0:
            return "0"
        if abs(value) >= 1e6 or abs(value) < 1e-5:
            return f"{value:.12e}"
        return f"{value:.12g}"
    return str(value)


def bisect_increasing(fn, lo: float, hi: float, target: float, iterations: int = 160) -> float:
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        if fn(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def verify_parent(parent_zip: Path) -> tuple[list[dict], dict]:
    archive_sha = sha256_file(parent_zip)
    archive_ok = archive_sha == EXPECTED_PARENT_SHA256
    rows: list[dict] = [
        {
            "check": "AM122_COMPLETE archive SHA-256",
            "observed": archive_sha,
            "expected": EXPECTED_PARENT_SHA256,
            "status": "PASS" if archive_ok else "FAIL",
        }
    ]
    internal_checked = 0
    internal_failed = 0
    with zipfile.ZipFile(parent_zip, "r") as zf:
        bad_zip = zf.testzip()
        rows.append(
            {
                "check": "ZIP CRC/integrity",
                "observed": "no bad member" if bad_zip is None else bad_zip,
                "expected": "no bad member",
                "status": "PASS" if bad_zip is None else "FAIL",
            }
        )
        names = set(zf.namelist())
        ledger_name = next((n for n in names if n.endswith("v1.22_SHA256.txt")), None)
        if ledger_name:
            ledger = zf.read(ledger_name).decode("utf-8")
            for line in ledger.splitlines():
                if not line.strip():
                    continue
                expected, member = line.split(None, 1)
                member = member.strip().lstrip("*")
                internal_checked += 1
                if member not in names or sha256_bytes(zf.read(member)) != expected:
                    internal_failed += 1
            rows.append(
                {
                    "check": "internal SHA ledger",
                    "observed": f"{internal_checked - internal_failed}/{internal_checked} pass",
                    "expected": "all listed members pass",
                    "status": "PASS" if internal_failed == 0 else "FAIL",
                }
            )
        else:
            rows.append(
                {
                    "check": "internal SHA ledger",
                    "observed": "missing",
                    "expected": "v1.22_SHA256.txt",
                    "status": "FAIL",
                }
            )
    metadata = {
        "archive_sha256": archive_sha,
        "archive_sha_matches_expected": archive_ok,
        "internal_hashes_checked": internal_checked,
        "internal_hashes_failed": internal_failed,
        "all_pass": archive_ok and internal_failed == 0 and all(r["status"] == "PASS" for r in rows),
    }
    return rows, metadata


def massive_kernel(x: float) -> float:
    return math.exp(-x) * (1.0 + x + x * x / 3.0)


def wilson_force_envelope(x: float, nmax: int = 10000) -> float:
    p1 = 1.0 + x + x * x / 3.0
    total = 0.0
    for n in range(2, nmax + 1):
        pn = 1.0 + n * x + (n * x) ** 2 / 3.0
        term = math.exp(-(n - 1) * x) * pn / (n**4 * p1)
        total += term
        if term < 1e-18:
            break
    return total


def wilson_curvature_ratio(x: float, at_top: bool = False, nmax: int = 10000) -> float:
    p1 = 1.0 + x + x * x / 3.0
    total = 0.0
    for n in range(1, nmax + 1):
        sign = (-1.0) ** n if at_top else 1.0
        term = sign * math.exp(-(n - 1) * x) * (1.0 + n * x + (n * x) ** 2 / 3.0) / (n**3 * p1)
        total += term
        if n > 5 and abs(term) < 1e-18:
            break
    return total


def wilson_amplitude_and_radial_force_ratios(x: float, nmax: int = 10000) -> tuple[float, float]:
    """Return sum A_n/A_1 and sum |d A_n/d ln R|/A_1 at fixed particle mass."""
    p1 = 1.0 + x + x * x / 3.0
    amplitude = 0.0
    radial_force = 0.0
    for n in range(1, nmax + 1):
        z = n * x
        pz = 1.0 + z + z * z / 3.0
        ratio = math.exp(-(n - 1) * x) * pz / (n**5 * p1)
        dlog_dlogr = -4.0 + z * (-1.0 + (1.0 + 2.0 * z / 3.0) / pz)
        amplitude += ratio
        radial_force += abs(ratio * dlog_dlogr)
        if n > 5 and ratio < 1e-18:
            break
    return amplitude, radial_force


def dilute_instanton_force_ratio(action: float) -> float:
    """Stable evaluation of sum_{n>=2} n exp[-(n-1) action]."""
    x = math.exp(-action)
    return x * (2.0 - x) / (1.0 - x) ** 2


def decimal_smallest_tridiagonal_eigenvalue(k_link: float, k_endpoint: float) -> float:
    """Small endpoint-induced eigenvalue of the 31x31 clockwork tridiagonal Hessian."""
    getcontext().prec = 105
    kl = Decimal(str(k_link))
    ke = Decimal(str(k_endpoint))

    def determinant(lam: Decimal) -> Decimal:
        diag = [kl] + [Decimal(10) * kl] * (N - 1) + [Decimal(9) * kl + ke]
        off_sq = (Decimal(3) * kl) ** 2
        d_prev = diag[0] - lam
        d_now = (diag[1] - lam) * d_prev - off_sq
        for idx in range(2, N + 1):
            d_prev, d_now = d_now, (diag[idx] - lam) * d_now - off_sq * d_prev
        return d_now

    if k_endpoint >= 0:
        lo, hi = Decimal("0"), Decimal("1e-23")
    else:
        lo, hi = Decimal("-1e-23"), Decimal("0")
    flo = determinant(lo)
    for _ in range(350):
        mid = (lo + hi) / 2
        fmid = determinant(mid)
        if flo * fmid <= 0:
            hi = mid
        else:
            lo, flo = mid, fmid
    return float((lo + hi) / 2)


def radiation_hubble(T: float, gstar: float, reduced: bool = True) -> float:
    if reduced:
        return math.sqrt(math.pi**2 * gstar / 90.0) * T**2 / MPL_REDUCED
    return 1.66 * math.sqrt(gstar) * T**2 / MPL_UNREDUCED


def build_calculations() -> dict:
    # Exact gauged character theorem.
    primitive = [Q ** (N - j) for j in range(N + 1)]
    primitive_degree = sum(primitive)
    f_invariant_short = F_ALPHA / (QN * S_INV)
    period_ratio = F_EFF / f_invariant_short

    source_rows = [
        {
            "quantity": "physical local/endpoint potential height A",
            "value": fmt(A_LOCAL),
            "unit": "GeV^4",
            "meaning": "height required for the inherited long-period force",
        },
        {
            "quantity": "A^(1/4)",
            "value": fmt(A_LOCAL**0.25),
            "unit": "GeV",
            "meaning": "local source energy scale",
        },
        {
            "quantity": "projected force normalization D=A/3^30",
            "value": fmt(DRIVE_PROJECTED),
            "unit": "GeV^4",
            "meaning": "not the physical potential height",
        },
        {
            "quantity": "D^(1/4)",
            "value": fmt(DRIVE_PROJECTED**0.25),
            "unit": "GeV",
            "meaning": "41.659 MeV drive scale",
        },
        {
            "quantity": "F_alpha",
            "value": fmt(F_ALPHA),
            "unit": "GeV",
            "meaning": "local/site-0 canonical scale",
        },
        {
            "quantity": "F_eff=3^30 F_alpha",
            "value": fmt(F_EFF),
            "unit": "GeV",
            "meaning": "desired endpoint period",
        },
        {
            "quantity": "primitive invariant period",
            "value": fmt(f_invariant_short),
            "unit": "GeV",
            "meaning": "compact invariant character has ultra-short period",
        },
    ]

    character_rows = []
    for j, kj in enumerate(primitive):
        character_rows.append(
            {
                "site": j,
                "primitive_k_j": kj,
                "kernel_check_kj_minus_3_kjplus1": "" if j == N else kj - Q * primitive[j + 1],
                "zero_mode_theta_weight_3_minus_j": fmt(Q ** (-j)),
            }
        )

    # Instanton action/purity ledger.
    instanton_rows = []
    for desired_name, height in [("projected D (too weak for long-period force)", DRIVE_PROJECTED), ("required A_local", A_LOCAL)]:
        for pref_name, prefactor in [("Lambda", LAMBDA), ("4pi Lambda", 4 * math.pi * LAMBDA)]:
            action = math.log(prefactor**4 / height)
            coupling = math.sqrt(8 * math.pi**2 / action)
            tower_force = dilute_instanton_force_ratio(action)
            instanton_rows.append(
                {
                    "desired_height": desired_name,
                    "prefactor": pref_name,
                    "prefactor_GeV": fmt(prefactor),
                    "action_S": fmt(action),
                    "diagnostic_g_sqrt_8pi2_over_S": fmt(coupling),
                    "dilute_tower_force_ratio": fmt(tower_force),
                    "purity_status": "PASS" if tower_force < PURITY_REMAINING else "FAIL",
                    "interpretation": "conditional; determinant/running not computed",
                }
            )
    instanton_action_gate = brentq(
        lambda s: dilute_instanton_force_ratio(s) - PURITY_REMAINING,
        0.1,
        30.0,
    )

    harmonic_rows = []
    for n in range(2, 6):
        harmonic_rows.append(
            {
                "harmonic_n": n,
                "minimum_action_gap_equal_prefactors": fmt(math.log(n / PURITY_REMAINING)),
                "criterion": "per-contaminant bound S_n-S_1 > ln(n/b_remaining); combined force sum must still stay below b_remaining",
            }
        )
    site_action_gap_rows = []
    for j in [29, 28, 20, 10, 0]:
        gap = (N - j) * math.log(Q) + math.log(1.0 / PURITY_REMAINING)
        site_action_gap_rows.append(
            {
                "unwanted_site_j": j,
                "minimum_Sj_minus_S30": fmt(gap),
                "criterion": "per-site equal-determinant bound if this term alone uses the budget; combined site sum must still stay below it",
            }
        )

    direct_suppression_action = math.log(LAMBDA**4 / DRIVE_PROJECTED)
    per_edge_action = direct_suppression_action / N
    two_edge_shortcut = math.exp(-2 * per_edge_action)
    physical_height_action = math.log(LAMBDA**4 / A_LOCAL)
    physical_per_edge_action = physical_height_action / N
    physical_two_edge_shortcut = math.exp(-2 * physical_per_edge_action)
    inherited_gap = 2.7872599926676243
    full_action_from_gap = N * inherited_gap
    amplitude_from_gap = LAMBDA**4 * math.exp(-full_action_from_gap)
    uniform_rows = [
        {
            "scenario": "fit correctly normalized physical A_local with uniform propagator",
            "full_action": fmt(physical_height_action),
            "per_edge_Mgap_a": fmt(physical_per_edge_action),
            "two_edge_coefficient": fmt(physical_two_edge_shortcut),
            "result": "FAIL_STRONGER",
            "reason": f"two-edge coefficient exceeds {PURITY_REMAINING:.6g} by {physical_two_edge_shortcut/PURITY_REMAINING:.3f}x",
        },
        {
            "scenario": "fit projected D with uniform propagator (conservative weaker no-go)",
            "full_action": fmt(direct_suppression_action),
            "per_edge_Mgap_a": fmt(per_edge_action),
            "two_edge_coefficient": fmt(two_edge_shortcut),
            "result": "FAIL",
            "reason": f"two-edge coefficient exceeds {PURITY_REMAINING:.6g} by {two_edge_shortcut/PURITY_REMAINING:.3f}x",
        },
        {
            "scenario": "impose inherited two-edge locality gap; compare with projected D",
            "full_action": fmt(full_action_from_gap),
            "per_edge_Mgap_a": fmt(inherited_gap),
            "two_edge_coefficient": fmt(math.exp(-2 * inherited_gap)),
            "result": "FAIL_AMPLITUDE",
            "reason": f"max full-chain height {amplitude_from_gap:.6e} GeV^4 undershoots D by {DRIVE_PROJECTED/amplitude_from_gap:.3e}",
        },
        {
            "scenario": "impose inherited two-edge locality gap; compare with physical A_local",
            "full_action": fmt(full_action_from_gap),
            "per_edge_Mgap_a": fmt(inherited_gap),
            "two_edge_coefficient": fmt(math.exp(-2 * inherited_gap)),
            "result": "FAIL_AMPLITUDE_STRONGER",
            "reason": f"max full-chain height {amplitude_from_gap:.6e} GeV^4 undershoots A_local by {A_LOCAL/amplitude_from_gap:.3e}",
        },
    ]

    # Standalone Wilson-line benchmark.
    f_site = F_ALPHA / math.sqrt(S_INV)
    d_endpoint = 8
    d_link = 4
    x_endpoint = 4.25
    target_link_kernel = (d_endpoint / d_link) * massive_kernel(x_endpoint)
    x_link = brentq(lambda x: massive_kernel(x) - target_link_kernel, 0.0, x_endpoint)
    c_single = 3.0 / (64.0 * math.pi**6)
    r_inverse = (A_LOCAL / (d_endpoint * c_single * massive_kernel(x_endpoint))) ** 0.25
    g4 = r_inverse / (2 * math.pi * f_site)
    g5_sq = 2 * math.pi * g4**2 / r_inverse
    m_endpoint = x_endpoint * r_inverse / (2 * math.pi)
    m_link = x_link * r_inverse / (2 * math.pi)
    wilson_harmonic = wilson_force_envelope(x_endpoint)
    x_harmonic_gate = brentq(lambda x: wilson_force_envelope(x) - PURITY_REMAINING, 0.0, 20.0)
    combined_stress = STRESS_PARENT + wilson_harmonic
    remaining_after_wilson = PURITY_TARGET - combined_stress
    hop_bound = math.sqrt(remaining_after_wilson)
    geometric_gap_tightened = -math.log(hop_bound)

    link_curvature_ratio = wilson_curvature_ratio(x_link)
    endpoint_curvature_min_ratio = wilson_curvature_ratio(x_endpoint)
    endpoint_curvature_top_ratio = wilson_curvature_ratio(x_endpoint, at_top=True)
    k_link = A_LOCAL * link_curvature_ratio / f_site**2
    k_endpoint_min = A_LOCAL * endpoint_curvature_min_ratio / f_site**2
    k_endpoint_top = A_LOCAL * endpoint_curvature_top_ratio / f_site**2

    link_q = np.zeros((N, N + 1))
    for j in range(N):
        link_q[j, j] = 1.0
        link_q[j, j + 1] = -Q
    source_off_hessian = k_link * (link_q.T @ link_q)
    source_off_eigs = np.linalg.eigvalsh(source_off_hessian)
    endpoint_vec = np.zeros(N + 1)
    endpoint_vec[-1] = 1.0
    min_eigs = np.linalg.eigvalsh(source_off_hessian + k_endpoint_min * np.outer(endpoint_vec, endpoint_vec))
    top_eigs = np.linalg.eigvalsh(source_off_hessian + k_endpoint_top * np.outer(endpoint_vec, endpoint_vec))
    small_min = decimal_smallest_tridiagonal_eigenvalue(k_link, k_endpoint_min)
    small_top = decimal_smallest_tridiagonal_eigenvalue(k_link, k_endpoint_top)

    c_eff = 11.0
    loop_parameter = c_eff * g4**2 / (16 * math.pi**2)
    nda_cutoff = 12 * math.pi**2 * r_inverse / (c_eff * g4**2)
    scalar_beta_max = 22.0 / 3.0
    scalar_beta_loop = scalar_beta_max * g4**2 / (16 * math.pi**2)
    adjacent_mixing_estimate = 2 * g4**2 / (16 * math.pi**2) * math.log(nda_cutoff / m_link)
    m5 = (MPL_REDUCED**2 * r_inverse / (2 * math.pi)) ** (1.0 / 3.0)
    endpoint_amplitude_ratio, endpoint_radial_force_ratio = wilson_amplitude_and_radial_force_ratios(x_endpoint)
    link_amplitude_ratio, link_radial_force_ratio = wilson_amplitude_and_radial_force_ratios(x_link)
    radion_force_abs = A_LOCAL * (endpoint_radial_force_ratio + N * link_radial_force_ratio)
    radion_barrier_scale = (A_LOCAL * (endpoint_amplitude_ratio + N * link_amplitude_ratio)) ** 0.25
    radion_mass_1pct_meV = math.sqrt(radion_force_abs / (0.01 * 1.5 * MPL_REDUCED**2)) * 1e12
    mild_axion_wgc = x_endpoint * F_EFF / MPL_REDUCED
    charge_matrix = np.zeros((N + 1, N + 1))
    charge_matrix[:N, :] = link_q
    charge_matrix[N, N] = 1.0
    charge_masses = np.array([m_link] * N + [m_endpoint])
    z_matrix = (g4 * MPL_REDUCED / charge_masses[:, None]) * charge_matrix
    z_sigma_min = np.linalg.svd(z_matrix, compute_uv=False)[-1]
    z_support_lower = z_sigma_min / math.sqrt(N + 1)

    wilson_rows = [
        {"quantity": "sites/holonomies", "value": N + 1, "unit": "count", "status": "chosen"},
        {"quantity": "site Wilson scale", "value": fmt(f_site), "unit": "GeV", "status": "derived"},
        {"quantity": "F_alpha", "value": fmt(F_ALPHA), "unit": "GeV", "status": "exact target"},
        {"quantity": "F_eff", "value": fmt(F_EFF), "unit": "GeV", "status": "PASS_EXACT"},
        {"quantity": "endpoint real degrees", "value": d_endpoint, "unit": "count", "status": "four charged complex scalars or same net SUSY-broken determinant"},
        {"quantity": "link real degrees per edge", "value": d_link, "unit": "count", "status": "two charged complex scalars or same net SUSY-broken determinant"},
        {"quantity": "endpoint winding action x_E", "value": fmt(x_endpoint), "unit": "dimensionless", "status": "PASS_HARMONIC"},
        {"quantity": "link winding action x_L", "value": fmt(x_link), "unit": "dimensionless", "status": "amplitude matched"},
        {"quantity": "R inverse", "value": fmt(r_inverse), "unit": "GeV", "status": "derived"},
        {"quantity": "g4", "value": fmt(g4), "unit": "dimensionless", "status": "moderately coupled"},
        {"quantity": "endpoint particle mass", "value": fmt(m_endpoint), "unit": "GeV", "status": "below R inverse"},
        {"quantity": "link particle mass", "value": fmt(m_link), "unit": "GeV", "status": "below R inverse"},
        {"quantity": "endpoint force harmonics", "value": fmt(wilson_harmonic), "unit": "relative force", "status": "PASS"},
        {"quantity": "inherited continuity stress target plus Wilson harmonics", "value": fmt(combined_stress), "unit": "relative force", "status": "PASS_LT_1PCT_IF_PARENT_PROFILE_IS_PORTED"},
        {"quantity": "remaining continuity-design force budget", "value": fmt(remaining_after_wilson), "unit": "relative force", "status": "tight; parent profile not yet inherited"},
        {"quantity": "tightened r_hop", "value": fmt(hop_bound), "unit": "dimensionless", "status": "conditional"},
        {"quantity": "tightened M_gap a", "value": fmt(geometric_gap_tightened), "unit": "dimensionless", "status": "conditional"},
        {"quantity": "conservative C_eff=11 NDA loop proxy", "value": fmt(loop_parameter), "unit": "dimensionless", "status": "WATCH_NEAR_0P1_CONVENTION_DEPENDENT"},
        {"quantity": "exact scalar beta loop proxy b=22/3", "value": fmt(scalar_beta_loop), "unit": "dimensionless", "status": "moderately coupled"},
        {"quantity": "adjacent kinetic-mixing leading-log estimate", "value": fmt(adjacent_mixing_estimate), "unit": "dimensionless", "status": "must include full kinetic matrix next"},
        {"quantity": "5D NDA cutoff diagnostic C_eff=11", "value": fmt(nda_cutoff), "unit": "GeV", "status": "conditional; only about 7.5 KK levels"},
        {"quantity": "NDA cutoff times R", "value": fmt(nda_cutoff / r_inverse), "unit": "dimensionless", "status": "moderate separation not parametric"},
        {"quantity": "5D Planck scale diagnostic", "value": fmt(m5), "unit": "GeV", "status": "diagnostic"},
        {"quantity": "all-harmonic absolute dV/dlnR", "value": fmt(radion_force_abs), "unit": "GeV^4", "status": "radion source estimate"},
        {"quantity": "radion mass for <1pct displacement", "value": fmt(radion_mass_1pct_meV), "unit": "meV", "status": "canonical f_rho=sqrt(3/2) Mpl estimate"},
        {"quantity": "all-harmonic radion barrier scale proxy", "value": fmt(radion_barrier_scale), "unit": "GeV", "status": "OPEN_STABILIZATION"},
        {"quantity": "charge-basis determinant", "value": fmt(round(np.linalg.det(charge_matrix))), "unit": "integer", "status": "unimodular basis"},
        {"quantity": "diagonal-metric WGC sigma_min(Z)", "value": fmt(z_sigma_min), "unit": "dimensionless", "status": "conditional electric diagnostic"},
        {"quantity": "WGC support lower bound sigma_min/sqrt31", "value": fmt(z_support_lower), "unit": "dimensionless", "status": "passes unit and sqrt2 diagnostic thresholds"},
        {"quantity": "S_E F_eff/Mpl", "value": fmt(mild_axion_wgc), "unit": "dimensionless", "status": "passes mild conjectural check only"},
    ]
    wilson_hessian_rows = [
        {
            "configuration": "source off",
            "light_mode_eV": 0.0,
            "heavy_min_GeV": fmt(math.sqrt(max(source_off_eigs[1], 0.0))),
            "heavy_max_GeV": fmt(math.sqrt(source_off_eigs[-1])),
            "status": "one exact zero mode",
        },
        {
            "configuration": "source minimum",
            "light_mode_eV": fmt(math.sqrt(small_min) * 1e9),
            "heavy_min_GeV": fmt(math.sqrt(min_eigs[1])),
            "heavy_max_GeV": fmt(math.sqrt(min_eigs[-1])),
            "status": "PASS_BENCHMARK",
        },
        {
            "configuration": "source maximum",
            "light_mode_eV": fmt(math.sqrt(abs(small_top)) * 1e9),
            "heavy_min_GeV": fmt(math.sqrt(top_eigs[1])),
            "heavy_max_GeV": fmt(math.sqrt(top_eigs[-1])),
            "status": "one intended tachyon; heavy modes positive",
        },
    ]

    # Hybrid Wilson lock: exact topology failure despite kinematics.
    f_w = F_ALPHA
    inherited_heavy_max = 876.1890010493187
    b_lock = inherited_heavy_max**2 / (1 / f_w**2 + 1 / F_EFF**2)
    b_lock_all_phase = b_lock + A_LOCAL
    hybrid_rows = [
        {
            "quantity": "B lock height",
            "value": fmt(b_lock),
            "unit": "GeV^4",
            "status": "source-off gap only",
        },
        {
            "quantity": "B^(1/4)",
            "value": fmt(b_lock**0.25),
            "unit": "GeV",
            "status": "source-off gap only",
        },
        {
            "quantity": "B through source maximum",
            "value": fmt(b_lock_all_phase),
            "unit": "GeV^4",
            "status": "keeps lock gap at least inherited heavy maximum",
        },
        {
            "quantity": "B^(1/4) through source maximum",
            "value": fmt(b_lock_all_phase**0.25),
            "unit": "GeV",
            "status": "kinematically sufficient before topology test",
        },
        {
            "quantity": "gauge topology",
            "value": "closed w makes lock noninvariant; shifting w makes cos(w) noninvariant",
            "unit": "",
            "status": "FAIL_GAUGE_TOPOLOGY",
        },
    ]

    # WE-DWSB exact-K_B energy audit.
    u_req_exact = K_B_EXACT / (2 * math.pi * C_SPH * N_DET_PARENT)
    u_req_round = K_B_ROUNDED / (2 * math.pi * C_SPH * N_DET_PARENT)
    rho_rad_ew = math.pi**2 / 30.0 * G_STAR_EW * T_SPH**4
    rho_kin_exact = 0.5 * (2 * math.pi * F_ALPHA * T_SPH * u_req_exact) ** 2
    kinetic_fraction_exact = rho_kin_exact / rho_rad_ew
    u_max_local = math.sqrt(2 * A_LOCAL) / (2 * math.pi * F_ALPHA * T_SPH)
    amplitude_ratio_exact = (u_req_exact / u_max_local) ** 2
    missing_injection = rho_kin_exact - A_LOCAL
    n_energy_cont = N_DET_PARENT * u_req_exact / u_max_local
    n_backreact_1pct_cont = N_DET_PARENT * math.sqrt(kinetic_fraction_exact / 0.01)
    endpoint_fraction = kinetic_fraction_exact * QN**2
    endpoint_u_max = u_max_local / QN
    endpoint_n_min = n_energy_cont * QN

    wedwsb_rows = []
    for mapping, j in [("site 0 (unique least-cost map)", 0), ("site 1", 1), ("site 10", 10), ("endpoint site 30", 30)]:
        cost = Q ** (2 * j)
        wedwsb_rows.append(
            {
                "mapping": mapping,
                "site_j": j,
                "energy_multiplier": fmt(cost),
                "rho_kin_over_rho_rad_kappadyn1": fmt(kinetic_fraction_exact * cost),
                "continuous_n_det_energy_min": fmt(n_energy_cont * Q**j),
                "decision": "PASS_LEAST_COST_MAPPING_ONLY" if j == 0 else ("PRACTICALLY_EXCLUDED_FIXED_BENCHMARK" if j == 30 else "DISFAVORED_ENERGY_COST"),
            }
        )
    wedwsb_energy_rows = [
        {"quantity": "K_B exact", "value": fmt(K_B_EXACT), "unit": "dimensionless", "status": "frozen input"},
        {"quantity": "u required at n=16 kappa_dyn=1", "value": fmt(u_req_exact), "unit": "dimensionless", "status": "derived"},
        {"quantity": "rho_kin/rho_rad at n=16", "value": fmt(kinetic_fraction_exact), "unit": "dimensionless", "status": "FAIL_RD_SELF_CONSISTENCY"},
        {"quantity": "u maximum from one conservative source-height budget", "value": fmt(u_max_local), "unit": "dimensionless", "status": "autonomous moving driver could inject additional work"},
        {"quantity": "A required/A available without driver work", "value": fmt(amplitude_ratio_exact), "unit": "ratio", "status": "FAIL_N16_WITHOUT_DRIVER_INJECTION"},
        {"quantity": "missing injection at n=16 under single-height budget", "value": fmt(missing_injection), "unit": "GeV^4", "status": "OPEN_DRIVER"},
        {"quantity": "minimum integer n_det from single-height energy", "value": math.ceil(n_energy_cont), "unit": "count", "status": "CONDITIONAL_NEW_OPERATOR_OR_DRIVER"},
        {"quantity": "minimum integer n_det for <1% backreaction", "value": math.ceil(n_backreact_1pct_cont), "unit": "count", "status": "CONDITIONAL_NEW_OPERATOR"},
        {"quantity": "endpoint rho_kin/rho_rad", "value": fmt(endpoint_fraction), "unit": "dimensionless", "status": "PRACTICALLY_EXCLUDED_FIXED_BENCHMARK"},
        {"quantity": "endpoint u maximum", "value": fmt(endpoint_u_max), "unit": "dimensionless", "status": "PRACTICALLY_EXCLUDED_FIXED_BENCHMARK"},
        {"quantity": "endpoint continuous n_det minimum", "value": fmt(endpoint_n_min), "unit": "count", "status": "could be altered only by enormous winding or autonomous work"},
        {"quantity": "rounded-K_B u", "value": fmt(u_req_round), "unit": "dimensionless", "status": "legacy comparison"},
    ]

    # Constant-source misalignment.
    t_osc = math.sqrt(M_SOURCE_RELAXED_GEV * MPL_UNREDUCED / (3 * 1.66 * math.sqrt(G_STAR_EW)))
    entropy_osc = 2 * math.pi**2 / 45.0 * G_STAR_EW * t_osc**3
    number_density_theta1 = 0.5 * M_SOURCE_RELAXED_GEV * F_EFF**2
    yield_theta1 = number_density_theta1 / entropy_osc
    omega_theta1 = M_SOURCE_RELAXED_GEV * yield_theta1 * S0_CM3 / RHO_CRIT_H2_GEV_CM3
    theta_max = math.sqrt(OMEGA_DM_H2 / omega_theta1)
    relaxed_curvature_height = M_SOURCE_RELAXED_GEV**2 * F_EFF**2
    misalignment_rows = [
        {"quantity": "constant-source oscillation temperature", "value": fmt(t_osc), "unit": "GeV", "status": "standard-RD estimate for inherited/global scalar branch"},
        {"quantity": "Omega_a h2 coefficient", "value": fmt(omega_theta1), "unit": "times theta_i^2", "status": "FAIL_GENERIC_INITIAL_CONDITIONS_INHERITED_GLOBAL_BRANCH"},
        {"quantity": "theta_i maximum for Omega h2<=0.12", "value": fmt(theta_max), "unit": "radian", "status": "tuned unless tracking/decay/dilution/transient source"},
        {"quantity": "effective relaxed harmonic curvature m_a^2 F_eff^2", "value": fmt(relaxed_curvature_height), "unit": "GeV^4", "status": f"{relaxed_curvature_height/A_LOCAL:.6f} times underlying A; used in estimate"},
        {"quantity": "underlying written potential height A", "value": fmt(A_LOCAL), "unit": "GeV^4", "status": "normalization corrected; not directly substituted for relaxed curvature"},
    ]

    # Discrete walls.
    y_vev = ETA * LAMBDA
    f_y = math.sqrt(2) * y_vev
    b_y = 0.1
    n_y = 3
    m_y_phase = n_y * math.sqrt(b_y * LAMBDA**4) / f_y
    sigma_y = 8 * f_y * math.sqrt(b_y * LAMBDA**4) / n_y
    x_vev = C_X * LAMBDA
    f_x = math.sqrt(2) * x_vev
    b_x = 1.0
    n_x = 12
    m_x_phase = n_x * math.sqrt(b_x * LAMBDA**4) / f_x
    sigma_x = 8 * f_x * math.sqrt(b_x * LAMBDA**4) / n_x
    g_late = 3.36
    tdom_y = math.sqrt((sigma_y / (3 * MPL_REDUCED**2)) * MPL_REDUCED / math.sqrt(math.pi**2 * g_late / 90.0))
    tdom_x = math.sqrt((sigma_x / (3 * MPL_REDUCED**2)) * MPL_REDUCED / math.sqrt(math.pi**2 * g_late / 90.0))
    t_bbn = 0.005
    h_bbn = radiation_hubble(t_bbn, 10.75)
    bias_y = sigma_y * h_bbn
    bias_x = sigma_x * h_bbn
    wall_rows = [
        {
            "sector": "Y pin",
            "R_charge": 8,
            "unbroken_subgroup": "Z8^R",
            "N_DW": n_y,
            "f_GeV": fmt(f_y),
            "phase_mass_GeV": fmt(m_y_phase),
            "rigid_radius_wall_tension_estimate_GeV3": fmt(sigma_y),
            "scaling_domination_temperature_estimate_GeV": fmt(tdom_y),
            "status": "FAIL_IF_POSTINFLATION_FORMATION",
        },
        {
            "sector": "diagnostic dynamical X pin",
            "R_charge": 2,
            "unbroken_subgroup": "Z2^R",
            "N_DW": n_x,
            "f_GeV": fmt(f_x),
            "phase_mass_GeV": fmt(m_x_phase),
            "rigid_radius_wall_tension_estimate_GeV3": fmt(sigma_x),
            "scaling_domination_temperature_estimate_GeV": fmt(tdom_x),
            "status": "FAIL_IF_DYNAMIC_AND_UNBIASED",
        },
        {
            "sector": "Sigma",
            "R_charge": 17,
            "unbroken_subgroup": "no breaking at zero VEV",
            "N_DW": 0,
            "f_GeV": "",
            "phase_mass_GeV": "",
            "rigid_radius_wall_tension_estimate_GeV3": "",
            "scaling_domination_temperature_estimate_GeV": "",
            "status": "NO_NEW_WALL",
        },
        {
            "sector": "combined separate Y and X pins",
            "R_charge": "8 and 2",
            "unbroken_subgroup": "Z2^R",
            "N_DW": "12 per exact R orbit; 36 separate-pin minima",
            "f_GeV": "",
            "phase_mass_GeV": "",
            "rigid_radius_wall_tension_estimate_GeV3": "",
            "scaling_domination_temperature_estimate_GeV": "",
            "status": "ACCIDENTAL_THREE_ORBIT_DEGENERACY_UNLESS_CROSS_COUPLING_LIFTS",
        },
    ]
    wall_bias_rows = [
        {
            "sector": "Y",
            "annihilation_target_T_GeV": t_bbn,
            "pressure_balance_reference_bias_GeV4": fmt(bias_y),
            "pressure_balance_reference_over_Lambda4": fmt(bias_y / LAMBDA**4),
            "maximum_action_for_unit_Lambda4_prefactor": fmt(math.log(LAMBDA**4 / bias_y)),
            "status": "ORDER_ONE_NETWORK_UNCERTAINTY; NUMERIC_WINDOW OPEN; UV COMPATIBILITY UNPROVED",
        },
        {
            "sector": "X",
            "annihilation_target_T_GeV": t_bbn,
            "pressure_balance_reference_bias_GeV4": fmt(bias_x),
            "pressure_balance_reference_over_Lambda4": fmt(bias_x / LAMBDA**4),
            "maximum_action_for_unit_Lambda4_prefactor": fmt(math.log(LAMBDA**4 / bias_x)),
            "status": "ORDER_ONE_NETWORK_UNCERTAINTY; NUMERIC_WINDOW OPEN; UV COMPATIBILITY UNPROVED",
        },
    ]
    a3 = b_y * LAMBDA**4 / (2 * y_vev**3)
    thermal_rows = [
        {
            "quantity": "Y pin energy scale proxy",
            "value": fmt((b_y * LAMBDA**4) ** 0.25),
            "unit": "GeV",
            "status": "not a critical temperature",
        },
        {
            "quantity": "naive analytic cubic coefficient A3",
            "value": fmt(a3),
            "unit": "GeV",
            "status": "FAIL_RADIAL_NATURALNESS",
        },
        {
            "quantity": "A3/Lambda",
            "value": fmt(a3 / LAMBDA),
            "unit": "dimensionless",
            "status": "about 238; nonperturbative/unnatural and shifts the frozen radial stationary point without further terms",
        },
        {
            "quantity": "critical/restoration temperature",
            "value": "undetermined",
            "unit": "",
            "status": "FAIL_INCOMPLETE_THERMAL_POTENTIAL",
        },
    ]

    # Stable odd relic diagnostic.
    y_max_sigma = OMEGA_DM_H2 / (2.742e8 * M_SIGMA)
    g_boson = 2.0
    g_weyl = 2.0
    gstar_rel = 106.75
    y_rel = (45 * zeta(3) / (2 * math.pi**4)) * (g_boson + 0.75 * g_weyl) / gstar_rel
    omega_rel = 2.742e8 * M_SIGMA * y_rel
    overproduction = y_rel / y_max_sigma
    y_eff_sigma = 2 * ETA
    gamma_over_h_185 = (y_eff_sigma**2 * LAMBDA / (8 * math.pi)) / radiation_hubble(LAMBDA, G_STAR_EW)
    # Optimistic equilibrium ceiling with g=2 and g*s=100; explicitly only a diagnostic.
    def equilibrium_yield(x: float) -> float:
        return 45 * 2.0 / (4 * math.pi**4 * 100.0) * x * x * kn(2, x)

    x_equil = brentq(lambda x: equilibrium_yield(x) - y_max_sigma, 1.0, 100.0)
    sigma_rows = [
        {"quantity": "m_Sigma", "value": fmt(M_SIGMA), "unit": "GeV", "status": "unit lambda benchmark"},
        {"quantity": "maximum all-DM yield", "value": fmt(y_max_sigma), "unit": "n/s", "status": "upper bound"},
        {"quantity": "illustrative relativistic degenerate full-chiral yield", "value": fmt(y_rel), "unit": "n/s", "status": "FAIL_IF_ALL_FOUR_DEGREES_ARE_POPULATED"},
        {"quantity": "relativistic Omega h2", "value": fmt(omega_rel), "unit": "dimensionless", "status": "FAIL"},
        {"quantity": "yield overproduction factor", "value": fmt(overproduction), "unit": "ratio", "status": "FAIL"},
        {"quantity": "effective hidden coupling 2 eta", "value": fmt(y_eff_sigma), "unit": "dimensionless", "status": "lambda_Sigma=1"},
        {"quantity": "rough broken-phase Gamma/H at 185 GeV", "value": fmt(gamma_over_h_185), "unit": "ratio", "status": "only if zero-temperature Y VEV persists and channels are open; thermal phase unknown"},
        {"quantity": "optimistic no-repopulation equilibrium x=m/T", "value": fmt(x_equil), "unit": "dimensionless", "status": "diagnostic only"},
        {"quantity": "optimistic same-bath no-repopulation temperature ceiling", "value": fmt(M_SIGMA / x_equil), "unit": "GeV", "status": "requires zero initial/inflaton production; cold/sequestered hidden bath can evade"},
    ]

    branches = [
        {
            "branch": "original gauged scalar moose + nonlocal electric source",
            "gauge_invariance": "FAIL_THEOREM",
            "long_period": "FAIL",
            "messenger_anomaly_inheritance": "yes before failed source",
            "cosmology": "not reached",
            "decision": "REJECT",
        },
        {
            "branch": "uniform full-chain propagator",
            "gauge_invariance": "not sufficient",
            "long_period": "not sufficient",
            "messenger_anomaly_inheritance": "conditional",
            "cosmology": "not reached",
            "decision": "REJECT_SHORTCUT_CONFLICT",
        },
        {
            "branch": "global scalar moose + endpoint hidden instanton",
            "gauge_invariance": "global branch only",
            "long_period": "PASS_KINEMATIC",
            "messenger_anomaly_inheritance": "conditional v1.22",
            "cosmology": "severe open gates",
            "decision": "CONDITIONAL_EFT_BEST_CONTINUITY",
        },
        {
            "branch": "standalone 31-holonomy Wilson clockwork",
            "gauge_invariance": "PASS_STANDALONE",
            "long_period": "PASS_EXACT",
            "messenger_anomaly_inheritance": "NOT_INHERITED",
            "cosmology": "severe open gates",
            "decision": "CONDITIONAL_NEW_MODEL",
        },
        {
            "branch": "two-field Wilson hybrid lock",
            "gauge_invariance": "FAIL_GAUGE_TOPOLOGY",
            "long_period": "PASS_KINEMATIC_ONLY",
            "messenger_anomaly_inheritance": "no",
            "cosmology": "not reached",
            "decision": "REJECT",
        },
    ]

    gates = [
        ("PARENT-01", "PASS", "v1.22 complete archive and internal ledger verified"),
        ("SOURCE-NORMALIZATION-01", "PASS_CORRECTION", "A_local is potential height; A_local/3^30 is projected force normalization"),
        ("GAUGED-NONLOCAL-CHARACTER-01", "FAIL_THEOREM", "compact invariant character is m(3^30,...,1) and has ultra-short period"),
        ("UNIFORM-PROPAGATION-01", "FAIL", "desired full-chain suppression violates two-edge shortcut budget"),
        ("GLOBAL-ENDPOINT-INSTANTON-01", "CONDITIONAL_PASS_EFT", "global scalar branch only; hidden dynamics, radial map, thermal history, and R-soft alignment open"),
        ("INSTANTON-NDA-01", "CONDITIONAL_PASS", "M=4pi Lambda gives S=10.7601 and passes dilute harmonic gate"),
        ("WILSON-PERIOD-01", "PASS_EXACT", "standalone 31-holonomy clockwork reproduces F_eff"),
        ("WILSON-GAUGE-01", "PASS_STANDALONE", "closed Wilson loops are gauge invariant"),
        ("WILSON-HARMONIC-01", "PASS_BENCHMARK", "x_E=4.25 keeps endpoint harmonics within the inherited continuity-design budget"),
        ("WILSON-HESSIAN-01", "PASS_BENCHMARK", "one light direction and positive heavy spectrum"),
        ("WILSON-HYBRID-LOCK-01", "FAIL_GAUGE_TOPOLOGY", "one cannot make both lock and source invariant with only the proposed phases"),
        ("WILSON-MESSENGER-PORT-01", "OPEN_NOT_INHERITED", "17+0 messenger, Sigma repair, and P/Y texture are absent from replacement"),
        ("WILSON-RADION-KINETIC-01", "OPEN", "radion, kinetic mixing, orbifold/parity anomalies, and SUSY breaking uncompleted"),
        ("TAU-MAP-01", "PASS_LEAST_COST_SITE0", "tau1=theta0/(2pi) is the unique least-cost map"),
        ("TAU-ENDPOINT-01", "PRACTICALLY_EXCLUDED_FIXED_BENCHMARK", "endpoint mapping costs 3^60; not a mathematical no-go if an enormous new driver/winding is allowed"),
        ("WE-ENERGY-16-01", "FAIL_BENCHMARK_WITHOUT_DRIVER_INJECTION", "one source-height budget supplies only 1/9.3546 of n=16 kinetic requirement"),
        ("WE-WINDING-01", "CONDITIONAL", "single-height energy budget requires n_det>=49 at unit exact-K_B efficiencies"),
        ("WE-BACKREACTION-01", "FAIL_AT_16", "kinetic energy is 54.9 percent of radiation"),
        ("AUTONOMOUS-DRIVE-01", "OPEN", "A(t), phase, reservoir, shutdown, and energy dump not derived"),
        ("SOURCE-MISALIGN-01", "FAIL_GENERIC_INITIAL_CONDITIONS_GLOBAL_BRANCH", "inherited/global constant source needs theta_i about 5e-5 or tracking/decay/dilution"),
        ("THERMAL-POTENTIAL-01", "FAIL_INCOMPLETE", "phase-only pins are undefined at field origin"),
        ("Y-WALL-01", "FAIL_IF_POSTINFLATION_FORMATION", "three degenerate vacua without compatible bias"),
        ("X-WALL-01", "FAIL_IF_DYNAMIC_AND_UNBIASED", "twelve degenerate vacua without compatible bias"),
        ("SIGMA-RELIC-01", "FAIL_IF_RELATIVISTIC_FULL_MULTIPLET_POPULATION", "illustrative degenerate stable-odd chiral population overproduced by about 1e7"),
        ("R-SOFT-ALIGNMENT-01", "OPEN", "source/instanton coefficient still needs aligned R=-2 breaking"),
        ("ANOMALY-NONLINEAR-GS-01", "OPEN", "nonlinear discrete, hidden mixed, and GS completion not closed"),
        ("BARYOGENESIS-01", "NO_CLAIM", "full CP invariant and coupled transport/energy evolution absent"),
        ("PUBLICATION-01", "HOLD", "conditional new models plus severe dynamical/cosmological gates remain"),
    ]
    gate_rows = [{"gate_id": gid, "status": status, "decision": decision} for gid, status, decision in gates]

    sources = [
        ("Extranatural Inflation", "https://arxiv.org/abs/hep-th/0301218", "closed Wilson loop, f=1/(2pi g4 R), one-loop harmonics, nonlocal protection"),
        ("(De)Constructing Dimensions", "https://arxiv.org/abs/hep-th/0104005", "deconstruction, link charges, lattice/continuum matching"),
        ("A Clockwork Theory", "https://arxiv.org/abs/1610.07962", "clockwork charge lattice and exponential zero-mode localization"),
        ("A Clockwork Axion", "https://arxiv.org/abs/1511.01827", "axion/phase clockwork realization"),
        ("General Continuum Clockwork", "https://arxiv.org/abs/1711.06228", "quantized clockwork charges and continuum limitations"),
        ("Pseudo-Goldstones from Supersymmetric Wilson Lines", "https://arxiv.org/abs/hep-ph/0503255", "orbifold/brane-to-brane Wilson-line realization and supersymmetric cancellation issues"),
        ("Deconstructing the Extra-Dimensional Axion", "https://arxiv.org/abs/2606.02728", "current deconstructed Wilson axion and fractional-instanton warning"),
        ("Axion Quality in Warped Extra Dimensions", "https://arxiv.org/abs/2604.08700", "current nonlocal charged propagation and axion-quality audit"),
        ("Modified instanton sums and higher groups", "https://arxiv.org/abs/1912.01033", "modified topological sectors imply extra discrete structure and vacua"),
        ("Weak Gravity Strongly Constrains Large-Field Axion Inflation", "https://arxiv.org/abs/1506.03447", "conjectural axion-WGC diagnostic only"),
        ("Standard Model sphaleron rate", "https://arxiv.org/abs/1404.3565", "electroweak crossover and sphaleron freeze-out temperature"),
        ("Baryogenesis from cosmological CP breaking", "https://arxiv.org/abs/2504.03506", "recent spontaneous/cosmological CP framework; not evidence for this model"),
        ("Axion domain walls with N_DW>1", "https://arxiv.org/abs/1207.3166", "long-lived domain-wall cosmology"),
        ("Planck 2018 cosmological parameters", "https://arxiv.org/abs/1807.06209", "dark-matter and annihilation constraints"),
        ("Planck 2018 inflation constraints", "https://arxiv.org/abs/1807.06211", "isocurvature constraint context"),
        ("Bounds on very low reheating", "https://arxiv.org/abs/1511.00672", "few-MeV reheating/BBN lower bound"),
        ("BBN constraints on long-lived particles", "https://arxiv.org/abs/1709.01211", "decay-before/during-BBN context"),
        ("Discrete symmetries in the MSSM", "https://arxiv.org/abs/1102.4611", "discrete-R anomaly and Green-Schwarz conventions"),
    ]
    source_reference_rows = [{"source": a, "url": b, "use": c} for a, b, c in sources]

    summary = {
        "version": VERSION,
        "title": TITLE,
        "parent_sha256_expected": EXPECTED_PARENT_SHA256,
        "q": Q,
        "N": N,
        "q_to_N": QN,
        "primitive_invariant_degree": primitive_degree,
        "desired_endpoint_period_GeV": F_EFF,
        "primitive_invariant_period_GeV": f_invariant_short,
        "period_ratio": period_ratio,
        "physical_source_height_GeV4": A_LOCAL,
        "projected_force_normalization_GeV4": DRIVE_PROJECTED,
        "remaining_parent_force_budget": PURITY_REMAINING,
        "instanton_dilute_tower_action_gate": instanton_action_gate,
        "uniform_physical_full_action": physical_height_action,
        "uniform_physical_per_edge_action": physical_per_edge_action,
        "uniform_physical_two_edge_coefficient": physical_two_edge_shortcut,
        "wilson_f_site_GeV": f_site,
        "wilson_x_endpoint": x_endpoint,
        "wilson_x_link": x_link,
        "wilson_R_inverse_GeV": r_inverse,
        "wilson_g4": g4,
        "wilson_endpoint_mass_GeV": m_endpoint,
        "wilson_link_mass_GeV": m_link,
        "wilson_force_harmonics": wilson_harmonic,
        "continuity_design_parent_plus_wilson_stress": combined_stress,
        "wilson_heavy_gap_GeV": math.sqrt(min_eigs[1]),
        "wilson_light_mass_eV": math.sqrt(small_min) * 1e9,
        "wilson_scalar_beta_loop_proxy": scalar_beta_loop,
        "wilson_adjacent_mixing_estimate": adjacent_mixing_estimate,
        "wilson_radion_mass_1pct_meV": radion_mass_1pct_meV,
        "wilson_radion_barrier_proxy_GeV": radion_barrier_scale,
        "wilson_WGC_sigma_min_diagonal_metric": z_sigma_min,
        "WE_u_required_exact_KB": u_req_exact,
        "WE_kinetic_over_radiation_n16": kinetic_fraction_exact,
        "WE_A_required_over_A": amplitude_ratio_exact,
        "WE_minimum_n_energy": math.ceil(n_energy_cont),
        "WE_minimum_n_1pct_backreaction": math.ceil(n_backreact_1pct_cont),
        "misalignment_Omega_h2_coefficient": omega_theta1,
        "misalignment_theta_max": theta_max,
        "misalignment_relaxed_curvature_height_GeV4": relaxed_curvature_height,
        "Y_wall_N": n_y,
        "X_wall_N": n_x,
        "Sigma_yield_max": y_max_sigma,
        "Sigma_full_chiral_relativistic_overproduction_diagnostic": overproduction,
        "best_continuity_branch": "global scalar moose plus endpoint hidden topological sector, conditional EFT",
        "best_gauge_invariant_new_model": "standalone 31-holonomy Wilson clockwork, conditional replacement",
        "recommended_next": "derive an autonomous site-0 source pulse and analytic thermal potential, then solve coupled phase-Friedmann-sphaleron-odd-relic Boltzmann dynamics; in parallel port messenger/anomaly structure to the Wilson replacement",
        "baryogenesis_claim": "NO_CLAIM",
        "publication_decision": "HOLD",
    }

    return {
        "summary": summary,
        "source_rows": source_rows,
        "character_rows": character_rows,
        "primitive_degree": primitive_degree,
        "f_invariant_short": f_invariant_short,
        "period_ratio": period_ratio,
        "instanton_rows": instanton_rows,
        "instanton_action_gate": instanton_action_gate,
        "harmonic_rows": harmonic_rows,
        "site_action_gap_rows": site_action_gap_rows,
        "uniform_rows": uniform_rows,
        "wilson_rows": wilson_rows,
        "wilson_hessian_rows": wilson_hessian_rows,
        "hybrid_rows": hybrid_rows,
        "x_harmonic_gate": x_harmonic_gate,
        "wilson_x_endpoint": x_endpoint,
        "wilson_harmonic": wilson_harmonic,
        "combined_stress": combined_stress,
        "remaining_after_wilson": remaining_after_wilson,
        "wedwsb_rows": wedwsb_rows,
        "wedwsb_energy_rows": wedwsb_energy_rows,
        "u_req_exact": u_req_exact,
        "u_max_local": u_max_local,
        "kinetic_fraction_exact": kinetic_fraction_exact,
        "n_energy_cont": n_energy_cont,
        "n_backreact_1pct_cont": n_backreact_1pct_cont,
        "misalignment_rows": misalignment_rows,
        "omega_theta1": omega_theta1,
        "theta_max": theta_max,
        "wall_rows": wall_rows,
        "wall_bias_rows": wall_bias_rows,
        "thermal_rows": thermal_rows,
        "sigma_rows": sigma_rows,
        "branches": branches,
        "gate_rows": gate_rows,
        "source_reference_rows": source_reference_rows,
    }


def make_plots(bundle: Path, calc: dict) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")

    xs = np.linspace(0.0, 10.0, 600)
    ys = np.array([wilson_force_envelope(float(x)) for x in xs])
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.semilogy(xs, ys, lw=2.2, label="massive Wilson force harmonics")
    ax.axhline(PURITY_REMAINING, color="#bf3f3f", ls="--", label="remaining v1.22 continuity budget")
    ax.axvline(calc["x_harmonic_gate"], color="#7d55b3", ls=":", label=f"gate x={calc['x_harmonic_gate']:.3f}")
    ax.scatter([calc["wilson_x_endpoint"]], [calc["wilson_harmonic"]], color="#1b7f5b", s=55, zorder=5, label="benchmark x=4.25")
    ax.set(xlabel=r"winding action $x=2\pi RM$", ylabel="relative higher-harmonic force", title="Standalone Wilson-line harmonic purity")
    ax.set_ylim(1e-8, 0.2)
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(bundle / "v1.23_wilson_harmonic_purity.png", dpi=180)
    plt.close(fig)

    labels = ["desired endpoint", "primitive invariant"]
    vals = [F_EFF, calc["f_invariant_short"]]
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    bars = ax.barh(labels, vals, color=["#2474b5", "#c65a42"])
    ax.set_xscale("log")
    ax.set_xlabel("phase period (GeV, logarithmic)")
    ax.set_title("Gauge-character theorem reverses the intended period")
    for bar, val in zip(bars, vals):
        ax.text(val * 1.12, bar.get_y() + bar.get_height() / 2, f"{val:.3e}", va="center")
    ax.set_xlim(1e-14, 1e19)
    fig.tight_layout()
    fig.savefig(bundle / "v1.23_source_period_obstruction.png", dpi=180)
    plt.close(fig)

    ns = np.arange(16, 161)
    fractions = calc["kinetic_fraction_exact"] * (N_DET_PARENT / ns) ** 2
    energy_ratio = (calc["n_energy_cont"] / ns) ** 2
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.semilogy(ns, fractions, label=r"$\rho_{kin}/\rho_{rad}$", lw=2.2)
    ax.semilogy(ns, energy_ratio, label=r"$\rho_{kin}/A_{available}$", lw=2.2)
    ax.axhline(1.0, color="#bf3f3f", ls="--", label="single-height source budget")
    ax.axhline(0.01, color="#7d55b3", ls=":", label="1% expansion backreaction")
    ax.axvline(math.ceil(calc["n_energy_cont"]), color="#1b7f5b", ls="--", alpha=0.8)
    ax.axvline(math.ceil(calc["n_backreact_1pct_cont"]), color="#7d55b3", ls="--", alpha=0.8)
    ax.set(xlabel=r"determinant winding $n_{det}$ (unit efficiencies)", ylabel="dimensionless burden", title="WE-DWSB conservative site-0 energy and expansion gates")
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(bundle / "v1.23_baryogenesis_energy_gate.png", dpi=180)
    plt.close(fig)

    theta = np.logspace(-7, 0, 500)
    omega = calc["omega_theta1"] * theta**2
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.loglog(theta, omega, lw=2.2, color="#c65a42")
    ax.axhline(OMEGA_DM_H2, color="#2474b5", ls="--", label=r"observed $\Omega_{DM}h^2\simeq0.12$")
    ax.axvline(calc["theta_max"], color="#1b7f5b", ls=":", label=f"theta limit {calc['theta_max']:.2e}")
    ax.set(xlabel="initial zero-mode misalignment |theta_i|", ylabel=r"estimated $\Omega_a h^2$", title="Constant-source misalignment obstruction")
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(bundle / "v1.23_misalignment_constraint.png", dpi=180)
    plt.close(fig)


def make_note(calc: dict, parent_meta: dict) -> str:
    s = calc["summary"]
    return rf"""# v1.23 Wilson-line, nonlocal-instanton, baryogenesis-energy, and cosmology audit

Date: 2026-08-17  
Status: **research scaffold / publication HOLD / no baryogenesis claim**

## Executive result

The v1.22 archive was independently replay-verified before this extension: archive SHA-256 `{parent_meta['archive_sha256']}`, {parent_meta['internal_hashes_checked'] - parent_meta['internal_hashes_failed']}/{parent_meta['internal_hashes_checked']} internal hashes passing.

This audit makes four substantive advances:

1. It proves an exact compact-character no-go for the original gauged scalar moose. A gauge-invariant electric character must be an integer multiple of 
   \( (3^{{30}},3^{{29}},\ldots,1) \). Its zero-mode period is only \({calc['f_invariant_short']:.6e}\) GeV, not the desired \({F_EFF:.6e}\) GeV. Nonlocality does not change charge quantization.
2. It constructs a concrete standalone 31-holonomy Wilson-line replacement. The benchmark has \(R^{{-1}}={s['wilson_R_inverse_GeV']:.3f}\) GeV and \(g_4={s['wilson_g4']:.3f}\). Imposing the inherited scalar stress proxy as a conservative **continuity design budget** gives a total \({100*s['continuity_design_parent_plus_wilson_stress']:.4f}\%<1\%\); that scalar stress has not yet been ported into the standalone model.
3. It fixes the source normalization. The physical cosine height is \(A=c_X\Lambda^4={A_LOCAL:.6e}\) GeV\(^4\), while \(A/3^{{30}}={DRIVE_PROJECTED:.6e}\) GeV\(^4\) is only the projected force normalization.
4. It exposes two severe dynamical/cosmological obstructions: without autonomous driver work, the parent \(n_{{det}}=16\) WE-DWSB benchmark needs \({s['WE_A_required_over_A']:.4f}\) times the conservative one-height source budget and carries \({100*s['WE_kinetic_over_radiation_n16']:.1f}\%\) of the radiation density; a constant endpoint source generically overcloses unless \(|\vartheta_i|\lesssim{s['misalignment_theta_max']:.2e}\).

The strongest continuity-preserving branch is now the **global** scalar moose plus a site-30 hidden topological sector, still conditional. The strongest gauge-invariant replacement is the standalone Wilson clockwork, also conditional. Neither is a completed theory of why matter dominates antimatter.

## 1. Exact gauged-character theorem

For the 30-by-31 incidence matrix

\[
L_{{aj}}=\delta_{{aj}}-3\delta_{{a+1,j}},
\]

a compact phase character \(\exp(i\sum_j k_j\theta_j)\), \(k_j\in\mathbb Z\), is invariant only if

\[
k_j-3k_{{j+1}}=0.
\]

Therefore

\[
\boldsymbol k=m(3^{{30}},3^{{29}},\ldots,1),\qquad
\sum_j k_j={calc['primitive_degree']}
\]

where the full primitive degree is `{calc['primitive_degree']:,}`. This conclusion applies after every charged insertion of a local polynomial, open-line dressing, or instanton zero mode is included. A new boundary/Green-Schwarz field can change the lattice, but it then adds a physical phase and must be re-audited.

Along the inherited zero mode \(\theta_j=3^{{-j}}\alpha/F_\alpha\), the endpoint character has

\[
F_{{end}}=3^{{30}}F_\alpha={F_EFF:.12e}\;\mathrm{{GeV}},
\]

but the primitive invariant has

\[
F_{{inv}}=\frac{{F_\alpha}}{{3^{{30}}\sum_j3^{{-2j}}}}
={calc['f_invariant_short']:.12e}\;\mathrm{{GeV}}.
\]

The period mismatch is {calc['period_ratio']:.6e}. Thus a nonlocal electric source does not repair the original compact gauged scalar branch.

## 2. Instanton and propagation audit

For \(A=M^4e^{{-S_I}}\) with unit determinant prefactor, a cutoff-scale \(M=\Lambda\) gives \(S_I=0.636006\) for the required physical height: not a dilute instanton. An NDA-scale \(M=4\pi\Lambda\) gives \(S_I=10.760103\). A dilute tower with \(A_n/A_1=e^{{-(n-1)S_I}}\) fits the remaining force budget only for

\[
S_I>{calc['instanton_action_gate']:.9f}.
\]

The NDA benchmark passes this harmonic test but remains conditional on the determinant, running, radial independence, thermal susceptibility, hidden mixed anomaly, Green-Schwarz sector, and aligned \(R=-2\) supersymmetry breaking.

A single uniform propagator also fails. With the corrected physical height \(A_{{local}}\), its total action would be only \(0.636006\), or \(M_{{gap}}a=0.0212002\) per edge. The resulting two-edge coefficient is 0.958486, about 253 times the remaining budget. Even the weaker comparison to the projected \(D\) gives 0.10650, about 28 times the budget. Conversely, enforcing the inherited locality gap undershoots \(A_{{local}}\) by about \(1.09\times10^{{36}}\). A truly topological winding sector would need every proper subpath to be exactly forbidden.

## 3. Standalone Wilson-line replacement

Take 31 compact 5D \(U(1)_j\) holonomies

\[
\theta_j=\oint A_{{5,j}}dy,
\qquad f_{{site}}=\frac1{{2\pi Rg_4}},
\]

with link particles of charges \(e_j-3e_{{j+1}}\) and an endpoint particle of charge \(e_{{30}}\). Winding loops generate closed, gauge-invariant potentials

\[
V_L=\sum_{{j,n}}A_{{L,n}}[1-\cos n(\theta_j-3\theta_{{j+1}})],
\quad
V_E=\sum_n A_{{E,n}}[1-\cos n\theta_{{30}}].
\]

For \(d\) real bosonic degrees of freedom,

\[
A_n=d\frac{{3}}{{64\pi^6R^4}}
\frac{{e^{{-nx}}}}{{n^5}}\left(1+nx+\frac{{n^2x^2}}3\right),
\quad x=2\pi RM.
\]

The benchmark uses \(d_E=8,x_E=4.25\), and \(d_L=4,x_L={s['wilson_x_link']:.12f}\) per link. It gives:

- \(f_{{site}}={s['wilson_f_site_GeV']:.6f}\) GeV;
- \(R^{{-1}}={s['wilson_R_inverse_GeV']:.6f}\) GeV and \(g_4={s['wilson_g4']:.6f}\);
- \(M_L={s['wilson_link_mass_GeV']:.6f}\) GeV and \(M_E={s['wilson_endpoint_mass_GeV']:.6f}\) GeV;
- endpoint force harmonics {s['wilson_force_harmonics']:.9f};
- source-minimum light mass {s['wilson_light_mass_eV']:.9f} eV and heavy gap {s['wilson_heavy_gap_GeV']:.6f} GeV.

Here \(d_L=4\) denotes two charged complex scalars and \(d_E=8\) four, or explicitly supersymmetry-broken packets with the same net determinant. A degenerate exact-SUSY spectrum cancels the loop potential. The standalone period follows exactly from

\[
\ker Q_L=(3^{{30}},\ldots,1),\quad \theta_j=3^{{30-j}}t,\quad t\sim t+2\pi,
\]

\[
F_W^2=f_{{site}}^2\sum_{{k=0}}^{{30}}9^k=F_{{eff}}^2,
\qquad \cos\theta_{{30}}=\cos t=\cos(a/F_{{eff}}).
\]

The conservative \(C_{{eff}}=11\) NDA proxy gives a 13.3 TeV cutoff, only about 7.5 KK spacings: moderate rather than parametric separation. The exact scalar beta proxy is 0.0666 and adjacent kinetic mixing is estimated near 0.0492, so the full kinetic matrix is a required next replay. A canonical-radion 1% displacement estimate needs \(m_\rho\gtrsim{s['wilson_radion_mass_1pct_meV']:.3f}\) meV and a barrier proxy near {s['wilson_radion_barrier_proxy_GeV']:.1f} GeV.

Limited conjectural gravity checks pass in the diagonal kinetic convention: the charge basis is unimodular, \(\sigma_{{min}}(Z)={s['wilson_WGC_sigma_min_diagonal_metric']:.2f}\), and \(S_EF_{{eff}}/M_{{Pl}}=0.08984\). This does not establish the magnetic, lattice, or sublattice WGC or survive an uncomputed kinetic-mixed metric automatically.

This closes the period and gauge-invariance questions only for the standalone replacement. It leaves open the port of the 17 intended messenger vertices, \(R(\Sigma)=17\) anomaly repair, \(P/Y\) texture, a parity/orbifold treatment of 4D vector zero modes, kinetic mixing, radion stabilization, supersymmetry breaking, and the autonomous drive.

The simpler two-field lock \(-B\cos(w-\theta_{{30}})-A\cos w\) fails exactly: if \(w\) is invariant the lock is not, while if \(w\) shifts the source is not. A new dynamical endpoint phase changes the charge lattice. Removing the extra mode with an independent lock requires a Smith-normal-form index containing \(3^{{30}}\): another order-one-charge chain or an explicit \(3^{{30}}\) charge/monodromy. A disorder loophole similarly needs a \(3^{{30}}\)-order quotient or one-form topological sector and a full attached-surface/branch audit. These are replacement UV models, not repairs by fixed charged spurions.

## 4. Matter-over-antimatter scaffold: mapping and energy

The inherited phenomenological relation is

\[
Y_B=c_{{sph}}\kappa_{{dyn}}(2\pi n_{{det}}\dot\tau_1/T)D_d.
\]

Because \(\theta_j=3^{{-j}}\theta_0\), the unique least-cost and fixed-benchmark-compatible identification is

\[
\tau_1=\frac{{\theta_0}}{{2\pi}},
\]

with the derivative \(B+L\) operator localized at site 0. The endpoint identification costs \(3^{{60}}\) in kinetic energy and is practically excluded in the fixed benchmark; it is not a mathematical theorem if an enormous new winding or autonomous driver is allowed.

For exact \(K_B=1.020689\), \(c_{{sph}}=0.0195\), \(n_{{det}}=16\), \(T_*=131.7\) GeV, and unit efficiency,

\[
\frac{{\dot\tau_1}}T={calc['u_req_exact']:.6f},\qquad
\frac{{\rho_{{kin}}}}{{\rho_{{rad}}}}={calc['kinetic_fraction_exact']:.6f}.
\]

Under a conservative single-source-height budget with no work injected by a moving driver, \(u_{{max}}={calc['u_max_local']:.6f}\). That accounting needs \(n_{{det}}\ge49\) at unit efficiencies, while a 1% expansion-backreaction target needs \(n_{{det}}\ge119\). A dynamical driver can do additional work, but then its reservoir and decay products must be evolved explicitly. The larger windings have no operator/R/locality derivation yet. A complete calculation must evolve the driver, phase, Friedmann equation, sphaleron rate, washout, spectators, and energy disposal together. It must also exhibit a physical CP-odd invariant rather than imposing the sign of motion.

## 5. Cosmology gates

### Constant-source misalignment

For the inherited/global scalar branch, if the endpoint cosine stays on, \(3H=m_a\) occurs near 332 GeV. Using the relaxed curvature \(m_a^2F_{{eff}}^2=5.695\times10^8\) GeV\(^4\), equal to \(0.9184A_{{local}}\), standard harmonic misalignment gives

\[
\Omega_a h^2\simeq {calc['omega_theta1']:.4e}\,\vartheta_i^2,
\]

so \(|\vartheta_i|\lesssim{calc['theta_max']:.3e}\). Tracking of the moving minimum, a transient pulse, decay/transfer, or later dilution is mandatory for generic initial conditions.

### Discrete walls and thermal completion

The written \(Y\) pin has three vacua and the diagnostic dynamical \(X\) pin has twelve. Separate pins have 36 minima arranged into three exact 12-vacuum \(Z_{{24}}^R\) orbits unless cross-couplings lift the accidental three-orbit degeneracy. Rigid-radius sine-Gordon/scaling estimates place unbiased domination near 0.32 keV and 0.84 keV, but a radial wall can lower its tension by passing through the origin. The \(\Delta V\sim\sigma H\) numbers are pressure-balance references with order-one network uncertainty, not guaranteed minima. Any bias also challenges the same discrete \(R\) symmetry used for operator selection and requires a full leakage/anomaly replay.

The phase-only pins are undefined at \(Y=0\) or \(X=0\); they are local zero-temperature coordinates, not finite-temperature potentials. Consequently restoration temperatures and post-reheating wall formation are presently incalculable.

### Stable odd relic

An exact \(Z_2^H\) makes the lightest odd state stable. If it is the 0.654 GeV \(\Sigma\), its yield must be below \(6.69\times10^{{-10}}\). An illustrative degenerate full chiral multiplet populated relativistically in the same bath gives a yield near \(9\times10^{{-3}}\), overproducing dark matter by about \(10^7\). A cold or sequestered hidden bath can evade that specific estimate. The broken-phase \(\Gamma/H\) diagnostic also assumes the zero-temperature \(Y\) VEV persists, which the missing thermal potential does not establish. The odd mass ordering, portal, annihilation channels, freeze-out/freeze-in, and possible decay or entropy dilution must be supplied.

## 6. Decision and next falsifier

This version advances the hypothesis by replacing a vague nonlocal-source hope with an exact no-go, a numerically closed conditional Wilson replacement, and quantitative baryogenesis/cosmology gates. It still supports **no claim that the observed matter excess has been derived**.

The recommended v1.24 task is:

1. build an analytic finite-temperature radial-plus-phase potential;
2. derive an autonomous site-0 source pulse, its energy reservoir, shutdown, and CP-odd invariant;
3. solve the coupled phase–Friedmann–sphaleron–spectator–odd-relic Boltzmann system;
4. in parallel, test whether the 17+0 messenger/anomaly structure can be ported to the standalone Wilson replacement without reintroducing shortcuts.

Publication remains **HOLD**.

## Primary technical anchors

- [Extranatural Inflation](https://arxiv.org/abs/hep-th/0301218)
- [(De)Constructing Dimensions](https://arxiv.org/abs/hep-th/0104005)
- [A Clockwork Theory](https://arxiv.org/abs/1610.07962)
- [A Clockwork Axion](https://arxiv.org/abs/1511.01827)
- [General Continuum Clockwork](https://arxiv.org/abs/1711.06228)
- [Pseudo-Goldstones from Supersymmetric Wilson Lines](https://arxiv.org/abs/hep-ph/0503255)
- [Deconstructing the Extra-Dimensional Axion](https://arxiv.org/abs/2606.02728)
- [Axion Quality in Warped Extra Dimensions](https://arxiv.org/abs/2604.08700)
- [Modified instanton sums and higher groups](https://arxiv.org/abs/1912.01033)
- [Standard Model sphaleron rate](https://arxiv.org/abs/1404.3565)
- [Baryogenesis from cosmological CP breaking](https://arxiv.org/abs/2504.03506)
- [Long-lived domain walls](https://arxiv.org/abs/1207.3166)
- [Planck cosmological parameters](https://arxiv.org/abs/1807.06209)
- [Planck inflation/isocurvature constraints](https://arxiv.org/abs/1807.06211)
- [Very low reheating bounds](https://arxiv.org/abs/1511.00672)
- [Long-lived-particle BBN constraints](https://arxiv.org/abs/1709.01211)
- [Discrete-symmetry anomaly conventions](https://arxiv.org/abs/1102.4611)

All values are audit benchmarks under stated assumptions, not observations of new physics.
"""


def make_one_page(calc: dict, parent_meta: dict) -> str:
    s = calc["summary"]
    return rf"""# AM v1.23 — one-page decision sheet

**Parent:** AM122_COMPLETE SHA `{parent_meta['archive_sha256']}` — verified.  
**Scientific status:** hypothesis scaffold; **NO baryogenesis claim; PUBLICATION HOLD**.

## What changed

- **Exact no-go:** in the original compact gauged scalar moose, every gauge-invariant electric character is a multiple of \((3^{{30}},\ldots,1)\). It has period `{calc['f_invariant_short']:.3e} GeV`, not `{F_EFF:.3e} GeV`. Calling an operator “nonlocal” does not evade this.
- **Conditional replacement:** a standalone 31-holonomy Wilson clockwork matches the long period and source height with `R^-1={s['wilson_R_inverse_GeV']:.1f} GeV` and `g4={s['wilson_g4']:.3f}`. Its own endpoint harmonics are `{100*s['wilson_force_harmonics']:.3f}%`; adding the unported parent stress as a conservative continuity target gives `{100*s['continuity_design_parent_plus_wilson_stress']:.3f}%`. It does **not** inherit the scalar 17+0 messenger/anomaly construction.
- **Normalization fixed:** the physical potential height is `{A_LOCAL:.6e} GeV^4`; `{DRIVE_PROJECTED:.6e} GeV^4` is only its projected long-period force normalization.
- **Baryogenesis energy gate:** site 0 is the unique least-cost map. Without work from an autonomous driver, the old `n_det=16` benchmark needs `{s['WE_A_required_over_A']:.3f}x` the one-height energy budget and carries `{100*s['WE_kinetic_over_radiation_n16']:.1f}%` of radiation. That budget gives `n_det>=49`; a 1% expansion target gives `>=119`, both awaiting operator justification.
- **Cosmology gate:** in the inherited/global branch, a persistent source gives `Omega h2 ~= {s['misalignment_Omega_h2_coefficient']:.3e} theta_i^2`, requiring `|theta_i| < {s['misalignment_theta_max']:.2e}` or tracking/shutdown/decay/dilution. Thermal Y/X walls and the stable-odd relic history are unresolved.

## Best surviving paths

1. **Continuity branch:** global scalar moose + site-30 hidden topological sector — conditional EFT only.
2. **Gauge-invariant new model:** standalone Wilson clockwork — conditional replacement, requiring messenger/anomaly/thermal/drive port.

## Next recommended calculation

Derive an analytic finite-temperature potential and autonomous site-0 source pulse, then solve the phase–Friedmann–sphaleron–spectator–odd-relic Boltzmann system. In parallel, attempt the 17+0 messenger/anomaly port to the Wilson replacement.
"""


def make_readme() -> str:
    return """# AM123 release bundle

This bundle is a deterministic v1.23 extension of the verified AM122 parent.

Start with:

1. `v1.23_ONE_PAGE.md` — concise outcome and next step.
2. `v1.23_wilson_instanton_cosmology_audit_note.md` — full derivation and caveats.
3. `v1.23_gates.csv` and `v1.23_branch_decision.csv` — machine-readable decisions.
4. The four PNG figures — the main obstructions and conditional benchmark.

Reproduce with:

```bash
python3 v1.23_wilson_instanton_cosmology_audit.py --parent-zip AM122_COMPLETE.zip --output-root replay
```

The script writes deterministic text, tables, plots, ZIP archives, manifests, and SHA-256 ledgers. The scientific result is a research scaffold, not an established physical theory. Publication remains HOLD.
"""


def build_bundle(bundle: Path, calc: dict, parent_rows: list[dict], parent_meta: dict, script_path: Path) -> None:
    bundle.mkdir(parents=True, exist_ok=False)
    write_csv(bundle / "v1.23_parent_verification.csv", parent_rows)
    write_csv(bundle / "v1.23_source_normalization.csv", calc["source_rows"])
    write_csv(bundle / "v1.23_gauge_kernel.csv", calc["character_rows"])
    write_csv(bundle / "v1.23_instanton_action_scan.csv", calc["instanton_rows"])
    write_csv(bundle / "v1.23_harmonic_action_gates.csv", calc["harmonic_rows"])
    write_csv(bundle / "v1.23_unwanted_site_action_gaps.csv", calc["site_action_gap_rows"])
    write_csv(bundle / "v1.23_uniform_propagator_audit.csv", calc["uniform_rows"])
    write_csv(bundle / "v1.23_wilson_benchmark.csv", calc["wilson_rows"])
    write_csv(bundle / "v1.23_wilson_hessian.csv", calc["wilson_hessian_rows"])
    write_csv(bundle / "v1.23_wilson_hybrid_lock.csv", calc["hybrid_rows"])
    write_csv(bundle / "v1.23_WE_DWSB_site_map.csv", calc["wedwsb_rows"])
    write_csv(bundle / "v1.23_WE_DWSB_energy.csv", calc["wedwsb_energy_rows"])
    write_csv(bundle / "v1.23_misalignment.csv", calc["misalignment_rows"])
    write_csv(bundle / "v1.23_domain_walls.csv", calc["wall_rows"])
    write_csv(bundle / "v1.23_wall_bias.csv", calc["wall_bias_rows"])
    write_csv(bundle / "v1.23_thermal_potential.csv", calc["thermal_rows"])
    write_csv(bundle / "v1.23_sigma_relic.csv", calc["sigma_rows"])
    write_csv(bundle / "v1.23_branch_decision.csv", calc["branches"])
    write_csv(bundle / "v1.23_gates.csv", calc["gate_rows"])
    write_csv(bundle / "v1.23_primary_sources.csv", calc["source_reference_rows"])

    write_text(bundle / "v1.23_README.md", make_readme())
    write_text(bundle / "v1.23_ONE_PAGE.md", make_one_page(calc, parent_meta))
    write_text(bundle / "v1.23_wilson_instanton_cosmology_audit_note.md", make_note(calc, parent_meta))
    write_text(bundle / "v1.23_summary.json", json.dumps(calc["summary"], indent=2, sort_keys=True))
    summary_rows = [{"quantity": key, "value": fmt(value)} for key, value in calc["summary"].items()]
    write_csv(bundle / "v1.23_summary.csv", summary_rows)
    shutil.copy2(script_path, bundle / script_path.name)
    make_plots(bundle, calc)

    primary_files = sorted(p for p in bundle.iterdir() if p.is_file())
    manifest_rows = [
        {"filename": p.name, "bytes": p.stat().st_size, "sha256": sha256_file(p)} for p in primary_files
    ]
    write_csv(bundle / "v1.23_bundle_manifest.csv", manifest_rows)
    ledger_files = sorted(p for p in bundle.iterdir() if p.is_file() and p.name != "v1.23_SHA256.txt")
    ledger = "\n".join(f"{sha256_file(p)}  {p.name}" for p in ledger_files)
    write_text(bundle / "v1.23_SHA256.txt", ledger)


def deterministic_zip(zip_path: Path, files: list[Path], base: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(files, key=lambda p: p.relative_to(base).as_posix()):
            arcname = path.relative_to(base).as_posix()
            info = zipfile.ZipInfo(arcname, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build_release(output_root: Path, parent_zip: Path, script_path: Path) -> None:
    if output_root.exists():
        if any(output_root.iterdir()):
            raise SystemExit(f"Refusing to overwrite non-empty output root: {output_root}")
    else:
        output_root.mkdir(parents=True)

    parent_rows, parent_meta = verify_parent(parent_zip)
    if not parent_meta["all_pass"]:
        raise SystemExit("Parent verification failed; v1.23 generation stopped")
    calc = build_calculations()
    calc["summary"]["parent_sha256_observed"] = parent_meta["archive_sha256"]
    calc["summary"]["parent_internal_hashes_passed"] = parent_meta["internal_hashes_checked"] - parent_meta["internal_hashes_failed"]
    calc["summary"]["parent_internal_hashes_total"] = parent_meta["internal_hashes_checked"]

    bundle = output_root / "AM123_COMPLETE"
    build_bundle(bundle, calc, parent_rows, parent_meta, script_path)

    complete_zip = output_root / "AM123_COMPLETE.zip"
    deterministic_zip(complete_zip, [p for p in bundle.iterdir() if p.is_file()], bundle)

    phone_names = [
        "v1.23_README.md",
        "v1.23_ONE_PAGE.md",
        "v1.23_wilson_instanton_cosmology_audit_note.md",
        "v1.23_summary.csv",
        "v1.23_gates.csv",
        "v1.23_branch_decision.csv",
        "v1.23_wilson_benchmark.csv",
        "v1.23_WE_DWSB_energy.csv",
        "v1.23_misalignment.csv",
        "v1.23_domain_walls.csv",
        "v1.23_sigma_relic.csv",
        "v1.23_wilson_harmonic_purity.png",
        "v1.23_source_period_obstruction.png",
        "v1.23_baryogenesis_energy_gate.png",
        "v1.23_misalignment_constraint.png",
        "v1.23_SHA256.txt",
    ]
    phone_zip = output_root / "AM123_PHONE.zip"
    deterministic_zip(phone_zip, [bundle / name for name in phone_names], bundle)

    all_in_one_parts = []
    for path in sorted(bundle.iterdir()):
        if path.suffix.lower() in {".md", ".csv", ".json", ".txt", ".py"}:
            all_in_one_parts.append(f"===== BEGIN {path.name} =====\n")
            all_in_one_parts.append(path.read_text(encoding="utf-8"))
            all_in_one_parts.append(f"===== END {path.name} =====\n\n")
    all_in_one = output_root / "AM123_ALL_IN_ONE.txt"
    write_text(all_in_one, "".join(all_in_one_parts))

    note_copy = output_root / "v1.23_wilson_instanton_cosmology_audit_note.md"
    shutil.copy2(bundle / note_copy.name, note_copy)
    one_page_copy = output_root / "v1.23_ONE_PAGE.md"
    shutil.copy2(bundle / one_page_copy.name, one_page_copy)

    checksums = output_root / "AM123_CHECKSUMS.txt"
    external = [complete_zip, phone_zip, all_in_one, note_copy, one_page_copy]
    write_text(checksums, "\n".join(f"{sha256_file(p)}  {p.name}" for p in external))

    result = {
        "output_root": str(output_root.resolve()),
        "parent_verified": parent_meta,
        "release_files": [
            {"filename": p.name, "bytes": p.stat().st_size, "sha256": sha256_file(p)}
            for p in [complete_zip, phone_zip, all_in_one, checksums, note_copy, one_page_copy]
        ],
        "bundle_member_count": len([p for p in bundle.iterdir() if p.is_file()]),
        "decision": "PUBLICATION HOLD / NO BARYOGENESIS CLAIM",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-zip", type=Path, required=True, help="Path to verified AM122_COMPLETE.zip")
    parser.add_argument("--output-root", type=Path, required=True, help="New, empty output directory")
    args = parser.parse_args()
    script_path = Path(__file__).resolve()
    build_release(args.output_root.resolve(), args.parent_zip.resolve(), script_path)


if __name__ == "__main__":
    main()
