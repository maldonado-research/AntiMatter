#!/usr/bin/env python3
"""AI scientific review: read originals and replay copied scripts only.

This is a consistency/reproducibility review, not external peer review.
Nothing under producer, independent, inventory, or a repository is modified.
"""
import hashlib
import json
import math
import os
from fractions import Fraction as F
from pathlib import Path
import shutil
import subprocess
import sys
from importlib.metadata import version

HERE = Path(__file__).resolve().parent
ROUND = HERE.parent
REPLAY = HERE / "replay"
SOURCE_RELATIVE = Path("research/AM1231/v1.23.1/v1.23.1_efficiency_energy_frontier.py")
SOURCE_SHA256 = "4a2bfece249ef634986256b45b75fc8ab89a147d16673972e5565aeca24fe3a9"
INVENTORY_ALLOWLIST = (
    "PUBLIC_SAFE_OPERATOR_INVENTORY.md", "verify_inventory.py", "EXACT_INVENTORY_CHECKS.json",
)


def public_context():
    configured = os.environ.get("ANTIMATTER_PUBLIC_REPO")
    if configured:
        candidates = [Path(configured).expanduser().resolve()]
    else:
        current = Path.cwd().resolve()
        roots = dict.fromkeys((HERE, *HERE.parents, current, *current.parents))
        candidates = [candidate for root in roots for candidate in (root, root / "AntiMatter")]
    for root in candidates:
        source = root / SOURCE_RELATIVE
        if source.is_file():
            if sha(source) != SOURCE_SHA256:
                raise RuntimeError("Public historical input differs from its frozen hash")
            return root.resolve()
    raise RuntimeError("Set ANTIMATTER_PUBLIC_REPO to the public AntiMatter checkout root")


