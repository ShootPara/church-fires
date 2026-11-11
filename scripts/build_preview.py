from html import escape
import json
from pathlib import Path
from shutil import copyfile

from PIL import Image

root = Path(__file__).resolve().parents[1]
out = root / 'ignore' / 'preview'
out.mkdir(parents=True, exist_ok=True)
index = json.loads((root / 'sources/extracted/pdf-index.json').read_text(encoding='utf-8'))
building = max(index[0]['pages'][9]['images'], key=lambda item: item['width'])
copyfile(root / building['path'], out / 'church.jpg')
for scan in index[1:]:
    if 'December_29_1925' in scan['source']:
        page = 1 if '__p1 ' in scan['source'] else 2
        with Image.open(root / scan['pages'][0]['render']) as image:
            image.thumbnail((2000, 2800))
            image.save(out / f'gazette-{page}.jpg', quality=85)
for n in (21, 22):
    with Image.open(root / index[0]['pages'][n-1]['render']) as image:
        w, h = image.size
        image.crop((0, 0, w, round(h * .88))).convert('RGB').save(out / f'clipping-{n}.jpg', quality=94)
source = (root / 'sources/extracted/excerpts.txt').read_text(encoding='utf-8')
paragraphs = source.split('\n\n')
end = next(i for i, p in enumerate(paragraphs) if i > 2 and 'METHODIST' in p.upper() and len(p) < 100)
excerpt = ''.join(f'<p>{escape(p)}</p>' for p in paragraphs[2:end] if p.strip())
pages = [
    ('overview', 'The Kalamazoo church fires', '<p>Between December 1925 and July 1926, fires destroyed First Congregational, First Methodist Episcopal, and First Presbyterian churches in Kalamazoo.</p>'),
    ('congregational-building', 'First Congregational Church', '<figure><img src="church.jpg" alt="Historic image of First Congregational Church"><figcaption>First Congregational Church before the fire. Presentation slide 10.</figcaption></figure>'),
    ('congregational-fire', 'December 29, 1925', '<p><cite>Kalamazoo Gazette</cite>, December 29, 1925, pages 1–2. Draft excerpt from the presentation archive.</p>' +
      '<div class="clippings">' + ''.join(
          f'<a href="clipping-{n}.jpg"><img src="clipping-{n}.jpg" alt="Gazette article clipping, part {n-20}"></a>'
          for n in (21, 22)
      ) + '</div><details><summary>Read extracted text</summary><blockquote>' + excerpt + '</blockquote></details>'),
    ('investigation', 'What investigators knew', '<p>Contemporary accounts differed in how confidently they identified the origins of the fires. Newspapers reported suspicion of arson across the series. The Methodist investigation reached an incident-specific finding involving an overheated flue.</p>'),
]
articles = ''.join(f'<article id="{key}"><h2>{title}</h2>{body}</article>' for key, title, body in pages)
template = (root / 'site/index.html').read_text(encoding='utf-8-sig')
(out / 'index.html').write_text(template.replace('<!-- PAGES -->', articles), encoding='utf-8')
for name in ('style.css', 'viewer.js'):
    copyfile(root / 'site' / name, out / name)
print(out / 'index.html')
