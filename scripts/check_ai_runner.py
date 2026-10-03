#!/usr/bin/env python3
"""Exercise a copied runner with synthetic local Git repositories and fake Codex."""
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

SOURCE = Path(__file__).resolve().with_name('run_ai_round.sh')
DEST = Path(tempfile.mkdtemp(prefix='antimatter-runner-proof.'))
SNAPSHOT = DEST / 'run_ai_round.snapshot.sh'
SNAPSHOT.write_bytes(SOURCE.read_bytes())
SNAPSHOT.chmod(0o700)
ROOT = Path(tempfile.mkdtemp(prefix='antimatter-runner-review.', dir='/tmp'))
ENV = {'PATH': f'{ROOT / "bin"}:/usr/local/bin:/usr/bin:/bin',
       'ANTIMATTER_CODEX_MODEL': 'mock-gpt-6.1-sol',
       'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null',
       'LC_ALL': 'C.UTF-8'}
(ROOT / 'bin').mkdir()
MOCK_TIMEOUT = ROOT / 'bin/timeout'
MOCK_TIMEOUT.write_text('''#!/usr/bin/env python3
import os, sys
args = sys.argv[1:]
if os.environ['HARNESS_CASE'] == 'timeout':
    args = ['--kill-after=1s', '0.1s'] + args[2:]
os.execv('/usr/bin/timeout', ['timeout'] + args)
''')
MOCK_TIMEOUT.chmod(0o700)
MOCK = ROOT / 'bin/codex'
MOCK.write_text('''#!/usr/bin/env python3
import json, os, pathlib, subprocess, sys
args = sys.argv[1:]
repo = pathlib.Path(args[args.index('--cd') + 1])
mode = os.environ['HARNESS_CASE']
pathlib.Path(os.environ['HARNESS_CALLED']).write_text(json.dumps(args))
prompt = sys.stdin.read()
pathlib.Path(args[args.index('--output-last-message') + 1]).write_text('Synthetic fixture round.\\n')
print(json.dumps({'type': 'mock_finished', 'case': mode}))
if mode == 'cli_failure': sys.exit(23)
if mode == 'no_checkpoint': sys.exit(0)
if mode == 'timeout':
    import time
    time.sleep(5)
    sys.exit(0)
if mode == 'history_rewind':
    subprocess.run(['git', '-C', str(repo), 'reset', '--hard', os.environ['HARNESS_REWIND_SHA']], check=True, stdout=subprocess.DEVNULL)
    sys.exit(0)
routine_path = repo / 'docs/research-routine/routine.json'
routine = json.loads(routine_path.read_text())
prior = routine['latest_completed_round']
round_dir = repo / 'research/rounds/fresh'
round_dir.mkdir(parents=True)
record = {'status': 'completed', 'predecessor': 'research/rounds/wrong' if mode == 'wrong_predecessor' else prior,
          'next_question': 'Test the next fixture control', 'validation_receipt': 'receipt.json'}
receipt = {'status': 'failed' if mode == 'failed_receipt' else 'passed'}
if mode == 'boolean_receipt': receipt = {'passed': True}
if mode == 'ignored_receipt_alias':
    (round_dir / 'actual').mkdir()
    (round_dir / 'actual/receipt.json').write_text(json.dumps(receipt))
    (round_dir / 'ignored-alias').symlink_to('actual', target_is_directory=True)
    (repo / '.gitignore').write_text('research/rounds/fresh/ignored-alias\\n')
    record['validation_receipt'] = 'ignored-alias/receipt.json'
if mode == 'absolute_receipt_path': record['validation_receipt'] = str(round_dir / 'receipt.json')
if mode == 'receipt_escape':
    record['validation_receipt'] = '../receipt.json'
    (round_dir.parent / 'receipt.json').write_text(json.dumps(receipt))
else:
    (round_dir / 'receipt.json').write_text(json.dumps(receipt))
if mode == 'symlink_round_record':
    (repo / 'docs/fixture-record.json').write_text(json.dumps(record))
    (round_dir / 'ROUND.json').symlink_to('../../../docs/fixture-record.json')
else:
    (round_dir / 'ROUND.json').write_text(json.dumps(record))
routine['latest_completed_round'] = 'docs/research-routine' if mode == 'round_escape' else 'research/rounds/fresh'
if mode == 'ignored_round_alias':
    (repo / 'research/rounds/ignored-alias').symlink_to('fresh', target_is_directory=True)
    (repo / '.gitignore').write_text('research/rounds/ignored-alias\\n')
    routine['latest_completed_round'] = 'research/rounds/ignored-alias'
if mode == 'absolute_round_path': routine['latest_completed_round'] = str(round_dir)
routine_path.write_text(json.dumps(routine))
if mode == 'untracked_evidence': (repo / '.gitignore').write_text('research/rounds/fresh/receipt.json\\n')
subprocess.run(['git', '-C', str(repo), 'add', '.'], check=True)
subprocess.run(['git', '-C', str(repo), 'commit', '-qm', 'Synthetic completed checkpoint'], check=True)
if mode == 'dirty_finish': (repo / 'unfinished.txt').write_text('Uncommitted fixture work')
''')
MOCK.chmod(0o700)

def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], env=ENV,
                          check=True, capture_output=True, text=True).stdout.strip()

