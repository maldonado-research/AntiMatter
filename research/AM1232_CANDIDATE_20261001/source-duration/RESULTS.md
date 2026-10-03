# Source-only duration bound and autonomous fixed-cosine trajectories

Date: October 1, 2026 Pacific (host date October 2 UTC). Candidate computation outside the public checkpoint.

The new result is a conditional **duration-dependent necessary energy bound**. Maintaining the frozen phenomenological speed threshold for 0.1 e-fold before T_* requires n eta >= 44.639769887 (n >= 45 at eta=1), strengthening the instantaneous n>=35 allowance. This is not a baryogenesis calculation.

## Model and canonical normalization

Use V=A[1-cos(theta)] and a_field=F_eff theta, with A=620116096.524 GeV^4 and F_eff=5.14727830237e+16 GeV = 3^30 * 250 GeV. The endpoint cosine is cos(a_field/F_eff). The conditional site-0 identification is theta_0=3^30 theta, tau_1=theta_0/(2 pi), so K=0.5(F_eff theta_dot)^2. The potential's full height is 2A.

Flat expanding homogeneous FRW contains separately conserved radiation and this scalar only. g_*=106.75 is constant, T=T_i exp[-(N-N_i)], rho_rad=pi^2 g_* T^4/30, and 3 Mbar_Pl^2 H^2=rho_rad+K+V with Mbar_Pl=2.435e18 GeV. The potential is fixed; there is no driver work or dissipation beyond expansion.

With p=F_eff theta_dot/sqrt(A), r=rho_rad/A, h=H/(sqrt(A)/F_eff), the dimensionless equations are theta'=p/h, p'=-3p-sin(theta)/h, r'=-4r and h^2=F_eff^2(r+p^2/2+1-cos(theta))/(3 Mbar_Pl^2). The integrated ledgers are L_phi'=3p^2 and L_rad'=4r. The scalar ledger measures cosmological dilution by expansion, not energy deposited into radiation.

## Analytic duration bound

The inherited linear relation supplies u=|dot(tau_1)|/T, with rho_kin(16,1)=5800951738.67 GeV^4. Keeping the required u fixed at given n and relative efficiency eta implies K_req(N)=K_req,* exp[-2(N-N_*)], where K_req,*=rho_kin(16,1)[16/(n eta)]^2. This pointwise threshold is an additional imposed requirement. An integrated baryon yield need not require this profile.

For any qualifying interval [N_*-Delta N,N_*], scalar conservation gives E_start=E_end+6 integral K dN. If it began from rest in the same fixed source at or before this interval, E_start<=2A. Since V>=0 and K>=K_req pointwise,

    2A >= E_start >= K_req,* + 6 integral_{-Delta N}^0 K_req,* exp(-2x) dx
       = K_req,* [3 exp(2 Delta N)-2]

    n eta >= 16 sqrt{rho_kin(16,1)/(2A) [3 exp(2 Delta N)-2]}.

| Delta N ending at T_* | Interval start T (GeV) | Required n eta | Minimum n at eta=1 |
|---:|---:|---:|---:|
| 0.00 | 131.700000 | 34.603347068 | 35 |
| 0.01 | 133.023607 | 35.636475339 | 36 |
| 0.10 | 145.551010 | 44.639769887 | 45 |
| 0.50 | 217.136591 | 85.847308972 | 86 |
| 1.00 | 357.997717 | 155.396262777 | 156 |

At Delta N=0 this recovers the public full-drop value 34.603347068 and integer 35. A positive threshold cannot hold at the release instant when the field is at rest; a qualifying interval must start later. Equality in this optimistic budget is not guaranteed attainable. A hilltop initially exactly at rest remains at rest. Initial potential below 2A, prior Hubble losses, residual potential, and additional dissipation strengthen the bound; initial kinetic energy or external work changes the budget.

This formula applies only to intervals ending at T_*. For an interval extending from N_*-a to N_*+b, the analogous necessary budget is K_req,*[3 exp(2a)-2 exp(-2b)]<=E_cap. Substituting its total width a+b into the endpoint table is unjustified. For a known smaller energy cap one may replace 2A by E_cap. Eta is a relative yield-law parameter, not an energy-conversion fraction.

## Registered trajectory sample

DOP853 integrates the fixed 10 phases at T_i=200,500,2000 GeV, initially at rest, to T_*=131.7 GeV, twice at (rtol,atol)=(1e-9,1e-11) and (1e-11,1e-13), max_step=0.02. Each dense solution is checked at 1001 fixed points. The grid was registered before integration and was not refined. The CSV reports all 30 cases; the table gives the largest endpoint K among the 10 registered phases for each T_i.

| T_i (GeV) | Sampled theta_i | K_* (GeV^4) | V_* (GeV^4) | rho_phi/rho_rad | Conditional n eta |
|---:|---:|---:|---:|---:|---:|
| 200 | 2.000000000 | 299876029 | 12700623.5 | 0.0295846926 | 70.371811944 |
| 500 | 3.000000000 | 199580970 | 77191009.4 | 0.026195859 | 86.260117385 |
| 2000 | 3.000000000 | 111167531 | 135771123 | 0.0233722005 | 115.579451516 |

