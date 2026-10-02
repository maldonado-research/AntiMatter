# Registered source-only duration and trajectory audit

Registered before calculation on October 1, 2026 Pacific (host date October 2 UTC).
Candidate work lives outside the immutable public `/workspace/AntiMatter` checkout.
The registration is preserved verbatim; implementation corrections, if required,
will be listed in RESULTS.md. This is a bounded new diagnostic, not a claim of
successful baryogenesis or scientific novelty.

## Frozen inputs and scope

Read only the public v1.23 summary JSON, source-normalization CSV, misalignment CSV,
audit note, and v1.23.1 efficiency-energy frontier. Use the exact published
`physical_source_height_GeV4`, `desired_endpoint_period_GeV`, and `q_to_N` values.
Use F_alpha = 250 GeV, g_* = 106.75, T_* = 131.7 GeV, reduced Planck mass
2.435e18 GeV, K_B = 1.020689, c_sph = 0.0195, n_0 = 16.
Recompute the reference kinetic density from the site-0 mapping and check it
against the published density ratios before integration.

The model is exactly one fixed potential V = A(1-cos(theta)), canonical field
a_field = F_eff theta, F_eff = 3^30 * 250 GeV. In particular 250 GeV is NOT the
period inside this endpoint cosine. Homogeneous flat expanding FRW contains
only this field and separately conserved radiation; there is no forcing,
energy transfer, finite-temperature correction, or dissipation beyond Hubble
friction. Radiation has fixed g_* and T proportional to scale factor^(-1).
This is not the full Wilson construction, finite-temperature model, or driver.
The public misalignment estimate uses relaxed curvature 0.918434 A; the present
explicit single cosine uses curvature A/F_eff^2 and does not reproduce that
late-time relic calculation.

## Independent analytic question

For an interval of length Delta N ending at T_*, assume the phenomenological
threshold |dot(tau_1)|/T is constant, with theta_0=3^30 theta and
tau_1=theta_0/(2 pi). It then means
K(N) >= K_req,* exp[-2(N-N_*)] throughout the interval, where
K_req,* = rho_kin(16,1) [16/(n eta)]^2.
The field initially rests at or before the interval, so E_initial <= 2A.
Use E'=-6K, V>=0, and E_final>=K_req,* to check the necessary inequality
K_req,* [3 exp(2 Delta N)-2] <= 2A. Evaluate Delta N in
{0, 0.01, 0.1, 0.5, 1}, including positive integer minima at eta=1 and a
comparison to the public instantaneous 35 bound. A positive threshold cannot
hold at the exact instant of release from rest; a nonzero-duration application
must begin after release. The assumption is an imposed speed threshold, not a
derived integrated baryon yield or a necessary condition for every possible
time-dependent baryogenesis history.

## Fixed numerical experiment

Initial p=F_eff theta_dot/sqrt(A)=0. Initial phases, in radians, are exactly
{0.0001, 0.01, 0.1, 0.5, 1, 1.5, 2, 2.5, 3, pi-0.01}; initial temperatures are
{200,500,2000} GeV. No tuning or adaptive scan refinement. Integrate all 30
cases to T_* twice using scipy solve_ivp DOP853, rtol 1e-9 / atol 1e-11 and
rtol 1e-11 / atol 1e-13, max_step 0.02 in N. Existing dependencies only.

Let x=N-N_i, r=rho_rad/A, v=V/A=2 sin(theta/2)^2,
h=H/(sqrt(A)/F_eff). Evolve

    h^2 = F_eff^2/(3 Mbar_Pl^2) [r + p^2/2 + v]
    theta' = p/h
    p' = -3p - sin(theta)/h
    L_phi' = 3p^2, r' = -4r, L_rad' = 4r.

Check E_phi/A + L_phi = initial E_phi/A and r + L_rad = r_initial
separately; compare r to r_initial exp(-4x) independently. Sample 1001 equally
spaced dense-output points for extrema and ledger checks. Verify radiation
positivity, V and K nonnegativity, E_phi <= E_initial <=2A, and H^2>0.
Require max absolute scalar-ledger error below 1e-7 A (also report relative
to initial energy), radiation analytic relative error below 1e-8, and
two-tolerance endpoint state and energy agreement below 1e-7 when normalized
to natural scales (theta and p in radians/dimensionless, K,V in A).

Controls: exact bottom and hilltop initially at rest; reflection theta->-theta
for a representative theta_i=1.5, T_i=500; and a small-angle theta_i=1e-5,
T_i=2000 control against the exact Bessel solution of the linear oscillator
in a prescribed radiation-only background. Run the linear numerical control
and the full nonlinear small-angle control; report normalized errors and
require each below 3e-7. These controls calibrate normalization/damping and
do not validate missing microphysics.

Report endpoint K, V, rho_phi/rho_rad, signed velocity and site-0 u,
canonical initial/final/dissipated energy ledger, and conditional n eta
needed to match the frozen final-instant target. The grid maximum is only
the largest sampled endpoint energy, never a global optimum. Do not identify
particle pair production with an asymmetry, and do not identify an initial
rolling sign with a physically derived CP-odd bias.

## Outputs and provenance

Save audit.py, results.json, trajectories.csv, duration_bounds.csv and
RESULTS.md. Save input hashes and exact software versions. Reproduce with
`/workspace/AntiMatter/.venv/bin/python audit.py` from this directory. Public
sources remain untouched. No new web or private-source claims enter this work.
