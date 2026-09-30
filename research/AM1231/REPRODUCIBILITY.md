# AM v1.23 reproducibility audit

Audit date: 2026-09-05. Result: **PASS for numerical replay and archive integrity**.

The preserved v1.23 generator was statically reviewed and run without changing its source. Its parent was recovered from the preceding local release. Both original archives passed their expected SHA-256 checks, their ZIP integrity checks, and their complete internal ledgers (31/31 files each). The replay archive also passed all 31 internal hashes.

The replay reproduced **all 21 scientific CSV files and the summary JSON byte for byte**. The three Markdown documents and generator source also matched exactly. Across all 32 complete-bundle members, 26 matched exactly; only the four PNG figures and the two manifests that include their hashes differed. There were **zero unexpected differences**. No numerical tolerance was required.

The tested environment was Python 3.12.14 on Darwin arm64, NumPy 2.5.2, SciPy 1.17.1, and Matplotlib 3.10.8. The JSON report records all plotting dependencies. The original rendering environment is unknown; its byte-identical PNG and ZIP behavior is not claimed across environments.

## Reproduce

Install the versions in `requirements-replay.txt`, place the preserved generator and `AM122_COMPLETE.zip` in a working directory, and use an empty output directory:

```sh
python v1.23_wilson_instanton_cosmology_audit.py --parent-zip AM122_COMPLETE.zip --output-root replay
```

Expected parent SHA-256:
`44e5e29bb345e3da82d1dbddcc662b1e6c852f99bf951a3a6f5038da4bb8b807`

Expected original complete v1.23 archive SHA-256:
`2014b0a707f7dcb2272ab6c0b47cce6893501db08fe61daa9327e8f60179bc5d`

The detailed JSON lists the SHA-256 hashes of every original and regenerated member. Warnings during first-time font-cache creation did not prevent the replay from completing.

## Scope and limits

The parent **archive** was verified, but its scientific calculations were not independently rerun. The v1.23 generator freezes parent parameters and checks the parent archive's bytes; it is not a fresh derivation of the parent model.

This successful replay confirms that the supplied numerical results follow from the supplied program in the tested environment. It does not establish the physical assumptions, successful baryogenesis, a UV completion, or a theory of everything. The unresolved scientific gates and `NO_CLAIM` status remain in force as descriptions of the research.

The phone archive is a reading subset. Its included SHA ledger references the complete archive and therefore includes files absent from that subset; use the external checksum to verify the original phone ZIP.
