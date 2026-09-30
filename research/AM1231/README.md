# AntiMatter v1.23.1

September 5, 2026 | Ricardo Maldonado

Start with AM1231_NOTE.pdf or IN_MORE_BASIC_TERMS.md. This is a research checkpoint:
no claim of successful baryogenesis or a completed unified theory is made.

## What is included

- AM1231_NOTE.pdf and .md: new release note, efficiency bounds and qualifications.
- v1.23.1/: new analytic calculation, CSV table and standard-library Python script.
- v1.23/: all 32 original AM123 complete-bundle members, unchanged.
- original/AM123_COMPLETE.zip: exact source archive.
- parents/AM122_COMPLETE.zip: exact dependency required by the original generator.
- REPRODUCIBILITY.md and reproducibility.json: fresh replay evidence and limits.
- requirements-replay.txt: tested numerical/plotting dependency versions.
- SHA256SUMS.txt and verify_release.py: integrity verification for this package.

## Reproduce from this directory

Verify the full package:

    python3 verify_release.py

Run the new energy calculation using the verified original archive:

    python3 v1.23.1/v1.23.1_efficiency_energy_frontier.py --source-zip original/AM123_COMPLETE.zip --output-dir frontier_replay

For the original v1.23 calculation, install requirements-replay.txt in an isolated
Python environment, then run:

    python3 v1.23/v1.23_wilson_instanton_cosmology_audit.py --parent-zip parents/AM122_COMPLETE.zip --output-root replay

The replay output directory must be empty or absent. Fresh numerical results
matched all 21 original scientific CSVs and the summary JSON exactly. Image bytes
can depend on the rendering environment. See REPRODUCIBILITY.md for full limits.

## Historical status and scientific scope

The preserved v1.23 files retain their historical publication-HOLD wording. This
release documents those findings and adds an efficiency sensitivity calculation;
it does not declare the unresolved thermal, driving, anomaly, relic or defect
questions solved. Version 1.23.1 is distinct from the proposed v1.24 research
programme, which remains future work.

The originally supplied outer ZIP, phone ZIP, all-in-one text, and loose copies
are redundant delivery formats and are not duplicated here. Their input hashes
are recorded in provenance_input_checksums.json. No private chat transcript or
desktop screenshot is included. The new PHONE bundle has its own correct subset
ledger; the original v1.23 phone ledger referred to the complete bundle.
