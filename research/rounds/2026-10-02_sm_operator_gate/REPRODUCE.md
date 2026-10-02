# Reproduce without overwriting preserved artifacts

From the AntiMatter root, install the baseline pins and the two additional
symbolic pins in an isolated Python 3.12.14 environment:

```bash
.venv/bin/python -m pip install -r research/AM1231/requirements-replay.txt -r research/rounds/2026-10-02_sm_operator_gate/requirements-operator.txt
.venv/bin/python -m pip check
.venv/bin/python scripts/reproduce_operator_round.py
```

The runner checks the round ledger and three exact public-context hashes, copies
only listed public files into a temporary directory, supplies the actual public
repository through `ANTIMATTER_PUBLIC_REPO`, and runs eight checks. It requires
15 output artifacts to match byte for byte, verifies registered control counts,
and retains a receipt and separate step logs outside the checkout. It performs
no AI invocation, private archive scan, Git push or publication.

The scientific implementation uses Fraction/Decimal standard-library arithmetic;
the separate symbolic implementation requires SymPy 1.14.0 and mpmath 1.3.0.
Exact receipts also include Python version metadata, so use the pinned patch
version. Context-resolution amendments are explicitly post-run and preserve
prior software provenance. Do not remove or rewrite originals to obtain a pass.

Manual replay must likewise use a copy. The reviewer creates a nested replay
workspace; run its script only inside a disposable round copy. Network citation
retrieval is separate and is not needed for numerical reproduction.