def selected_files():
    for sub in ("producer", "independent"):
        for path in sorted((ROUND / sub).glob("*")):
            if path.is_file():
                yield path
    for name in INVENTORY_ALLOWLIST:
        path = ROUND / "inventory" / name
        if not path.is_file():
            raise RuntimeError(f"Missing public inventory artifact: {name}")
        yield path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checks = []

    def check(name, ok, detail=None):
        checks.append({"name": name, "passed": bool(ok), "detail": detail})
        if not ok:
            raise AssertionError(name)

    original_hashes = {path.relative_to(ROUND).as_posix(): sha(path) for path in selected_files()}
    context = public_context()
    replay_env = os.environ.copy()
    replay_env["ANTIMATTER_PUBLIC_REPO"] = str(context)
    tasks = (
        ("producer", "sm_charge_diagnostic.py", (
            "results.json", "species_response.csv", "reaction_charges.csv",
            "conserved_density_basis.csv", "tests.csv")),
        ("producer", "conditional_sensitivity.py", (
            "conditional_sensitivity.json", "conditional_sensitivity.csv", "PROVENANCE.json")),
        ("independent", "sm_charge_response.py", ("matrices.json", "receipt.json")),
        ("independent", "conditional_normalization_sensitivity.py", ("sensitivity_receipt.json",)),
        ("independent", "compare_frozen_producer.py", ("comparison_receipt.json",)),
        ("independent", "portability_replay.py", ("portability_receipt.json",)),
        ("inventory", "verify_inventory.py", ("EXACT_INVENTORY_CHECKS.json",)),
    )
    for sub in ("producer", "independent", "inventory"):
        target = REPLAY / sub
        target.mkdir(parents=True, exist_ok=True)
        for path in selected_files():
            if path.parent != ROUND / sub:
                continue
            if path.suffix == ".py" or "REGISTRATION" in path.name or "CONTROLS" in path.name or path.name in (
                    "portability_provenance.json", "provenance_note.json"):
                shutil.copy2(path, target / path.name)
    for sub, script, outputs in tasks:
        result = subprocess.run([sys.executable, str(REPLAY / sub / script)], env=replay_env,
                                cwd=REPLAY, capture_output=True, text=True, timeout=60)
        check(f"replay_exit_{sub}_{script}", result.returncode == 0,
              {"returncode": result.returncode,
               "stdout": result.stdout.strip().replace(str(REPLAY), "replay"),
               "stderr": result.stderr.strip().replace(str(REPLAY), "replay")})
        for output in outputs:
            check(f"byte_reproducible_{sub}_{output}",
                  (ROUND / sub / output).read_bytes() == (REPLAY / sub / output).read_bytes(),
                  {"original_sha256": sha(ROUND / sub / output), "replay_sha256": sha(REPLAY / sub / output)})

    # A hand-reduced two-constraint check for the flavor-symmetric source.
    # Species order is aggregate q,u,d,l,e,H, with all internal generations.
    w = (18, 9, 9, 6, 3, 4)
    b = (F(1, 3),) * 3 + (F(0),) * 3
    l = (F(0),) * 3 + (F(1), F(1), F(0))
    y = tuple(map(F, ("1/6", "2/3", "-1/3", "-1/2", "-1", "1/2")))
    plus = tuple(x + z for x, z in zip(b, l))
    minus = tuple(x - z for x, z in zip(b, l))
    dot = lambda x, z: sum((wi*xi*zi for wi, xi, zi in zip(w, x, z)), F(0))
    check("hand_gram", (dot(y, y), dot(y, minus), dot(minus, minus)) == (11, 8, 13))
    check("hand_source_contractions", (dot(y, plus), dot(minus, plus)) == (-4, -5))
    det = 11*13-8*8
    lambda_y, lambda_minus = F(13*4-8*5, det), F(11*5-8*4, det)
    mu = tuple(plus[i] + y[i]*lambda_y + minus[i]*lambda_minus for i in range(6))
    check("hand_mu", mu == tuple(F(n, 79) for n in (36, 42, 30, 50, 44, 6)))
    check("hand_fixed_charges", dot(y, mu) == dot(minus, mu) == 0)
    check("hand_source_B_72_over_79", dot(b, mu)/6 == F(72, 79))
    no_source_mu = tuple(y[i]*F(-8, 79) + minus[i]*F(11, 79) for i in range(6))
    check("hand_no_source_B_28_over_79", dot(b, no_source_mu) == F(28, 79))

    # Per-generation LH anomaly traces; the RH global signs are conjugated.
    multiplicity = (6, 3, 3, 2, 1)
    chirality = (1, -1, -1, 1, -1)
    anomaly_yy = lambda charge: sum(F(g)*s*x*yy**2 for g, s, x, yy in zip(multiplicity, chirality, charge, y))
    anomaly_ww = lambda charge: F(1, 2)*(3*charge[0]+charge[3])
    anomaly_grav = lambda charge: sum(F(g)*s*x for g, s, x in zip(multiplicity, chirality, charge))
    check("hand_B_L_anomalies", anomaly_ww(b) == anomaly_ww(l) == F(1, 2)
          and anomaly_yy(b) == anomaly_yy(l) == F(-1, 2))
    check("hand_B_minus_L_gauge_zero_gravity_minus_one", anomaly_ww(minus) == anomaly_yy(minus) == 0
          and anomaly_grav(minus) == -1)
    check("hand_topological_normalization", 2*3*anomaly_ww(plus) == 6
          and 2*3*anomaly_yy(plus) == -6)

    # Compare the genuinely different ten- and sixteen-species implementations.
    producer = json.loads((ROUND / "producer/results.json").read_text())
    independent = json.loads((ROUND / "independent/matrices.json").read_text())
    imus = [F(value) for value in independent["source_response_examples"]["B_plus_L"]["mu_vector"]]
    pmus = [F(value) for value in producer["zero_Delta_B_plus_L_drive"]["mu_over_kappa"]]
    ordered = [imus[0], imus[1], imus[2], imus[3], imus[8], imus[13], imus[4], imus[9], imus[14], imus[15]]
    check("ten_sixteen_species_agreement", ordered == pmus
          and all(imus[g*5:g*5+5] == imus[:5] for g in (1, 2)))
    sensitivity = json.loads((ROUND / "independent/sensitivity_receipt.json").read_text())["values"]
    old_threshold = 16*math.sqrt(9.35462209607388)
    c_ideal = (72/79)/(2*math.pi**2*106.75/45)
    new_threshold = old_threshold*0.0195/c_ideal
    check("hand_old_eta_required_n49", abs(old_threshold/49 - 0.9987045454458) < 1e-13)
    check("hand_new_eta_required_n49", abs(new_threshold/49 - float(sensitivity["new_required_eta_at_n49"])) < 1e-14)
    check("hand_conditional_integer_change", math.ceil(old_threshold) == 49 and math.ceil(new_threshold) == 50)
    check("no_original_edits", original_hashes == {
        path.relative_to(ROUND).as_posix(): sha(path) for path in selected_files()
    })
    receipt = {
        "status": "PASS", "review_kind": "Post-portability current AI consistency and reproducibility review; not external peer review",
        "check_count": len(checks), "checks": checks, "reviewed_sha256": original_hashes,
        "review_script_sha256": sha(Path(__file__)),
        "blinding": "two methods independently implemented; producer implementation frozen before independent coefficient message, but producer first execution followed it; not fully blinded",
        "conditional_comparator_only": True,
        "portability_amendment": "Post-run software context/metadata changes only; original scientific controls and numerical values unchanged",
        "declared_analysis_dependencies": {"sympy": "1.14.0", "mpmath": "1.3.0"},
        "replay_dependency_versions": {name: version(name) for name in ("sympy", "mpmath")},
        "historical_source_path": SOURCE_RELATIVE.as_posix(), "historical_source_sha256": SOURCE_SHA256,
        "inventory_scope": list(INVENTORY_ALLOWLIST),
    }
    (HERE / "REVIEW_RECEIPT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "check_count": len(checks), "reviewed_file_count": len(original_hashes)}))


if __name__ == "__main__":
    main()
