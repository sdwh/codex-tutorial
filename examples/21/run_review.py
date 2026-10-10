"""Optional live CLI wrapper. Default preview does not write files or call Codex."""
import argparse, hashlib, json, subprocess
from pathlib import Path
from batch_lab import accept
BASE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--timeout',type=int,default=180)
    args=parser.parse_args()
    repo=args.repo.resolve();out=args.out.resolve()
    if not repo.is_dir() or not (repo/'README.md').is_file():
        raise SystemExit('Expected a repository directory containing README.md')
    if args.timeout<1 or args.timeout>1800:raise SystemExit('timeout must be 1..1800 seconds')
    prompt=(BASE/'prompt.txt').read_text(encoding='utf-8')
    command=['codex','exec','-C',str(repo),'--sandbox','read-only','--json',
             '--output-schema',str(BASE/'schema.json'),'-o',str(out/'result.json'),'-']
    metadata={'input_sha256':hashlib.sha256((repo/'README.md').read_bytes()).hexdigest(),
              'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),
              'command':command,'timeout':args.timeout,'model_observation':None}
    if not args.execute:
        print(json.dumps({'preview':True,**metadata},indent=2));return 0
    out.mkdir(parents=True,exist_ok=False)
    try:
        result=subprocess.run(command,input=prompt,text=True,capture_output=True,cwd=repo,timeout=args.timeout)
    except (subprocess.TimeoutExpired,OSError) as error:
        metadata.update(status='runtime-failed',error=str(error))
        (out/'run.json').write_text(json.dumps(metadata,indent=2));return 2
    (out/'events.jsonl').write_text(result.stdout,encoding='utf-8')
    (out/'stderr.log').write_text(result.stderr,encoding='utf-8')
    metadata['process_returncode']=result.returncode
    metadata['acceptance']='not-evaluated'
    if result.returncode==0:
        try:metadata['acceptance']=accept(json.loads((out/'result.json').read_text()))
        except (OSError,ValueError):metadata['acceptance']='missing-or-invalid-artifact'
    metadata['status']='completed' if result.returncode==0 and metadata['acceptance']=='accepted' else 'rejected'
    (out/'run.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    print(json.dumps(metadata,indent=2))
    return 0 if metadata['status']=='completed' else 1

if __name__=='__main__':raise SystemExit(main())
