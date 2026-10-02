#!/usr/bin/env python3
"""Exact ideal-SM checks for this newly authored inventory; no physics yield."""
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
names = ['q_L', 'u_R', 'd_R', 'l_L', 'e_R', 'H']
B = [F(1, 3)] * 3 + [F(0)] * 3
L = [F(0)] * 3 + [F(1), F(1), F(0)]
Y = [F(1, 6), F(2, 3), F(-1, 3), F(-1, 2), F(-1), F(1, 2)]
plus = [b + l for b, l in zip(B, L)]
minus = [b - l for b, l in zip(B, L)]
C = [F(3), F(3, 2), F(3, 2), F(1), F(1, 2), F(2, 3)]


def dot(a, b):
    return sum(c * ai * bi for c, ai, bi in zip(C, a, b))


def projected_density(d):
    a, b, e = dot(minus, minus), dot(minus, Y), dot(Y, Y)
    r, s = dot(minus, d), dot(Y, d)
    det = a * e - b * b
    if det <= 0:
        raise ValueError('Conserved-charge Gram matrix must be positive definite')
    alpha_m, alpha_y = -(e * r - b * s) / det, -(-b * r + a * s) / det
    mu = [di + alpha_m * mi + alpha_y * yi for di, mi, yi in zip(d, minus, Y)]
    return [c * v for c, v in zip(C, mu)], mu, alpha_m, alpha_y


n, mu, alpha_m, alpha_y = projected_density(plus)
checks = {
    'constraint_B_minus_L': sum(q * ni for q, ni in zip(minus, n)) == 0,
    'constraint_hypercharge': sum(q * ni for q, ni in zip(Y, n)) == 0,
    'density_B': sum(q * ni for q, ni in zip(B, n)) == F(72, 79),
    'density_B_plus_L': sum(q * ni for q, ni in zip(plus, n)) == F(144, 79),
    'alpha_B_minus_L': alpha_m == F(23, 79),
    'alpha_hypercharge': alpha_y == F(12, 79),
    'conserved_B_minus_L_zero': projected_density(minus)[0] == [F(0)] * 6,
    'conserved_hypercharge_zero': projected_density(Y)[0] == [F(0)] * 6,
}
shifted = [d + F(7, 3) * q - F(11, 5) * y for d, q, y in zip(plus, minus, Y)]
checks['adding_conserved_bias_changes_no_density'] = projected_density(shifted)[0] == n

# Three-generation anomaly traces, in left-handed conjugate convention.
# Density species H is excluded. Chirality signs turn physical RH particles
# into LH conjugates, whose global and hypercharges have opposite signs.
chirality = [1, -1, -1, 1, -1]
g = [18, 9, 9, 6, 3]


def trace_y2(q):
    return sum(si * gi * qi * yi**2 for si, gi, qi, yi in zip(chirality, g, q, Y))


def trace_su2(q):
    return F(1, 2) * (9 * q[0] + 3 * q[3])


def trace_grav(q):
    return sum(si * gi * qi for si, gi, qi in zip(chirality, g, q))


anomaly = {
    'B_plus_L_SU2_trace': trace_su2(plus),
    'B_plus_L_Y2_trace': trace_y2(plus),
    'B_minus_L_SU2_trace': trace_su2(minus),
    'B_minus_L_Y2_trace': trace_y2(minus),
    'B_minus_L_gravitational_trace_no_RH_neutrinos': trace_grav(minus),
}
checks.update({
    'B_plus_L_SU2_coefficient_6': 2 * anomaly['B_plus_L_SU2_trace'] == 6,
    'B_plus_L_Y2_coefficient_minus_6': 2 * anomaly['B_plus_L_Y2_trace'] == -6,
    'B_minus_L_mixed_gauge_traces_zero': anomaly['B_minus_L_SU2_trace'] == anomaly['B_minus_L_Y2_trace'] == 0,
    'B_minus_L_gravitational_trace_minus_3': anomaly['B_minus_L_gravitational_trace_no_RH_neutrinos'] == -3,
})
if not all(checks.values()):
    raise ValueError('Exact inventory identity failed: ' + str(checks))
c_ideal = float(F(72, 79)) * 45 / (2 * math.pi**2 * 106.75)
result = {
    'scope': 'Ideal relativistic one-Higgs Standard Model charge/anomaly arithmetic; no baryon-yield prediction',
    'species_order': names,
    'susceptibility_over_T2': [str(x) for x in C],
    'mu_over_mu_plus': [str(x) for x in mu],
    'density_over_mu_plus_T2': [str(x) for x in n],
    'anomaly_traces': {k: str(v) for k, v in anomaly.items()},
    'c_ideal_at_gstar_106_75': c_ideal,
    'legacy_c_sph': 0.0195,
    'legacy_relative_difference': 0.0195 / c_ideal - 1,
    'exact_checks': checks,
    'all_passed': all(checks.values()),
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(ROOT / 'EXACT_INVENTORY_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'all_passed': result['all_passed'], 'exact_check_count': len(checks), 'c_ideal': c_ideal}))
