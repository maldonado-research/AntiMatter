#!/usr/bin/env python3
"""Bounded generalized Wilson-metric audit; see immutable REGISTRATION.md.

Public inputs are read only. Output defaults to this script's directory; an
explicit --output-dir supports a fresh, non-overwriting reproduction directory.
No release generator imports, private input files, matched loops or WGC claims.
"""
from __future__ import annotations

import argparse
import ast
import csv
from decimal import Decimal as D, localcontext
import hashlib
import json
import math
from pathlib import Path
import platform
import sys

import numpy as np
import scipy
from scipy.linalg import eigh, solve_triangular

HERE = Path(__file__).resolve().parent
SOURCE = Path('/workspace/AntiMatter/research/AM1231/v1.23')
SOURCE_NAMES = [
    'v1.23_wilson_instanton_cosmology_audit.py',
    'v1.23_wilson_instanton_cosmology_audit_note.md',
    'v1.23_wilson_benchmark.csv', 'v1.23_wilson_hessian.csv',
    'v1.23_summary.json',
]
PRECISIONS = (60, 90, 110)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def curvature(x, top=False):
    # Exact formula and stopping rule of public generator lines 204-213.
    p1 = 1.0 + x + x*x / 3.0
    total = 0.0
    for n in range(1, 10001):
        sign = (-1.0)**n if top else 1.0
        term = sign * math.exp(-(n-1)*x) * (1.0+n*x+(n*x)**2/3.0) / (n**3*p1)
        total += term
        if n > 5 and abs(term) < 1e-18:
            break
    return total


def inputs(source):
    # Parse selected public literal constants, without executing its generator.
    tree = ast.parse((source / SOURCE_NAMES[0]).read_text())
    wanted = {'Q', 'N', 'LAMBDA', 'C_X', 'F_ALPHA'}
    literals = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            name = getattr(node.targets[0], 'id', None)
            if name in wanted:
                literals[name] = ast.literal_eval(node.value)
    assert literals['Q'] == 3 and literals['N'] == 30
    summary = json.loads((source / 'v1.23_summary.json').read_text())
    f = summary['wilson_f_site_GeV']
    amplitude = literals['C_X'] * literals['LAMBDA']**4
    k_link = amplitude * curvature(summary['wilson_x_link']) / f**2
    k_min = amplitude * curvature(summary['wilson_x_endpoint']) / f**2
    k_top = amplitude * curvature(summary['wilson_x_endpoint'], True) / f**2
    eps = D(str(summary['wilson_adjacent_mixing_estimate']))
    with localcontext() as ctx:
        ctx.prec = 110
        return {
            'n': 31, 'q': 3, 'f_site_GeV': D(str(f)),
            'epsilon_published': eps, 'c_nominal': eps / 3,
            'k_link_GeV2': D(str(k_link)),
            'k_min_GeV2': D(str(k_min)), 'k_top_GeV2': D(str(k_top)),
            'literal_constants': literals,
            'source_files_sha256': {name: digest(source/name) for name in SOURCE_NAMES},
        }


def families(inp):
    c0 = inp['c_nominal']
    rows = [{'case': 'baseline', 'family': 'structural', 'c': D(0), 'b': D(0), 'epsilon': D(0)}]
    with localcontext() as ctx:
        ctx.prec = 110
        for mult in (1, 3, 10):
            for bmult in (0, 1, 3):
                c = c0*mult
                rows.append({'case': f'structural_c{mult}_b{bmult}c', 'family': 'structural',
                             'c': c, 'b': c*bmult, 'epsilon': D(0)})
        for sign, name in ((1, 'positive'), (-1, 'negative')):
            rows.append({'case': f'adjacent_{name}', 'family': 'adjacent_sensitivity',
                         'c': D(0), 'b': D(0), 'epsilon': inp['epsilon_published']*sign})
    return rows


def pencil(inp, case, endpoint):
    kl = inp['k_link_GeV2']
    hd = [kl] + [10*kl]*29 + [9*kl+endpoint]
    ho = [-3*kl]*30
    if case['family'] == 'structural':
        c, b = case['c'], case['b']
        gd = [1+c] + [1+10*c]*29 + [1+9*c+b]
        go = [-3*c]*30
    else:
        gd, go = [D(1)]*31, [case['epsilon']]*30
    return hd, ho, gd, go


