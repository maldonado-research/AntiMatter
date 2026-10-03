#!/usr/bin/env python3
"""Compare outputs and require immutable registration and public input provenance."""
from pathlib import Path
import hashlib
import json
import numpy as np
from independent_check import propagate, b, C, PRODUCER, arguments

HERE = Path(__file__).resolve().parent
OTHER = PRODUCER
ORIGINAL_REGISTRATION_SHA256 = "a8cf1c87f1dc5fd0d404a2f5b8a8b56ccf3cfe993aef8daeb08c8e35d4513006"
ORIGINAL_RECEIPT_SHA256 = "2bbd13f5465735b84968d92384b2633972300ad56d8c678eb1258764ff5a0bba"
RECORDED_REPO_ROOT = Path("/workspace/AntiMatter")
independent = json.loads((HERE/"independent_results.json").read_text())
producer = json.loads((OTHER/"results.json").read_text())
comparisons = []
validation_errors = []


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def compare(name, actual, expected, tolerance=2e-12):
    actual, expected = np.asarray(actual), np.asarray(expected)
    finite = np.isfinite(actual).all() and np.isfinite(expected).all()
    same_shape = actual.shape == expected.shape
    error = float(np.max(np.abs(actual-expected))) if finite and same_shape else None
    comparisons.append(dict(name=name, max_absolute_error=error,
                            absolute_tolerance=tolerance,
                            passed=bool(error is not None and error <= tolerance)))


ic=independent["cases"]
for name, actual_a, actual_b in [
    ("compatible stationary",ic["equal"]["stationary"],producer["compatible_stationary_x"]),
    ("positive interval",ic["equal"]["x_at_1"],producer["positive_pulse_x_at_1"]),
    ("signed interval",ic["equal"]["signed_x_at_2"],producer["zero_integrated_signed_bias_x_at_2"]),
    ("shutdown",ic["equal"]["signed_x_at_2"],producer["freeze_at_2_x_at_22"]),
    ("washout",ic["equal"]["washed_x_at_22"],producer["washout_x_at_22"]),
    ("equal cycle stationary",ic["cycle_equal"]["stationary"],producer["equal_rate_cycle_stationary_x"]),
    ("equal cycle current",ic["cycle_equal"]["flux"],producer["equal_rate_cycle_progress"]),
    ("unequal cycle stationary",ic["cycle_unequal"]["stationary"],producer["uneven_rate_cycle_stationary_x"]),
    ("unequal cycle current",ic["cycle_unequal"]["flux"],producer["uneven_rate_cycle_progress"]),
    ("nonzero relaxation eigenvalues",ic["equal"]["relaxation_eigenvalues"][1:],producer["positive_relaxation_eigenvalues"]),
]:
    compare(name,actual_a,actual_b)

# A missing column/row cannot silently drop the required eleventh comparison.
columns = ("tau","x_A","x_B","x_C","mu_A_over_T","mu_B_over_T","mu_C_over_T","conserved_charge")
trajectory_path = OTHER/"signed_trajectory.csv"
trajectory_valid = False
try:
    trajectory = np.atleast_1d(np.genfromtxt(trajectory_path,delimiter=",",names=True))
    if not set(columns).issubset(trajectory.dtype.names or ()):
        validation_errors.append("trajectory is missing required columns")
    elif trajectory.size != 201:
        validation_errors.append(f"trajectory requires 201 rows, found {trajectory.size}")
    elif not all(np.isfinite(trajectory[column]).all() for column in columns):
        validation_errors.append("trajectory contains non-finite values")
    elif not np.allclose(trajectory["tau"],np.linspace(0,2,201),rtol=0,atol=2e-12):
        validation_errors.append("trajectory time grid differs from the required registered 201-point grid")
    else:
        trajectory_valid = True
        x1=propagate(np.zeros(3),b,np.ones(3),1)
        predicted=[]
        actual=[]
        for row in trajectory:
            t=row["tau"]
            x=propagate(np.zeros(3),b,np.ones(3),t) if t<=1 else propagate(x1,-b,np.ones(3),t-1)
            predicted.append(np.r_[x,np.linalg.solve(C,x),np.sum(x)])
            actual.append([row[column] for column in columns[1:]])
        compare("complete signed trajectory",predicted,actual)
