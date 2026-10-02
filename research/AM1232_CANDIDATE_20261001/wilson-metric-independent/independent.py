#!/usr/bin/env python3
"""Independent Wilson metric check: exact charge-factor inverse iteration.

Only Python's standard library is needed. Does not import the producer or release
generator. High precision resolves a frozen-input eigenproblem, not physical
matching uncertainty. Writes only to the selected output directory.
"""
from decimal import Decimal as D, localcontext
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/workspace/AntiMatter/research/AM1231/v1.23/v1.23_summary.json')
N = 30


def published_inputs(source=SOURCE):
    s = json.loads(source.read_text())
    def curvature(x, top=False):
        p = 1.0+x+x*x/3.0
        return sum(((-1.0)**n if top else 1.0)
                   * math.exp(-(n-1)*x)
                   * (1+n*x+(n*x)**2/3.0)/(n**3*p)
                   for n in range(1, 100))
    pref = s['physical_source_height_GeV4']/s['wilson_f_site_GeV']**2
    return {
        'k_link': pref*curvature(s['wilson_x_link']),
        'k_min': pref*curvature(s['wilson_x_endpoint']),
        'k_top': pref*curvature(s['wilson_x_endpoint'], True),
        'epsilon': s['wilson_adjacent_mixing_estimate'],
    }


def families(inputs):
    eps = D(str(inputs['epsilon']))
    c0 = eps/3
    yield 'baseline', D(0), D(0), D(0)
    for factor in (1, 3, 10):
        for bfactor in (0, 1, 3):
            yield f'c{factor}_b{bfactor}', c0*factor, c0*factor*bfactor, D(0)
    yield 'adjacent_plus', D(0), D(0), eps
    yield 'adjacent_minus', D(0), D(0), -eps


def metric_diagonals(c, b, a):
    diagonal = [1+c]+[1+10*c]*(N-1)+[1+9*c+b]
    off = [-3*c+a]*N
    return diagonal, off


def product(diagonal, off, vector):
    out = [diagonal[i]*vector[i] for i in range(N+1)]
    for i in range(N):
        out[i] += off[i]*vector[i+1]
        out[i+1] += off[i]*vector[i]
    return out


def inverse_hessian(vector, kl, ke):
    # B has diagonal 1, superdiagonal -3; H=B^T diag(kl,...,kl,ke) B.
    # Solve B^T z=v; divide by the diagonal; solve B x=z.
    z = [vector[0]]
    for i in range(1, N+1):
        z.append(vector[i]+3*z[-1])
    for i in range(N):
        z[i] /= kl
    z[N] /= ke
    x = [D(0)]*(N+1)
    x[N] = z[N]
    for i in range(N-1, -1, -1):
        x[i] = z[i]+3*x[i+1]
    return x


def light_mode(kl, ke, gd, go):
    vector = [D(3)**(N-i) for i in range(N+1)]
    previous = None
    for iteration in range(12):
        vector = inverse_hessian(product(gd, go, vector), kl, ke)
        scale = max(abs(x) for x in vector)
        vector = [x/scale for x in vector]
        qv = [vector[i]-3*vector[i+1] for i in range(N)]
        numerator = kl*sum(x*x for x in qv)+ke*vector[N]**2
        gv = product(gd, go, vector)
        denominator = sum(x*y for x, y in zip(vector, gv))
        eigenvalue = numerator/denominator
        if eigenvalue == previous:
            break
        previous = eigenvalue
    hv = [kl*qv[0]]
    hv += [kl*(qv[i]-3*qv[i-1]) for i in range(1, N)]
    hv += [ke*vector[N]-3*kl*qv[N-1]]
    residual = max(abs(x-eigenvalue*y) for x,y in zip(hv,gv))
    denominator = max(max(abs(x) for x in hv), abs(eigenvalue)*max(abs(y) for y in gv))
    return eigenvalue, residual/denominator, iteration+1


def inertia(diagonal, off, gd, go, lam):
    # Congruence to a diagonal matrix via LDL^T: negative pivots count roots.
    pivot = diagonal[0]-lam*gd[0]
    count = int(pivot < 0)
    for i in range(1, N+1):
        if not pivot:
            # Exact encounter has zero measure in our Decimal bisection. Stop
            # instead of imposing a physically ambiguous zero-pivot convention.
            raise ArithmeticError('Exact LDL pivot zero')
        edge = off[i-1]-lam*go[i-1]
        pivot = diagonal[i]-lam*gd[i]-edge*edge/pivot
        count += int(pivot < 0)
    return count


