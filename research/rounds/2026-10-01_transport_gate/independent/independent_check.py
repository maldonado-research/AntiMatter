#!/usr/bin/env python3
"""Independent audit: chemical-potential coordinates and augmented expm.

No producer imports or numerical outputs are used to construct this audit.
Fixtures come solely from REGISTRATION.md. All inputs are dimensionless toy
inputs; this program calculates no baryon abundance or physical reaction rate.
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform

import numpy as np
import scipy
from scipy.linalg import expm, null_space, orth

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--producer-dir", type=Path, default=None,
                    help="producer directory; defaults to sibling producer/ or the local registered round")
parser.add_argument("--repo-root", type=Path, default=None,
                    help="source repository root for required comparator provenance validation")
arguments = parser.parse_args()
default_producer = HERE.parent / "producer"
if not default_producer.is_dir():
    default_producer = HERE.parent / "ROUND_20261001_TRANSPORT"
PRODUCER = (arguments.producer_dir or default_producer).resolve()
S = np.array([[-1., 0., 1.], [1., -1., 0.], [0., 1., -1.]])
C = np.diag([1., 2., 3.])
q = np.ones(3)
d = np.array([1., 0., 0.])
amp = 0.01
b = amp * S.T @ d
checks = []
cases = {}


def close(name, actual, expected, tolerance=2e-12):
    error = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
    passed = bool(error <= tolerance)
    checks.append(dict(name=name, passed=passed, max_absolute_error=error,
                       absolute_tolerance=tolerance))
    if not passed:
        raise AssertionError(f"{name}: {error} > {tolerance}")


def validated(c, rates):
    c, rates = np.asarray(c, float), np.asarray(rates, float)
    if not np.allclose(c, c.T, atol=1e-14, rtol=0):
        raise ValueError("susceptibility must be symmetric")
    if np.min(np.linalg.eigvalsh(c)) <= 0:
        raise ValueError("susceptibility must be positive definite")
    if np.min(rates) < 0:
        raise ValueError("rates cannot be negative")
    return c, rates


def propagate(x, bias, rates, duration, c=C):
    """Solve dmu/dtau = -C^-1 L mu + C^-1 S R b by block expm."""
    c, rates = validated(c, rates)
    r = np.diag(rates)
    block = np.zeros((4, 4))
    block[:3, :3] = -np.linalg.solve(c, S @ r @ S.T)
    block[:3, 3] = np.linalg.solve(c, S @ r @ bias)
    initial = np.r_[np.linalg.solve(c, x), 1.]
    return c @ (expm(duration * block) @ initial)[:3]


def stationary(x0, bias, rates, c=C):
    """Solve symmetric chemical-force equation with all conserved charges."""
    c, rates = validated(c, rates)
    active = rates > 0
    charges = null_space(S[:, active].T)
    l = S @ np.diag(rates) @ S.T
    k = charges.shape[1]
    kkt = np.block([[l, charges],
                    [charges.T @ c, np.zeros((k, k))]])
    rhs = np.r_[S @ np.diag(rates) @ bias, charges.T @ x0]
    mu = np.linalg.solve(kkt, rhs)[:3]
    return c @ mu, charges


def projection(bias, rates):
    """Weighted least-squares projection in active reaction coordinates."""
    active = rates > 0
    active_s = S[:, active]
    basis = orth(active_s.T)
    r = np.diag(rates[active])
    if basis.shape[1] == 0:
        return np.zeros(np.count_nonzero(active)), active
    coefficient = np.linalg.solve(basis.T @ r @ basis,
                                  basis.T @ r @ bias[active])
    return basis @ coefficient, active


expected = amp * np.array([5/6, -1/3, -1/2])
close("stoichiometric conservation", S.T @ q, np.zeros(3))
close("cycle null vector", S @ q, np.zeros(3))
close("compatible bias cycle sum", np.sum(b), 0)
close("conserved source gauge", amp*S.T@(d+7*q), b)
close("conserved-current source bias", amp*S.T@q, np.zeros(3))

for name, rates in [("equal", np.ones(3)), ("unequal", np.array([1., 2., 4.]))]:
    xs, charges = stationary(np.zeros(3), b, rates)
    close(name + " compatible stationary", xs, expected)
    close(name + " compatible flux", rates*(b-S.T@np.linalg.solve(C,xs)), 0)
    x30 = propagate(np.zeros(3), b, rates, 30)
    close(name + " stationary relaxation", x30, xs)
    projected, active = projection(b, rates)
    close(name + " compatible projection", projected, b[active])
    # Explicit similarity transform checks PSD and density zero modes.
    evals, evecs = np.linalg.eigh(C)
    root = (evecs*np.sqrt(evals))@evecs.T
    invroot = (evecs*(1/np.sqrt(evals)))@evecs.T
    a = invroot @ S @ np.diag(rates) @ S.T @ invroot
    close(name + " whitened symmetric", a, a.T)
    close(name + " charge zero mode", a @ root @ q, 0)
    close(name + " density zero mode", S @ np.diag(rates) @ S.T @ q, 0)
    if np.linalg.eigvalsh(a)[0] < -2e-12:
        raise AssertionError("negative relaxation eigenvalue")
    x1 = propagate(np.zeros(3), b, rates, 1)
    x2 = propagate(x1, -b, rates, 1)
    e = expm(-S @ np.diag(rates) @ S.T @ np.linalg.inv(C))
    signed_prediction = -(np.eye(3)-e)@(np.eye(3)-e)@expected
    close(name + " signed analytic history", x2, signed_prediction)
    close(name + " signed source zero area", b+(-b), 0)
    close(name + " reversal", propagate(propagate(np.zeros(3),-b,rates,1),b,rates,1), -x2)
    close(name + " shutdown", propagate(x2, np.zeros(3), np.zeros(3), 20), x2)
    washed = propagate(x2, np.zeros(3), rates, 20)
    close(name + " washout", washed, 0, tolerance=1e-10)
    close(name + " signed conserved charge", q@x2, 0)
    cases[name] = dict(stationary=xs.tolist(), x_at_1=x1.tolist(),
                       signed_x_at_2=x2.tolist(), signed_norm=float(np.linalg.norm(x2)),
                       washed_x_at_22=washed.tolist(),
                       washed_norm=float(np.linalg.norm(washed)),
                       relaxation_eigenvalues=np.linalg.eigvalsh(a).tolist())

for name, rates in [("equal", np.ones(3)), ("unequal", np.array([1.,2.,4.]))]:
    cb = amp*q
    xs, _ = stationary(np.zeros(3), cb, rates)
    expected_cycle = np.zeros(3) if name == "equal" else amp*np.array([11/21,-8/21,-1/7])
    expected_flux = amp*q if name == "equal" else (12*amp/7)*q
    flux = rates*(cb-S.T@np.linalg.solve(C,xs))
    close(name + " cycle stationary", xs, expected_cycle)
    close(name + " cycle flux", flux, expected_flux)
    close(name + " cycle charge production", S@flux, 0)
    projected, active = projection(cb,rates)
    close(name + " weighted bias projection", projected, S[:,active].T@np.linalg.solve(C,xs))
    close(name + " weighted residual orthogonality", S[:,active]@(rates[active]*(cb[active]-projected)), 0)
    # Work supplied to sustain circulation equals irreversible dissipation.
    dissipation = np.dot(flux,flux/rates)
    close(name + " steady work/dissipation", np.dot(cb,flux), dissipation)
    cases["cycle_"+name] = dict(stationary=xs.tolist(), flux=flux.tolist(),
                               projected_bias=projected.tolist(),
                               cycle_sum=float(np.sum(cb)), dissipation=float(dissipation))

x0 = np.array([.4,-.1,.2])
xeq, _ = stationary(x0, np.zeros(3), np.ones(3))
close("nonzero-charge equilibrium", xeq, C@q*(q@x0)/(q@C@q))
close("nonzero-charge preservation", q@propagate(x0,np.zeros(3),np.ones(3),2),q@x0)
times = np.linspace(0,4,101)
free = [0.5*np.dot(x,np.linalg.solve(C,x)) for x in
        (propagate(x0,np.zeros(3),np.ones(3),t) for t in times)]
checks.append(dict(name="zero-bias quadratic free energy decreases",passed=bool(np.max(np.diff(free)) <= 2e-12),
                   max_increment=float(np.max(np.diff(free)))))
if not checks[-1]["passed"]:
    raise AssertionError("free energy increases")
for i in range(9):
    state = np.array([0.03*i,-0.01,0.007])
    rates = np.array([1.,2.,4.])
    affinity = S.T @ np.linalg.solve(C,state)
    flux = rates*(b-affinity)
    work = np.dot(b,flux)
    dissip = np.dot(flux,flux/rates)
    free_dot = np.dot(np.linalg.solve(C,state), S@flux)
    close(f"work/entropy identity {i}", free_dot, work-dissip)

ndc = np.array([[2.,.2,.1],[.2,1.5,.3],[.1,.3,3.]])
ndeq = amp*ndc@(d-q*(q@ndc@d)/(q@ndc@q))
nds, _ = stationary(np.zeros(3),b,np.array([1.,2.,4.]),ndc)
close("non-diagonal susceptibility stationary", nds, ndeq)
ndsigned = propagate(propagate(np.zeros(3),b,np.ones(3),1,ndc),-b,np.ones(3),1,ndc)
close("non-diagonal susceptibility charge",q@ndsigned,0)
cases["nondiagonal"] = dict(susceptibility=ndc.tolist(),stationary=nds.tolist(),signed_x_at_2=ndsigned.tolist())

for rates, expected_dimension in [(np.ones(3),1),(np.array([1.,0.,0.]),2),(np.zeros(3),3)]:
    xs, charges = stationary(x0,b,rates)
    close("active conserved dimension " + str(expected_dimension),charges.shape[1],expected_dimension)
    xt = propagate(x0,b,rates,3)
    close("active charges " + str(expected_dimension), charges.T@xt, charges.T@x0)
    close("active stationary charges " + str(expected_dimension),charges.T@xs,charges.T@x0)
    close("active stationary motion " + str(expected_dimension),S@(rates*(b-S.T@np.linalg.solve(C,xs))),0)

for name, c, rates in [("negative susceptibility",np.diag([1.,-2.,3.]),np.ones(3)),
                       ("negative rate",C,np.array([1.,-1.,1.]))]:
    try:
        validated(c,rates)
    except ValueError:
        checks.append(dict(name=name+" rejected",passed=True))
    else:
        raise AssertionError(name+" was accepted")

registration = PRODUCER / "REGISTRATION.md"
payload = dict(method="Chemical-potential coordinates with scipy.linalg.expm augmented generator; constrained linear equilibrium and weighted least squares",
               producer_imports=False, input_source="REGISTRATION.md only; producer implementation not read before independent implementation",
               registration_sha256=hashlib.sha256(registration.read_bytes()).hexdigest(),
               python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
               controls=checks, control_count=len(checks), all_passed=all(c["passed"] for c in checks),cases=cases)
(HERE/"independent_results.json").write_text(json.dumps(payload,indent=2)+"\n")
print(json.dumps(dict(all_passed=payload["all_passed"],control_count=len(checks),
                      largest_absolute_error=max(c.get("max_absolute_error",0) for c in checks),
                      equal_signed_norm=cases["equal"]["signed_norm"],
                      equal_washed_norm=cases["equal"]["washed_norm"]),indent=2))
