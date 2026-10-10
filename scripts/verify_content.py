"""Check curriculum contract, authored HTML, referenced examples and code syntax.
No network access or paid API calls.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import ast,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'content/curriculum.json').read_text())
lessons=catalog['lessons']
assert len(lessons)==20 and sum(x['minutes'] for x in lessons)==2400
assert all(x['minutes']==120 for x in lessons)
class Fragment(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True);self.code=[];self.copies=[];self.ids=[];self.refs=[];self.in_code=False;self.current='';self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if 'data-copy-target' in a:self.copies.append(a['data-copy-target'])
        if 'href' in a:self.refs.append(a['href'])
        if tag=='code':self.in_code=True;self.current=''
        assert tag not in ['script','iframe','object'],f'Unexpected authored tag: {tag}'
    def handle_data(self,data):
        if self.in_code:self.current+=data
    def handle_endtag(self,tag):
        if tag=='code':self.code.append(self.current);self.in_code=False
for item in lessons[12:]:
    d=json.loads((ROOT/f'content/lessons/{item["id"]}.json').read_text())
    assert d['id']==item['id'] and d['slug']==item['slug']
    assert d['minutes']==120 and sum(x['minutes'] for x in d['schedule'])==120
    assert len(d['sections'])>=6 and len(d['prerequisites'])>=1 and len(d['outcomes'])>=3
    assert len(d['checklist'])>=3 and len(d['quiz']['options'])>=2
    assert sum(x['correct'] is True for x in d['quiz']['options'])==1
    assert d['reviewed']==catalog['reviewed'] and len(d['sources'])>=1
    for source in d['sources']:
        assert source['supports'] and urlsplit(source['url']).scheme=='https'
    text=''.join(s['html'] for s in d['sections']);parsed=Fragment(text)
    assert parsed.copies,f'No copyable task: {item["id"]}'
    assert len(parsed.ids)==len(set(parsed.ids))
    for target in parsed.copies:assert target in parsed.ids,f'Missing copy target {target}'
    for ref in parsed.refs:
        if not urlsplit(ref).scheme and not ref.startswith('#'):
            assert (ROOT/ref).exists(),f'Missing local example {ref}'
    han=len(re.findall(r'[\u4e00-\u9fff]',text))
    assert han>=1200,f'Lesson {item["id"]} insufficient detail: {han} Han characters'
    print(f'{item["id"]}: {len(d["sections"])} sections, 120min, {han} Han characters, {len(d["sources"])} primary sources')
for path in (ROOT/'examples').rglob('*.py'):
    ast.parse(path.read_text(),filename=str(path))
for path in (ROOT/'examples').rglob('*.json'):
    json.loads(path.read_text())
print('Content contract, downloadable examples and Python syntax passed; total 40 hours.')