def fixture(name):
    base = ROOT / name
    repo = base / 'repo'
    state = base / 'private-state'
    repo.mkdir(parents=True)
    git(repo, 'init', '-q')
    git(repo, 'config', 'user.name', 'Synthetic Fixture')
    git(repo, 'config', 'user.email', 'fixture@example.invalid')
    git(repo, 'config', 'commit.gpgsign', 'false')
    docs = repo / 'docs/research-routine'
    docs.mkdir(parents=True)
    (docs / 'routine.json').write_text(json.dumps({'latest_completed_round': 'research/rounds/prior'}))
    (docs / 'ROUND_PROMPT.md').write_text('Run exactly one synthetic fixture.\n')
    (repo / 'research/rounds/prior').mkdir(parents=True)
    (repo / 'research/rounds/prior/ROUND.json').write_text(json.dumps({'status': 'completed'}))
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'Initial synthetic fixture')
    return base, repo, state

results = []

def run(name, expected, expected_marker=True, setup=None):
    base, repo, state = fixture(name)
    env = {**ENV, 'HARNESS_CASE': name, 'HARNESS_CALLED': str(base / 'called.json')}
    lock = None
    if setup:
        replacement_state, lock = setup(base, repo, state, env)
        if replacement_state: state = replacement_state
    baseline = git(repo, 'rev-parse', 'HEAD')
    result = subprocess.run(['bash', str(SNAPSHOT), str(repo), str(state)],
                            env=env, text=True, capture_output=True, timeout=15)
    if lock: lock.close()
    runs = list(state.glob('round.*')) if state.exists() else []
    runs = [item for item in runs if item.is_dir()]
    run_dir = runs[0] if runs else None
    marker = (base / 'called.json').exists()
    correct = result.returncode == expected and marker == expected_marker
    entry = {'name': name, 'expected_exit': expected, 'actual_exit': result.returncode,
             'expected_mock_called': expected_marker, 'mock_called': marker,
             'status': 'passed' if correct else 'failed', 'baseline_commit': baseline,
             'final_commit': git(repo, 'rev-parse', 'HEAD'),
             'stdout': result.stdout, 'stderr': result.stderr, 'fixture': str(base)}
    if run_dir:
        entry['private_run_dir'] = str(run_dir)
        entry['cli_exit_receipt'] = (run_dir / 'cli-exit-code.txt').read_text().strip()
        entry['wrapper_exit_receipt'] = (run_dir / 'exit-code.txt').read_text().strip()
        entry['restricted_permissions'] = all((item.stat().st_mode & 0o077) == 0 for item in run_dir.rglob('*'))
        if not entry['restricted_permissions']: entry['status'] = 'failed'
        if (run_dir / 'checkpoint-guard.json').exists():
            entry['checkpoint'] = json.loads((run_dir / 'checkpoint-guard.json').read_text())
    if marker:
        entry['cli_arguments'] = json.loads((base / 'called.json').read_text())
    results.append(entry)

def dirty_start(base, repo, state, env):
    (repo / 'docs/research-routine/ROUND_PROMPT.md').write_text('Preserve this existing work.\n')
    return None, None

def lock_collision(base, repo, state, env):
    state.mkdir()
    handle = (state / 'round.lock').open('w')
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    return None, handle

def nested_state(base, repo, state, env):
    return repo / 'private-state', None

def history_rewind(base, repo, state, env):
    docs = repo / 'docs/research-routine/routine.json'
    new_round = repo / 'research/rounds/previously-completed'
    new_round.mkdir()
    (new_round / 'ROUND.json').write_text(json.dumps({'status': 'completed', 'predecessor': 'research/rounds/prior',
        'next_question': 'Old checkpoint next test', 'validation_receipt': 'receipt.json'}))
    (new_round / 'receipt.json').write_text(json.dumps({'status': 'passed'}))
    docs.write_text(json.dumps({'latest_completed_round': 'research/rounds/previously-completed'}))
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'Older completed checkpoint')
    env['HARNESS_REWIND_SHA'] = git(repo, 'rev-parse', 'HEAD')
    docs.write_text(json.dumps({'latest_completed_round': 'research/rounds/prior'}))
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'Reset pointer while preserving old evidence')
    return None, None

for name, expected in [('success', 0), ('boolean_receipt', 0), ('cli_failure', 23), ('timeout', 124), ('no_checkpoint', 1),
                       ('failed_receipt', 1), ('dirty_finish', 1), ('untracked_evidence', 1),
                       ('wrong_predecessor', 1), ('receipt_escape', 1), ('round_escape', 1)]:
    run(name, expected)
run('dirty_start', 2, False, dirty_start)
run('lock_collision', 75, False, lock_collision)
run('nested_state', 2, False, nested_state)
run('history_rewind', 1, True, history_rewind)
run('symlink_round_record', 1)
run('ignored_round_alias', 1)
run('absolute_round_path', 1)
run('ignored_receipt_alias', 1)
run('absolute_receipt_path', 1)

receipt = {'schema_version': 1, 'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'source': str(SOURCE), 'tested_snapshot': str(SNAPSHOT),
           'source_sha256': hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest(),
           'mock_only': True, 'actual_ai_execution': False, 'scheduler_installed': False,
           'repository_modified_by_this_review': False,
           'fixture_root': str(ROOT), 'checks': results,
           'passed': sum(item['status'] == 'passed' for item in results),
           'failed': sum(item['status'] == 'failed' for item in results)}
receipt['status'] = 'passed' if receipt['failed'] == 0 else 'bugs_found'
output = DEST / 'receipt.json'
output.write_text(json.dumps(receipt, indent=2) + '\n')
output.chmod(0o600)
print(json.dumps({'receipt': str(output), 'status': receipt['status'], 'passed': receipt['passed'],
                  'failed': receipt['failed'], 'failures': [item['name'] for item in results if item['status'] == 'failed']}))

raise SystemExit(0 if receipt['failed'] == 0 else 1)
