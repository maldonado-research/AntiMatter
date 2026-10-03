"""Narrow, explicit archival comparison policy; never alter scientific artifacts."""
import csv
from decimal import Decimal, InvalidOperation, localcontext
import json
import math
from pathlib import Path
import re


POLICY = 'candidate-portability-v3'
BOUND = Decimal('2e-12')
HEAVY_BOUND = Decimal('1e-12')
PORTABLE_FIELDS = {'heavy_min_GeV', 'heavy_max_GeV',
                   'heavy_min_relative_change', 'heavy_max_relative_change',
                   'metric_correction_operator_norm'}
SOURCE_FIXED = {'T_i_GeV', 'theta_i_rad', 'Delta_N_total', 'initial_E_phi_GeV4'}
SOURCE_ENDPOINTS = {'theta_star_rad', 'p_star', 'K_star_GeV4', 'V_star_GeV4',
                    'u_site0_star_signed', 'rho_phi_over_rho_rad_star',
                    'H_star_over_H_radiation_star', 'conditional_n_eta_for_final_instant'}
SOURCE_DERIVED = {'theta_dot_star_GeV', 'a_field_dot_star_GeV2', 'E_phi_star_GeV4',
                  'rho_rad_star_GeV4', 'rho_kin_over_rho_rad_star',
                  'integrated_Hubble_loss_GeV4', 'final_scalar_ledger_residual_GeV4'}
SOURCE_DIAGNOSTICS = {'max_scalar_ledger_abs_error_over_A', 'max_scalar_ledger_rel_initial_error',
                      'max_radiation_ledger_rel_initial_error', 'max_radiation_analytic_rel_error',
                      'max_scalar_energy_over_initial', 'min_K_over_A', 'min_V_over_A',
                      'min_radiation_over_A', 'min_H2_over_m2', 'nfev', 'loose_nfev',
                      'tolerance_endpoint_max_natural_scale_difference',
                      'loose_max_scalar_ledger_abs_error_over_A'}
SOURCE_CHECKS = {'all_initial_energies_at_most_2A', 'all_sampled_energies_nonnegative_and_H_positive',
                 'scalar_ledger_below_1e_minus_7_A', 'no_scalar_energy_above_initial_beyond_1e_minus_7_relative',
                 'radiation_analytic_error_below_1e_minus_8', 'radiation_ledger_error_below_1e_minus_8',
                 'two_tolerance_endpoint_agreement_below_1e_minus_7', 'bottom_and_hilltop_at_rest',
                 'reflection_below_1e_minus_7', 'Bessel_controls_below_3e_minus_7', 'public_inputs_unchanged'}
SOURCE_CONTROL_FIELDS = {
    'bottom': {'max_abs_phase_departure', 'max_abs_p', 'scalar_ledger_error_over_A'},
    'hilltop': {'max_abs_phase_departure', 'max_abs_p', 'scalar_ledger_error_over_A'},
    'reflection': {'endpoint_phase_sum', 'endpoint_velocity_sum', 'endpoint_energy_difference_over_A'},
    'linear_radiation_Bessel': {'max_phase_abs_error_over_initial_phase', 'max_p_abs_error_over_initial_phase', 'max_scalar_ledger_rel_initial_error'},
    'full_small_angle_Bessel': {'max_phase_abs_error_over_initial_phase', 'max_p_abs_error_over_initial_phase', 'max_scalar_ledger_rel_initial_error'},
}
SOURCE_SUMMARIES = {
    'max_scalar_ledger_error_over_A': 'max_scalar_ledger_abs_error_over_A',
    'max_scalar_ledger_rel_initial_error': 'max_scalar_ledger_rel_initial_error',
    'max_radiation_analytic_rel_error': 'max_radiation_analytic_rel_error',
    'max_radiation_ledger_rel_initial_error': 'max_radiation_ledger_rel_initial_error',
    'max_tolerance_endpoint_natural_scale_difference': 'tolerance_endpoint_max_natural_scale_difference',
    'max_scalar_energy_over_initial': 'max_scalar_energy_over_initial',
}


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


