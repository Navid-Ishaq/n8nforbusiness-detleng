from pathlib import Path
import json,re,hashlib,zipfile,xml.etree.ElementTree as E
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
class Site(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.current=None;self.blocks=[];self.ids=set();self.links=[];self.ends=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   assert a['id'] not in self.ids,('Duplicate ID',a['id']);self.ids.add(a['id'])
  if 'data-source-block' in a:self.current='';self.ends.append(tag)
  if tag=='br' and self.current is not None:self.current+='\n'
  if tag=='a':self.links.append(a)
 def handle_data(self,data):
  if self.current is not None:self.current+=data
 def handle_endtag(self,tag):
  if self.ends and tag==self.ends[-1] and self.current is not None:self.blocks.append(self.current);self.current=None;self.ends.pop()
def norm(t):return re.sub(r'\s+',' ',t).strip()
def verify(browser_file=None):
 manifest=json.loads((ROOT/'tools/source-manifest.json').read_text(encoding='utf8'));source_path=Path(manifest['source'])
 assert hashlib.sha256(source_path.read_bytes()).hexdigest()==manifest['sha256'],'Source DOCX changed'
 with zipfile.ZipFile(source_path) as z:
  doc=E.fromstring(z.read('word/document.xml'));blocks=[]
  for p in doc.findall('.//w:body//w:p',NS):
   text=''
   for el in p.iter():
    tag=el.tag.split('}')[-1]
    if tag=='t':text+=el.text or ''
    elif tag=='tab':text+='\t'
    elif tag in ('br','cr'):text+='\n'
   if text.strip():blocks.append(text)
 parser=Site();parser.feed((ROOT/'index.html').read_text(encoding='utf8'))
 for target in [parser.blocks]+([json.loads(Path(browser_file).read_text(encoding='utf8'))] if browser_file else []):
  assert len(blocks)==len(target),(len(blocks),len(target))
  for i,(a,b) in enumerate(zip(blocks,target)):assert norm(a)==norm(b),(i,a,b)
 for a in parser.links:
  href=a.get('href','')
  if href.startswith('#'):assert href[1:] in parser.ids,href
  if a.get('target')=='_blank':assert {'noopener','noreferrer'}<=set(a.get('rel','').split()),a
 assert (ROOT/'CNAME').read_text().strip()=='n8nforbusiness.detleng.com'
 result={'source_blocks':len(blocks),'website_blocks':len(parser.blocks),'missing_blocks':0,'all_blocks_in_original_order':True,'beginning_middle_final_verified':True,'all_examples_lists_quotes_and_node_explanations_compared':True,'source_docx_sha256_unchanged':True,'source_sha256':manifest['sha256'],'rendered_browser_text_verified':bool(browser_file),'internal_anchor_links_verified':sum(a.get('href','').startswith('#') for a in parser.links),'cname':'n8nforbusiness.detleng.com'}
 (ROOT/'tools/integrity-report.json').write_text(json.dumps(result,indent=2),encoding='utf8');return result
if __name__=='__main__':
 import sys
 print(json.dumps(verify(sys.argv[1] if len(sys.argv)>1 else None),indent=2))
