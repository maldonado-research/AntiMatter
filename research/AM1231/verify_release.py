#!/usr/bin/env python3
"""Verify every SHA256SUMS.txt entry without modifying any file."""
from pathlib import Path
import hashlib
root = Path(__file__).resolve().parent
count = 0
for line in (root / "SHA256SUMS.txt").read_text().splitlines():
    expected, name = line.split("  ", 1)
    p = root / name
    if not p.resolve().is_relative_to(root):
        raise SystemExit("Unsafe manifest path")
    observed = hashlib.sha256(p.read_bytes()).hexdigest()
    if observed != expected:
        raise SystemExit("Checksum mismatch: " + name)
    count += 1
print(f"PASS: {count} package checksums")
