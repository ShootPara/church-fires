"""Select completed approved article recordings; preserve archive paths and original assignments."""
import json,re,hashlib
from pathlib import Path
r=Path(__file__).resolve().parents[1]
p=r/'sources/audio-assignments.json';mapping=json.loads(p.read_text(encoding='utf-8'))
archive={}
for n,clips in mapping.items():
 for clip in clips:
  match=re.match(r'(\d\d) ',clip['title'])
  if clip.get('article_id'):archive[clip['article_id']]=clip.get('original_audio',clip['source'])
  elif match: archive['article-'+match[1]]=clip.get('original_audio',clip['source'])
result={'1':mapping['1']}
for row in json.loads((r/'sources/narration/articles.json').read_text(encoding='utf-8')):
 if not row['slides']:continue
 audio=r/'sources/audio/articles'/row['id']/'reading.mp3'
 assert audio.is_file(),f'Missing replacement {row["id"]}'
 receipt=json.loads(audio.with_suffix('.json').read_text(encoding='utf-8'))
 assert hashlib.sha256(audio.read_bytes()).hexdigest()==receipt['sha256']
 for number in row['slides']:
  result.setdefault(str(number),[]).append(dict(title=row['title'],source=audio.relative_to(r).as_posix(),script=row['script'],article_id=row['id'],original_audio=archive.get(row['id'],'G:/My Drive/Church Fires Presentation/Gazette Article Audios/17 Another Church Fire.mp3'),assignment='User-approved correction for slides 51/52' if number in [51,52] else 'Original native placement',voice='OpenAI Cedar'))
p.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print('Selected',sum(len(v) for k,v in result.items() if k!='1'),'replacement articles')