def heavy_root(kl, ke, gd, go, index):
    hd = [kl]+[10*kl]*(N-1)+[9*kl+ke]
    ho = [-3*kl]*N
    lower, upper = D(1), D('1e7')
    assert inertia(hd,ho,gd,go,lower) <= index
    assert inertia(hd,ho,gd,go,upper) > index
    for _ in range(260):
        middle = (lower+upper)/2
        if inertia(hd,ho,gd,go,middle) <= index:
            lower = middle
        else:
            upper = middle
    return (lower+upper)/2


def run(precision, inputs):
    with localcontext() as ctx:
        ctx.prec = precision
        kl = D(str(inputs['k_link']))
        endpoint = {'off':D(0), 'minimum':D(str(inputs['k_min'])), 'top':D(str(inputs['k_top']))}
        winding = [D(3)**(N-i) for i in range(N+1)]
        norm = sum(x*x for x in winding)
        rows = []
        for name,c,b,a in families(inputs):
            gd,go = metric_diagonals(c,b,a)
            norm_metric = sum(x*y for x,y in zip(winding,product(gd,go,winding)))
            shift = (norm_metric-norm)/norm
            expected = b/norm+2*a*sum(winding[i]*winding[i+1] for i in range(N))/norm
            assert abs(shift-expected) < D(10)**(-(precision-5))
            # Use the exact algebraic identity in reported shifts, rather than
            # carrying Decimal matrix-contraction cancellation into b=0 output.
            shift = expected
            assert all(gd[i]-sum(abs(go[j]) for j in (i-1,i) if 0<=j<N)>0 for i in range(N+1))
            for state,ke in endpoint.items():
                light,residual,iterations = light_mode(kl,ke,gd,go) if ke else (D(0),D(0),0)
                lo = heavy_root(kl,ke,gd,go,1)
                hi = heavy_root(kl,ke,gd,go,N)
                rows.append({'case':name,'state':state,'c':str(c),'b':str(b),'adjacent':str(a),
                             'light_mass_squared_GeV2':str(light),
                             'light_signed_mass_eV':str(light.copy_abs().sqrt()*D('1e9')*(-1 if light<0 else 1)),
                             'light_equation_relative_residual':str(residual),'inverse_iterations':iterations,
                             'heavy_min_GeV':str(lo.sqrt()),'heavy_max_GeV':str(hi.sqrt()),
                             'period_squared_relative_shift':str(shift),
                             'period_relative_shift':str(shift/((1+shift).sqrt()+1))})
        return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=SOURCE.parent,
                        help='Directory containing the public v1.23_summary.json.')
    parser.add_argument('--output-dir', type=Path, default=ROOT,
                        help='Directory for independent-results.json.')
    args = parser.parse_args()
    if args.output_dir.resolve().is_relative_to(args.source_root.resolve()):
        parser.error('Output must be outside the preserved public input directory.')
    source = args.source_root/'v1.23_summary.json'
    inputs = published_inputs(source)
    rows80,rows110 = run(80,inputs),run(110,inputs)
    max_relative = D(0)
    with localcontext() as ctx:
        ctx.prec = 110
        for low,high in zip(rows80,rows110):
            for key in ('light_mass_squared_GeV2','heavy_min_GeV','heavy_max_GeV'):
                value = D(high[key])
                if value:
                    relative = abs(D(low[key])-value)/abs(value)
                    max_relative = max(max_relative,relative)
                    assert relative < D('1e-45'), (low['case'],low['state'],key,relative)
    output = {'status':'PASS independent precision and structural checks',
              'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
              'inputs_reconstructed_independently_from_public_summary':inputs,
              'method':'Decimal triangular charge-factor inverse iteration for tiny roots; LDL inertia bisection for heavy roots',
              'precision_digits':[80,110], 'max_cross_precision_relative_difference':str(max_relative),
              'cases':rows110}
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'independent-results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='cases'},indent=2))
    print('Checked',len(rows110),'case/state rows.')


if __name__=='__main__':
    main()