def inertia_at(lam, pencil_data, precision):
    """Negative inertia of H-lambda G from tridiagonal LDL^T.

    For SPD G this equals the number of generalized roots below lambda.
    An exact zero pivot uses a negative infinitesimal (one-sided Sturm limit).
    None of the decisive registered root brackets hits such a pivot.
    """
    hd, ho, gd, go = pencil_data
    tiny = D(10) ** (-2*precision)
    pivot = hd[0]-lam*gd[0]
    if not pivot:
        pivot = -tiny
    count = int(pivot < 0)
    for j in range(1, len(hd)):
        off = ho[j-1]-lam*go[j-1]
        pivot = hd[j]-lam*gd[j] - off*off/pivot
        if not pivot:
            pivot = -tiny
        count += int(pivot < 0)
    return count


def small_root(inp, case, endpoint, precision):
    with localcontext() as ctx:
        ctx.prec = precision
        data = pencil(inp, case, endpoint)
        low, high = (D(0), D('1e-23')) if endpoint > 0 else (D('-1e-23'), D(0))
        assert inertia_at(low, data, precision) == 0
        assert inertia_at(high, data, precision) == 1
        for _ in range(4*precision):
            middle = (low+high)/2
            if middle == low or middle == high:
                break
            if inertia_at(middle, data, precision) == 0:
                low = middle
            else:
                high = middle
        return (low+high)/2


def float_matrix(diag, off):
    return np.diag(np.array(diag, dtype=float)) + np.diag(np.array(off, dtype=float), 1) + np.diag(np.array(off, dtype=float), -1)


