"""Offline acceptance of lessons 21–25. No model calls or user config edits."""
from pathlib import Path
import copy, hashlib, importlib.util, json, subprocess, tempfile
ROOT=Path(__file__).resolve().parents[1]
def load(relative):
    spec=importlib.util.spec_from_file_location(relative.replace('/','_'),ROOT/relative)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def run(relative,*args,expected=0):
    result=subprocess.run(['python3',str(ROOT/relative),*map(str,args)],capture_output=True,text=True)
    assert result.returncode==expected,(relative,result.stdout,result.stderr)
    return result

run('examples/21/batch_lab.py');run('examples/22/config_lab.py');run('examples/23/test_handoff.py')
checker=load('examples/24/asset-manifest-check/scripts/check_manifest.py')
records=load('examples/25/check_records.py');capstone=load('examples/25/verify_capstone.py')
with tempfile.TemporaryDirectory(prefix='codex-advanced-') as folder:
    temp=Path(folder)
    preview=run('examples/21/run_review.py','--repo',ROOT,'--out',temp/'preview-only')
    assert json.loads(preview.stdout)['preview'] and not (temp/'preview-only').exists()
    run('examples/21/run_review.py','--repo',ROOT,'--out',temp/'bad-timeout','--timeout',0,expected=1)
    assets=ROOT/'examples/24/fixtures/assets'
    valid=ROOT/'examples/24/fixtures/manifest.valid.csv';invalid=ROOT/'examples/24/fixtures/manifest.invalid.csv'
    assert checker.check(valid,assets)['ok']
    issues=checker.check(invalid,assets)['issues']
    assert {'path_boundary','duplicate_file','required','hash_mismatch'}<={x['code'] for x in issues}
    run('examples/24/asset-manifest-check/scripts/check_manifest.py',valid,'--asset-root',assets,'--report',temp/'assets.json')
    run('examples/24/asset-manifest-check/scripts/check_manifest.py',valid,'--asset-root',assets,'--report',temp/'assets.json',expected=2)
    run('examples/24/asset-manifest-check/scripts/check_manifest.py',invalid,'--asset-root',assets,'--report',temp/'bad-assets.json',expected=1)
    data=json.loads((ROOT/'examples/25/blank-records.json').read_text())
    assert records.check(data,ROOT/'examples/25')['not_run']==2
    fake=copy.deepcopy(data);fake['records'][0]['scores']['quality']='pass'
    try:records.check(fake,ROOT/'examples/25')
    except ValueError:pass
    else:raise AssertionError('Unrun record falsely passed')
    fake=copy.deepcopy(data);fake['performance_claim']='B is better'
    try:records.check(fake,ROOT/'examples/25')
    except ValueError:pass
    else:raise AssertionError('Unsupported performance claim passed')
    source=ROOT/'examples/20/orders.csv';bundle=temp/'report'
    run('examples/20/report.py','--out',bundle)
    before={p.name:p.read_bytes() for p in bundle.glob('*.json')}
    assert capstone.verify(bundle,source)['fixture_report']=='pass'
    run('examples/20/report.py','--out',bundle)
    assert before=={p.name:p.read_bytes() for p in bundle.glob('*.json')}
    report_path=bundle/'report.json';report=json.loads(report_path.read_text());report['total_TWD']='999.99';report_path.write_text(json.dumps(report))
    try:capstone.verify(bundle,source)
    except ValueError:pass
    else:raise AssertionError('Wrong total passed')
    report_path.write_bytes(before['report.json']);report=json.loads(report_path.read_text());report['source_sha256']='0'*64;report_path.write_text(json.dumps(report))
    try:capstone.verify(bundle,source)
    except ValueError:pass
    else:raise AssertionError('Stale source passed')
print('PASS: batch contracts/retries, config simulation, checkpoints, skill assets, honest eval records, capstone correctness/staleness/repeatability. No model/API calls.')
