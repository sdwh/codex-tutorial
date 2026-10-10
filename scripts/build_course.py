"""Render authored lessons and synchronize the 40-hour course catalog.
Run after editing content/curriculum.json or content/lessons/*.json.
Existing 01–12 body content stays hand-authored; shared metadata/navigation is updated.
"""
from pathlib import Path
import html,json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
BASE='https://codex-tutorial.sdwh.dev/'
def esc(value):return html.escape(str(value),quote=True)
def read(path):return json.loads((ROOT/path).read_text())
catalog=read('content/curriculum.json');lessons=catalog['lessons']
assert len(lessons)==20 and sum(l['minutes'] for l in lessons)==2400
assert [l['id'] for l in lessons]==[f'{i:02d}' for i in range(1,21)]
header='''<a class="skip-link" href="#main">跳到主要內容</a>
<header><div class="bar"><a class="brand" href="index.html">CODEX <span>/ FIELD GUIDE</span></a><div class="bar-right">{label}</div>
<nav class="global-nav" aria-label="主要導覽"><a href="index.html#curriculum">40 小時課程</a><a href="customization.html">客製化</a><a href="plus-playbook.html">Plus 效益</a><a href="multi-agent.html">多代理</a><label class="theme-control"><span>主題</span><select id="theme-select" aria-label="選擇顯示主題"><option value="system">跟隨系統</option><option value="light">淺色</option><option value="dark">深色</option></select></label></nav></div></header>'''
def navigation(index):
 parts=[]
 if index:parts.append(f'<a href="{lessons[index-1]["slug"]}.html">← {esc(lessons[index-1]["title"])}</a>')
 parts.append('<a href="index.html#curriculum">40 小時學習路線</a>')
 if index<len(lessons)-1:parts.append(f'<a href="{lessons[index+1]["slug"]}.html">{esc(lessons[index+1]["title"])} →</a>')
 else:parts.append('<a href="index.html#curriculum">回顧與選擇下一個實作 →</a>')
 return '<footer class="footer-nav lesson-navigation" aria-label="單元導覽">'+''.join(parts)+'</footer>'
def section(tag,title,body):return f'<section class="section"><div class="tag">{esc(tag)}</div><h2>{esc(title)}</h2>{body}</section>'
def render_lesson(item,index):
 data=read(f'content/lessons/{item["id"]}.json')
 assert data['id']==item['id'] and data['slug']==item['slug']
 assert data['minutes']==120 and sum(s['minutes'] for s in data['schedule'])==120
 assert len(data['sections'])>=6 and data['sources']
 url=BASE+item['slug']+'.html';title=data['title'];desc=data['description']
 ld={'@context':'https://schema.org','@type':'LearningResource','name':title,'description':desc,'inLanguage':'zh-Hant','timeRequired':'PT2H','dateModified':data['reviewed'],'isAccessibleForFree':True,'url':url,'isPartOf':{'@type':'Course','name':catalog['title'],'url':BASE,'timeRequired':'PT40H'}}
 head=f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(item['id'])} {esc(title)}｜Codex 實戰學院</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="zh-Hant" href="{url}"><meta name="robots" content="index,follow"><meta property="og:type" content="article"><meta property="og:locale" content="zh_TW"><meta property="og:site_name" content="Codex 實戰學院"><meta property="og:title" content="{esc(title)}｜Codex 實戰學院"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}social-preview.png"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="manifest" href="site.webmanifest"><script src="theme.js"></script><link rel="stylesheet" href="course.css"><script type="application/ld+json">{json.dumps(ld,ensure_ascii=False).replace('<','\\u003c')}</script></head>