def trace_inverse_approx(inp, case, endpoint):
    """1/tr(H^-1 G) from exact charge-triangular factorization.

    H=B^T diag(kL,...,kL,kE) B, (B^-1)_ij=3^(j-i), j>=i.
    Valid only with nonzero endpoint. Heavy inverse roots produce a relative
    O(|lambda_light| sum 1/lambda_heavy) correction, ~1e-28 here.
    """
    kl = inp['k_link_GeV2']
    sums = [D((9**(r+1)-1)//8) for r in range(31)]
    trace = sum(sums[:-1])/kl + sums[-1]/endpoint
    if case['family'] == 'structural':
        trace += 30*case['c']/kl + case['b']/endpoint
    else:
        adjacent_trace = 6*(sum(sums[:-2])/kl + sums[-2]/endpoint)
        trace += case['epsilon']*adjacent_trace
    return 1/trace


def run(source=SOURCE, output=HERE):
    inp = inputs(source)
    cases = families(inp)
    checks, result_rows, metrics = [], [], []

    def check(name, observed, bound=None, passed=None):
        if passed is None:
            passed = observed <= bound
        checks.append({'check': name, 'observed': str(observed),
                       'bound': str(bound) if bound is not None else None,
                       'passed': bool(passed)})

    w = [3**(30-j) for j in range(31)]
    S = sum(x*x for x in w)
    T = 2*sum(w[j]*w[j+1] for j in range(30))
    check('exact integer Qw=0', all(w[j]-3*w[j+1] == 0 for j in range(30)), passed=all(w[j]-3*w[j+1] == 0 for j in range(30)))
    check('exact norm geometric sum', S == (9**31-1)//8, passed=S == (9**31-1)//8)

    with localcontext() as ctx:
        ctx.prec = 110
        for case in cases:
            hd, ho, gd, go = pencil(inp, case, D(0))
            G = float_matrix(gd, go)
            g_eigs = np.linalg.eigvalsh(G)
            correction_norm = float(np.linalg.norm(G-np.eye(31), 2))
            positive_lower_bound = 1.0 if case['family'] == 'structural' else 1-2*abs(float(case['epsilon']))*math.cos(math.pi/32)
            check(f"{case['case']}: metric positive", positive_lower_bound, passed=positive_lower_bound > 0)
            # Compute period using exact structural form, preserving the ~1e-30 endpoint shift.
            norm_shift = case['b'] if case['family'] == 'structural' else case['epsilon']*T
            F2_ratio_minus1 = norm_shift/D(S)
            F_ratio = (1+F2_ratio_minus1).sqrt()
            direct_norm = sum(D(w[j]*w[j])*gd[j] for j in range(31)) + 2*sum(D(w[j]*w[j+1])*go[j] for j in range(30))
            check(f"{case['case']}: direct period identity", abs(direct_norm-(D(S)+norm_shift))/D(S), D('1e-100'))
            metrics.append({**case, 'metric_min_eig_float': float(g_eigs[0]), 'metric_max_eig_float': float(g_eigs[-1]),
                            'metric_positive_lower_bound': positive_lower_bound,
                            'metric_correction_operator_norm': correction_norm,
                            'F_over_F0': F_ratio, 'F_over_F0_minus1': F_ratio-1,
                            'F2_over_F02_minus1': F2_ratio_minus1,
                            'F2_shift_GeV2': inp['f_site_GeV']**2*norm_shift})
            for configuration, endpoint in (('source off', D(0)), ('source minimum', inp['k_min_GeV2']), ('source maximum', inp['k_top_GeV2'])):
                hd, ho, gd, go = pencil(inp, case, endpoint)
                H = float_matrix(hd, ho)
                eigs = eigh(H, G, eigvals_only=True, driver='gvd')
                L = np.linalg.cholesky(G)
                left = solve_triangular(L, H, lower=True)
                canonical = solve_triangular(L, left.T, lower=True).T
                whitened_eigs = np.linalg.eigvalsh((canonical+canonical.T)/2)
                coordinate_error = float(np.max(abs(eigs[1:]-whitened_eigs[1:])/abs(eigs[1:])))
                check(f"{case['case']}/{configuration}: heavy coordinate consistency", coordinate_error, 2e-12)
                if endpoint == 0:
                    root = D(0)
                    roots = {str(p): D(0) for p in PRECISIONS}
                    # Q has row rank 30; SPD G preserves nullity/inertia.
                    count_negative, count_zero = 0, 1
                    check(f"{case['case']}: positive source-off heavy spectrum", float(eigs[1]), passed=eigs[1] > 0)
                    approx, approx_error = D(0), D(0)
                    if case['family'] == 'structural' and case['b'] == 0:
                        mu = np.array([10-6*math.cos(j*math.pi/31) for j in range(1,31)])
                        exact = float(inp['k_link_GeV2'])*mu/(1+float(case['c'])*mu)
                        err = float(np.max(abs(eigs[1:]-exact)/exact))
                        check(f"{case['case']}: analytic source-off spectrum", err, 2e-12)
                else:
                    roots = {str(p): small_root(inp, case, endpoint, p) for p in PRECISIONS}
                    root = roots['110']
                    for p, bound in ((60, D('1e-24')), (90, D('1e-50'))):
                        check(f"{case['case']}/{configuration}: {p} vs 110 digit light root", abs((roots[str(p)]-root)/root), bound)
                    count_negative = inertia_at(D(0), (hd,ho,gd,go), 110)
                    count_zero = 0
                    expected_negative = 0 if endpoint > 0 else 1
                    check(f"{case['case']}/{configuration}: expected negative inertia", count_negative, passed=count_negative == expected_negative)
                    check(f"{case['case']}/{configuration}: light sign", root*endpoint, passed=root*endpoint > 0)
                    approx = trace_inverse_approx(inp, case, endpoint)
                    approx_error = abs((approx-root)/root)
                    check(f"{case['case']}/{configuration}: inverse-trace light estimate", approx_error, D('1e-25'))
                signed_mass = root.copy_abs().sqrt()*D('1e9')*(1 if root >= 0 else -1)
                result_rows.append({**case, 'configuration': configuration,
                    'F_over_F0': F_ratio, 'F_over_F0_minus1': F_ratio-1,
                    'metric_positive_lower_bound': positive_lower_bound,
                    'metric_correction_operator_norm': correction_norm,
                    'light_mass_squared_GeV2': root, 'light_signed_sqrt_eV': signed_mass,
                    'light_roots_by_decimal_precision_GeV2': roots,
                    'heavy_min_GeV': math.sqrt(eigs[1]), 'heavy_max_GeV': math.sqrt(eigs[-1]),
                    'negative_modes': count_negative, 'exact_zero_modes': count_zero,
                    'inverse_trace_light_estimate_GeV2': approx,
                    'inverse_trace_light_relative_error': approx_error,
                    'heavy_coordinate_relative_error': coordinate_error})

        baseline = {r['configuration']: r for r in result_rows if r['case'] == 'baseline'}
        for row in result_rows:
            ref = baseline[row['configuration']]
            row['heavy_min_relative_change'] = row['heavy_min_GeV']/ref['heavy_min_GeV']-1
            row['heavy_max_relative_change'] = row['heavy_max_GeV']/ref['heavy_max_GeV']-1
            row['light_mass_squared_relative_change'] = ((row['light_mass_squared_GeV2']/ref['light_mass_squared_GeV2'])-1) if ref['light_mass_squared_GeV2'] else D(0)
        with (source/'v1.23_wilson_hessian.csv').open() as handle:
            for published in csv.DictReader(handle):
                observed = baseline[published['configuration']]
                for public_col, local_col in [('light_mode_eV','light_signed_sqrt_eV'), ('heavy_min_GeV','heavy_min_GeV'), ('heavy_max_GeV','heavy_max_GeV')]:
                    ref = D(published[public_col])
                    obs = D(str(observed[local_col])).copy_abs()
                    error = abs(obs/ref-1) if ref else abs(obs)
                    check(f"baseline CSV/{published['configuration']}/{public_col}", error, D('1e-10'))

    check('all 12 registered cases retained', len(metrics), passed=len(metrics) == 12)
    check('all 36 registered configurations retained', len(result_rows), passed=len(result_rows) == 36)
    check('source hashes unchanged during audit', all(digest(source/name) == sha for name,sha in inp['source_files_sha256'].items()), passed=all(digest(source/name) == sha for name,sha in inp['source_files_sha256'].items()))
    payload = {
        'status': 'PASS' if all(x['passed'] for x in checks) else 'FAIL',
        'date_local': '2026-10-01', 'timezone': 'America/Los_Angeles',
        'scope': 'Registered finite assumed-metric sensitivity; not computed or matched full 5D loops.',
        'normalization': 'K=f_site^2 G; phase U=f_site^2 H; solve H v=m^2 G v with fixed published f_site.',
        'input_precision': 'Public float-derived curvatures promoted to Decimal. Root precision is numerical precision for those rounded coefficients, not physical input accuracy.',
        'signed_mass_convention': 'sign(m^2)*sqrt(abs(m^2)) in eV; a negative value denotes an imaginary-frequency tachyon magnitude, not a negative particle mass.',
        'off_light_root_convention': 'Exact algebraic zero from rank(Q)=30; not inferred from a floating eigensolver.',
        'f_period_convention': 'F is the compact winding/trough norm from Qw=0; finite endpoint source relaxes the local curvature eigenvector.',
        'inputs': inp,
        'exact_winding_vector': w, 'exact_w_norm_squared': S, 'exact_w_adjacency_w': T,
        'runtime': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__, 'python_executable': sys.executable},
        'provenance': {'audit_sha256': digest(Path(__file__)), 'registration_sha256': digest(HERE/'REGISTRATION.md')},
        'metrics': metrics, 'results': result_rows, 'checks': checks,
    }
    def serial(value):
        if isinstance(value, D):
            return str(value)
        raise TypeError(type(value).__name__)
    output.mkdir(parents=True, exist_ok=True)
    (output/'results.json').write_text(json.dumps(payload, indent=2, default=serial)+'\n')
    columns = [key for key in result_rows[0] if key != 'light_roots_by_decimal_precision_GeV2']
    with (output/'results.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(result_rows)
    print(json.dumps({'status': payload['status'], 'cases': len(metrics), 'configurations': len(result_rows),
                      'checks': len(checks), 'failures': [x for x in checks if not x['passed']]}))
    return 0 if payload['status'] == 'PASS' else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=SOURCE,
                        help='Directory containing the five public v1.23 source files.')
    parser.add_argument('--output-dir', type=Path, default=HERE,
                        help='Output directory for results.json and results.csv; use a fresh directory for reproduction.')
    args = parser.parse_args()
    source, output = args.source_root.resolve(), args.output_dir.resolve()
    if output == source or source in output.parents:
        parser.error('--output-dir must be outside the input release directory')
    raise SystemExit(run(source, output))
