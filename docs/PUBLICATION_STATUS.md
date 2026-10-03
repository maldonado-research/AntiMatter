# Antimatter publication status and project links

Updated 2 October 2026, Pacific. Public working research and archived publication have different roles.

| Where | What it contains |
| --- | --- |
| [GitHub profile](https://github.com/maldonado-research) | The owner's repository directory; it is not a separate copy of this research. |
| [AntiMatter repository](https://github.com/maldonado-research/AntiMatter) | Current public code, results, notes, limitations and reproduction records on main. |
| [Antimatter overview](https://maldonado-research.github.io/projects/antimatter/) | The readable project summary maintained in the research-directory website source. |
| [Research hub](https://maldonado-research.github.io/) | Links to all projects. |
| [Published Zenodo version](https://zenodo.org/records/22400470) | Immutable v1.23.1 archive; it remains the latest confirmed published version. |
| [Zenodo concept DOI](https://doi.org/10.5281/zenodo.18193771) | The existing Antimatter version family; retain it for subsequent publication. |

The separate [HDBLAST site](https://maldonado-research.github.io/HDblast/) belongs to the HDBLAST project. Its scientific content is maintained separately.

## Current public work

Research PR1 was independently checked and merged. Main includes the [v1.23.2 follow-up diagnostics](../research/AM1232_CANDIDATE_20261001/README.md), [transport round](../research/rounds/2026-10-01_transport_gate/README.md), and [SM operator round](../research/rounds/2026-10-02_sm_operator_gate/README.md). The original v1.23.1 files remain preserved. The computations are conditional; Wilson matching, physical CP, a self-consistent reservoir, electroweak crossover and a final baryon yield remain open.

[Hosted verification](https://github.com/maldonado-research/AntiMatter/actions/runs/37082254718) passed for the reviewed changes. The default-branch workflow can schedule numerical verification every four hours; this does not launch AI research. External continuous AI hosting remains inactive.

## Zenodo update

The v1.23.2 package is prepared for the existing DOI family. Current secret binding and authenticated ownership/new-version access were verified. Metadata transport remains blocked: legacy API updates returned HTTP500, and a native-schema update returned HTTP200 with empty metadata on readback. A reserved draft DOI is not a published version. No incomplete draft or inherited v1.23.1 files were published as v1.23.2.

Keep the existing draft for the authenticated browser editor fallback. Before publication, save and read back the full approved title, description, version, date and creator/license fields; replace inherited files with the verified v1.23.2 package; verify every filename, byte count and checksum. Do not create a GitHub release merely to test repaired integration: automatic deposition might create a separate record family. A Git tag/source snapshot can be added when the existing-family version is actually published.

Website PR3 is merged. GitHub Pages reports a successful build for commit 0d46469f87840d66ae5ffa6ae990ab9d48eef080. The [prepared v1.23.2 report/download package](../research/AM1232_PUBLICATION_PACKAGE_20261002/README.md) is available on GitHub while the Zenodo update remains unpublished.
