#!/usr/bin/env python3
"""Reproduce the AM123 efficiency/energy frontier using the Python standard library.

No archive code is executed or extracted. Optional --source-zip verifies the exact
AM123 archive and reads its JSON summary. Otherwise frozen summary values are used.
Writes only the named CSV and Markdown outputs in --output-dir (default: script dir).
"""

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import zipfile


SOURCE_SHA256 = "2014b0a707f7dcb2272ab6c0b47cce6893501db08fe61daa9327e8f60179bc5d"
SOURCE_MEMBER = "v1.23_summary.json"
FROZEN = {
    "physical_source_height_GeV4": 620116096.5235525,
    "WE_A_required_over_A": 9.35462209607388,
    "WE_kinetic_over_radiation_n16": 0.5490473226780251,
    "WE_u_required_exact_KB": 0.5206657041971909,
}
N0, F_ALPHA, T_STAR, K_B, C_SPH, G_STAR = 16, 250.0, 131.7, 1.020689, 0.0195, 106.75
EFFICIENCIES = (1.0, 0.75, 0.5, 0.25)
STEM = "v1.23.1_efficiency_energy_frontier"


def check(condition, message):
    if not condition:
        raise ValueError(message)


def load_inputs(source_zip):
    if source_zip is None:
        return dict(FROZEN)
    data = source_zip.read_bytes()
    check(hashlib.sha256(data).hexdigest() == SOURCE_SHA256, "AM123 archive SHA-256 mismatch")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        values = json.loads(archive.read(SOURCE_MEMBER))
    check(all(values[key] == value for key, value in FROZEN.items()), "AM123 inputs differ from frozen values")
    return {key: values[key] for key in FROZEN}


def calculate(values):
    amplitude = values["physical_source_height_GeV4"]
    ratio_a = values["WE_A_required_over_A"]
    ratio_rad = values["WE_kinetic_over_radiation_n16"]
    rho_kin = amplitude * ratio_a
    rho_rad = rho_kin / ratio_rad

    # Independent numerical route from the parent script's stated frozen inputs.
    u_independent = K_B / (2.0 * math.pi * C_SPH * N0)
    rho_kin_independent = 0.5 * (2.0 * math.pi * F_ALPHA * T_STAR * u_independent) ** 2
    rho_rad_independent = math.pi**2 * G_STAR * T_STAR**4 / 30.0
    for actual, expected, name in (
        (u_independent, values["WE_u_required_exact_KB"], "phase speed"),
        (rho_kin_independent, rho_kin, "kinetic density"),
        (rho_rad_independent, rho_rad, "radiation density"),
    ):
        check(math.isclose(actual, expected, rel_tol=2e-14), "Independent check failed: " + name)

    thresholds = {
        "one_A": N0 * math.sqrt(ratio_a),
        "two_A": N0 * math.sqrt(ratio_a / 2.0),
        "strict_1pct_radiation": N0 * math.sqrt(ratio_rad / 0.01),
    }
    rows = []
    for eta in EFFICIENCIES:
        row = {"eta_relative_efficiency": eta}
        for name, budget in (("one_A", amplitude), ("two_A", 2.0 * amplitude), ("strict_1pct_radiation", 0.01 * rho_rad)):
            continuous = thresholds[name] / eta
            strict = name == "strict_1pct_radiation"
            n_min = math.floor(continuous) + 1 if strict else math.ceil(continuous)

            # Check the chosen integer and its predecessor using the energy formula,
            # independently of the threshold rounding operation.
            def passes(n):
                energy = rho_kin * (N0 / (n * eta)) ** 2
                return energy < budget if strict else energy <= budget

            check(passes(n_min), "Integer minimum does not pass: " + name)
            check(n_min == 1 or not passes(n_min - 1), "Predecessor unexpectedly passes: " + name)
            row["n_continuous_" + name] = format(continuous, ".15g")
            row["n_min_" + name] = n_min
            row["rho_kin_over_radiation_at_min_" + name] = format(ratio_rad * (N0 / (eta * n_min)) ** 2, ".15g")
        rows.append(row)
    return amplitude, rho_kin, rho_rad, thresholds, rows


