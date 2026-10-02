#!/usr/bin/env python3
"""Reproduce the public candidate in a disposable copy; no AI or publishing."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from reproduction_policy import compare_artifact


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_ledger(root, expected_count):
    entries = []
    for line in (root / 'SHA256SUMS.txt').read_text().splitlines():
        digest, name = line.split('  ', 1)
        path = root / name
        if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
            raise RuntimeError(f'Unsafe checksum path: {name}')
        if sha(path) != digest:
            raise RuntimeError(f'Checksum mismatch: {name}')
        entries.append(name)
    if len(entries) != expected_count or len(set(entries)) != expected_count:
        raise RuntimeError('Unexpected checksum ledger size or duplicate paths')
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    output = (args.output or Path(tempfile.mkdtemp(prefix='antimatter-checks.'))).resolve()
    if output.is_relative_to(repo):
        parser.error('Output must be outside the checkout')
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        parser.error('Output directory must be empty')
    report = {
        'schema_version': 1, 'kind': 'numerical_reproduction', 'status': 'running',
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'scientific_status': 'conditional diagnostics; no baryogenesis demonstration',
        'python': sys.version, 'commands': [], 'producer_byte_identical': {},
        'producer_content_checks': {},
        'ai_research_performed': False, 'publication_performed': False,
    }
    receipt = output / 'receipt.json'
    copy = output / '_work' / 'checkpoint'
    exit_code = 1
    try:
        report['git_commit'] = subprocess.check_output(
            ['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
        source = repo / 'research' / 'AM1231'
        candidate = repo / 'research' / 'AM1232_CANDIDATE_20261001'
        if not source.resolve().is_relative_to(repo) or not candidate.resolve().is_relative_to(repo):
            raise RuntimeError('Research input root escapes the public checkout')
        report['baseline_checksums'] = len(check_ledger(source, 48))
        candidate_entries = check_ledger(candidate, 40)
        report['candidate_checksums'] = len(candidate_entries)
        report['candidate_ledger_sha256'] = sha(candidate / 'SHA256SUMS.txt')
        report['dependencies'] = subprocess.check_output(
            [sys.executable, '-m', 'pip', 'list', '--format=json'], text=True)
        report['dependencies'] = json.loads(report['dependencies'])
        # Copy only verified ledger entries, never future unlisted references or all of /workspace.
        for relative in [*candidate_entries, 'SHA256SUMS.txt']:
            destination = copy / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(candidate / relative, destination)
        commands = [
            ['wilson-metric/audit.py', '--source-root', str(source / 'v1.23'), '--output-dir', str(copy / 'wilson-metric')],
            ['wilson-metric-independent/independent.py', '--source-root', str(source / 'v1.23'), '--output-dir', str(copy / 'wilson-metric-independent')],
            ['wilson-metric-independent/compare.py', '--source-root', str(source / 'v1.23'), '--producer-dir', str(copy / 'wilson-metric'), '--output-dir', str(copy / 'wilson-metric-independent')],
            ['source-duration/audit.py', '--source-root', str(source / 'v1.23'), '--output-dir', str(copy / 'source-duration')],
            ['source-duration-independent/independent_time_check.py', '--registered-grid', '--output', str(copy / 'source-duration-independent' / 'registered_grid_time_results.json')],
            ['source-duration-independent/independent_duration_check.py'],
            ['source-duration-independent/compare_outputs.py'],
        ]
        for number, command in enumerate(commands, 1):
            proc = subprocess.run([sys.executable, *command], cwd=copy, capture_output=True, text=True)
            (output / f'step-{number}.log').write_text(proc.stdout + proc.stderr)
            report['commands'].append({'script': command[0], 'exit_code': proc.returncode})
            print(json.dumps(report['commands'][-1]), flush=True)
            if proc.returncode:
                # These commands process public mathematical inputs only. Include their
                # failure detail in GitHub's check annotation as well as the public log.
                detail = (proc.stdout + proc.stderr)[-1800:]
                raise RuntimeError(f'Calculation failed: {command[0]}\n{detail}')
        for folder, names in {
            'wilson-metric': ['results.json', 'results.csv'],
            'source-duration': ['results.json', 'trajectories.csv', 'duration_bounds.csv'],
        }.items():
            for name in names:
                relative = f'{folder}/{name}'
                comparison = compare_artifact(relative, candidate / relative, copy / relative)
                report['producer_byte_identical'][relative] = comparison['byte_identical']
                report['producer_content_checks'][relative] = comparison
                if not comparison['passed']:
                    rejected = comparison['scientific_or_unapproved_differences']
                    patterns = sorted({re.sub(r'/\d+(?=/|$)', '/[]', item['path'])
                                       for item in rejected})
                    detail = json.dumps({'first_differences': rejected[:8],
                                         'rejected_path_patterns': patterns})
                    raise RuntimeError(f'Producer output changed: {relative}\n{detail}')
        for name, relative in {
            'wilson_comparison': 'wilson-metric-independent/comparison-results.json',
            'source_comparison': 'source-duration-independent/comparison_results.json',
        }.items():
            report[name] = json.loads((copy / relative).read_text())
        report['status'] = 'passed'
        exit_code = 0
    except Exception as error:
        report['status'] = 'failed'
        report['error'] = str(error)
        print(str(error), file=sys.stderr)
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            message = str(error).replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
            print(f'::error title=Antimatter replay failure::{message}', flush=True)
    finally:
        report['ended_utc'] = datetime.now(timezone.utc).isoformat()
        receipt.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'receipt': str(receipt)}))
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