The largest sampled endpoint K is 299876028.681 GeV^4 (0.483580462 A), at T_i=200 GeV and theta_i=2.000000000. Its conditional final-instant requirement is n eta >= 70.371811944. This is a sampled endpoint value, not an optimized trajectory or an integrated yield. Increasing n or changing eta only changes that inferred threshold in this computation; it does not reduce the actual scalar energy of an already fixed trajectory.

For that sampled case, the scalar ledger (GeV^4) is E_initial = 878175448.384, E_final = 312576652.196, integrated 6K dN = 565598796.185, residual = -0.00255766. Its total scalar/radiation ratio is 0.0295846926, while its kinetic/radiation ratio is 0.0283826065; both components enter Friedmann.

## Verification

All registered checks: **PASS**. The worst tight-run scalar-ledger error is 4.26e-11 A (worst relative to initial scalar energy 2.92e-10). Radiation is checked separately: worst analytic-scaling relative error 3.11e-15 and ledger relative error 1.54e-15. Maximum endpoint difference across the two tolerances, using theta,p and K/A,V/A natural scales, is 4e-10. Sampled K and V are nonnegative, radiation and H^2 are positive, and no sampled scalar energy exceeds its initial value beyond the stated tolerance.

The small-angle control uses the exact prescribed-radiation solution theta=z^(-1/4)[C_J J_(1/4)(z)+C_Y Y_(1/4)(z)], z=mt=m/(2H_rad), with theta_i=1e-5 and zero initial velocity. The constants are fixed at T_i=2000 GeV. This independently checks the linear damping normalization; full nonlinear small-angle evolution approaches it because scalar backreaction and anharmonicity vanish with amplitude.

| Control | Max phase error / theta_i | Max p error / theta_i |
|---|---:|---:|
| linear_radiation_Bessel | 2.72e-11 | 6.76e-11 |
| full_small_angle_Bessel | 2.48e-11 | 6.57e-11 |

Bottom and exact hilltop controls remain exactly at rest. For these declared mathematical stationary points, the RHS returns zero force when theta is exactly 0 or +/-pi and p=0; floating-point sin(pi) is not treated as a physical seed. Reflection theta_i -> -theta_i reverses the velocity and preserves scalar energy. Thus selecting a rolling sign here does not derive a physical CP-odd bias.

## Limits and provenance

This source-only model omits the analytic finite-temperature potential, autonomous driver/reservoir, CP-odd invariant, sphaleron/washout/spectator transport, and odd-relic evolution requested by the public next-step program. It is not the full Wilson or inherited scalar model. The public misalignment estimate uses relaxed curvature 0.918434 A; this explicit single-cosine diagnostic instead uses A/F_eff^2 and stops at T_*. It makes no new late-time relic prediction. Pair production is not a matter-antimatter asymmetry. No physical asymmetry success, operator construction, or scientific novelty is claimed.

Public source anchors (SHA-256 values are in results.json):
- [v1.23_summary.json](https://github.com/maldonado-research/AntiMatter/blob/main/research/AM1231/v1.23/v1.23_summary.json)
- [v1.23_source_normalization.csv](https://github.com/maldonado-research/AntiMatter/blob/main/research/AM1231/v1.23/v1.23_source_normalization.csv)
- [v1.23_misalignment.csv](https://github.com/maldonado-research/AntiMatter/blob/main/research/AM1231/v1.23/v1.23_misalignment.csv)
- [v1.23_wilson_instanton_cosmology_audit_note.md](https://github.com/maldonado-research/AntiMatter/blob/main/research/AM1231/v1.23/v1.23_wilson_instanton_cosmology_audit_note.md)
- [v1.23_wilson_instanton_cosmology_audit.py](https://github.com/maldonado-research/AntiMatter/blob/main/research/AM1231/v1.23/v1.23_wilson_instanton_cosmology_audit.py)
- [v1.23.1_efficiency_energy_frontier.md](https://github.com/maldonado-research/AntiMatter/blob/main/research/AM1231/v1.23.1/v1.23.1_efficiency_energy_frontier.md)
- [v1.23.1_efficiency_energy_frontier.py](https://github.com/maldonado-research/AntiMatter/blob/main/research/AM1231/v1.23.1/v1.23.1_efficiency_energy_frontier.py)

The public source files were hashed before and after the run and remained unchanged. Only candidate outputs outside the checkout were written. The exact benchmark densities were independently recomputed from F_alpha,T_*,K_B,c_sph,g_* and agree with the published ratios within 2e-14 relative tolerance. Duration factors also agree with independent numerical quadrature, and every reported integer passes while its predecessor fails.

Reproduce using existing dependencies:

```bash
cd /workspace/research-progress/antimatter/source-duration
/workspace/AntiMatter/.venv/bin/python audit.py
# Independent output folder:
/workspace/AntiMatter/.venv/bin/python audit.py --output-dir /tmp/antimatter-source-duration-replay
```

Software: Python 3.12.14, NumPy 2.5.2, SciPy 1.17.1. See [REGISTRATION.md](REGISTRATION.md), [audit.py](audit.py), [results.json](results.json), [trajectories.csv](trajectories.csv), and [duration_bounds.csv](duration_bounds.csv).

Implementation correction before the final rerun: the exact stationary control explicitly returns zero force, removing the artificial sin(pi) floating-point seed. The first run had already passed its registered tolerance; no scan phase, physical parameter, target, tolerance, or threshold was changed. This correction implements the registered exact-rest control rather than treating numerical roundoff as dynamics.
