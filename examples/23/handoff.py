"""Read-only repository checkpoint verifier. Python 3.10+, no model calls."""
import argparse, hashlib, json, subprocess
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_read(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def safe_file(root, name):
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('only root-relative paths are allowed')
    path = root / relative
    if path.is_symlink() or root not in path.resolve().parents:
        raise ValueError('symlinks/out-of-root paths are not allowed')
    if not path.is_file():
        raise ValueError(f'missing file: {name}')
    return path


def snapshot(root, files):
    return {'schema': 1, 'root': str(root.resolve()),
            'git_head': git_read(root, 'rev-parse', 'HEAD'),
            'git_status': git_read(root, 'status', '--porcelain=v1'),
            'files': {name: digest(safe_file(root, name)) for name in files},
            'goal': 'Prepare a synthetic local review draft',
            'constraints': ['No network', 'No deletion', 'No publishing'],
            'next': 'Check hashes, then validate timestamps and totals',
            'session_id': None, 'last_validation': None}


def check(root, manifest):
    errors = []
    if manifest['root'] != str(root.resolve()):
        errors.append('root directory changed; confirm task identity')
    for name, expected in manifest['files'].items():
        try:
            if digest(safe_file(root, name)) != expected:
                errors.append(f'changed: {name}')
        except ValueError as exc:
            errors.append(str(exc))
    if git_read(root, 'rev-parse', 'HEAD') != manifest['git_head']:
        errors.append('git HEAD changed')
    if git_read(root, 'status', '--porcelain=v1') != manifest['git_status']:
        errors.append('git working tree status changed; inspect diff')
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['snapshot', 'check'])
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--manifest', type=Path, required=True)
    ap.add_argument('--files', nargs='+', default=['task.txt'])
    args = ap.parse_args(); root = args.root.resolve()
    if args.mode == 'snapshot':
        data = snapshot(root, args.files)
        # Keep the manifest outside root, so its own creation does not change git status.
        if root == args.manifest.resolve() or root in args.manifest.resolve().parents:
            raise ValueError('manifest must be outside the checkpoint root')
        args.manifest.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        print('checkpoint written; no validation has been run')
    else:
        errors = check(root, json.loads(args.manifest.read_text()))
        print(json.dumps({'fresh': not errors, 'differences': errors}))
        raise SystemExit(1 if errors else 0)

if __name__ == '__main__':
    main()