except (OSError,ValueError,TypeError) as error:
    validation_errors.append("trajectory cannot be read: "+str(error))
if not trajectory_valid:
    comparisons.append(dict(name="complete signed trajectory",max_absolute_error=None,
                            absolute_tolerance=2e-12,passed=False))

receipt_path=OTHER/"registration_receipt.json"
receipt=json.loads(receipt_path.read_text())
receipt_sha=digest(receipt_path)
receipt_unchanged=receipt_sha==ORIGINAL_RECEIPT_SHA256
registration_sha=digest(OTHER/"REGISTRATION.md")
registration_unchanged=(registration_sha==ORIGINAL_REGISTRATION_SHA256
                        and registration_sha==receipt.get("registration_sha256"))
if not receipt_unchanged:
    validation_errors.append("original registration receipt hash mismatch")
if not registration_unchanged:
    validation_errors.append("original registration document hash mismatch")
if producer.get("registration_receipt") != receipt:
    validation_errors.append("producer results embed a different registration receipt")
if len(receipt.get("inputs",[])) != 4:
    validation_errors.append("registration receipt must identify four required public-context inputs")

repo_root=arguments.repo_root.resolve() if arguments.repo_root is not None else None
if repo_root is None:
    for ancestor in list(OTHER.parents)+list(HERE.parents):
        if (ancestor/"research"/"AM1231").is_dir():
            repo_root=ancestor
            break
if repo_root is None:
    validation_errors.append("required context repository not found; supply --repo-root")

hashes=[]
for item in receipt.get("inputs",[]):
    recorded_path=Path(item["path"])
    try:
        relative_path=recorded_path.relative_to(RECORDED_REPO_ROOT)
    except ValueError:
        validation_errors.append("registered input lies outside its recorded source repository")
        relative_path=None
    # Always resolve against the supplied actual repository, even when the
    # original recorded absolute path still happens to exist on this machine.
    source_path=repo_root/relative_path if repo_root is not None and relative_path is not None else None
    got=digest(source_path) if source_path is not None else None
    matches=got==item["sha256"]
    hashes.append(dict(source_relative_path=str(relative_path),
                       expected_sha256=item["sha256"],actual_sha256=got,
                       exists=got is not None,matches=matches))
    if not matches:
        validation_errors.append("required public input missing or hash mismatch: "+str(relative_path))

all_numerical_passed=all(c["passed"] for c in comparisons) and len(comparisons)==11
all_provenance_passed=(receipt_unchanged and registration_unchanged
                       and len(hashes)==4 and all(x["matches"] for x in hashes)
                       and producer.get("registration_receipt")==receipt)
all_passed=all_numerical_passed and all_provenance_passed and not validation_errors
errors=[c["max_absolute_error"] for c in comparisons if c["max_absolute_error"] is not None]
payload=dict(all_passed=all_passed,all_numerical_comparisons_passed=all_numerical_passed,
             all_provenance_checks_passed=all_provenance_passed,
             validation_errors=validation_errors,comparisons=comparisons,
             maximum_numerical_discrepancy=max(errors,default=None),
             trajectory_valid=trajectory_valid,required_trajectory_rows=201,
             required_trajectory_columns=list(columns),
             provenance_scope="current rerun checked against immutable original session snapshot; original receipt not modified",
             registration_unchanged=registration_unchanged,
             registration_sha256=registration_sha,
             original_registration_sha256=ORIGINAL_REGISTRATION_SHA256,
             registration_receipt_unchanged=receipt_unchanged,
             registration_receipt_sha256=receipt_sha,
             original_registration_receipt_sha256=ORIGINAL_RECEIPT_SHA256,
             registered_inputs=hashes,
             audited_file_sha256={path.name:digest(path) for path in
                                  [OTHER/"transport.py",OTHER/"results.json",trajectory_path]})
(HERE/"comparison_results.json").write_text(json.dumps(payload,indent=2)+"\n")
print(json.dumps(dict(all_passed=all_passed,
                      maximum_numerical_discrepancy=payload["maximum_numerical_discrepancy"],
                      registration_unchanged=registration_unchanged,
                      registration_receipt_unchanged=receipt_unchanged,
                      registered_inputs_unchanged=len(hashes)==4 and all(x["matches"] for x in hashes),
                      validation_errors=validation_errors),indent=2))
if not all_passed:
    raise SystemExit(1)
