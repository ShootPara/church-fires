"""One paid ElevenLabs request per reviewed chunk. Defaults to dry-run. No automatic retries.
No credentials or paid calls are needed to prepare/validate a job.
"""
import argparse, datetime, hashlib, json, os, urllib.request, urllib.parse
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('job',type=Path); p.add_argument('--generate',action='store_true'); a=p.parse_args()
j=json.loads(a.job.read_text(encoding='utf-8-sig'))
script=Path(j['script']); text=script.read_text(encoding='utf-8').strip()
assert text and len(text)<=3000, 'Use reviewed paragraph-boundary chunks of at most 3000 characters.'
digest=hashlib.sha256(script.read_bytes()).hexdigest()
assert digest==j['script_sha256'], 'Script changed since review; update review and hash.'
assert j['review_status']=='approved', 'Script must be checked against displayed source text.'
assert j['voice_id'] and j['model_id'] and j['pronunciation_notes'] is not None
out=Path(j['output']); receipt=out.with_suffix('.json'); pending=out.with_suffix('.pending.json')
assert not out.exists() and not receipt.exists() and not pending.exists(), 'Existing output/attempt: inspect it; never blindly repeat a charged request.'
summary={'characters':len(text),'model':j['model_id'],'voice':j['voice_id'],'script_sha256':digest,'output':str(out),'paid_request':a.generate}
print(json.dumps(summary))
if a.generate:
    key=os.environ['ELEVENLABS_API_KEY']
    out.parent.mkdir(parents=True,exist_ok=True)
    pending.write_text(json.dumps(summary),encoding='utf-8')
    body={'text':text,'model_id':j['model_id']}
    if j.get('voice_settings'): body['voice_settings']=j['voice_settings']
    req=urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/'+urllib.parse.quote(j['voice_id'],safe='')+'?output_format=mp3_44100_128',data=json.dumps(body).encode(),headers={'xi-api-key':key,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=180) as r:
            data=r.read(); request_id=r.headers.get('request-id')
            assert r.headers.get('Content-Type','').startswith('audio/'), 'Unexpected response type'
        assert len(data)>100, 'Empty/truncated response'
        out.write_bytes(data)
        receipt.write_text(json.dumps({**j,**summary,'provider':'ElevenLabs','generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'request_id':request_id,'audio_sha256':hashlib.sha256(data).hexdigest(),'listening_review':'pending'},indent=2),encoding='utf-8')
        pending.unlink()
    except Exception as exc:
        raise SystemExit('Generation incomplete: '+type(exc).__name__+'. Pending receipt retained; inspect provider history before retrying.') from None
