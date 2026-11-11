"""Offline release validation; standard library only. Never performs paid generation."""
import argparse,hashlib,json,re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
p=argparse.ArgumentParser();p.add_argument('directory',nargs='?',default='dist');a=p.parse_args();root=Path(a.directory)
s=(root/'index.html').read_text(encoding='utf-8')
assert '<meta charset="utf-8">' in s
assert len(re.findall(r'<article id="slide-\d+"',s))==101
assert '006 &#183; Investigating the causes' in s
assert 'Narration pending' not in s
assert 'https://github.com/ShootPara/church-fires' in s
assert 'start=1093' in s and 'start=110' in s
class Check(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k not in ['src','href'] or not v or v.startswith('#'):continue
   url=urlsplit(v)
   if url.scheme or url.netloc:continue
   assert (root/unquote(url.path)).is_file(),v
Check().feed(s)
for item in json.loads((root/'asset-manifest.json').read_text(encoding='utf-8')):
 assert hashlib.sha256((root/item['output']).read_bytes()).hexdigest()==item['sha256'],item['output']
assert not list(root.rglob('dev.vars'))
print('PASS: 101 slides, local references, asset hashes, titles, video starts, repository link')
