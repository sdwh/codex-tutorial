"""Offline MIME lab, Python 3.10+. Never sends mail or opens a socket."""
import argparse, hashlib, json
from pathlib import Path
from email import policy
from email.parser import BytesParser


def parse(raw):
    msg = BytesParser(policy=policy.default).parsebytes(raw)
    body = msg.get_body(preferencelist=('plain',))
    text = body.get_content() if body else ''
    attachments = [{'filename': p.get_filename(), 'type': p.get_content_type(),
                    'bytes': len(p.get_payload(decode=True) or b'')}
                   for p in msg.iter_attachments()]
    category = '待人工檢查' if attachments or not text else ('帳務' if 'invoice' in str(msg['Subject']).lower() else '一般')
    return {'subject': str(msg['Subject'] or ''), 'from': str(msg['From'] or ''),
            'body_preview': text[:160], 'category': category,
            'attachments': attachments, 'defects': [str(d) for p in msg.walk() for d in p.defects],
            'draft': '草稿：已收到來信，將由承辦人確認內容後回覆。', 'send': False}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, default=Path('mail-output'))
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    state_file = args.out / 'state.json'
    state = json.loads(state_file.read_text()) if state_file.exists() else {'processed': []}
    completed = set(state['processed'])
    count = skipped = 0
    for path in sorted((Path(__file__).parent / 'fixtures').glob('*.eml')):
        raw = path.read_bytes()
        # A real mailbox uses account+server+UIDL, not this offline fixture hash.
        key = hashlib.sha256(raw).hexdigest()
        if key in completed:
            skipped += 1
            continue
        result = parse(raw)
        if not args.dry_run:
            args.out.mkdir(parents=True, exist_ok=True)
            tmp = args.out / (key + '.tmp')
            tmp.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
            tmp.replace(args.out / (key + '.json'))
            completed.add(key)  # Only acknowledge after output exists.
            tmp_state = args.out / 'state.tmp'
            tmp_state.write_text(json.dumps({'processed': sorted(completed)}), encoding='utf-8')
            tmp_state.replace(state_file)
        count += 1
    print(json.dumps({'new': count, 'skipped': skipped, 'dry_run': args.dry_run}))

if __name__ == '__main__':
    main()
