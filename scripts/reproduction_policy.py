"""Narrow, explicit archival comparison policy; never alter scientific artifacts."""
import csv
from decimal import Decimal, InvalidOperation
import json
import math
from pathlib import Path
import re


POLICY = 'wilson-portability-v1'
BOUND = Decimal('2e-12')


def differences(expected, observed, path=''):
    """Return every difference, including missing keys and type changes."""
    if type(expected) is not type(observed):
        return [{'path': path, 'expected': expected, 'observed': observed}]
    if isinstance(expected, dict):
        result = []
        for key in sorted(expected.keys() | observed.keys()):
            child = path + '/' + key.replace('~', '~0').replace('/', '~1')
            if key not in expected or key not in observed:
                result.append({'path': child, 'expected': expected.get(key),
                               'observed': observed.get(key), 'missing_key': True})
            else:
                result.extend(differences(expected[key], observed[key], child))
        return result
    if isinstance(expected, list):
        if len(expected) != len(observed):
            return [{'path': path, 'expected_length': len(expected),
                     'observed_length': len(observed)}]
        return [change for index, pair in enumerate(zip(expected, observed))
                for change in differences(*pair, path + '/' + str(index))]
    return [] if expected == observed else [{'path': path, 'expected': expected, 'observed': observed}]


def number(value):
    if isinstance(value, bool):
        raise ValueError('Boolean is not a numerical observation')
    result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError('Nonfinite observation')
    return result


def bounded_control(before, after, name):
    if (before.get('check') != name or after.get('check') != name
            or before.get('passed') is not True or after.get('passed') is not True
            or before.get('bound') != after.get('bound')
            or number(after['bound']) != BOUND):
        raise ValueError('Changed control identity, pass status or registered bound')
    if not (0 <= number(before['observed']) <= BOUND
            and 0 <= number(after['observed']) <= BOUND):
        raise ValueError('Control exceeds its original 2e-12 bound')
    return {'check': name, 'criterion': '0 <= observed <= bound',
            'original_bound': before['bound']}


def coordinate_gate(before_doc, after_doc, index):
    before, after = before_doc['results'][index], after_doc['results'][index]
    if (before['case'], before['configuration']) != (after['case'], after['configuration']):
        raise ValueError('Changed case or configuration')
    name = after['case'] + '/' + after['configuration'] + ': heavy coordinate consistency'
    expected = [row for row in before_doc['checks'] if row['check'] == name]
    observed = [row for row in after_doc['checks'] if row['check'] == name]
    if len(expected) != 1 or len(observed) != 1:
        raise ValueError('Missing or duplicate named coordinate control')
    gate = bounded_control(expected[0], observed[0], name)
    for result, check in [(before, expected[0]), (after, observed[0])]:
        if number(result['heavy_coordinate_relative_error']) != number(check['observed']):
            raise ValueError('Coordinate diagnostic disagrees with named control')
    return gate


def json_gate(change, before, after):
    path = change['path']
    if (change.get('missing_key') or 'expected' not in change or 'observed' not in change
            or type(change['expected']) is not type(change['observed'])):
        raise ValueError('Missing field, changed shape or changed value type')
    if (path == '/runtime/python_executable' and not change.get('missing_key')
            and isinstance(change.get('expected'), str)
            and isinstance(change.get('observed'), str)):
        return 'metadata', {'criterion': 'Interpreter installation path only'}
    match = re.fullmatch(r'/checks/(\d+)/observed', path)
    if match and not change.get('missing_key'):
        index = int(match[1])
        old, new = before['checks'][index], after['checks'][index]
        name = old['check']
        if name.endswith(': heavy coordinate consistency') or name.endswith(': analytic source-off spectrum'):
            return 'diagnostic', bounded_control(old, new, name)
        if name.endswith(': positive source-off heavy spectrum'):
            if (new['check'] != name or old['passed'] is not True or new['passed'] is not True
                    or old['bound'] is not None or new['bound'] is not None
                    or number(old['observed']) <= 0 or number(new['observed']) <= 0):
                raise ValueError('Changed or failed positive-spectrum control')
            case = name.split(': positive source-off heavy spectrum')[0]
            rows = [row for row in after['results']
                    if row['case'] == case and row['configuration'] == 'source off']
            if len(rows) != 1 or math.sqrt(float(new['observed'])) != rows[0]['heavy_min_GeV']:
                raise ValueError('Positive-spectrum observation disagrees with generated heavy mass')
            return 'diagnostic', {'check': name, 'original_bound': None,
                                  'criterion': 'observed > 0; sqrt(observed) equals generated heavy_min_GeV'}
    match = re.fullmatch(r'/results/(\d+)/heavy_coordinate_relative_error', path)
    if match and not change.get('missing_key'):
        return 'diagnostic', coordinate_gate(before, after, int(match[1]))
    raise ValueError('Field is outside the explicit portability allowlist')


def compare_artifact(relative, expected_path, observed_path):
    """Compare one producer artifact and return complete, JSON-safe evidence.

    Caller must first execute all original producers and independent comparisons.
    All primary values, versions, hashes and source-duration files stay exact.
    """
    expected_path, observed_path = Path(expected_path), Path(observed_path)
    byte_identical = expected_path.read_bytes() == observed_path.read_bytes()
    report = {'policy': POLICY, 'byte_identical': byte_identical,
              'metadata_differences': [], 'diagnostic_differences': [],
              'scientific_or_unapproved_differences': []}
    if relative.endswith('.json'):
        before, after = [json.loads(path.read_text()) for path in [expected_path, observed_path]]
    elif relative.endswith('.csv'):
        documents = []
        for path in [expected_path, observed_path]:
            with path.open(newline='') as handle:
                reader = csv.DictReader(handle)
                documents.append({'columns': reader.fieldnames, 'rows': list(reader)})
        before, after = documents
    else:
        raise ValueError('Only documented JSON and CSV producer artifacts are supported')
    for change in differences(before, after):
        try:
            if relative == 'wilson-metric/results.json':
                category, gate = json_gate(change, before, after)
            elif relative == 'wilson-metric/results.csv':
                match = re.fullmatch(r'/rows/(\d+)/heavy_coordinate_relative_error', change['path'])
                if not match or change.get('missing_key'):
                    raise ValueError('CSV field is outside the coordinate-diagnostic allowlist')
                index = int(match[1])
                old_json, new_json = [json.loads(path.with_suffix('.json').read_text())
                                      for path in [expected_path, observed_path]]
                gate = coordinate_gate(old_json, new_json, index)
                for csv_doc, json_doc in [(before, old_json), (after, new_json)]:
                    row, result = csv_doc['rows'][index], json_doc['results'][index]
                    if (row['case'], row['configuration']) != (result['case'], result['configuration']):
                        raise ValueError('CSV row identity disagrees with JSON')
                    if row['heavy_coordinate_relative_error'] != str(result['heavy_coordinate_relative_error']):
                        raise ValueError('CSV coordinate diagnostic disagrees with JSON')
                category = 'diagnostic'
            else:
                raise ValueError('Source-duration content remains exact')
            report[category + '_differences'].append({**change, 'gate': gate})
        except (ValueError, KeyError, IndexError, TypeError, InvalidOperation) as error:
            report['scientific_or_unapproved_differences'].append({**change, 'reason': str(error)})
    report['difference_counts'] = {name: len(report[name]) for name in
                                   ['metadata_differences', 'diagnostic_differences',
                                    'scientific_or_unapproved_differences']}
    report['passed'] = not report['scientific_or_unapproved_differences']
    return report
