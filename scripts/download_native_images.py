"""Download native image bytes from an existing Slides snapshot. No credentials needed.
Expired URLs: refresh get_presentation once and save raw-template.json, then retry failed items.
"""
import argparse, hashlib, json, urllib.request
from pathlib import Path
from extract_sources import ROOT, read, unwrap, objects, write
parser=argparse.ArgumentParser(); parser.add_argument('--limit',type=int); args=parser.parse_args()
out=ROOT/'ignore/native-images'; out.mkdir(parents=True,exist_ok=True)
deck=unwrap(read(ROOT/'ignore/drive-review/raw-template.json'))
rows=[]
for n,s in enumerate(deck['slides'],1):
    for e in objects(s.get('pageElements',[])):
        if 'image' not in e: continue
        if args.limit is not None and len(rows)>=args.limit: continue
        target=out/(e['objectId']+'.bin')
        row={'slide':n,'object_id':e['objectId'],'path':target.relative_to(ROOT).as_posix()}
        try:
            if not target.exists():
                with urllib.request.urlopen(e['image']['contentUrl'],timeout=30) as r:
                    data=r.read()
                    if not r.headers.get('Content-Type','').startswith('image/'): raise ValueError('Not an image')
                target.write_bytes(data)
            row.update(status='downloaded',sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        except Exception as exc:
            row.update(status='failed',error=type(exc).__name__) # Never log temporary signed URLs.
        rows.append(row)
write(ROOT/'sources/extracted'/('native-image-sample.json' if args.limit is not None else 'native-image-index.json'),rows)
print({s:sum(r['status']==s for r in rows) for s in ['downloaded','failed']})
