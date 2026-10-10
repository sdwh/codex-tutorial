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
docs={p.name:Document(p.read_text()) for p in ROOT.glob('*.html')}
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
    page.set_viewport_size({'width':1440,'height':1000});page.goto(url)
    page.select_option('#theme-select','dark');page.reload();expect(page.locator('html')).to_have_attribute('data-theme','dark')
    page.goto(url+'/customization.html');expect(page.locator('#theme-select')).to_have_value('dark')
    page.select_option('#theme-select','system');page.emulate_media(color_scheme='light');expect(page.locator('html')).to_have_attribute('data-theme','light')
    page.emulate_media(color_scheme='dark');expect(page.locator('html')).to_have_attribute('data-theme','dark')
    page.goto(url);page.locator('#course-search').fill('不存在的單元');expect(page.locator('.course-card:visible')).to_have_count(0);expect(page.locator('#search-status')).to_contain_text('0')
    page.keyboard.press('Escape');expect(page.locator('.course-card:visible')).to_have_count(12)
    page.locator('#course-search').fill('Debug');expect(page.locator('.course-card:visible')).to_have_count(1);page.keyboard.press('Escape')
    page.select_option('#learning-path','start');expect(page.locator('.recommended')).to_have_count(3)
    page.locator('[data-copy-target="first-prompt"]').click();expect(page.locator('[data-copy-target="first-prompt"]')).to_contain_text('已複製')
    assert page.evaluate('navigator.clipboard.readText()')==page.locator('#first-prompt').input_value()
    page.goto(url+'/01-tasking.html');page.locator('#lesson-done').check();page.reload();expect(page.locator('#lesson-done')).to_be_checked()
    page.locator('#timer-start').click();page.wait_for_timeout(1200);assert page.locator('#timer-value').inner_text()!='00:00:00'
    page.locator('#timer-pause').click();value=page.locator('#timer-value').inner_text();page.wait_for_timeout(1100);assert page.locator('#timer-value').inner_text()==value
    page.reload();assert page.locator('#timer-value').inner_text()==value
    page.locator('#timer-reset').click();expect(page.locator('#timer-value')).to_have_text('00:00:00')
    page.locator('.quiz button[data-correct="true"]').first.click();expect(page.locator('.quiz .feedback').first).not_to_be_empty()
    page.goto(url);expect(page.locator('#course-progress')).to_contain_text('1 / 12');expect(page.locator('#resume-learning')).to_have_attribute('href','02-commands.html')
    page.goto(url+'/09-project-customization.html');group=page.locator('.tabs').first;tabs=group.locator('.tab');tabs.nth(1).click();expect(tabs.nth(1)).to_have_attribute('aria-selected','true');page.keyboard.press('ArrowRight');expect(tabs.nth(2)).to_have_attribute('aria-selected','true')
    page.locator('.contents summary').click();expect(page.locator('.contents nav a').first).to_be_visible();page.locator('.contents nav a').first.click();assert '#section-1' in page.url
    # Theme and progress still work with localStorage denied.
    blocked=browser.new_context();blocked.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('Storage unavailable')}})");bp=blocked.new_page();bp.on('pageerror',lambda e:errors.append(str(e)));bp.goto(url);expect(bp.locator('#course-progress')).to_contain_text('0 / 12');bp.select_option('#theme-select','dark');expect(bp.locator('html')).to_have_attribute('data-theme','dark');blocked.close()
    for mode,width in [('light',1440),('dark',1440),('light',390)]:
        page.set_viewport_size({'width':width,'height':1000});page.goto(url);page.select_option('#theme-select',mode);page.screenshot(path=f'/tmp/codex-{mode}-{width}.png',full_page=True)
    assert not errors,f'Browser errors: {errors}'
    bad=[(u,s) for u,s in responses if u.startswith(url) and s>=400];assert not bad,f'HTTP failures: {bad}'
    print('Passed: theme persistence/system changes, search, learning paths, clipboard, saved progress, timer, quiz, keyboard tabs, contents, denied storage, zero JS/local HTTP errors',flush=True)
    browser.close()
