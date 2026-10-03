# AntiMatter: Why Is There More Matter Than Antimatter?

[Readable project overview](https://maldonado-research.github.io/projects/antimatter/) · [All research projects](https://maldonado-research.github.io/)


**Ricardo Maldonado · Public research checkpoint v1.23.1**

This repository makes the AntiMatter working hypothesis, calculations, and audit results available for inspection. It explores possible field mechanisms for the matter–antimatter imbalance in the early Universe. It is part of a broader research programme toward unification, but the present checkpoint does **not** establish successful baryogenesis or a completed theory of everything.

The research was published on **September 5, 2026**. This GitHub mirror was prepared on **September 30, 2026** and preserves that scientific version without adding a new physics result.

**Latest public working updates — 2 October 2026, Pacific:** the follow-up kinetic/source-duration diagnostics, transport controls and [Standard Model charge/source comparator](research/rounds/2026-10-02_sm_operator_gate/README.md) are available on this repository’s main branch. They remain conditional research; the final matter excess has not been calculated. The latest published Zenodo version is still v1.23.1. See [publication status and project links](docs/PUBLICATION_STATUS.md).

**Archived publication:** [Zenodo record 22400470](https://zenodo.org/records/22400470) · [DOI: 10.5281/zenodo.22400470](https://doi.org/10.5281/zenodo.22400470)

## In More Basic Terms

The Universe contains much more matter than antimatter. This research asks whether a chain of interacting fields could help explain how that imbalance developed.

The latest audit narrows the possibilities. One proposed source fails the symmetry requirements of the specific model being tested. A different construction, using fields around an extra spatial dimension, can produce a desired long variation scale under stated assumptions. Its connection to the particles and interactions that would create the matter excess remains incomplete.

The energy bill also matters. At the original benchmark, the motion costs more energy than the proposed source supplies. Lower efficiency makes the problem harder. Any viable model must also avoid leaving too many stable particles, excess field energy, or persistent boundaries between vacuum states.

The progress is a clearer account of what fails, what is conditional, and what must be tested next. Read the complete [In More Basic Terms note](research/AM1231/IN_MORE_BASIC_TERMS.md).

## Start here

| What you want | File |
| --- | --- |
| Plain-language overview | [In More Basic Terms](research/AM1231/IN_MORE_BASIC_TERMS.md) |
| Main research note | [Markdown](research/AM1231/AM1231_NOTE.md) · [PDF](research/AM1231/AM1231_NOTE.pdf) |
| Efficiency and energy calculation | [v1.23.1 calculation note](research/AM1231/v1.23.1/v1.23.1_efficiency_energy_frontier.md) |
| Earlier Wilson-line and cosmology audit | [Preserved v1.23 note](research/AM1231/v1.23/v1.23_wilson_instanton_cosmology_audit_note.md) |
| Replay evidence and limitations | [Reproducibility report](research/AM1231/REPRODUCIBILITY.md) |
| Original archive and required parent | [v1.23 source ZIP](research/AM1231/original/AM123_COMPLETE.zip) · [v1.22 parent ZIP](research/AM1231/parents/AM122_COMPLETE.zip) |
| Complete and phone-friendly downloads | [GitHub release](https://github.com/maldonado-research/AntiMatter/releases/tag/v1.23.1) · [Zenodo files](https://zenodo.org/records/22400470) |
| Follow-up candidate diagnostics | [v1.23.2 candidate](research/AM1232_CANDIDATE_20261001/README.md) |
| Transport diagnostic | [Conserved charges and signed response](research/rounds/2026-10-01_transport_gate/README.md) |
| Latest operator and charge diagnostic | [Ideal Standard Model response and source matching](research/rounds/2026-10-02_sm_operator_gate/README.md) |
| Repeated research workflow | [Round protocol and scheduling status](docs/research-routine/ROUND_PROTOCOL.md) |
| Remaining scientific questions | [Research status and next tests](docs/RESEARCH_STATUS.md) |

## What the checkpoint establishes

- A symmetry obstruction for the stated compact gauged-scalar source construction. This is a result for the specified field content and assumptions, not a universal impossibility proof.
- A conditional Wilson-line alternative with a matched long variation scale. Its full particle content, anomaly cancellation, thermal history, and driving mechanism still require construction.
- An efficiency-dependent energy frontier: necessary bounds become more demanding as the response efficiency decreases. Meeting a bound alone does not construct a viable mechanism.
- Archive integrity and numerical replay evidence for the supplied calculations. Reproducing numbers verifies the calculation pipeline in the tested environment; it does not validate the underlying physical hypothesis.

No independent experimental validation or independent peer review is claimed. AI assistance was used in preparation and computational auditing; Ricardo Maldonado is the named author. Scientific assumptions and unresolved gates are retained in the source notes.

## Reproduce the calculations

The entire published package is preserved under `research/AM1231/`. First verify its files:

```sh
cd research/AM1231
python3 verify_release.py
```

The v1.23.1 energy calculation uses Python's standard library:

```sh
python3 v1.23.1/v1.23.1_efficiency_energy_frontier.py \
  --source-zip original/AM123_COMPLETE.zip --output-dir frontier_replay
```

For the original v1.23 numerical and plotting replay, use an isolated Python environment with the versions in `requirements-replay.txt`, then run:

```sh
python3 v1.23/v1.23_wilson_instanton_cosmology_audit.py \
  --parent-zip parents/AM122_COMPLETE.zip --output-root replay
```

The replay output directory must be empty or absent. The recorded audit matched 21 non-manifest CSVs and the summary JSON byte for byte; these include the parent-verification and primary-source tables. Of 32 preserved bundle members, 26 matched exactly. Four PNGs and their two manifests varied with rendering. The parent archive was checked for integrity; its physics was not independently rerun. See the [full report](research/AM1231/REPRODUCIBILITY.md) for the tested environment and scope.

## Cite and reuse

Maldonado, Ricardo. (2026). *AntiMatter: Wilson-Line and Cosmology Audit - Efficiency-Dependent Energy Bounds and Reproducibility* (v1.23.1). Zenodo. https://doi.org/10.5281/zenodo.22400470

[CITATION.cff](CITATION.cff) supplies machine-readable citation information. The published research is shared under **Creative Commons Attribution 4.0 International**, matching its Zenodo record. See [LICENSE](LICENSE) and [LICENSE_NOTICE.md](LICENSE_NOTICE.md). Referenced third-party publications remain subject to their own rights.

The original release files are unchanged. GitHub-specific documentation, citation information, and license notices sit outside the preserved package. Historic `HOLD` and `NO_CLAIM` wording describes unresolved scientific conditions; public availability does not mean those conditions have been solved.
