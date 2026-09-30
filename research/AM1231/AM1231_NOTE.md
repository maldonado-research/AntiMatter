# AntiMatter: Wilson-Line and Cosmology Audit
## v1.23.1 - Efficiency-dependent energy bounds and reproducibility release

Ricardo Maldonado | September 5, 2026

**Research status:** theoretical research checkpoint. This release does not derive the observed matter-antimatter asymmetry or establish a unified theory. Its results are conditional calculations and consistency tests, not observations of new physics.

## In More Basic Terms

The question is why the Universe contains so much more matter than antimatter. This research explores whether a chain of interacting fields could help create that imbalance in the early Universe.

The latest audit finds that one proposed mathematical route cannot work as written: the source needed to drive the mechanism does not satisfy that model's gauge-symmetry requirements. A different construction, using fields around an extra spatial dimension, can reproduce the desired long variation scale under specific assumptions. It still needs a complete connection to the particles and interactions that would create the matter excess.

The energy accounting is also demanding. At the original benchmark, the required motion costs more energy than the proposed source budget supplies. Making the mechanism less efficient increases that cost. Even if the mechanism were driven successfully, the model must explain how it avoids leaving too many stable particles, too much field energy, or persistent boundaries between different vacuum states.

The progress is a clearer map of what fails, what remains possible, and what must be calculated next. This release adds a quantitative efficiency test and makes the earlier calculations easier to inspect and reproduce. It does not claim that the matter-antimatter problem has been solved.

## What this version adds

The computational base is the author's AM123 / v1.23 archive dated August 17, 2026. Version 1.23.1 adds an analytic efficiency-dependent energy bound, distinguishes a one-height source budget from a full cosine drop, clarifies period and expansion terminology, records fresh reproduction checks, and supplies the missing v1.22 provenance dependency.

The original v1.23 files are preserved. Their historical "publication HOLD" wording remains part of the archived record. This release makes the audit available as a research checkpoint; it does not assert that any unresolved scientific gate has been passed. The proposed v1.24 finite-temperature and autonomous-driver programme has not been completed here.

## What the inherited audit establishes

### 1. A restricted compact-character obstruction

For the specified compact gauged scalar model, an integer electric character with charges k_j must satisfy k_j - 3 k_(j+1) = 0. The primitive solution is (3^30, 3^29, ..., 1). Along the inherited zero-mode direction, the allowed primitive invariant has scale F_inv = 1.079319055471e-12 GeV, while the desired endpoint scale is F_end = 5.147278302366e16 GeV. Their ratio is 4.7690053e28.

Calling an electric operator nonlocal does not remove that charge constraint. This result is restricted to the stated fields, transformations and integer charge lattice. Additional boundary fields, phases or topological structure change the model and require a new audit. It is not a theorem excluding all clockwork or Wilson-line models.

**Period convention:** in a cosine cos(a/F), F is a decay constant or period scale; the complete field repeat interval is 2*pi*F. The archived notes sometimes call F the "period." Both quoted scales use the same convention, so the obstruction ratio is unchanged.

### 2. A conditional Wilson-line replacement

A separate model with 31 compact holonomies yields the desired scale with inverse radius R^-1 = 1773.308 GeV and four-dimensional coupling g4 = 1.1974. The endpoint higher-harmonic force fraction is 0.26717% at the benchmark.

The often-quoted 0.88784% combines that result with 0.62067% inherited scalar stress as a continuity design budget. The scalar contribution has not been derived in the Wilson model. The combined number therefore does not establish a complete Wilson-model contamination bound. The replacement also has not inherited the scalar model's 17+0 messenger construction or anomaly repair. Its kinetic matrix, radion stabilization, thermal history and driving mechanism remain incomplete.

### 3. Source normalization and cosmology limits

The physical coefficient of the endpoint cosine is A = 6.201160965236e8 GeV^4. The much smaller A/3^30 = 3.011864038119e-6 GeV^4 is a projected force normalization, not the available potential-energy density.

In the inherited/global branch, the persistent-source harmonic misalignment estimate is Omega_a*h^2 = 4.5727478e7*theta_i^2. Under that calculation's assumptions, avoiding excess dark matter requires |theta_i| <= 5.1227e-5 or a mechanism such as tracking, shutdown, decay or dilution. Domain-wall estimates and a stable odd-particle relic diagnostic expose further unresolved constraints. These are branch- and thermal-history-dependent estimates, not measured exclusions of a completed model.

## New calculation: the efficiency-dependent energy frontier

Let n be the positive integer determinant winding and let 0 < eta <= 1 multiply the baryon-yield response relative to the inherited unit-efficiency benchmark. Here eta denotes a new response factor; it is not the unrelated parameter named ETA inside the original audit script. At fixed target yield and with the same assumed linear response, the required site-0 velocity scales as 16/(n*eta). Thus its kinetic energy scales as:

rho_kin(n, eta) = rho_kin(16, 1) * [16/(n*eta)]^2.

Using the archived ratios rho_kin(16,1)/A = 9.354622096074 and rho_kin(16,1)/rho_rad = 0.549047322678 gives:

