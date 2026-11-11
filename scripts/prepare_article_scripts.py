import json,re
from pathlib import Path
r=Path(__file__).resolve().parents[1]
starts=[0,22,37,49,53,62,77,94,134,142,151,155,161,168,178,185,193,198,227,233,241,267,313,324,332,338]
p=json.loads((r/'sources/extracted/gazette.json').read_text(encoding='utf-8'))['paragraphs']
m=json.loads((r/'sources/audio-assignments.json').read_text(encoding='utf-8'))
dest=r/'sources/narration';dest.mkdir(exist_ok=True)
existing=json.loads((r/'sources/narration/articles.json').read_text(encoding='utf-8')) if (r/'sources/narration/articles.json').exists() else []
manifest=[]
for i,(start,end) in enumerate(zip(starts,starts[1:]),1):
 text='\n\n'.join(x['text'] for x in p[start:end]).replace('\x0b','\n').strip()
 path=dest/f'article-{i:02}.txt';path.write_text(text,encoding='utf-8')
 clips=[(n,c) for n,cs in m.items() for c in cs if c.get('article_id')==f'article-{i:02}' or re.match(fr'{i:02} ',c['title'])]
 manifest.append(dict(id=f'article-{i:02}',script=path.as_posix(),paragraph_start=start,paragraph_end_exclusive=end,slides=[int(n) for n,c in clips],title=p[start+1]['text'].split('\x0b')[0],source_document='1-VtFJRzG7h7WN0zO37hNezaNp66vlPzbluVLFXgBlek',approved='User accepted Gazette Article Contents as accurate'))
manifest += [row for row in existing if row['id']=='article-26']
(r/'sources/narration/articles.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
print('Prepared',len(manifest),'source scripts;',sum(bool(x['slides']) for x in manifest),'assigned articles')
