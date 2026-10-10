"""Offline manifest checker, schema v1. Python 3.10+, standard library only."""
import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

REQUIRED = ('file', 'purpose', 'source', 'rights', 'sha256')

def check(manifest, asset_root):
    root = Path(asset_root).resolve(strict=True)
    issues, seen, count = [], set(), 0
    with Path(manifest).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or any(k not in reader.fieldnames for k in REQUIRED):
            return {'schema': 'asset-manifest-v1', 'rows': 0, 'ok': False,
                    'issues': [{'row': 1, 'code': 'columns'}]}
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            return {'schema': 'asset-manifest-v1', 'rows': 0, 'ok': False,
                    'issues': [{'row': 1, 'code': 'duplicate_columns'}]}
        for row_no, row in enumerate(reader, 2):
            count += 1
            if None in row:
                issues.append({'row': row_no, 'code': 'extra_values'})
            missing = [k for k in REQUIRED if not (row.get(k) or '').strip()]
            if missing:
                issues.append({'row': row_no, 'code': 'required', 'fields': missing})
            name = (row.get('file') or '').strip()
            if not name:
                continue
            relative = Path(name)
            if relative.is_absolute() or '..' in relative.parts:
                issues.append({'row': row_no, 'code': 'path_boundary'})
                continue
            normalized = relative.as_posix()
            if normalized in seen:
                issues.append({'row': row_no, 'code': 'duplicate_file'})
            seen.add(normalized)
            target = root / relative
            if any(p.is_symlink() for p in [target, *target.parents] if p != root):
                issues.append({'row': row_no, 'code': 'symlink'})
                continue
            resolved = target.resolve()
            if not resolved.is_relative_to(root):
                issues.append({'row': row_no, 'code': 'path_boundary'})
                continue
            if not target.is_file():
                issues.append({'row': row_no, 'code': 'missing_file'})
                continue
            expected = (row.get('sha256') or '').strip()
            if not re.fullmatch('[0-9a-f]{64}', expected):
                issues.append({'row': row_no, 'code': 'hash_format'})
            elif hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                issues.append({'row': row_no, 'code': 'hash_mismatch'})
    if not count:
        issues.append({'row': 1, 'code': 'empty_manifest'})
    return {'schema': 'asset-manifest-v1', 'rows': count, 'ok': not issues, 'issues': issues}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('manifest')
    parser.add_argument('--asset-root', required=True)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    try:
        report = check(args.manifest, args.asset_root)
        # Exclusive create prevents accidental replacement of previous evidence.
        with Path(args.report).open('x', encoding='utf-8') as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
    except (OSError, ValueError, csv.Error) as error:
        print(f'CHECK ERROR: {error}', file=sys.stderr)
        return 2
    print('PASS' if report['ok'] else 'ISSUES')
    return 0 if report['ok'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
