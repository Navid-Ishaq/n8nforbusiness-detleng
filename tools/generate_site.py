from pathlib import Path
import zipfile,xml.etree.ElementTree as E,html,json,hashlib,re
ROOT=Path(__file__).resolve().parents[1];SOURCE=Path('D:/Web-Sites-Ideas/02 Sell n8n Workflows.docx')
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
NODES=['Respond to Webhook','Execute Sub-workflow','Remove Duplicates','OpenAI Chat Model','Schedule Trigger','Structured Output Parser','Structured Output','Loop Over Items','HTTP Request','Error Trigger','Stop And Error','Date & Time','Google Sheets','Google Drive','Split Out','Edit Fields','AI Agent','WhatsApp Business Cloud','Data Tables','Webhook','Aggregate','Summarize','Postgres','Supabase','Airtable','Telegram','WhatsApp','OpenAI','HubSpot','Notion','MySQL','Gmail','Slack','Switch','Filter','Merge','Wait','Code','IF']
PAT=re.compile(r'(?<![\w])('+ '|'.join(re.escape(x) for x in NODES)+r')(?![\w])')
def rich_text(p):
 text='';rich=''
 for run in p.findall('.//w:r',NS):
  rt=''
  for node in run:
   t=node.tag.split('}')[-1]
   if t=='t':rt+=node.text or ''
   elif t=='tab':rt+='\t'
   elif t in ('br','cr'):rt+='\n'
  text+=rt
  # Tokenize raw run text first, then escape; all wording remains unchanged.
  pos=0;part=''
  for match in PAT.finditer(rt):
   part+=html.escape(rt[pos:match.start()])+ '<span class="node-name">'+html.escape(match.group())+'</span>';pos=match.end()
  part+=html.escape(rt[pos:]);part=part.replace('\n','<br>')
  if run.find('w:rPr/w:b',NS) is not None:part='<strong>'+part+'</strong>'
  if run.find('w:rPr/w:i',NS) is not None:part='<em>'+part+'</em>'
  rich+=part
 return text,rich
with zipfile.ZipFile(SOURCE) as z:
 doc=E.fromstring(z.read('word/document.xml'))
 assert not doc.findall('.//w:del',NS),'Review tracked deletions before generating'
 assert not doc.findall('.//w:txbxContent',NS),'Review text boxes before generating'
 for part in z.namelist():
  if any(s in part for s in ['header','footer','footnotes','endnotes']):assert not E.fromstring(z.read(part)).findall('.//w:t',NS),part
 ps=doc.findall('.//w:body//w:p',NS);rows=[]
 for p in ps:
  text,rich=rich_text(p)
  if not text.strip():continue
  outline=p.find('w:pPr/w:outlineLvl',NS)
  level=int(outline.get('{'+NS['w']+'}val')) if outline is not None else None
  rows.append({'text':text,'rich':rich,'level':level,'bold':p.find('.//w:b',NS) is not None})
base=next(i for i,r in enumerate(rows) if r['text']=='How to Sell n8n Workflows')
headings=[(i,r['text']) for i,r in enumerate(rows) if r['level']==0]
heading_map={text:f'source-{i}' for i,text in headings}
def anchor(text):return '#'+heading_map[text]
toc=''.join(f'<a href="#source-{i}" data-title="{html.escape(text.lower(),quote=True)}"><span aria-hidden="true">{num:02}</span><span>{html.escape(text)}</span></a>' for num,(i,text) in enumerate(headings,1))
# Semantic source lists; block identity remains one-to-one.
list_ranges=[(36,38),(66,84),(97,108),(115,126),(176,180),(225,231),(239,243),(253,258),(267,270),(285,289),(341,350),(366,376),(406,413),(418,420),(433,438),(444,450),(460,470),(489,492),(500,506),(518,522),(528,537),(539,542),(617,622),(641,647),(650,654),(674,682),(687,691),(699,711),(742,749),(761,773),(819,834),(840,846),(848,854),(856,862),(868,875),(878,886),(893,902),(916,922),(955,961),(979,984),(991,997),(1009,1016),(1025,1035),(1044,1051),(1054,1058),(1061,1063),(1066,1070),(1073,1080),(1083,1090),(1093,1095),(1098,1101),(1104,1106),(1121,1124),(1161,1166),(1190,1195),(1211,1216),(1222,1228),(1230,1237),(1258,1267),(1294,1300),(1332,1341),(1361,1366),(1371,1376),(1382,1388),(1395,1405),(1413,1416),(1426,1446),(1456,1460),(1477,1487),(1495,1499),(1502,1507),(1520,1548),(1554,1561),(1568,1576),(1591,1595),(1602,1606),(1614,1619),(1649,1652)]
# Remove first item group with mixed prose that is better kept flowing.
list_ranges=[r for r in list_ranges if r not in [(36,38),(66,84),(699,711)]]
list_ranges=[(s+base,e+base) for s,e in list_ranges]
starts={s:e for s,e in list_ranges};ends={e:s for s,e in list_ranges}
body=[];section=False;chapter=0
before_starts={777:'before',784:'after',132:'before',142:'after',545:'before',550:'after'}
before_starts={k+base:v for k,v in before_starts.items()}
before_ends={x+base for x in (141,157,549,556,783,792)}
for i,r in enumerate(rows):
 j=i-base
 lvl=r['level'];tag='h2' if lvl==0 else 'h3' if lvl is not None and lvl<9 else 'p'
 if lvl==0:
  if section:body.append('</section>')
  chapter+=1;theme=''
  if j in (1108,1110,1154,1182):theme+=' case-study'
  if j in (684,752,914,933,943,964,1424):theme+=' professional'
  if j in (1489,1621,1659):theme+=' closing'
  body.append(f'<section class="chapter{theme}" aria-labelledby="source-{i}"><div class="chapter-index" aria-hidden="true">{chapter:02} <span> / </span> THE BUSINESS GUIDE</div>');section=True
 if i in before_starts:body.append(f'<div class="comparison {before_starts[i]}">')
 if i in starts:body.append('<ul class="source-list">')
 cls='source-block'
 if i<base:cls+=' source-preface'
 if tag=='p' and r['bold'] and 35<len(r['text'])<240 and j not in range(1622,1642):cls+=' principle'
 if '\n→' in r['text']:cls+=' workflow-strip'
 if r['text'] in ('Before:','After:','Without automation:','With automation:'):cls+=' comparison-label'
 if j in range(1622,1642):cls+=' formula-line'+(' formula-outcome' if j%2 else '')
 if j in range(777,793) or j in range(132,158) or j in range(545,557):cls+=' comparison-line'
 if i in starts or any(s<i<=e for s,e in list_ranges):tag='li'
 body.append(f'<{tag} id="source-{i}" class="{cls}" data-source-block="{i}">{r["rich"]}</{tag}>')
 if i in ends:body.append('</ul>')
 if i in before_ends:body.append('</div>')