<body data-lesson="{item['id']}">{header.format(label=f'單元 {item["id"]} / 20')}<main id="main">
<section class="hero"><div class="tag">UNIT {item['id']} / 40-HOUR COURSE</div><h1>{esc(title)}</h1><p>{esc(desc)}</p><div class="unit-meta"><span class="pill">建議實作 · 120 分鐘</span><span class="pill">查證 · {esc(data['reviewed'])}</span><span class="pill">階段 {item['phase']} / 4</span></div></section>'''
 prerequisites='<div class="grid"><div class="box"><h3>開始前準備</h3><ul>'+''.join('<li>'+esc(x)+'</li>' for x in data['prerequisites'])+'</ul></div><div class="box"><h3>完成後你能</h3><ul>'+''.join('<li>'+esc(x)+'</li>' for x in data['outcomes'])+'</ul></div></div>'
 schedule='<div class="timeline">'+''.join(f'<div><b>{s["minutes"]} 分</b>{esc(s["activity"])}</div>' for s in data['schedule'])+'</div><p class="note">時間包含閱讀、操作、修正與驗收；不是純閱讀時間，也不是工具執行時間保證。</p><div class="timerbox"><span>本單元計時</span><strong id="timer-value">00:00:00</strong><button id="timer-start">開始</button><button id="timer-pause">暫停</button><button id="timer-reset">歸零</button></div>'
 body=section('BEFORE YOU START','準備與學習成果',prerequisites)+section('120 MINUTES','兩小時實作安排',schedule)
 body+='\n'.join(section(s['tag'],s['title'],s['html']) for s in data['sections'])
 q=data['quiz'];quiz='<div class="quiz"><strong>'+esc(q['question'])+'</strong><div class="quiz-options">'+''.join(f'<button data-correct="{str(o["correct"]).lower()}" data-explain="{esc(o["explain"])}">{esc(o["text"])}</button>' for o in q['options'])+'</div><div class="feedback" aria-live="polite"></div></div>'
 checks='<div class="checklist">'+''.join(f'<label><input type="checkbox"> {esc(x)}</label>' for x in data['checklist'])+'</div><label class="donebox"><input id="lesson-done" type="checkbox"> 已完成本單元的實作與驗收</label>'
 sources='<p class="note">範例與操作安排由本站整理。查證日期：'+esc(data['reviewed'])+'；版本、帳號與本機環境不同時，請核對原始文件。</p><div class="source-links">'+''.join(f'<a href="{esc(s["url"])}" target="_blank" rel="noreferrer" title="{esc(s["supports"])}">{esc(s["label"])} ↗</a>' for s in data['sources'])+'</div>'
 text=head+body+section('CHECK YOUR UNDERSTANDING','情境判斷',quiz)+section('ACCEPTANCE','驗收與完成',checks)+section('PRIMARY SOURCES','官方與第一手來源',sources)+navigation(index)+'</main><script src="icons.js"></script><script src="course-data.js"></script><script src="course.js"></script></body></html>\n'
 (ROOT/(item['slug']+'.html')).write_text(text)
for index,item in enumerate(lessons):
 if int(item['id'])>=13:render_lesson(item,index)
 else:
  p=ROOT/(item['slug']+'.html');s=p.read_text()
  s=re.sub(r'<div class="bar-right">.*?</div>',f'<div class="bar-right">單元 {item["id"]} / 20</div>',s,count=1)
  s=s.replace('/ 20H + BONUS','/ FIELD GUIDE')
  s=s.replace('href="index.html#curriculum">學習路線','href="index.html#curriculum">40 小時課程')
  s=re.sub(r'<(?:div|footer) class="footer-nav(?: lesson-navigation)?"[^>]*>.*?</(?:div|footer)>',navigation(index),s,flags=re.S)
  s=s.replace('<script src="course.js">','<script src="course-data.js"></script><script src="course.js">') if 'src="course-data.js"' not in s else s
  p.write_text(s)
# Catalog drives JS counts/time, without a runtime fetch or build framework.
(ROOT/'course-data.js').write_text('window.CODEX_COURSE = '+json.dumps(catalog,ensure_ascii=False,indent=2)+';\n')
p=ROOT/'index.html';s=p.read_text()
s=s.replace('12 個實作單元','20 個實作單元 · 40 小時').replace('完成 0 / 12 單元','完成 0 / 20 單元').replace('Codex 實戰學院 · 主課程 20 小時 + 4 小時加值章','Codex 實戰學院 · 20 單元 × 2 小時 = 40 小時')
s=s.replace('<span class="pill">12 個實作單元</span>','<span class="pill">20 個實作單元 · 40 小時</span>')
s=re.sub(r'<div class="callout"><b>20 小時主課程怎麼安排：</b>.*?</div>','<div class="callout"><b>40 小時怎麼安排：</b>20 個單元各 2 小時，包含閱讀、引導、實作、變體挑戰與驗收。原有生活應用與網站案例已納入完整路線，新增八個開發者工具與多媒體／郵件應用單元。三篇進階指南不重複計入時數；已有的學習進度會保留。</div>',s,flags=re.S)
s=s.replace('依 01–10 完成主課程，再選讀兩篇案例。','依 01–20 完成四個階段，每階段 10 小時；也可依需求先選主題。')
s=s.replace('<option value="scale">進階協作</option>','<option value="scale">進階協作</option><option value="automation">開發者與自動化</option><option value="creative">生圖與影音</option>')
cards=[]
for l in lessons:
 cards.append(f'<a class="card course-card" data-lesson="{l["id"]}" data-phase="{l["phase"]}" href="{l["slug"]}.html" style="color:inherit;text-decoration:none"><div class="tag">{l["id"]} · 2 小時</div><h3>{esc(l["title"])}</h3><p>{esc(l["description"])}</p><span class="pill">階段 {l["phase"]} / 4</span></a>')
a=s.index('<div class="grid" style="margin-top:12px">');b=s.index('</div></section><section class="section"><div class="tag">WHAT',a)
s=s[:a]+'<div class="grid" style="margin-top:12px">\n'+'\n'.join(cards)+'\n'+s[b:]
phase='''<section class="section" id="course-map"><div class="tag">40 HOURS / FOUR STAGES</div><h2>四個階段，把能力帶到更多場景。</h2><div class="loop-grid"><div class="box"><span class="tag">01–05 / 10 小時</span><h3>完成可靠交辦</h3><p>需求、脈絡、除錯、規劃與驗收。</p><a href="01-tasking.html">從基礎起步 →</a></div><div class="box"><span class="tag">06–10 / 10 小時</span><h3>建立協作方式</h3><p>隔離工作、UI、Cloud、設定與整合。</p><a href="06-git-worktrees.html">提高協作效率 →</a></div><div class="box"><span class="tag">11–15 / 10 小時</span><h3>擴充與自動化</h3><p>生活应用、案例、Hooks、SDK 與工具。</p><a href="13-hooks.html">探索開發者工具 →</a></div><div class="box"><span class="tag">16–20 / 10 小時</span><h3>創作與資料流程</h3><p>生圖、影音、郵件與可重跑報告。</p><a href="16-image-generation.html">開始新情境實作 →</a></div></div><p class="note">所有時間都是建議實作安排。需要 API 帳號、外部服務或額外工具的單元會標示；可先完成離線練習。</p></section>'''
if 'id="course-map"' not in s:s=s.replace('<section class="section" id="curriculum">',phase+'<section class="section" id="curriculum">',1)
s=s.replace('href="index.html#curriculum">學習路線','href="index.html#curriculum">40 小時課程')
# Replace only the JSON-LD script, preserving the remaining head.
ld={'@context':'https://schema.org','@graph':[{'@type':'WebSite','name':'Codex 實戰學院','url':BASE,'inLanguage':'zh-Hant'},{'@type':'Course','name':catalog['title'],'description':'20 個兩小時單元，從 Codex 工作循環到開發者工具、多媒體與郵件自動化。','timeRequired':'PT40H','inLanguage':'zh-Hant','isAccessibleForFree':True,'hasPart':[{'@type':'LearningResource','name':l['title'],'url':BASE+l['slug']+'.html','timeRequired':'PT2H'} for l in lessons]},{'@type':'ItemList','numberOfItems':20,'itemListElement':[{'@type':'ListItem','position':i,'url':BASE+l['slug']+'.html','name':l['title']} for i,l in enumerate(lessons,1)]}]}
s=re.sub(r'<script type="application/ld\+json">.*?</script>','<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>',s,count=1,flags=re.S)
if 'src="course-data.js"' not in s:s=s.replace('<script src="course.js">','<script src="course-data.js"></script><script src="course.js">')
s=s.replace('生活应用','生活應用');p.write_text(s)
for name in ['customization.html','plus-playbook.html','multi-agent.html','404.html']:
 p=ROOT/name;s=p.read_text().replace('href="index.html#curriculum">學習路線','href="index.html#curriculum">40 小時課程').replace('href="/index.html#curriculum">學習路線','href="/index.html#curriculum">40 小時課程').replace('12 個互動單元','20 個互動單元')
 if 'src="course-data.js"' not in s and 'src="/course-data.js"' not in s:
  s=s.replace('<script src="course.js">','<script src="course-data.js"></script><script src="course.js">').replace('<script src="/course.js">','<script src="/course-data.js"></script><script src="/course.js">')
 p.write_text(s)
# Discovery metadata, no dependency on the generated HTML page count.
ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
node=ET.Element('{'+ns+'}urlset')
for path in ['']+[l['slug']+'.html' for l in lessons]+['customization.html','plus-playbook.html','multi-agent.html']:
 u=ET.SubElement(node,'{'+ns+'}url');ET.SubElement(u,'{'+ns+'}loc').text=BASE+path;ET.SubElement(u,'{'+ns+'}lastmod').text=catalog['reviewed']
ET.indent(node);ET.ElementTree(node).write(ROOT/'sitemap.xml',encoding='unicode',xml_declaration=True)
llms='# Codex 實戰學院\n\n> 繁體中文 40 小時完整實作課程：20 單元 × 120 分鐘。時間含閱讀、操作與驗收；三篇進階指南不重複計入。\n\n## 課程\n'
llms+='\n'.join(f'- [{l["id"]} {l["title"]}]({BASE}{l["slug"]}.html): {l["description"]}' for l in lessons)
llms+='\n\n## 進階指南\n- [客製化]('+BASE+'customization.html)\n- [Plus 效益]('+BASE+'plus-playbook.html)\n- [多代理]('+BASE+'multi-agent.html)\n\n## 維護\n官方文件查證：'+catalog['reviewed']+'。網站索引見 /sitemap.xml。\n'
(ROOT/'llms.txt').write_text(llms)
print('Rendered 8 new lessons; synchronized 20 lessons, 2400 minutes, navigation and discovery metadata.')
