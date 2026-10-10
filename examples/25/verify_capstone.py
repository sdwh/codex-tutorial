"""Check the fixed synthetic 20-unit report output, not model behaviour."""
import argparse, hashlib, json
from pathlib import Path
from decimal import Decimal


def verify(bundle, source):
    report = json.loads((bundle / 'report.json').read_text())
    state = json.loads((bundle / 'state.json').read_text())
    errors = json.loads((bundle / 'errors.json').read_text())
    expected_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if report['source_sha256'] != expected_hash or state['source_sha256'] != expected_hash:
        raise ValueError('source mismatch: output is stale')
    expected = {'input_rows': 5, 'accepted': 2, 'duplicates': 1, 'rejected': 2, 'total_TWD': '300.30'}
    for key, value in expected.items():
        if report[key] != value:
            raise ValueError(f'wrong fixed-fixture result: {key}')
    if sorted(r['order_id'] for r in report['rows']) != ['A001', 'A002']:
        raise ValueError('accepted order IDs mismatch')
    if {e['line'] for e in errors} != {5, 6} or len(errors) != 2:
        raise ValueError('wrong rejection evidence')
    if sum(Decimal(r['amount']) for r in report['rows']) != Decimal('300.30'):
        raise ValueError('independent total mismatch')
    if state['status'] != 'completed':
        raise ValueError('batch not completed')
    return {'fixture_report': 'pass', 'model_effectiveness': None,
            'trigger_observed': None, 'publishing_performed': False}

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--bundle', type=Path, required=True)
    ap.add_argument('--source', type=Path, required=True); a = ap.parse_args()
    print(json.dumps(verify(a.bundle, a.source)))