if section:body.append('</section>')
nav=[('Stop Selling n8n','Sell the outcome'),('Think in Layers','The system'),('A Simple Commercial Structure','The offer'),('A Simple Delivery Standard','Delivery')]
nav_html=''.join(f'<a href="{anchor(title)}">{label}</a>' for title,label in nav)
journey=['Problem','Workflow','Outcome','Proof','Offer','Sale','Delivery','Support']
journey_html=''.join(f'<li><span>{i:02}</span><strong>{name}</strong></li>' for i,name in enumerate(journey,1))
page='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>How to Sell n8n Workflows | n8n for Business — DeTLeng</title><meta name="description" content="Learn how to turn n8n workflows into clear business value, professional automation offers, trustworthy client solutions, and sustainable services."><meta name="theme-color" content="#c8462b"><link rel="canonical" href="https://n8nforbusiness.detleng.com/"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><meta property="og:title" content="How to Sell n8n Workflows | n8n for Business — DeTLeng"><meta property="og:description" content="Turn practical workflows into business solutions clients can understand, trust, buy, and use."><meta property="og:type" content="article"><meta property="og:url" content="https://n8nforbusiness.detleng.com/"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="n8n for Business — Turn Workflows Into Business Value"><meta name="twitter:description" content="Build automation. Create value. Get paid. A complete guide to selling n8n workflows professionally."><link rel="stylesheet" href="assets/css/style.css"><script defer src="assets/js/app.js"></script><script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","headline":"How to Sell n8n Workflows","url":"https://n8nforbusiness.detleng.com/","inLanguage":"en","author":{"@type":"Person","name":"Muhammad Naveed Ishaque"},"publisher":{"@type":"Organization","name":"DeTLeng"}}</script></head>
<body><a class="skip" href="#guide">Skip to the complete guide</a><header class="site-header"><div class="nav-shell"><a class="brand" href="#top" aria-label="n8n for Business home"><span class="brand-symbol" aria-hidden="true"><i></i><i></i><i></i></span><span><strong>n8n <span>for Business</span></strong><small>A DETLENG RESOURCE</small></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Open navigation"><span aria-hidden="true">☰</span> Menu</button><nav id="primary-nav" class="primary-nav" aria-label="Main navigation">'''+nav_html+'''<a href="#contents">Contents</a><a class="lfds-link" href="https://lfds.detleng.com/" target="_blank" rel="noopener noreferrer" aria-label="Explore LFDS (opens in a new tab)">Explore LFDS <span aria-hidden="true">↗</span></a></nav></div><div class="progress-track"><div id="reading-progress"></div></div></header>
<main id="top"><section class="hero shell" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow"><span></span> HOW TO SELL n8n WORKFLOWS</p><h1 id="hero-title">Build Automation.<br><span>Create Value.</span><br>Get Paid.</h1><p class="hero-lead">Turn practical workflows into business solutions clients can understand, trust, buy, and use.</p><div class="hero-actions"><a class="button primary" href="#guide">Start the journey <span aria-hidden="true">↓</span></a><a class="text-link" href="#contents">Explore the contents <span aria-hidden="true">↗</span></a></div><p class="hero-audience">For builders, freelancers, consultants &amp; agencies.</p></div><div class="value-visual" aria-label="From technical workflow to business outcome"><div class="visual-label"><span class="live-dot"></span> THE VALUE TRANSLATION</div><div class="canvas-label">THE WORKFLOW</div><div class="mini-flow"><div class="flow-node"><span aria-hidden="true">↘</span>Webhook</div><span class="connector" aria-hidden="true"></span><div class="flow-node"><span aria-hidden="true">◇</span>IF</div><span class="connector" aria-hidden="true"></span><div class="flow-node"><span aria-hidden="true">✉</span>Gmail</div></div><div class="translation-arrow" aria-hidden="true">↓</div><div class="outcome-card"><span class="outcome-label">THE BUSINESS OUTCOME</span><strong>Every lead.<br>Remembered.</strong><div class="outcome-tags"><span>Captured</span><span>Answered</span><span>Followed up</span></div></div><p class="visual-note">The client buys what happens <br><strong>outside the canvas.</strong></p></div></section>
<section class="journey-section" aria-label="The business journey"><div class="shell"><div class="journey-intro"><span class="eyebrow">TURN WORKFLOWS INTO BUSINESS VALUE</span><span>From the first problem to ongoing care.</span></div><ol class="journey">'''+journey_html+'''</ol></div></section>
<div class="book-bar shell" id="guide"><span class="eyebrow">THE COMPLETE BUSINESS GUIDE</span><span class="book-bar-note">Read. Build. Explain. Deliver.</span></div><div class="book-layout shell"><aside class="contents" id="contents"><details open><summary><span>Inside the guide</span><span class="contents-icon" aria-hidden="true">−</span></summary><div class="contents-inner"><label for="contents-search">Find a section</label><input id="contents-search" type="search" placeholder="Try: pricing, trust, API…" autocomplete="off"><nav aria-label="Guide table of contents">'''+toc+'''</nav><p id="no-sections" role="status" hidden>No matching headings.</p><div class="contents-footer"><span id="reading-label">Ready to begin</span><a href="#top" aria-label="Back to top">↑</a></div></div></details></aside><article id="source-article" aria-label="How to Sell n8n Workflows — full source content">'''+''.join(body)+'''</article></div>
<section class="ecosystem"><div class="shell"><div class="ecosystem-heading"><div><p class="eyebrow">PART OF THE DETLENG AUTOMATION ECOSYSTEM</p><h2>One connected journey.</h2></div><a class="button secondary" href="https://lfds.detleng.com/" target="_blank" rel="noopener noreferrer" aria-label="Explore LFDS (opens in a new tab)">Explore LFDS ↗</a></div><div class="ecosystem-grid"><a href="https://n8n.detleng.com/" target="_blank" rel="noopener noreferrer"><span>LEARN ↗</span><strong>n8n DeTLeng</strong><small>Build practical understanding.</small></a><a href="https://n8nlab.detleng.com/" target="_blank" rel="noopener noreferrer"><span>BUILD / EXPLAIN ↗</span><strong>DeTLeng n8n Lab</strong><small>Follow the thinking behind the work.</small></a><a href="https://ops.detleng.com/" target="_blank" rel="noopener noreferrer"><span>SHOW ↗</span><strong>DeTLeng Ops</strong><small>Explore architecture and project evidence.</small></a></div></div></section></main>
<footer><div class="shell"><div class="footer-grid"><div class="footer-identity"><strong>n8n for Business</strong><p>How to Sell n8n Workflows</p><p class="footer-principle">Turn workflows into business value.</p><a href="https://lfds.detleng.com/" target="_blank" rel="noopener noreferrer">LFDS — Logic First Digital Solutions ↗</a></div><div class="attribution"><p>AI-Generated, Human-Curated Content</p><strong>Muhammad Naveed Ishaque</strong><p>Business &amp; Education Solutions Provider</p></div></div><div class="footer-bottom"><span>© <span id="year">2026</span> DeTLeng</span><a href="https://n8nforbusiness.detleng.com/">n8nforbusiness.detleng.com</a><a href="#top">Back to top ↑</a></div><p class="independent">Independent educational and business resource. Not affiliated with n8n GmbH.</p></div></footer></body></html>'''
(ROOT/'index.html').write_text(page,encoding='utf8')
manifest={'source':str(SOURCE),'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'source_blocks':len(rows),'raw_paragraphs':len(ps),'blocks':[r['text'] for r in rows]}
(ROOT/'tools/source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
cn=ROOT/'CNAME'
if cn.exists():assert cn.read_text().strip()=='n8nforbusiness.detleng.com'
else:cn.write_text('n8nforbusiness.detleng.com\n',encoding='utf8')
(ROOT/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#c8462b"/><path d="M15 42L32 22 49 42" fill="none" stroke="#fff" stroke-width="4"/><g fill="#fff"><circle cx="15" cy="42" r="6"/><circle cx="32" cy="22" r="6"/><circle cx="49" cy="42" r="6"/></g></svg>',encoding='utf8')
print('Generated',len(rows),'source blocks and',len(headings),'contents entries')