- Available kinetic budget A: n*eta >= 48.93652273.
- Ideal full cosine drop 2A: n*eta >= 34.60334707.
- Kinetic-to-radiation target rho_kin/rho_rad < 0.01: n*eta > 118.55636407.

| Response efficiency eta | Minimum n for budget A | Minimum n for ideal 2A | Minimum n for kinetic fraction <1% |
| --- | ---: | ---: | ---: |
| 1.00 | 49 | 35 | 119 |
| 0.75 | 66 | 47 | 159 |
| 0.50 | 98 | 70 | 238 |
| 0.25 | 196 | 139 | 475 |

The n=49 one-height benchmark needs eta >= 0.9987045454. The n=119 kinetic-fraction benchmark needs eta > 0.9962719669. Their margin for inefficiency is therefore very small. A successful operator realization of these windings has not been supplied.

### Energy accounting and scope

For V = A[1 - cos(theta)], the maximum-to-minimum drop is 2A. The earlier one-A budget is a deliberately conservative benchmark, not a universal maximum. At n=16, the required kinetic energy is 4.677311 times the full 2A drop, before losses. The 2A column is a favorable kinematic envelope and does not prove that cosmological dynamics can realize it.

More generally, if E_avail is a positive net kinetic-energy budget, the necessary bound is n*eta >= 16*sqrt[rho_kin(16,1)/E_avail]. For a trajectory with negligible initial kinetic energy, E_avail is limited by the potential drop plus work supplied by an autonomous driver minus friction and transfer losses. Initial kinetic energy, if present, is another term that must be accounted for. Arbitrary external work is not a free solution: the driver's energy, origin, dissipation and cosmological effect must be evolved.

The 1% condition above bounds kinetic energy relative to radiation. If kinetic energy were the only extra contribution at fixed radiation density, Friedmann's equation gives H/H_rad = sqrt(1 + rho_kin/rho_rad), so 1% kinetic energy raises H by about 0.499%. Other potential, driver or relic energy can change H further. This table is not a full expansion-history calculation.

These are necessary bounds within the frozen phenomenological ansatz. The table neither predicts eta nor justifies extrapolating the linear response to arbitrary velocity or large n. It does not demonstrate CP violation, compute transport or washout, or produce the observed baryon abundance.

## What would constitute further scientific progress

1. Specify an analytic radial-plus-phase finite-temperature potential so symmetry restoration and vacuum selection can be calculated.
2. Derive an autonomous site-0 driving pulse, including its energy reservoir, a physical CP-odd invariant and shutdown or energy-transfer mechanism.
3. Evolve the phase and driver together with Friedmann expansion, sphalerons, washout, spectator effects and odd-particle abundances. Compute the sign and magnitude of the final baryon yield.
4. Test the Wilson replacement's messenger and anomaly structure, kinetic mixing and stabilization in that replacement's own field content.

The outputs should include controlled initial conditions, an energy ledger, error and parameter sensitivity, and simultaneous relic and domain-wall consistency. For the wall calculation, specify whether the discrete symmetry is global or gauged and identify physically distinct vacua before importing a stable-wall network model. Counting minima alone does not settle the defect topology. Failure of those tests is informative and should be recorded.

## Reproducibility and attribution

The accompanying package preserves the original v1.23 technical note, calculation script, tables and figures. The exact v1.22 parent archive is supplied as a provenance dependency. REPRODUCIBILITY.md describes the fresh checks performed for this release and their limits; the machine-readable comparison report records differences. SHA256SUMS.txt checks the new bundle contents.

The fresh v1.23 replay matches all 21 scientific CSV tables and the summary JSON byte for byte, as well as the three Markdown documents and original generator. Four rendered PNG images and their two associated checksum manifests differ; no unexpected differences were found. The original and parent archives each pass all 31 internal checksum entries. The parent calculations themselves were not rerun.

The additional energy-frontier script uses Python's standard library, verifies its input summary against frozen benchmark constants, and writes the new CSV table. Reproducing arithmetic is different from validating the physical model or independently reproducing every calculation in v1.22.

Prepared with AI assistance for source review, calculations, consistency checks and exposition. No independent peer review or experimental verification is claimed.

## Selected primary context

The new frontier follows algebraically from the supplied AM123 benchmark, not from a new measurement. The following papers provide context for the underlying research topics; their existence does not validate this proposed model.

1. N. Arkani-Hamed et al., Extranatural Inflation: https://arxiv.org/abs/hep-th/0301218
2. G. F. Giudice and M. McCullough, A Clockwork Theory: https://arxiv.org/abs/1610.07962
3. M. D'Onofrio, K. Rummukainen and A. Tranberg, Sphaleron Rate in the Minimal Standard Model: https://arxiv.org/abs/1404.3565
4. T. Hiramatsu et al., Axion cosmology with long-lived domain walls: https://arxiv.org/abs/1207.3166
5. Planck Collaboration, Planck 2018 results. VI. Cosmological parameters: https://arxiv.org/abs/1807.06209

The original v1.23 source list is retained with the archive for fuller context.
