# Independent computational review of the source-duration diagnostic

October 1, 2026 Pacific (host date October 2 UTC).

**Verdict: the duration derivation and all 30 registered endpoint trajectories
pass this independent implementation check after the stationary-hilltop correction.**
This is an internal computational review, not external peer review, experimental
validation, or a completed baryogenesis calculation.

Reviewed producer result SHA-256:
`4d72bb8f6a5edd92a9543f904fefaa1935036bf5fbfdc12582e713b6264ce9f1`.
The producer files were read, not edited. Public checkpoint files were not modified.
The final reviewed script and registration identities are in
[comparison_results.json](comparison_results.json).

## Independent derivation

With canonical field alpha=F_eff theta, the correct endpoint scale is
F_eff=3^30*250 GeV, not 250 GeV. For V=A(1-cos theta), K=F_eff^2 theta_dot^2/2,
and an expanding homogeneous universe with no driver or energy exchange,

    d(K+V)/dN = -6K.

The site-0 mapping u=3^30 theta_dot/(2 pi T) therefore gives the frozen threshold
K_req,*=rho_kin,16 [16/(n eta)]^2. Extending constant required |u| away from T_*
is an explicitly stipulated diagnostic, not a result derived in the published
frozen-instant frontier. Separately conserved radiation and fixed degrees of
freedom imply T proportional to exp(-N), hence K_req(N) proportional to exp(-2N).

For a contiguous qualifying interval ending at N_*,

    E_start = E_end + 6 integral K dN
            >= K_req,* + 6 integral_{-Delta_N}^0 K_req,* exp(-2x) dx
            = K_req,* [3 exp(2 Delta_N)-2].

Initial rest in this nonnegative fixed cosine implies E_start<=E_initial<=2A.
This proves the producer's necessary duration bound. Direct 60-digit decimal
arithmetic reproduces minimum integers 35,36,45,86,156 for Delta_N
0,0.01,0.1,0.5,1 at eta=1; each predecessor fails. Maximum difference from the
producer's floating-point bounds is 2.85e-14 in n eta.

This result bounds an interval ending at T_*. For an interval extending from
N_*-a to N_*+b, the correct energy requirement is
K_req,*[3 exp(2a)-2 exp(-2b)]<=E_cap. The producer now states this distinction.
Disconnected intervals cannot be added together. A positive threshold cannot
hold at the release instant; the qualifying interval begins later.

For context, n=35 and eta=1 permit at most Delta_N=0.00382815679538 in this
optimistic 2A accounting; that is a necessary ceiling, not an attained duration.
The bound permits replacing 2A with a justified smaller energy cap.

## Independent proper-time calculation

[independent_time_check.py](independent_time_check.py) imports no producer code.
It uses x=m(t-t_i), m=sqrt(A)/F_eff, q=dtheta/dx, R=rho_rad/A, and tracks the
scale factor and scalar energy loss as separate variables:

    h = F_eff sqrt(R+q^2/2+2 sin(theta/2)^2)/(sqrt(3) Mbar_Pl)
    dtheta/dx = q
    dq/dx = -3h q - sin(theta)
    dR/dx = -4hR
    dL/dx = 3h q^2
    dN/dx = h.

Integration stops at the independently evolved radiation temperature T_*.
This checks the producer's use of N as time, all factors of h, total scalar
energy in Friedmann, the site-0 velocity, and radiation cooling. It uses
Python 3.12.14, NumPy 2.3.5 and SciPy 1.17.0, separately from the producer's
NumPy 2.5.2 and SciPy 1.17.1 environment. Independent tolerances are
(2e-11,2e-13), refined to (2e-12,2e-14), with maximum step 0.03 in x.

All 30 registered initial conditions were rerun; no trajectory grid was tuned.
Maximum differences between implementations are:

| Quantity | Maximum absolute difference |
|---|---:|
| theta_* | 4.28e-12 |
| p_*=theta_dot/m | 3.13e-12 |
| K_*/A | 2.55e-12 |
| V_*/A | 4.25e-12 |
| signed u_* | 3.77e-13 |
| total scalar/radiation | 3.45e-13 |
| H_*/H_rad,* | 1.68e-13 |

The relative difference in inferred n eta is at most 4.64e-11. The independent
energy identity E/A+L=E_initial/A has maximum residual 2.86e-14; changing the
independent tolerances changes K_*/A by at most 1.28e-13. The maximum radiation
identity residual |ln(R/R_i)+4N| is 9.08e-12.

The largest registered endpoint K occurs at theta_i=2, T_i=200 GeV:
K_*/A=0.483580462373294, total scalar/radiation=0.02958469260771,
and inferred n eta=70.3718119433847. This is a maximum over the specified sample,
not a global optimum. Its positive endpoint velocity follows prior oscillatory
motion from positive initial displacement; it is not an independently selected
CP sign. Signed velocity and energy agree between implementations.

## Correction and interpretation checks

The first producer implementation used floating-point sin(pi) in the exact
hilltop control. The final implementation recognizes the declared stationary
equilibrium and sets its force to zero. The final minimum/hilltop controls have
exactly zero phase departure and momentum, and the registered pi-0.01 scan
point is unchanged. This correction is recorded in the producer's report.

The producer's prescribed-radiation Bessel solution has the correct order 1/4,
power z^(-1/4), z=mt, and initial derivative matching. Its reflection control
reverses momentum and preserves energy. The independent solver also treats
mathematical hilltop rest as an exact equilibrium.

Eta remains a phenomenological response multiplier, not an energy-conversion
fraction. n and eta change the diagnostic speed threshold; they do not reduce
the energy of any already fixed numerical trajectory. Crossing a threshold is
an availability diagnostic, not a solution of the required yield equality or
an integrated asymmetry. Hubble loss is cosmological dilution, not radiation
heating. The total scalar energy, including V, enters Friedmann; a kinetic-only
fraction is not a complete expansion bound. The finite-temperature potential,
autonomous driver, CP bias, washout, spectator, and relic problems remain open.

## Reproduce this cross-check

Run in this independent directory using a Python environment with NumPy and SciPy:

```bash
python independent_time_check.py --registered-grid
python independent_duration_check.py
python compare_outputs.py
```

The first two commands independently regenerate the proper-time endpoints and
high-precision bounds. The last reads the finalized producer outputs and
records their digests and numerical differences. Additional initial-condition
and stationary controls from a separate 16-case check are retained in
[proper_time_results.json](proper_time_results.json); they were not used to
change the registered producer grid or choose its best result.
