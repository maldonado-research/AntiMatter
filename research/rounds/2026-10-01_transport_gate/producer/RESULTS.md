# Transport comparator result

The registered diagnostic passes nine control tests and an internal,
separate-algorithm ordinary-coordinate RK4 cross-check. It separates four
requirements that the current candidate does
not yet supply: a physical source vector, the active reaction/charge structure,
its susceptibility-weighted relaxation rates, and a signed source-to-freeze-out
history. This is a reusable comparator and identifiability result, not a completed
AntiMatter transport calculation or novel mathematical discovery.

The mathematical derivation is in `DERIVATION.md`; preselected assumptions and
tolerances are in `REGISTRATION.md`. `AMENDMENTS.md` records the reviewer's
qualification about inactive reaction channels. Original registration unchanged.

## Illustrative outputs

Three species A, B, C convert around a cycle; total A+B+C is conserved.
`C=diag(1,2,3)` and source amplitude 0.01 are dimensionless. The label A has
no identification with baryon number. Outputs x are densities divided by T^3,
not entropy-normalized yields.

| Control | Output | Meaning |
|---|---|---|
| Compatible source `.01 S^T(1,0,0)` | stationary x=(0.00833333,-0.00333333,-0.005) | Susceptibility and conserved-charge projection replace an arbitrary conversion factor. Positive rates (1,1,1) and (1,2,4) give the same stationary state. |
| Species source in the conserved direction (1,1,1) | no induced x | A derivative-current source along a truly conserved direction has no bias in these reactions. Adding this direction to a source is invisible. |
| Cycle source b=(0.01,0.01,0.01), equal rates | x=0, progress=(0.01,0.01,0.01) | Incompatible biases can circulate without changing densities; zero density is not detailed balance. |
| Same cycle source, rates (1,2,4) | stationary x=(0.00523810,-0.00380952,-0.00142857), progress=(0.01714286,0.01714286,0.01714286) | Externally driven stationary densities depend on the actual rates. |
| Compatible +bias for one unit, -bias for one unit | x_A(2)=-0.006857817217618563 | Zero integrated signed bias leaves a nonzero density because early and late production are weighted differently. |
| All signs reversed | all x reverse signs | This checks signed response; it supplies no cosmological sign-selection mechanism. |
| Reactions shut off at tau=2 | x(22)=x(2) | The instantaneous conserved space enlarges; the residual freezes in this comparator. |
| Reactions remain active without bias for 20 more units | norm(x(22))=2.3826630547752883e-14 | Nonconserved density washes out. |

Positive relaxation eigenvalues are approximately 1.2324081 and 2.4342585.
Maximum sampled `|mu_i|/T` on the two-segment signed trajectory is
0.007554369824542495; this is a smallness check for these illustrative inputs.
Conserved total-charge drift stays at floating-point roundoff. The non-diagonal
SPD susceptibility control also preserves its null space and monotonically
decreases the source-free quadratic free energy.

Internal RK4 errors relative to exact symmetric spectral propagation are
1.1566520542148456e-9, 7.003277837201252e-11 and 4.3081965686770655e-12 for
32, 64 and 128 steps per segment. The convergence and final error pass the
registered 2e-10 bound. Invalid susceptibility and negative reaction rates are
rejected. Nine tests executed, nine passed; none skipped. A separate AI agent
supplied an independent chemical-potential-coordinate matrix-exponential
implementation and review, maintained in the sibling `independent/` directory.
This is an independent computational check, not external peer review.

## Candidate identifiability remains open

The supplied frozen relation
`Y_B=c_sph kappa_dyn (2 pi n_det dot(tau_1)/T) D_d` cannot uniquely determine
this response. The same source amplitude or oscillation duration can produce
zero density, a nonzero signed residual, or complete washout depending on its
species projection, reaction rates and shutdown. Source-equivalent shifts along
conserved charges also demonstrate why a texture exponent alone cannot identify
the species source. These are algebraic/nonuniqueness examples, not exclusions of
the candidate or observations about its unconstructed microscopic sector.

The next physical gate requires an action-derived, rephasing-invariant source;
actual species/stoichiometry/anomalies; susceptibility with gauge and spectator
constraints; normalized thermal reaction coefficients; initial conserved charges;
coupled source/bath energy, expansion and entropy histories; and a physical
freeze-out prescription. Only after these are supplied should the network compute
`b_phys^T Y(t_f)` and compare its abundance and validity conditions with data.
No efficiency, actual sphaleron yield, observed asymmetry, driver work reservoir,
Standard Model temperature fit or new microscopic operator has been invented.

## Reproduce

The original producer run used Python 3.12.14 and NumPy 2.3.5; no new dependency
was installed for that run. The parent's reusable environment pins NumPy 2.5.2.
Those environment versions must be reported separately; this producer receipt
records the original run, and does not itself assert a pinned-environment rerun.
After copying or entering the complete round directory, run the producer with:

```sh
cd producer
python -m unittest -v test_transport
python run_round.py
```

`results.json` records protocol, registration receipt, environment and outputs;
`signed_trajectory.csv` records 201 sample states. The rerun regenerates only
these local outputs and records a new run timestamp. Protected baseline inputs
and repository files are unchanged by this round. No publication was performed.

The comparator is anchored to baseline commit
`fadef6b67064eda06b3528a7a73ef959c205d8a2` and the separate prior candidate
`research/AM1232_CANDIDATE_20261001/`; it does not supersede that candidate or
recalibrate its preserved inputs. No private material or microscopic candidate
operator values were assumed.
