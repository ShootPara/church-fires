"""Paid article replacements from approved scripts. Resume receipts; never automatically retry a paid request."""
import argparse,concurrent.futures,datetime,hashlib,json,re,subprocess,urllib.request,urllib.error
from pathlib import Path
r=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--generate',action='store_true');p.add_argument('--only');a=p.parse_args()
rows=json.loads((r/'sources/narration/articles.json').read_text(encoding='utf-8'))
if a.only: rows=[row for row in rows if row['id']==a.only]
key=re.search(r'sk-[A-Za-z0-9_-]+',(r/'dev.vars').read_text(encoding='utf-8-sig')).group() if a.generate else None
instructions='Read this historical newspaper article verbatim, with a warm, resonant documentary delivery. Dignified, engaging, measured American English. Moderate consistent pace. No introductions, commentary, music or sound effects. Pronounce Kalamazoo kal-uh-muh-ZOO. Read newspaper headings naturally; do not shout capital letters.'
def build(row):
 if not row['slides']:return
 text=(r/row['script']).read_text(encoding='utf-8-sig').strip()
 chunks=[];current=''
 for paragraph in text.split('\n\n'):
  assert len(paragraph)<=3000, 'Long paragraph needs explicit splitting'
  if len(current)+len(paragraph)+2>3000:
   chunks.append(current);current=''
  current+= ('\n\n' if current else '')+paragraph
 if current:chunks.append(current)
 assert '\n\n'.join(chunks)==text
 dest=r/'sources/audio/articles'/row['id'];dest.mkdir(parents=True,exist_ok=True)
 final=dest/'reading.mp3'
 if final.exists():
  meta=json.loads(final.with_suffix('.json').read_text(encoding='utf-8'))
  assert hashlib.sha256(final.read_bytes()).hexdigest()==meta['sha256']
  saved='\n\n'.join(p.read_text(encoding='utf-8') for p in sorted(dest.glob('[0-9][0-9].txt')))
  assert saved==text, 'Script changed: prepare a new versioned generation job'
  print(f'{row["id"]} reused verified final',flush=True)
  return
 for i,chunk in enumerate(chunks,1):
  output=dest/f'{i:02}.mp3';receipt=output.with_suffix('.json');pending=output.with_suffix('.pending.json')
  digest=hashlib.sha256(chunk.encode()).hexdigest()
  if output.exists() and receipt.exists():
   meta=json.loads(receipt.read_text());assert meta['script_sha256']==digest and meta['audio_sha256']==hashlib.sha256(output.read_bytes()).hexdigest();continue
  assert not output.exists() and not pending.exists(), 'Interrupted attempt: inspect provider history before retrying'
  script=dest/f'{i:02}.txt';script.write_text(chunk,encoding='utf-8')
  meta=dict(provider='OpenAI',model='gpt-4o-mini-tts',voice='cedar',instructions=instructions,script_sha256=digest,script=str(script.relative_to(r)),source=row['script'],generated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
  if not a.generate:continue
  pending.write_text(json.dumps(meta,indent=2),encoding='utf-8')
  body=dict(model=meta['model'],voice=meta['voice'],instructions=instructions,input=chunk,response_format='mp3')
  req=urllib.request.Request('https://api.openai.com/v1/audio/speech',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
  try:
   with urllib.request.urlopen(req,timeout=180) as response:
    data=response.read();meta['request_id']=response.headers.get('x-request-id')
   assert len(data)>1000
  except urllib.error.HTTPError as exc:
   raise RuntimeError(f'{row["id"]} chunk {i}: HTTP {exc.code}; receipt retained; no retry') from None
  output.write_bytes(data);meta['audio_sha256']=hashlib.sha256(data).hexdigest();receipt.write_text(json.dumps(meta,indent=2),encoding='utf-8');pending.unlink()
  print(f'{row["id"]} generated chunk {i}/{len(chunks)}',flush=True)
 if not a.generate:return
 listing=dest/'concat.txt';listing.write_text('\n'.join(f"file '{i:02}.mp3'" for i in range(1,len(chunks)+1)))
 joined=dest/'joined.mp3';final=dest/'reading.mp3'
 if not joined.exists():subprocess.run(['ffmpeg','-v','error','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(joined)],check=True)
 if not final.exists():subprocess.run(['python',str(r/'scripts/normalize_audio.py'),str(joined),str(final)],capture_output=True,check=True)
 receipt=dict(row,provider='OpenAI',model='gpt-4o-mini-tts',voice='cedar',chunks=len(chunks),sha256=hashlib.sha256(final.read_bytes()).hexdigest(),full_listening_review='not performed')
 final.with_suffix('.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
 print(f'{row["id"]} COMPLETE',flush=True)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for result in pool.map(build,rows):pass
 print('All assigned article replacements complete.',flush=True)
