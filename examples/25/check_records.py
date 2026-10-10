"""Validate evaluation records; never evaluates model semantics or calls an API."""
import argparse, hashlib, json, math
from pathlib import Path
DIMS = ['trigger', 'boundary', 'format', 'quality']
VERDICTS = {'pass', 'partial', 'fail', 'unobserved', 'not-applicable'}


def evidence_file(root, name):
    if not isinstance(name, str) or not name:
        raise ValueError('evidence path must be a nonempty string')
    rel = Path(name)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('evidence path must be root-relative')
    path = root / rel
    if path.is_symlink() or root.resolve() not in path.resolve().parents or not path.is_file():
        raise ValueError('evidence missing or outside root')
    return path


def check(data, root):
    if data.get('performance_claim') is not None:
        raise ValueError('this teaching recorder makes no aggregate performance claim')
    records = data['records']; ids = [r['id'] for r in records]
    if sorted(ids) != ['A1', 'B1']:
        raise ValueError('expected exactly A1 and B1')
    for r in records:
        if r['status'] not in {'not-run', 'completed', 'interrupted'}:
            raise ValueError('invalid run status')
        if set(r['scores']) != set(DIMS):
            raise ValueError('missing dimension')
        if r['status'] == 'not-run':
            if r['seconds'] is not None or any(v is not None for v in r['scores'].values()) or r['evidence']:
                raise ValueError('unrun record must have null scores/time and no evidence')
            continue
        secs = r['seconds']
        if secs is not None and (isinstance(secs, bool) or not isinstance(secs, (int, float)) or not math.isfinite(secs) or secs < 0):
            raise ValueError('invalid measured time')
        if not isinstance(r['model'], str) or not r['model']:
            raise ValueError('record actual model label or unknown')
        for dim, verdict in r['scores'].items():
            if verdict not in VERDICTS:
                raise ValueError('invalid score')
            note = r['evidence'].get(dim)
            if not isinstance(note, dict) or not note.get('reason'):
                raise ValueError('every observed/unknown dimension needs a reason')
            if verdict in {'pass', 'partial', 'fail'}:
                evidence_file(root, note.get('path'))
        input_path = evidence_file(root, r['input_path'])
        if hashlib.sha256(input_path.read_bytes()).hexdigest() != r['input_sha256']:
            raise ValueError('input hash mismatch')
    return {'not_run': sum(r['status'] == 'not-run' for r in records),
            'completed': sum(r['status'] == 'completed' for r in records), 'performance_claim': None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--records', type=Path, default=Path(__file__).with_name('blank-records.json'))
    ap.add_argument('--evidence-root', type=Path, default=Path(__file__).parent)
    args = ap.parse_args()
    print(json.dumps(check(json.loads(args.records.read_text()), args.evidence_root)))

if __name__ == '__main__':
    main()
