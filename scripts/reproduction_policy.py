"""Narrow, explicit archival comparison policy; never alter scientific artifacts."""
import csv
from decimal import Decimal, InvalidOperation, localcontext
import json
import math
from pathlib import Path
import re


POLICY = 'wilson-portability-v2'
BOUND = Decimal('2e-12')
HEAVY_BOUND = Decimal('1e-12')
PORTABLE_FIELDS = {'heavy_min_GeV', 'heavy_max_GeV',
                   'heavy_min_relative_change', 'heavy_max_relative_change',
                   'metric_correction_operator_norm'}


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


def heavy_gate(before, after):
    expected, observed = number(before), number(after)
    if expected <= 0 or observed <= 0:
        raise ValueError('Heavy masses must be finite and positive')
    with localcontext() as context:
        context.prec = 110
        error = abs(observed / expected - 1)
    if not error < HEAVY_BOUND:
        raise ValueError('Heavy mass drift exceeds existing independent spectral criterion')
    return {'check': 'Independent Wilson heavy-mass spectral comparison',
            'criterion': 'positive finite masses; abs(observed/expected - 1) < 1e-12',
            'existing_comparator_bound': str(HEAVY_BOUND),
            'relative_difference': str(error)}


def norm_gate(before, after):
    expected, observed = float(number(before)), float(number(after))
    if not (math.isfinite(expected) and math.isfinite(observed)) or min(expected, observed) < 0:
        raise ValueError('Operator norms must be finite and nonnegative')
    with localcontext() as context:
        context.prec = 1200
        bound = 64 * Decimal.from_float(math.ulp(max(expected, observed)))
        error = abs(Decimal.from_float(observed) - Decimal.from_float(expected))
    if error > bound:
        raise ValueError('Operator norm drift exceeds explicit 64-ULP portability gate')
    return {'criterion': 'abs(observed - expected) <= 64 ulp(max(expected, observed))',
            'gate_scope': 'New display/portability gate adopted after observed hosted drift; not a preregistered physics criterion',
            'max_allowed_absolute_difference': str(bound),
            'observed_absolute_difference': str(error)}


def relative_baseline(document, row, mass_field):
    baseline = [item for item in document['results']
                if item['case'] == 'baseline' and item['configuration'] == row['configuration']]
    if len(baseline) != 1:
        raise ValueError('Missing or duplicate matching baseline row')
    baseline = baseline[0]
    if number(row[mass_field]) <= 0 or number(baseline[mass_field]) <= 0:
        raise ValueError('Relative change references a nonpositive mass')
    relative_field = mass_field.replace('_GeV', '_relative_change')
    if row[relative_field] != row[mass_field] / baseline[mass_field] - 1:
        raise ValueError('Relative change is not exactly recomputed from matching masses')
    return baseline


def primary_gate(before_doc, after_doc, section, index, field):
    before, after = before_doc[section][index], after_doc[section][index]
    identities = ['case'] + (['configuration'] if section == 'results' else [])
    if any(before[key] != after[key] for key in identities):
        raise ValueError('Changed primary row identity')
    if field == 'metric_correction_operator_norm':
        gate = norm_gate(before[field], after[field])
        for document, row in [(before_doc, before), (after_doc, after)]:
            metric = [item for item in document['metrics'] if item['case'] == row['case']]
            if len(metric) != 1:
                raise ValueError('Missing or duplicate metric case')
            results = [item for item in document['results'] if item['case'] == row['case']]
            if not results or any(item[field] != metric[0][field] for item in results):
                raise ValueError('Result operator norm disagrees with its metric case')
        return gate
    if section != 'results':
        raise ValueError('Unknown metric primary field')
    if field in {'heavy_min_GeV', 'heavy_max_GeV'}:
        for document, row in [(before_doc, before), (after_doc, after)]:
            relative_baseline(document, row, field)
            if row['case'] == 'baseline':
                for item in document['results']:
                    if item['configuration'] == row['configuration']:
                        relative_baseline(document, item, field)
        return heavy_gate(before[field], after[field])
    if field in {'heavy_min_relative_change', 'heavy_max_relative_change'}:
        mass_field = field.replace('_relative_change', '_GeV')
        baseline_rows = []
        for document, row in [(before_doc, before), (after_doc, after)]:
            baseline_rows.append(relative_baseline(document, row, mass_field))
        return {'criterion': 'Exact same-document mass/baseline - 1; both masses satisfy existing 1e-12 spectral criterion',
                'row_mass_gate': heavy_gate(before[mass_field], after[mass_field]),
                'baseline_mass_gate': heavy_gate(baseline_rows[0][mass_field], baseline_rows[1][mass_field])}
    raise ValueError('Unknown primary field')


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
    match = re.fullmatch(r'/(metrics|results)/(\d+)/([a-zA-Z0-9_]+)', path)
    if match and match[3] in PORTABLE_FIELDS:
        return 'scientific', primary_gate(before, after, match[1], int(match[2]), match[3])
    raise ValueError('Field is outside the explicit portability allowlist')


def compare_artifact(relative, expected_path, observed_path):
    """Compare one producer artifact and return complete, JSON-safe evidence.

    Caller must first execute all original producers and independent comparisons.
    Immutable inputs/Decimal values, versions, hashes and source-duration stay exact.
    """
    expected_path, observed_path = Path(expected_path), Path(observed_path)
    byte_identical = expected_path.read_bytes() == observed_path.read_bytes()
    report = {'policy': POLICY, 'byte_identical': byte_identical,
              'metadata_differences': [], 'diagnostic_differences': [],
              'scientific_differences': [],
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
                match = re.fullmatch(r'/rows/(\d+)/([a-zA-Z0-9_]+)', change['path'])
                if (not match or change.get('missing_key') or
                        match[2] not in PORTABLE_FIELDS | {'heavy_coordinate_relative_error'}):
                    raise ValueError('CSV field is outside the explicit portability allowlist')
                index = int(match[1])
                field = match[2]
                old_json, new_json = [json.loads(path.with_suffix('.json').read_text())
                                      for path in [expected_path, observed_path]]
                if field == 'heavy_coordinate_relative_error':
                    gate = coordinate_gate(old_json, new_json, index)
                    category = 'diagnostic'
                else:
                    gate = primary_gate(old_json, new_json, 'results', index, field)
                    category = 'scientific'
                for csv_doc, json_doc in [(before, old_json), (after, new_json)]:
                    row, result = csv_doc['rows'][index], json_doc['results'][index]
                    if (row['case'], row['configuration']) != (result['case'], result['configuration']):
                        raise ValueError('CSV row identity disagrees with JSON')
                    if row[field] != str(result[field]):
                        raise ValueError('CSV portability field disagrees with JSON')
            else:
                raise ValueError('Source-duration content remains exact')
            report[category + '_differences'].append({**change, 'gate': gate})
        except (ValueError, KeyError, IndexError, TypeError, InvalidOperation) as error:
            report['scientific_or_unapproved_differences'].append({**change, 'reason': str(error)})
    report['difference_counts'] = {name: len(report[name]) for name in
                                   ['metadata_differences', 'diagnostic_differences',
                                    'scientific_differences',
                                    'scientific_or_unapproved_differences']}
    report['passed'] = not report['scientific_or_unapproved_differences']
    return report