def markdown(amplitude, rho_kin, rho_rad, thresholds, rows):
    table = "\n".join(
        f"| {r['eta_relative_efficiency']:g} | {r['n_min_one_A']} | {r['n_min_two_A']} | {r['n_min_strict_1pct_radiation']} |"
        for r in rows
    )
    return rf"""# AM v1.23.1 — efficiency and energy frontier

Date: 2026-09-05. This is a new algebraic extension of the frozen AM123 benchmark,
not a finite-temperature calculation or a solution of the proposed v1.24 dynamics.
It establishes conditional necessary energy bounds, not successful baryogenesis.

## Source and independent check

Source: `AM123_COMPLETE.zip`, SHA-256 `{SOURCE_SHA256}`;
member `{SOURCE_MEMBER}`. The source archive remains unchanged.
The stored values are A = `{amplitude:.16g}` GeV^4,
rho_kin(16)/A = `9.35462209607388`, and
rho_kin(16)/rho_rad = `0.5490473226780251`.
These imply rho_kin(16) = `{rho_kin:.16g}` GeV^4 and
rho_rad = `{rho_rad:.16g}` GeV^4.

The accompanying script also recalculates the densities independently from
F_alpha = 250 GeV, T_* = 131.7 GeV, K_B = 1.020689, c_sph = 0.0195,
g_* = 106.75, and n_0 = 16, using

\[
u_0=\frac{{K_B}}{{2\pi c_{{sph}}n_0}},\qquad
\rho_{{kin,16}}=\frac12(2\pi F_\alpha T_*u_0)^2,\qquad
\rho_{{rad}}=\frac{{\pi^2}}{{30}}g_*T_*^4.
\]

The two numerical routes agree within 2 x 10^-14 relative tolerance.
Every integer minimum below passes its stated inequality, while its predecessor fails.

## Derivation and conditional bounds

Keep the site-0 mapping, target yield, kinetic normalization, temperature,
and inherited linear yield law fixed. Define eta as the positive product of
phenomenological yield efficiencies **relative to the frozen benchmark**.
It is a sensitivity parameter, not a calculated transport efficiency.
For example, multiplying the benchmark dynamical efficiency and dilution factor
by a net eta, with the other factors fixed, gives

\[
u(n,\eta)=u_0\frac{{16}}{{n\eta}},\qquad
\rho_{{kin}}(n,\eta)=\rho_{{kin,16}}
\left(\frac{{16}}{{n\eta}}\right)^2.
\]

Consequently an available kinetic-energy density E_available > 0 requires

\[
\boxed{{n\eta\geq16\sqrt{{\rho_{{kin,16}}/E_{{available}}}}}}.
\]

The bound is conditional on the frozen linear relation remaining applicable.
Actual efficiencies may depend on the trajectory, winding, temperature, washout,
and spectator interactions. Those dependencies have not been solved.

| Budget or target | Bound on n eta |
|---|---:|
| Conservative one-A energy allowance, rho_kin <= A | >= {thresholds['one_A']:.12f} |
| Ideal full cosine drop, rho_kin <= 2A | >= {thresholds['two_A']:.12f} |
| Strict kinetic-to-radiation target, rho_kin/rho_rad < 0.01 | > {thresholds['strict_1pct_radiation']:.12f} |

The resulting minimum positive integers are:

| Relative efficiency eta | Minimum n: one A | Minimum n: full 2A | Minimum n: strict 1% radiation |
|---:|---:|---:|---:|
{table}

The last column is a **kinetic-energy fraction** target. It does not bound the
entire new-sector energy density. If kinetic energy were the only added component
at the same radiation density, rho_kin/rho_rad < 0.01 would give
H/H_rad < sqrt(1.01), a Hubble-rate increase below 0.499%. Potential energy,
the driver reservoir, or other species must also enter a complete Friedmann calculation.

## Why the assumptions matter

The parent describes A as the source height; more precisely A is the cosine
coefficient in V = A[1 - cos(theta)]. That potential has a full peak-to-trough
drop of 2A. The parent's one-A allowance is conservative, rather than a universal
maximum. The 2A column is an ideal maximum-drop allowance for that one fixed
cosine, requiring suitable initial conditions and neglecting Hubble friction,
other dissipation, and transfer to other degrees of freedom. It is not evidence
that an autonomous trajectory actually achieves that drop.

External driver work or initially stored kinetic energy can enlarge the budget;
losses reduce it. In that case replace E_available by the actual net energy
transferred to the rolling mode, and evolve the reservoir and its effects on
expansion. Adding driver energy does not by itself solve the separate 1% kinetic
target or establish a correct matter asymmetry. Thus the energy obstruction is
conditional on the stated budget, not a universal no-go for every possible driver.

The familiar n = 49 result requires eta >=
`{thresholds['one_A']/49:.13f}` for the one-A allowance.
The n = 119 result requires eta >
`{thresholds['strict_1pct_radiation']/119:.13f}` for the strict 1% kinetic target.
These benchmarks therefore have only about 0.130% and 0.373% relative-efficiency
loss margin, respectively. Larger integer windings in this table are arithmetic
requirements only: the necessary operator, charge, locality, and anomaly
construction has not been derived. Meeting a row is necessary under the model
assumptions, and is insufficient for a working cosmology.

## In More Basic Terms

If the mechanism produces matter less efficiently than assumed, the same target
needs faster field motion, and the energy cost rises as the square of that speed.
The earlier numbers 49 and 119 therefore rely on efficiency staying very close
to the benchmark. At half that efficiency, the corresponding requirements become
98 and 238. This calculation makes the energy accounting clearer; it does not
show that the proposed mechanism actually produces the observed matter excess.

## Reproduction

Run `python3 v1.23.1_efficiency_energy_frontier.py` to reproduce the Markdown and
CSV beside the script using the frozen inputs. Optionally add
`--source-zip /path/to/AM123_COMPLETE.zip` to verify the archive hash and read the
same values directly. Use `--output-dir /path/to/output` to choose a different
output directory. Only the Python standard library is required. The program
does not execute archived code or extract archive members to disk.
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-zip", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    results = calculate(load_inputs(args.source_zip))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / (STEM + ".csv")).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[-1][0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(results[-1])
    (args.output_dir / (STEM + ".md")).write_text(markdown(*results), encoding="utf-8")
    print("Verified source inputs, independent density calculation, and all integer minima.")
    print("Wrote " + str(args.output_dir / (STEM + ".csv")))
    print("Wrote " + str(args.output_dir / (STEM + ".md")))


if __name__ == "__main__":
    main()
