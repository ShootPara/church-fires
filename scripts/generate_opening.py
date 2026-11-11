"""Generate the approved opening document once, with resumable receipts; no automatic paid retries."""
import argparse,datetime,hashlib,json,re,urllib.request,urllib.error,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--generate',action='store_true');a=p.parse_args()
r=Path(__file__).resolve().parents[1]; dest=r/'sources/audio';dest.mkdir(exist_ok=True)
text=(r/'sources/extracted/excerpts.txt').read_text(encoding='utf-8').strip()
chunks=[];current=''
for paragraph in text.split('\n\n'):
 if len(current)+len(paragraph)+2>2800:
  chunks.append(current);current=''
 current+= ('\n\n' if current else '')+paragraph
if current:chunks.append(current)
assert '\n\n'.join(chunks)==text
final=dest/'opening-reading.mp3'
if final.exists():
 meta=json.loads(final.with_suffix('.json').read_text(encoding='utf-8'))
 assert hashlib.sha256(final.read_bytes()).hexdigest()==meta['sha256']
 assert '\n\n'.join(p.read_text(encoding='utf-8') for p in sorted(dest.glob('opening-[0-9][0-9].txt')))==text
 print('Reused verified opening recording');raise SystemExit(0)
key=re.search(r'sk-[A-Za-z0-9_-]+',(r/'dev.vars').read_text(encoding='utf-8-sig')).group() if a.generate else None
for i,chunk in enumerate(chunks,1):
 script=dest/f'opening-{i:02}.txt';script.write_text(chunk,encoding='utf-8')
 output=dest/f'opening-{i:02}.mp3';receipt=output.with_suffix('.json');pending=output.with_suffix('.pending.json')
 digest=hashlib.sha256(chunk.encode()).hexdigest()
 if output.exists() and receipt.exists():
  assert json.loads(receipt.read_text())['script_sha256']==digest
  continue
 assert not output.exists() and not pending.exists(), 'Inspect interrupted paid attempt before retrying'
 body=dict(model='gpt-4o-mini-tts',voice='cedar',input=chunk,response_format='mp3',instructions='Read this historical newspaper text verbatim in a warm, resonant documentary voice. Measured, engaging, dignified, with subtle dramatic gravity. Natural American English, clear names and dates. No added introduction, commentary, or sound effects. Kalamazoo is kal-uh-muh-ZOO. Keep a consistent moderate pace throughout.')
 meta=dict(provider='OpenAI',model=body['model'],voice=body['voice'],instructions=body['instructions'],script_sha256=digest,script=str(script.relative_to(r)),source='sources/extracted/excerpts.txt',approved_by='Brian: use verbatim document',generated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 if not a.generate:print(i,len(chunk));continue
 pending.write_text(json.dumps(meta,indent=2),encoding='utf-8')
 req=urllib.request.Request('https://api.openai.com/v1/audio/speech',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(req,timeout=180) as response:
   data=response.read();meta['request_id']=response.headers.get('x-request-id')
  assert len(data)>1000
 except urllib.error.HTTPError as e:
  raise SystemExit(f'Provider returned HTTP {e.code}; inspect pending receipt, no automatic retry.') from None
 output.write_bytes(data);meta['audio_sha256']=hashlib.sha256(data).hexdigest();receipt.write_text(json.dumps(meta,indent=2),encoding='utf-8');pending.unlink();print(f'Generated {i}/{len(chunks)}',flush=True)
if a.generate:
 joined=dest/'opening-joined.mp3'
 listing=dest/'opening-concat.txt';listing.write_text('\n'.join("file '"+f'opening-{i:02}.mp3'+"'" for i in range(1,len(chunks)+1)))
 if not joined.exists():subprocess.run(['ffmpeg','-v','error','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(joined)],check=True)
 if not (dest/'opening-reading.mp3').exists():subprocess.run(['python',str(r/'scripts/normalize_audio.py'),str(joined),str(dest/'opening-reading.mp3')],check=True)
