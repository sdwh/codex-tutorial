"""Static integrity and browser acceptance checks. Needs playwright and Chromium.
Run: python3 scripts/verify_site.py [http://127.0.0.1:8765]
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Document(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.refs=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for k in ('href','src'):
            if k in a:self.refs.append(a[k])
catalog=json.loads((ROOT/'content/curriculum.json').read_text())
lesson_count=len(catalog['lessons'])
assert lesson_count==25 and sum(l['minutes'] for l in catalog['lessons'])==3000
docs={p.name:Document(p.read_text()) for p in ROOT.glob('*.html')}
for lesson in catalog['lessons']:
    info=lesson['surface']
    assert all(info.get(key) for key in ['entry','environment','operation','transfer'])
    document=docs[lesson['slug']+'.html']
    assert document.ids.count('lesson-surface')==1
    assert 'surfaces.html' in document.refs
assert 'surfaces.html' in docs and 'surfaces.html' in docs['index.html'].refs
assert 'surfaces.html' in (ROOT/'sitemap.xml').read_text()

for name,doc in docs.items():
    assert len(doc.ids)==len(set(doc.ids)),f'{name}: duplicate IDs'
    for ref in doc.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=unquote(u.path).lstrip('/') or (name if u.fragment else 'index.html')
        assert (ROOT/target).exists(),f'{name}: missing {ref}'
        if u.fragment and target in docs:assert u.fragment in docs[target].ids,f'{name}: missing anchor {ref}'
ET.parse(ROOT/'sitemap.xml');json.loads((ROOT/'site.webmanifest').read_text())
print(f'Static checks passed: {len(docs)} HTML pages, local links, anchors, sitemap, manifest',flush=True)
from playwright.sync_api import sync_playwright,expect
url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8765'
with sync_playwright() as pw:
    browser=pw.chromium.launch()
    ctx=browser.new_context(viewport={'width':1440,'height':1000},permissions=['clipboard-read','clipboard-write'],color_scheme='light',reduced_motion='reduce')
    errors=[];page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    # Network requests are checked for local assets; optional external font failure is separate.
    responses=[];page.on('response',lambda res:responses.append((res.url,res.status)))
    for width in [1440,390,320]:
        page.set_viewport_size({'width':width,'height':1000})
        for name in docs:
            page.goto(f'{url}/{name}',wait_until='load')
            expect(page.locator('h1')).to_have_count(1)
            expect(page.locator('#theme-select')).to_be_visible()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'{name}: overflow at {width}px'
            if name!='404.html':
                for mode in ['dark','light']:
                    page.select_option('#theme-select',mode)
                    assert page.locator('html').get_attribute('data-theme')==mode
        print(f'All pages passed at {width}px in both themes',flush=True)
    page.goto(url+'/surfaces.html')
    expect(page.locator('#comparison')).to_contain_text('ChatGPT Work')
    expect(page.locator('#operators')).to_contain_text('codex exec')
    page.locator('.quiz button[data-correct="true"]').click()
    expect(page.locator('.quiz .feedback')).not_to_be_empty()
    page.goto(url+'/21-codex-exec.html')
    expect(page.locator('#lesson-surface')).to_contain_text('非互動 exec')
    for width in [1440,390]:
        page.set_viewport_size({'width':width,'height':1000})
        page.goto(url+'/surfaces.html')
        page.screenshot(path=f'/tmp/codex-surfaces-{width}.png',full_page=True)
    page.set_viewport_size({'width':1440,'height':1000});page.goto(url)
    page.select_option('#theme-select','dark');page.reload();expect(page.locator('html')).to_have_attribute('data-theme','dark')
    page.goto(url+'/customization.html');expect(page.locator('#theme-select')).to_have_value('dark')
    page.select_option('#theme-select','system');page.emulate_media(color_scheme='light');expect(page.locator('html')).to_have_attribute('data-theme','light')
    page.emulate_media(color_scheme='dark');expect(page.locator('html')).to_have_attribute('data-theme','dark')
    page.goto(url);page.locator('#course-search').fill('不存在的單元');expect(page.locator('.course-card:visible')).to_have_count(0);expect(page.locator('#search-status')).to_contain_text('0')
    page.keyboard.press('Escape');expect(page.locator('.course-card:visible')).to_have_count(lesson_count)
    page.locator('#course-search').fill('Debug');expect(page.locator('.course-card:visible')).to_have_count(1);page.keyboard.press('Escape')
    for query in ['Hooks','GPT Image','FFmpeg','Remotion','POP3','codex exec','CLI 設定','長任務、脈絡','可重用 Skill','50小時畢業']:
        page.locator('#course-search').fill(query);expect(page.locator('.course-card:visible')).to_have_count(1);page.keyboard.press('Escape')
    page.select_option('#learning-path','creative');expect(page.locator('.recommended')).to_have_count(3)
    page.select_option('#learning-path','automation');expect(page.locator('.recommended')).to_have_count(8)
    page.select_option('#learning-path','deep');expect(page.locator('.recommended')).to_have_count(5)
    assert page.locator('#learning-path option').count()==7
    page.select_option('#learning-path','start');expect(page.locator('.recommended')).to_have_count(3)
    page.locator('[data-copy-target="first-prompt"]').click();expect(page.locator('[data-copy-target="first-prompt"]')).to_contain_text('已複製')
    assert page.evaluate('navigator.clipboard.readText()')==page.locator('#first-prompt').input_value()
    page.goto(url+'/01-tasking.html');page.locator('#lesson-done').check();page.reload();expect(page.locator('#lesson-done')).to_be_checked()
    page.locator('#timer-start').click();page.wait_for_timeout(1200);assert page.locator('#timer-value').inner_text()!='00:00:00'
    page.locator('#timer-pause').click();value=page.locator('#timer-value').inner_text();page.wait_for_timeout(1100);assert page.locator('#timer-value').inner_text()==value
    page.reload();assert page.locator('#timer-value').inner_text()==value
    page.locator('#timer-reset').click();expect(page.locator('#timer-value')).to_have_text('00:00:00')
    page.locator('.quiz button[data-correct="true"]').first.click();expect(page.locator('.quiz .feedback').first).not_to_be_empty()
    page.goto(url);expect(page.locator('#course-progress')).to_contain_text(f'1 / {lesson_count}');expect(page.locator('#resume-learning')).to_have_attribute('href','02-commands.html')
    # Existing progress/time keys survive the expanded course, and new units count.
    page.evaluate("localStorage.setItem('codex-done-12','1');localStorage.setItem('codex-time-20','3600')")
    page.goto(url+'/20-data-capstone.html');page.locator('#lesson-done').check();page.reload();expect(page.locator('#lesson-done')).to_be_checked()
    page.goto(url);expect(page.locator('#course-progress')).to_contain_text(f'3 / {lesson_count}');expect(page.locator('#course-hours')).to_contain_text('1 小時')
    page.goto(url+'/25-workflow-evaluation.html');page.locator('#lesson-done').check()
    page.goto(url);expect(page.locator('#course-progress')).to_contain_text(f'4 / {lesson_count}')
    page.evaluate("for(let i=1;i<=25;i++)localStorage.setItem('codex-done-'+String(i).padStart(2,'0'),'1')")
    page.reload();expect(page.locator('#course-progress')).to_contain_text('25 / 25');expect(page.locator('#resume-learning')).to_have_attribute('href','25-workflow-evaluation.html')
    for item in catalog['lessons'][12:]:
        page.goto(url+'/'+item['slug']+'.html')
        expect(page.locator('.lesson-navigation')).to_be_visible()
        ids=page.locator('[id]').evaluate_all('(els)=>els.map(el=>el.id)');assert len(ids)==len(set(ids)),f"Duplicate runtime IDs: {item['slug']}"
        for button in page.locator('[data-copy-target]').all():
            target=button.get_attribute('data-copy-target');value=page.locator('[id="'+target+'"]').input_value() if page.locator('[id="'+target+'"]').evaluate('(el)=>el.tagName')=='TEXTAREA' else page.locator('[id="'+target+'"]').inner_text()
            button.click();assert page.evaluate('navigator.clipboard.readText()')==value
        page.locator('.quiz button[data-correct="true"]').first.click();expect(page.locator('.quiz .feedback').first).not_to_be_empty()
    page.goto(url+'/09-project-customization.html');group=page.locator('.tabs').first;tabs=group.locator('.tab');tabs.nth(1).click();expect(tabs.nth(1)).to_have_attribute('aria-selected','true');page.keyboard.press('ArrowRight');expect(tabs.nth(2)).to_have_attribute('aria-selected','true')
    page.locator('.contents summary').click();expect(page.locator('.contents nav a').first).to_be_visible();page.locator('.contents nav a').first.click();assert '#section-1' in page.url
    # Theme and progress still work with localStorage denied.
    blocked=browser.new_context();blocked.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('Storage unavailable')}})");bp=blocked.new_page();bp.on('pageerror',lambda e:errors.append(str(e)));bp.goto(url);expect(bp.locator('#course-progress')).to_contain_text(f'0 / {lesson_count}');bp.select_option('#theme-select','dark');expect(bp.locator('html')).to_have_attribute('data-theme','dark');blocked.close()
    for mode,width in [('light',1440),('dark',1440),('light',390)]:
        page.set_viewport_size({'width':width,'height':1000});page.goto(url);page.select_option('#theme-select',mode);page.screenshot(path=f'/tmp/codex-{mode}-{width}.png',full_page=True)
    page.set_viewport_size({'width':390,'height':1000});page.goto(url+'/21-codex-exec.html');page.screenshot(path='/tmp/codex-exec-390.png',full_page=True)
    assert not errors,f'Browser errors: {errors}'
    bad=[(u,s) for u,s in responses if u.startswith(url) and s>=400];assert not bad,f'HTTP failures: {bad}'
    print('Passed: theme persistence/system changes, search, learning paths, clipboard, saved progress, timer, quiz, keyboard tabs, contents, denied storage, zero JS/local HTTP errors',flush=True)
    browser.close()
