#!/usr/bin/env python3
"""Compare independent algorithms to the producer's retained frozen-input data."""
from decimal import Decimal as D, localcontext
import argparse
import csv
import hashlib
import json
from pathlib import Path
import independent

ROOT = Path(__file__).resolve().parent
PRODUCER = ROOT.parent/'wilson-metric'


def mapped_case(name):
    if name.startswith('c'):
        return 'structural_'+name+'c'
    return {'adjacent_plus':'adjacent_positive','adjacent_minus':'adjacent_negative'}.get(name,name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--producer-dir', type=Path, default=PRODUCER,
                        help='Directory containing producer results.json, audit.py and REGISTRATION.md.')
    parser.add_argument('--source-root', type=Path, default=independent.SOURCE.parent,
                        help='Directory containing the public v1.23 inputs.')
    parser.add_argument('--output-dir', type=Path, default=ROOT,
                        help='Directory for comparison-results.json.')
    args = parser.parse_args()
    if args.output_dir.resolve().is_relative_to(args.source_root.resolve()):
        parser.error('Output must be outside the preserved public input directory.')
    result_path = args.producer_dir/'results.json'
    p = json.loads(result_path.read_text())
    assert p['provenance']['audit_sha256']==hashlib.sha256((args.producer_dir/'audit.py').read_bytes()).hexdigest()
    assert p['provenance']['registration_sha256']==hashlib.sha256((args.producer_dir/'REGISTRATION.md').read_bytes()).hexdigest()
    source_inputs = p['inputs']
    matched = {'k_link':source_inputs['k_link_GeV2'],
               'k_min':source_inputs['k_min_GeV2'],
               'k_top':source_inputs['k_top_GeV2'],
               'epsilon':source_inputs['epsilon_published']}
    # This second run deliberately uses precisely the retained input strings so
    # that last-bit differences in curvature reconstruction are not mistaken for
    # differences between high-precision eigenvalue methods.
    independent_rows = independent.run(110,matched)
    producer_rows = {(r['case'],r['configuration']):r for r in p['results']}
    assert len(producer_rows)==len(independent_rows)==36
    with (args.producer_dir/'results.csv').open(newline='') as handle:
        csv_rows = list(csv.DictReader(handle))
    assert len(csv_rows)==len(producer_rows)
    for csv_row in csv_rows:
        json_row = producer_rows[csv_row['case'],csv_row['configuration']]
        for key,value in csv_row.items():
            assert str(json_row[key])==value, (csv_row['case'],key,'CSV/JSON mismatch')
    maxima = {key:D(0) for key in ('light_mass_squared_relative','heavy_mass_relative',
                                  'period_shift_relative','relative_light_change_absolute')}
    comparisons = []
    state_map = {'off':'source off','minimum':'source minimum','top':'source maximum'}
    with localcontext() as ctx:
        ctx.prec = 110
        ibase = {r['state']:D(r['light_mass_squared_GeV2']) for r in independent_rows if r['case']=='baseline'}
        for independent_row in independent_rows:
            name = mapped_case(independent_row['case'])
            state = state_map[independent_row['state']]
            row = producer_rows[name,state]
            record = {'case':name,'configuration':state}
            root = D(independent_row['light_mass_squared_GeV2'])
            error = abs((D(row['light_mass_squared_GeV2'])-root)/root) if root else D(0)
            if not root:
                assert D(row['light_mass_squared_GeV2'])==0
            assert error < D('1e-70'), (name,state,error)
            maxima['light_mass_squared_relative'] = max(maxima['light_mass_squared_relative'],error)
            record['light_mass_squared_relative_error'] = str(error)
            heavy_errors = []
            for key in ('heavy_min_GeV','heavy_max_GeV'):
                reference = D(independent_row[key])
                error = abs(D(str(row[key]))/reference-1)
                assert error<D('1e-12'), (name,state,key,error)
                heavy_errors.append(error)
                maxima['heavy_mass_relative'] = max(maxima['heavy_mass_relative'],error)
            record['max_heavy_mass_relative_error'] = str(max(heavy_errors))
            delta = D(independent_row['period_relative_shift'])
            error = abs((D(row['F_over_F0_minus1'])-delta)/delta) if delta else D(0)
            if not delta:
                assert D(row['F_over_F0_minus1'])==0
            assert error<D('1e-70'), (name,state,error)
            maxima['period_shift_relative'] = max(maxima['period_shift_relative'],error)
            relative = root/ibase[independent_row['state']]-1 if root else D(0)
            error = abs(D(row['light_mass_squared_relative_change'])-relative)
            assert error < D('1e-70')
            maxima['relative_light_change_absolute'] = max(maxima['relative_light_change_absolute'],error)
            assert row['negative_modes']==int(state=='source maximum')
            assert row['exact_zero_modes']==int(state=='source off')
            comparisons.append(record)
        reconstructed = independent.published_inputs(args.source_root/'v1.23_summary.json')
        input_deltas = {name: str(abs(D(str(reconstructed[name]))/D(value)-1)) for name,value in matched.items()}
        assert all(D(value)<D('1e-14') for value in input_deltas.values())
    checks = p['checks']
    assert len(checks)>=210 and all(row['passed'] for row in checks)
    for name,expected in source_inputs['source_files_sha256'].items():
        source = args.source_root/name
        assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
    out = {'status':'PASS independent implementation comparison',
           'scope':'Same assumed metrics and precisely matched frozen inputs; no physical matching or peer-review claim.',
           'producer_results_sha256':hashlib.sha256(result_path.read_bytes()).hexdigest(),
           'producer_csv_sha256':hashlib.sha256((args.producer_dir/'results.csv').read_bytes()).hexdigest(),
           'producer_script_sha256':hashlib.sha256((args.producer_dir/'audit.py').read_bytes()).hexdigest(),
           'registration_sha256':hashlib.sha256((args.producer_dir/'REGISTRATION.md').read_bytes()).hexdigest(),
           'independent_script_sha256':hashlib.sha256((ROOT/'independent.py').read_bytes()).hexdigest(),
           'comparison_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'case_state_rows_compared':len(comparisons), 'csv_rows_matched_to_json':len(csv_rows),
           'producer_checks_passed':len(checks),
           'maximum_errors':{key:str(value) for key,value in maxima.items()},
           'independently_reconstructed_input_relative_differences':input_deltas,
           'comparisons':comparisons}
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'comparison-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='comparisons'},indent=2))


if __name__=='__main__':
    main()
