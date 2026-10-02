# AntiMatter v1.23.1: research status and next tests

This is a guide to the published checkpoint, not a new result or a claim that the remaining work is complete. The detailed source notes and data are authoritative for each calculation's assumptions.

## What remains open

1. **Construct the physical source and couplings.** The rejected compact gauged-scalar construction and the conditional Wilson-line alternative must be kept distinct. The alternative needs a complete particle and interaction model, including charge assignments and anomaly cancellation.
2. **Calculate the driving and response.** The efficiency parameter in v1.23.1 is a sensitivity input. Its value has not been derived from a constructed operator and a solved thermal history.
3. **Close the full energy budget.** The physical source amplitude and its projected force are different quantities. The complete cosine potential can release at most twice its amplitude. Source, kinetic, thermal, and other energy contributions must be included in the cosmological evolution.
4. **Calculate a matter excess.** A viable baryogenesis claim requires the relevant CP bias, interactions that change baryon or lepton number, rate evolution, washout, and final abundance. These are not supplied by the current energy bounds.
5. **Check relics and defects in the actual model.** Abundance and domain-wall estimates must use the correct physical fields, vacuum identifications, and thermal history. Bounds inherited from a different branch are not automatically bounds on the Wilson-line alternative.
6. **Seek independent scrutiny.** Reproducing the program's outputs is valuable, but it is different from independent derivation, peer review, or experimental confirmation.

## How to interpret the efficiency bounds

The new calculation scales the kinetic requirement with the inverse square of winding times efficiency. Under its fixed benchmark assumptions, decreasing efficiency increases the minimum winding needed to fit a given energy allowance. The integer thresholds are necessary conditions within that calculation; they are not demonstrated physical solutions.

Read [the v1.23.1 calculation](../research/AM1231/v1.23.1/v1.23.1_efficiency_energy_frontier.md) alongside [the main note](../research/AM1231/AM1231_NOTE.md). Neither a numerical match nor passing a necessary gate establishes a completed unified theory.

## Version boundary

The September 30, 2026 GitHub publication mirrors the September 5, 2026 Zenodo v1.23.1 release. Proposed v1.24 investigations remain future work. Any subsequent change to the scientific calculations should receive a distinct version with its own assumptions, data, checksums, and citation record.

## Proposed October 2026 research rounds

The draft [transport gate](../research/rounds/2026-10-01_transport_gate/README.md)
checks signed response, conserved charges and washout in an illustrative network.
The subsequent [SM operator gate](../research/rounds/2026-10-02_sm_operator_gate/README.md)
derives an exact ideal symmetric-SM response to an assumed derivative B+L
operator with two separate methods and copied-script verification. It also
reviews a concrete 2026 scalar/Higgs wall mechanism as a possible next branch.
These are conditional public-input diagnostics: Wilson-specific matching, CP,
crossover rates, an autonomous energy reservoir and a surviving cosmological
yield remain open. The official release is still v1.23.1.

A [completion-driven research routine](research-routine/ROUND_PROTOCOL.md) and
[external Linux service template](research-routine/deployment/DEPLOYMENT.md) are
prepared. Runner controls passed with mocked invocations. No continuous AI
service is active, and external authenticated model/host execution remains untested.
