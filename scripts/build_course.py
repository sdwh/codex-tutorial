"""Render authored lessons and synchronize the 50-hour course catalog.
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
count=len(lessons);hours=catalog['minutes']//60;phases=max(l['phase'] for l in lessons)
assert count==25 and sum(l['minutes'] for l in lessons)==catalog['minutes']==3000
assert [l['id'] for l in lessons]==[f'{i:02d}' for i in range(1,count+1)]
header='''<a class="skip-link" href="#main">跳到主要內容</a>
<header><div class="bar"><a class="brand" href="index.html">CODEX <span>/ FIELD GUIDE</span></a><div class="bar-right">{label}</div>
<nav class="global-nav" aria-label="主要導覽"><a href="index.html#curriculum">50 小時課程</a><a href="customization.html">客製化</a><a href="plus-playbook.html">Plus 效益</a><a href="multi-agent.html">多代理</a><a href="assets.html">課程資產</a><label class="theme-control"><span>主題</span><select id="theme-select" aria-label="選擇顯示主題"><option value="system">跟隨系統</option><option value="light">淺色</option><option value="dark">深色</option></select></label></nav></div></header>'''
def navigation(index):
 parts=[]
 if index:parts.append(f'<a href="{lessons[index-1]["slug"]}.html">← {esc(lessons[index-1]["title"])}</a>')
 parts.append('<a href="index.html#curriculum">50 小時學習路線</a>')
 if index<len(lessons)-1:parts.append(f'<a href="{lessons[index+1]["slug"]}.html">{esc(lessons[index+1]["title"])} →</a>')
 else:parts.append('<a href="index.html#curriculum">回顧與選擇下一個實作 →</a>')
 return '<footer class="footer-nav lesson-navigation" aria-label="單元導覽">'+''.join(parts)+'</footer>'
def section(tag,title,body):return f'<section class="section"><div class="tag">{esc(tag)}</div><h2>{esc(title)}</h2>{body}</section>'
def surface_note(item):
 info=item['surface']
 return '<aside class="surface-note" id="lesson-surface" aria-label="本課入口與環境"><div class="tag">WHERE YOU WORK / 本課操作定位</div><h2>'+esc(info['entry'])+'</h2><dl><dt>執行環境</dt><dd>'+esc(info['environment'])+'</dd><dt>操作位置</dt><dd>'+esc(info['operation'])+'</dd><dt>換入口時</dt><dd>'+esc(info['transfer'])+'</dd></dl><a href="surfaces.html">比較 Chat、Work、Codex App 與 CLI →</a></aside>'
def render_lesson(item,index):
 data=read(f'content/lessons/{item["id"]}.json')
 assert data['id']==item['id'] and data['slug']==item['slug']
 assert data['minutes']==120 and sum(s['minutes'] for s in data['schedule'])==120
 assert len(data['sections'])>=6 and data['sources']
 url=BASE+item['slug']+'.html';title=data['title'];desc=data['description']
 ld={'@context':'https://schema.org','@type':'LearningResource','name':title,'description':desc,'inLanguage':'zh-Hant','timeRequired':'PT2H','dateModified':data['reviewed'],'isAccessibleForFree':True,'url':url,'isPartOf':{'@type':'Course','name':catalog['title'],'url':BASE,'timeRequired':'PT50H'}}
 head=f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(item['id'])} {esc(title)}｜Codex 實戰學院</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="zh-Hant" href="{url}"><meta name="robots" content="index,follow"><meta property="og:type" content="article"><meta property="og:locale" content="zh_TW"><meta property="og:site_name" content="Codex 實戰學院"><meta property="og:title" content="{esc(title)}｜Codex 實戰學院"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}social-preview.png"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="manifest" href="site.webmanifest"><script src="theme.js"></script><link rel="stylesheet" href="course.css"><script type="application/ld+json">{json.dumps(ld,ensure_ascii=False).replace('<','\\u003c')}</script></head>
<body data-lesson="{item['id']}">{header.format(label=f'單元 {item["id"]} / {count}')}<main id="main">
<section class="hero"><div class="tag">UNIT {item['id']} / 50-HOUR COURSE</div><h1>{esc(title)}</h1><p>{esc(desc)}</p><div class="unit-meta"><span class="pill">建議實作 · 120 分鐘</span><span class="pill">查證 · {esc(data['reviewed'])}</span><span class="pill">階段 {item['phase']} / {phases}</span></div></section>
<div class="illustration-frame"><img src="assets/illustrations/lessons/{item['slug']}.svg" alt="{esc(title)} 單元圖解" width="900" height="600" loading="eager"><div class="illustration-caption"><span>單元 {item['id']} 核心圖解：{esc(title)}</span><a href="assets.html#curriculum-vectors" style="color:var(--lime);text-decoration:none">素材庫 ↗</a></div></div>'''
 prerequisites='<div class="grid"><div class="box"><h3>開始前準備</h3><ul>'+''.join('<li>'+esc(x)+'</li>' for x in data['prerequisites'])+'</ul></div><div class="box"><h3>完成後你能</h3><ul>'+''.join('<li>'+esc(x)+'</li>' for x in data['outcomes'])+'</ul></div></div>'
 schedule='<div class="timeline">'+''.join(f'<div><b>{s["minutes"]} 分</b>{esc(s["activity"])}</div>' for s in data['schedule'])+'</div><p class="note">時間包含閱讀、操作、修正與驗收；不是純閱讀時間，也不是工具執行時間保證。</p><div class="timerbox"><span>本單元計時</span><strong id="timer-value">00:00:00</strong><button id="timer-start">開始</button><button id="timer-pause">暫停</button><button id="timer-reset">歸零</button></div>'
 body=section('BEFORE YOU START','準備與學習成果',prerequisites)+section('120 MINUTES','兩小時實作安排',schedule)
 body+='\n'.join(section(s['tag'],s['title'],s['html']) for s in data['sections'])
 q=data['quiz'];quiz='<div class="quiz"><strong>'+esc(q['question'])+'</strong><div class="quiz-options">'+''.join(f'<button data-correct="{str(o["correct"]).lower()}" data-explain="{esc(o["explain"])}">{esc(o["text"])}</button>' for o in q['options'])+'</div><div class="feedback" aria-live="polite"></div></div>'
 checks='<div class="checklist">'+''.join(f'<label><input type="checkbox"> {esc(x)}</label>' for x in data['checklist'])+'</div><label class="donebox"><input id="lesson-done" type="checkbox"> 已完成本單元的實作與驗收</label>'
 sources='<p class="note">範例與操作安排由本站整理。查證日期：'+esc(data['reviewed'])+'；版本、帳號與本機環境不同時，請核對原始文件。</p><div class="source-links">'+''.join(f'<a href="{esc(s["url"])}" target="_blank" rel="noreferrer" title="{esc(s["supports"])}">{esc(s["label"])} ↗</a>' for s in data['sources'])+'</div>'
 text=head+surface_note(item)+body+section('CHECK YOUR UNDERSTANDING','情境判斷',quiz)+section('ACCEPTANCE','驗收與完成',checks)+section('PRIMARY SOURCES','官方與第一手來源',sources)+navigation(index)+'</main><script src="icons.js"></script><script src="course-data.js"></script><script src="course.js"></script></body></html>\n'
 (ROOT/(item['slug']+'.html')).write_text(text)
for index,item in enumerate(lessons):
 if int(item['id'])>=13:render_lesson(item,index)
 else:
  p=ROOT/(item['slug']+'.html');s=p.read_text()
  s=re.sub(r'<div class="bar-right">.*?</div>',f'<div class="bar-right">單元 {item["id"]} / {count}</div>',s,count=1)
  s=s.replace('/ 20H + BONUS','/ FIELD GUIDE').replace('40 小時課程','50 小時課程')
  s=s.replace('href="index.html#curriculum">學習路線','href="index.html#curriculum">50 小時課程')
  s=re.sub(r'<(?:div|footer) class="footer-nav(?: lesson-navigation)?"[^>]*>.*?</(?:div|footer)>',navigation(index),s,flags=re.S)
  s=s.replace('<script src="course.js">','<script src="course-data.js"></script><script src="course.js">') if 'src="course-data.js"' not in s else s
  s=re.sub(r'<aside class="surface-note".*?</aside>','',s,flags=re.S)
  end=s.index('</section>',s.index('<section class="hero"'))+len('</section>')
  s=s[:end]+surface_note(item)+s[end:]
  p.write_text(s)
# Catalog drives JS counts/time, without a runtime fetch or build framework.
(ROOT/'course-data.js').write_text('window.CODEX_COURSE = '+json.dumps(catalog,ensure_ascii=False,indent=2)+';\n')
p=ROOT/'index.html';s=p.read_text()
s=s.replace('20 個實作單元 · 40 小時','25 個實作單元 · 50 小時').replace('完成 0 / 20 單元','完成 0 / 25 單元').replace('20 單元 × 2 小時 = 40 小時','25 單元 × 2 小時 = 50 小時')
s=re.sub(r'<div class="callout"><b>(?:40|50) 小時怎麼安排：</b>.*?</div>','<div class="callout"><b>50 小時怎麼安排：</b>25 個單元各 2 小時，包含閱讀、引導、實作、變體挑戰與驗收。前 40 小時建立開發與應用能力，最後 10 小時深入非互動執行、設定診斷、長任務恢復、Skill 工程與工作流評估。三篇進階指南不重複計入時數；已有的學習進度會保留。</div>',s,flags=re.S)
s=re.sub(r'<select id="learning-path">.*?</select>','<select id="learning-path"><option value="all">完整課程</option><option value="start">第一次使用</option><option value="build">開發與除錯</option><option value="scale">進階協作</option><option value="automation">開發者與自動化</option><option value="creative">生圖與影音</option><option value="deep">深度工作流</option></select>',s,flags=re.S)
s=re.sub(r'(<p class="note" id="path-description">).*?(</p>)',r'\1依 01–25 完成五個階段，每階段 10 小時；也可依需求先選主題。\2',s,flags=re.S)
cards=[]
for l in lessons:
 cards.append(f'<a class="card course-card" data-lesson="{l["id"]}" data-phase="{l["phase"]}" href="{l["slug"]}.html" style="color:inherit;text-decoration:none"><div class="tag">{l["id"]} · 2 小時</div><h3>{esc(l["title"])}</h3><p>{esc(l["description"])}</p><span class="pill">階段 {l["phase"]} / {phases}</span><span class="pill surface-label">{esc(l["surface"]["entry"])}</span></a>')
a=s.index('<div class="grid" style="margin-top:12px">');b=s.index('</div></section><section class="section"><div class="tag">WHAT',a)
s=s[:a]+'<div class="grid" style="margin-top:12px">\n'+'\n'.join(cards)+'\n'+s[b:]
phase_data=[('01–05','完成可靠交辦','需求、脈絡、除錯、規劃與驗收。','01-tasking.html','stage-1-tasking.jpg'),('06–10','建立協作方式','隔離工作、UI、Cloud、設定與整合。','06-git-worktrees.html','stage-2-collaboration.jpg'),('11–15','擴充與自動化','生活應用、案例、Hooks、SDK 與工具。','11-beyond-coding.html','stage-3-automation.jpg'),('16–20','創作與資料流程','生圖、影音、郵件與可重跑報告。','16-image-generation.html','stage-4-creative.jpg'),('21–25','掌握深度工作流','批次執行、設定診斷、恢復、Skill 工程與評估。','21-codex-exec.html','stage-5-deep-workflow.jpg')]
phase='<section class="section" id="course-map"><div class="tag">50 HOURS / FIVE STAGES</div><h2>五個階段，從第一次交辦到深度工作流。</h2><div class="loop-grid">'+''.join(f'<div class="box"><div class="stage-media"><img src="assets/illustrations/{img}" alt="{title} 階段插圖" loading="lazy" width="600" height="338"></div><span class="tag">{ids} / 10 小時</span><h3>{title}</h3><p>{desc}</p><a href="{href}">進入這個階段 →</a></div>' for ids,title,desc,href,img in phase_data)+'</div><p class="note">所有時間都是建議實作安排。需要 API 帳號、外部服務或額外工具的單元會標示；可先完成離線練習。</p></section>'
s=re.sub(r'<section class="section" id="course-map">.*?</section>',phase,s,flags=re.S)
s=s.replace('href="index.html#curriculum">40 小時課程','href="index.html#curriculum">50 小時課程')
# Replace only the JSON-LD script, preserving the remaining head.
ld={'@context':'https://schema.org','@graph':[{'@type':'WebSite','name':'Codex 實戰學院','url':BASE,'inLanguage':'zh-Hant'},{'@type':'Course','name':catalog['title'],'description':'25 個兩小時單元，從 Codex 工作循環到批次執行、Skill 工程、恢復與工作流評估。','timeRequired':'PT50H','inLanguage':'zh-Hant','isAccessibleForFree':True,'hasPart':[{'@type':'LearningResource','name':l['title'],'url':BASE+l['slug']+'.html','timeRequired':'PT2H'} for l in lessons]},{'@type':'ItemList','numberOfItems':count,'itemListElement':[{'@type':'ListItem','position':i,'url':BASE+l['slug']+'.html','name':l['title']} for i,l in enumerate(lessons,1)]}]}
s=re.sub(r'<script type="application/ld\+json">.*?</script>','<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>',s,count=1,flags=re.S)
if 'src="course-data.js"' not in s:s=s.replace('<script src="course.js">','<script src="course-data.js"></script><script src="course.js">')
s=s.replace('生活应用','生活應用');p.write_text(s)
for name in ['customization.html','plus-playbook.html','multi-agent.html','surfaces.html','404.html']:
 p=ROOT/name;s=p.read_text().replace('40 小時課程','50 小時課程').replace('20 個互動單元','25 個互動單元').replace('href="index.html#curriculum">學習路線','href="index.html#curriculum">50 小時課程').replace('href="/index.html#curriculum">學習路線','href="/index.html#curriculum">50 小時課程').replace('12 個互動單元','20 個互動單元')
 if 'src="course-data.js"' not in s and 'src="/course-data.js"' not in s:
  s=s.replace('<script src="course.js">','<script src="course-data.js"></script><script src="course.js">').replace('<script src="/course.js">','<script src="/course-data.js"></script><script src="/course.js">')
 p.write_text(s)
# Discovery metadata, no dependency on the generated HTML page count.
ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
node=ET.Element('{'+ns+'}urlset')
for path in ['']+[l['slug']+'.html' for l in lessons]+['customization.html','plus-playbook.html','multi-agent.html','surfaces.html','assets.html']:
 u=ET.SubElement(node,'{'+ns+'}url');ET.SubElement(u,'{'+ns+'}loc').text=BASE+path;ET.SubElement(u,'{'+ns+'}lastmod').text=catalog['reviewed']
ET.indent(node);ET.ElementTree(node).write(ROOT/'sitemap.xml',encoding='unicode',xml_declaration=True)
llms='# Codex 實戰學院\n\n> 繁體中文 50 小時完整實作課程：25 單元 × 120 分鐘。時間含閱讀、操作與驗收；三篇進階指南不重複計入。\n\n## 課程\n'
llms+='\n'.join(f'- [{l["id"]} {l["title"]}]({BASE}{l["slug"]}.html): {l["description"]}' for l in lessons)
llms+='\n\n- [入口比較]('+BASE+'surfaces.html): 區分 ChatGPT Chat／Work、Codex App／CLI 與本機／雲端環境。\n\n## 進階指南\n- [客製化]('+BASE+'customization.html)\n- [Plus 效益]('+BASE+'plus-playbook.html)\n- [多代理]('+BASE+'multi-agent.html)\n\n## 維護\n官方文件查證：'+catalog['reviewed']+'。網站索引見 /sitemap.xml。\n'
(ROOT/'llms.txt').write_text(llms)
print(f'Rendered {count-12} authored lessons; synchronized {count} lessons, {catalog["minutes"]} minutes, navigation and discovery metadata.')

# Keep the comparison discoverable across hand-authored and generated pages.
for p in ROOT.glob('*.html'):
 s=p.read_text()
 if 'href="surfaces.html">入口比較' not in s and 'href="/surfaces.html">入口比較' not in s:
  s=s.replace('<nav class="global-nav" aria-label="主要導覽">','<nav class="global-nav" aria-label="主要導覽"><a href="surfaces.html">入口比較</a>',1)
 p.write_text(s)
