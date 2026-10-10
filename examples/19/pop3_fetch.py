"""Optional live reader. NOT part of offline lab. Provider must permit USER/PASS."""
import getpass, json, os, poplib, ssl
from pathlib import Path


def fetch():
    host = os.environ['POP3_HOST']
    user = os.environ['POP3_USER']
    out = Path('private-mail')
    out.mkdir(exist_ok=True)
    state_file = out / 'uidl-state.json'
    state = json.loads(state_file.read_text()) if state_file.exists() else {}
    account = host + ':' + user
    seen = set(state.get(account, []))
    client = poplib.POP3_SSL(host, 995, timeout=120, context=ssl.create_default_context())
    try:
        client.user(user)
        client.pass_(getpass.getpass('App password (never printed): '))
        for line in client.uidl()[1]:
            number, uid = line.decode('ascii').split()
            if uid in seen:
                continue
            raw = b'\r\n'.join(client.retr(int(number))[1]) + b'\r\n'
            # Use a hash as filename: never trust remote UIDL as a path.
            import hashlib
            name = hashlib.sha256((account + ':' + uid).encode()).hexdigest()
            tmp = out / (name + '.tmp')
            tmp.write_bytes(raw)
            tmp.replace(out / (name + '.eml'))
            seen.add(uid)
            state[account] = sorted(seen)
            tmp_state = out / 'uidl-state.tmp'
            tmp_state.write_text(json.dumps(state), encoding='utf-8')
            tmp_state.replace(state_file)
            break  # At most one new message in this introductory reader.
    finally:
        client.quit()

if __name__ == '__main__':
    raise SystemExit('Live connection disabled. Review provider settings and code before explicitly calling fetch().')