def source_duration_gate(before, after):
    """New archival semantic comparison, reusing original endpoint/control gates."""
    variable = {'trajectories', 'controls', 'largest_sampled_endpoint_K', 'summaries'}
    fixed = {'date_user_facing', 'host_date', 'status', 'scope', 'software',
             'registration_sha256', 'audit_py_sha256', 'public_source_sha256',
             'parameters', 'duration_bounds', 'checks'}
    for document in [before, after]:
        if set(document) != variable | fixed:
            raise ValueError('Unknown or missing source-duration root field')
    for key in fixed:
        if differences(before[key], after[key]):
            raise ValueError('Changed frozen source-duration field: ' + key)
    if before['status'] != 'PASS':
        raise ValueError('Source-duration status must remain PASS')
    measurements = []
    for document in [before, after]:
        if set(document['checks']) != SOURCE_CHECKS or not all(value is True for value in document['checks'].values()):
            raise ValueError('All 11 original source checks must remain present and true')
        rows, parameters = document['trajectories'], document['parameters']
        if len(rows) != 30:
            raise ValueError('Registered source grid must contain all 30 ordered rows')
        amplitude = float(number(parameters['A_GeV4']))
        if amplitude <= 0:
            raise ValueError('Source amplitude must be positive')
        if set(document['controls']) != set(SOURCE_CONTROL_FIELDS):
            raise ValueError('Unknown or missing source control')
        for label, fields in SOURCE_CONTROL_FIELDS.items():
            control = document['controls'][label]
            if set(control) != fields:
                raise ValueError('Changed source control schema: ' + label)
            for field, value in control.items():
                value = float(number(value))
                if label == 'reflection':
                    valid = abs(value) < 1e-7
                elif field in {'max_phase_abs_error_over_initial_phase', 'max_p_abs_error_over_initial_phase'}:
                    valid = 0 <= value < 3e-7
                elif field == 'max_scalar_ledger_rel_initial_error':
                    valid = value >= 0  # Original Bessel ledger diagnostic has no numerical acceptance bound.
                else:
                    valid = 0 <= value < 1e-7
                if not valid:
                    raise ValueError('Original source control criterion failed: ' + label + '/' + field)
        for row in rows:
            if set(row) != SOURCE_FIXED | SOURCE_ENDPOINTS | SOURCE_DERIVED | SOURCE_DIAGNOSTICS:
                raise ValueError('Unknown or missing source trajectory field')
            for value in row.values():
                number(value)
            conditions = [
                0 <= row['initial_E_phi_GeV4'] <= 2 * amplitude,
                row['min_K_over_A'] >= 0, row['min_V_over_A'] >= 0,
                row['min_radiation_over_A'] > 0, row['min_H2_over_m2'] > 0,
                0 <= row['max_scalar_ledger_abs_error_over_A'] < 1e-7,
                0 <= row['loose_max_scalar_ledger_abs_error_over_A'] < 1e-7,
                0 <= row['max_scalar_energy_over_initial'] < 1 + 1e-7,
                0 <= row['max_radiation_analytic_rel_error'] < 1e-8,
                0 <= row['max_radiation_ledger_rel_initial_error'] < 1e-8,
                0 <= row['tolerance_endpoint_max_natural_scale_difference'] < 1e-7,
                row['max_scalar_ledger_rel_initial_error'] >= 0,
                type(row['nfev']) is int and row['nfev'] > 0,
                type(row['loose_nfev']) is int and row['loose_nfev'] > 0,
                row['K_star_GeV4'] >= 0, row['V_star_GeV4'] >= 0,
                row['rho_rad_star_GeV4'] > 0, row['integrated_Hubble_loss_GeV4'] >= 0,
                row['conditional_n_eta_for_final_instant'] > 0,
                row['theta_dot_star_GeV'] == parameters['m_GeV'] * row['p_star'],
                row['a_field_dot_star_GeV2'] == math.sqrt(amplitude) * row['p_star'],
                row['H_star_over_H_radiation_star'] == math.sqrt(1 + row['rho_phi_over_rho_rad_star']),
                row['conditional_n_eta_for_final_instant'] == 16 * math.sqrt(parameters['rho_kin_16_GeV4'] / row['K_star_GeV4']),
                abs(row['rho_rad_star_GeV4'] / parameters['rho_rad_star_GeV4'] - 1) < 1e-8,
                abs((row['E_phi_star_GeV4'] - row['K_star_GeV4'] - row['V_star_GeV4']) / amplitude) < 1e-7,
                abs(row['rho_phi_over_rho_rad_star'] - row['E_phi_star_GeV4'] / row['rho_rad_star_GeV4']) < 1e-7,
                abs(row['rho_kin_over_rho_rad_star'] - row['K_star_GeV4'] / row['rho_rad_star_GeV4']) < 1e-7,
                abs((row['E_phi_star_GeV4'] + row['integrated_Hubble_loss_GeV4'] - row['initial_E_phi_GeV4']) / amplitude) < 1e-7,
                abs(row['final_scalar_ledger_residual_GeV4'] / amplitude) < 1e-7,
            ]
            if not all(conditions):
                raise ValueError('Original source controls or derived endpoint consistency failed')
        if set(document['summaries']) != set(SOURCE_SUMMARIES):
            raise ValueError('Unknown or missing source summary')
        for field, row_field in SOURCE_SUMMARIES.items():
            if document['summaries'][field] != max(row[row_field] for row in rows):
                raise ValueError('Source summary does not match generated row extrema')
        maximum = max(rows, key=lambda row: row['K_star_GeV4'])
        if differences(document['largest_sampled_endpoint_K'], maximum):
            raise ValueError('Largest-sample record does not exactly match generated maximum row')
    for index, (old, new) in enumerate(zip(before['trajectories'], after['trajectories'])):
        if any(differences(old[key], new[key]) for key in SOURCE_FIXED):
            raise ValueError('Changed source initial state or ordered grid at row ' + str(index))
        amplitude = before['parameters']['A_GeV4']
        delta = {key: abs(new[key] - old[key]) / (amplitude if key in {'K_star_GeV4', 'V_star_GeV4'} else 1)
                 for key in SOURCE_ENDPOINTS - {'conditional_n_eta_for_final_instant'}}
        delta['conditional_n_eta_for_final_instant'] = abs(new['conditional_n_eta_for_final_instant'] / old['conditional_n_eta_for_final_instant'] - 1)
        if not all(value < 1e-7 for value in delta.values()):
            raise ValueError('Archived/fresh physical endpoint exceeds original 1e-7 criterion at row ' + str(index))
        measurements.append({'row': index, 'T_i_GeV': new['T_i_GeV'], 'theta_i_rad': new['theta_i_rad'], 'differences': delta})
    if any(before['largest_sampled_endpoint_K'][key] != after['largest_sampled_endpoint_K'][key]
           for key in ['T_i_GeV', 'theta_i_rad']):
        raise ValueError('Changed largest-sample identity')
    return {'passed': True, 'criterion': 'Eight original independent endpoint measures < 1e-7; all original controls pass',
            'gate_scope': 'New portable archival comparison reusing original criteria; not preregistered new verification',
            'physical_endpoint_differences': measurements,
            'original_checks': sorted(SOURCE_CHECKS)}


