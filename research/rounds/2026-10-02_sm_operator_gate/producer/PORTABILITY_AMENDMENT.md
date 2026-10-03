# Post-run portability amendment, 2026-10-02

This is a software-path amendment after the registered scientific calculation.
It is not a new preregistration. The primary thermodynamic solver, equations,
scientific outputs, registration, and derivation remain unchanged.

The initial conditional-sensitivity script discovered public parent files only
through its ancestors. That works in the original workspace but prevents replay
from an arbitrary disposable copy. The script now accepts the explicit,
task-specific environment variable `ANTIMATTER_PUBLIC_REPO`. When supplied, it
selects that repository instead of guessing an ancestor. All three required
public context paths are resolved and checked as regular files beneath the
chosen real repository. A missing chosen repository or a context symlink that
escapes it fails explicitly. Repository code is read as AST literals and CSV;
it is never imported or executed by this calculation.

For a disposable copy, run for example:

```sh
ANTIMATTER_PUBLIC_REPO=/workspace/AntiMatter python3 verify_reproducibility.py
```

The SHA ledger writer now includes nested preservation artifacts. Its scientific
calculations and byte-reproduction checks are unchanged.

`ORIGINAL_PORTABILITY_INPUTS/` preserves the complete original conditional
script, verification script, receipt, public-source provenance, and SHA ledger.
`ORIGINAL_SHA256.json` records their pre-amendment hashes. The original
conditional-script SHA256 is
`ed9a9089fecd0b99604fb6ad23ef27b99dd9cf51470a288c43ace69bbba1c92c`;
the original receipt SHA256 is
`696089626585eeb4784a8bbb17a1c1af0d3059cbf83552493e9ade00acd2d6cb`.

A `/tmp` disposable-copy replay with an explicit public context completed all
84 scientific controls, reproduced all eight prior output files byte-for-byte,
and removed its temporary directory. Two additional portability controls
confirmed rejection of a missing explicit repository and an escaping public
context symlink. These are software checks, separate from the registered
scientific controls.

The existing `PROVENANCE.json` is among the eight reproduced outputs and is
preserved byte-identically. It records public input and registration hashes,
not software implementation hashes. New/old software hashes and the disposable
replay evidence are recorded separately in `PORTABILITY_PROVENANCE.json`.
The current receipt and SHA ledger are regenerated for the amended software.
No new physics, coefficient replacement, or physical yield follows from this
portability change.
