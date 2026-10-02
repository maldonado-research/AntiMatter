#!/usr/bin/env python3
"""Replay the public SM operator comparator in a verified disposable copy."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from reproduce_candidate import check_ledger


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    output = (args.output or Path(tempfile.mkdtemp(prefix='antimatter-operator-checks.'))).resolve()
    if output.is_relative_to(repo):
        parser.error('Output must be outside the checkout')
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        parser.error('Output directory must be empty')
    source = repo / 'research/rounds/2026-10-02_sm_operator_gate'
    report = {'status': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(),
              'kind': 'public_operator_round_reproduction', 'commands': [],
              'scientific_scope': 'Conditional ideal-SM comparator; no physical baryon-yield claim',
              'ai_research_performed': False, 'publication_performed': False,
              'byte_comparisons': {}}
    code = 1
    try:
        record = json.loads((source / 'ROUND.json').read_text())
        entries = check_ledger(source, record['checksum_entries'])
        report['round_checksums'] = len(entries)
        for item in record['public_context_hashes']:
            path = repo / item['path']
            if path.is_symlink() or not path.resolve().is_relative_to(repo) or digest(path) != item['sha256']:
                raise RuntimeError('Changed or unsafe public context: ' + item['path'])
        report['public_context_checks'] = len(record['public_context_hashes'])
        report['git_commit'] = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
        copy = output / '_work/round'
        for relative in [*entries, 'SHA256SUMS.txt']:
            target = copy / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / relative, target)
        environment = {**os.environ, 'ANTIMATTER_PUBLIC_REPO': str(repo)}
        commands = ['producer/sm_charge_diagnostic.py', 'producer/conditional_sensitivity.py',
                    'independent/sm_charge_response.py', 'independent/conditional_normalization_sensitivity.py',
                    'independent/compare_frozen_producer.py', 'inventory/verify_inventory.py',
                    'wall_literature/compare_susceptibilities.py', 'reviewer/review_checks.py']
        for number, script in enumerate(commands, 1):
            result = subprocess.run([sys.executable, str(copy / script)], cwd=copy,
                                    env=environment, capture_output=True, text=True, timeout=180)
            (output / f'step-{number}.log').write_text(result.stdout + result.stderr)
            report['commands'].append({'script': script, 'exit_code': result.returncode})
            print(json.dumps(report['commands'][-1]), flush=True)
            if result.returncode:
                raise RuntimeError('Operator calculation failed: ' + script + '\n' + (result.stdout + result.stderr)[-2000:])
        artifacts = ['producer/results.json', 'producer/species_response.csv', 'producer/reaction_charges.csv',
                     'producer/conserved_density_basis.csv', 'producer/tests.csv',
                     'producer/conditional_sensitivity.json', 'producer/conditional_sensitivity.csv',
                     'producer/PROVENANCE.json', 'independent/matrices.json', 'independent/receipt.json',
                     'independent/sensitivity_receipt.json', 'independent/comparison_receipt.json',
                     'inventory/EXACT_INVENTORY_CHECKS.json', 'wall_literature/SUSCEPTIBILITY_COMPARISON.json',
                     'reviewer/REVIEW_RECEIPT.json']
        for relative in artifacts:
            same = (source / relative).read_bytes() == (copy / relative).read_bytes()
            report['byte_comparisons'][relative] = same
            if not same:
                raise RuntimeError('Operator output differs from preserved artifact: ' + relative)
        summaries = {name: json.loads((copy / relative).read_text()) for name, relative in {
            'producer': 'producer/results.json', 'conditional': 'producer/conditional_sensitivity.json',
            'independent': 'independent/receipt.json', 'comparison': 'independent/comparison_receipt.json',
            'reviewer': 'reviewer/REVIEW_RECEIPT.json'}.items()}
        expected = [('producer', 'test_count', 48), ('conditional', 'test_count', 36),
                    ('independent', 'check_count', 24), ('comparison', 'checks', 11),
                    ('reviewer', 'check_count', 35)]
        for name, field, count in expected:
            actual = len(summaries[name][field]) if field == 'checks' else summaries[name][field]
            if actual != count:
                raise RuntimeError('Unexpected registered control count: ' + name)
        report['control_counts'] = {name: count for name, _, count in expected}
        report['status'] = 'passed'
        code = 0
    except Exception as error:
        report['status'] = 'failed'
        report['error'] = str(error)
        print(str(error), file=sys.stderr)
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            message = str(error).replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
            print(f'::error title=SM operator replay failure::{message}', flush=True)
    finally:
        report['ended_utc'] = datetime.now(timezone.utc).isoformat()
        (output / 'receipt.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'receipt': str(output / 'receipt.json')}))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