def source_json_gate(change, validation):
    if (change.get('missing_key') or 'expected' not in change or 'observed' not in change
            or type(change['expected']) is not type(change['observed'])):
        raise ValueError('Missing source field, changed shape or changed value type')
    match = re.fullmatch(r'/trajectories/(\d+)/([a-zA-Z0-9_]+)', change['path'])
    largest = re.fullmatch(r'/largest_sampled_endpoint_K/([a-zA-Z0-9_]+)', change['path'])
    if match or largest:
        field = match[2] if match else largest[1]
        if field in SOURCE_ENDPOINTS | SOURCE_DERIVED:
            return 'scientific', {'criterion': validation['criterion'], 'gate_scope': validation['gate_scope']}
        if field in SOURCE_DIAGNOSTICS:
            return 'diagnostic', {'criterion': 'Explicit finite solver diagnostic; all original source controls pass'}
    if re.fullmatch(r'/controls/[a-zA-Z0-9_]+/[a-zA-Z0-9_]+', change['path']) or re.fullmatch(r'/summaries/[a-zA-Z0-9_]+', change['path']):
        return 'diagnostic', {'criterion': 'Original control/schema gates and exact generated summary extrema'}
    raise ValueError('Source field is outside the explicit semantic portability allowlist')


def compare_artifact(relative, expected_path, observed_path):
    """Compare one producer artifact and return complete, JSON-safe evidence.

    Caller must first execute all original producers and independent comparisons.
    Immutable inputs/Decimal values, versions and hashes stay exact.
    """
    if relative not in {'wilson-metric/results.json', 'wilson-metric/results.csv',
                        'source-duration/results.json', 'source-duration/trajectories.csv',
                        'source-duration/duration_bounds.csv'}:
        raise ValueError('Unknown producer artifact')
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
    source_error = None
    if relative.startswith('source-duration/'):
        try:
            old_source, new_source = (before, after) if relative.endswith('.json') else [
                json.loads(path.with_name('results.json').read_text()) for path in [expected_path, observed_path]]
            source_validation = source_duration_gate(old_source, new_source)
            report['source_semantic_checks'] = source_validation
            if relative.endswith('.csv'):
                section = 'trajectories' if relative.endswith('trajectories.csv') else 'duration_bounds'
                for csv_doc, source_doc in [(before, old_source), (after, new_source)]:
                    rows = source_doc[section]
                    if csv_doc['columns'] != list(rows[0]) or len(csv_doc['rows']) != len(rows):
                        raise ValueError('Source CSV columns, order or count disagree with JSON')
                    for csv_row, json_row in zip(csv_doc['rows'], rows):
                        if any(csv_row[key] != str(json_row[key]) for key in csv_doc['columns']):
                            raise ValueError('Source CSV cell does not exactly match corresponding JSON')
        except (ValueError, KeyError, IndexError, TypeError, InvalidOperation, ZeroDivisionError) as error:
            source_error = str(error)
            report['source_semantic_checks'] = {'passed': False, 'error': source_error}
            report['scientific_or_unapproved_differences'].append({'path': '/source_semantic_gate', 'reason': source_error})
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
            elif relative == 'source-duration/results.json':
                if source_error:
                    raise ValueError(source_error)
                category, gate = source_json_gate(change, source_validation)
            elif relative == 'source-duration/trajectories.csv':
                if source_error:
                    raise ValueError(source_error)
                match = re.fullmatch(r'/rows/(\d+)/([a-zA-Z0-9_]+)', change['path'])
                if not match or match[2] not in SOURCE_ENDPOINTS | SOURCE_DERIVED | SOURCE_DIAGNOSTICS:
                    raise ValueError('Source CSV field is outside explicit portability allowlist')
                category = 'diagnostic' if match[2] in SOURCE_DIAGNOSTICS else 'scientific'
                gate = {'criterion': source_validation['criterion'], 'gate_scope': source_validation['gate_scope']}
            else:
                raise ValueError('Duration bounds or unknown artifacts remain exact')
            report[category + '_differences'].append({**change, 'gate': gate})
        except (ValueError, KeyError, IndexError, TypeError, InvalidOperation) as error:
            report['scientific_or_unapproved_differences'].append({**change, 'reason': str(error)})
    report['difference_counts'] = {name: len(report[name]) for name in
                                   ['metadata_differences', 'diagnostic_differences',
                                    'scientific_differences',
                                    'scientific_or_unapproved_differences']}
    report['passed'] = not report['scientific_or_unapproved_differences']
    return report
