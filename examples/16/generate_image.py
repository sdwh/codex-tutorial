import argparse, base64, json, os
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument('--execute', action='store_true')
a = p.parse_args()
request = dict(model='gpt-image-2.5-sunburst',
    prompt='A single friendly teal robot reading a book, isolated, no text, transparent background',
    size='1024x1024', quality='low', background='transparent', output_format='png', n=1)
out = Path('output'); out.mkdir(exist_ok=True)
(out / 'request.json').write_text(json.dumps(request, indent=2), encoding='utf-8')
if not a.execute:
    print('DRY RUN: output/request.json; no API call')
else:
    if not os.environ.get('OPENAI_API_KEY'):
        raise SystemExit('Missing OPENAI_API_KEY')
    from openai import OpenAI
    result = OpenAI().images.generate(**request)
    if not result.data or not result.data[0].b64_json:
        raise RuntimeError('No image returned')
    (out / 'robot.png').write_bytes(base64.b64decode(result.data[0].b64_json, validate=True))
    (out / 'usage.json').write_text(json.dumps(result.usage.model_dump() if result.usage else {}, indent=2))
    print('Saved output/robot.png')
