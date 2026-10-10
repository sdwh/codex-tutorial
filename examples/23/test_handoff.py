"""Fixture checks are not evidence of model task success."""
import json, subprocess, tempfile
from pathlib import Path
SCRIPT = Path(__file__).with_name('handoff.py')
with tempfile.TemporaryDirectory() as td:
    base = Path(td); root = base / 'work'; root.mkdir()
    (root / 'task.txt').write_text('first\n')
    manifest = base / 'checkpoint.json'
    common = ['python3', str(SCRIPT), '--root', str(root), '--manifest', str(manifest)]
    assert subprocess.run(common + ['snapshot'], capture_output=True).returncode == 0
    assert subprocess.run(common + ['check'], capture_output=True).returncode == 0
    (root / 'task.txt').write_text('edited after handoff\n')
    r = subprocess.run(common + ['check'], capture_output=True, text=True)
    assert r.returncode == 1 and 'changed: task.txt' in r.stdout
    (root / 'task.txt').unlink()
    assert subprocess.run(common + ['check'], capture_output=True).returncode == 1
    (root / 'outside.txt').symlink_to(manifest)
    assert subprocess.run(common + ['snapshot', '--files', 'outside.txt'], capture_output=True).returncode != 0
    assert subprocess.run(common + ['snapshot', '--files', '../checkpoint.json'], capture_output=True).returncode != 0
print('5 checkpoint tests passed: fresh, changed, missing, symlink, traversal')
