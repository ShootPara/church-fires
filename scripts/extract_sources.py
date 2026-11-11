"""Rebuild source exports/worklists; no website, source mutation or paid calls.
Run from repository root. Outputs under sources/extracted are generated, not edited.
"""
import argparse, hashlib, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def unwrap(d):
    d = d.get('structuredContent', d)
    return d.get('result', d)
def objects(elements):
    for e in elements:
        yield e
        yield from objects(e.get('elementGroup', {}).get('children', []))
def text_of(v):
    if isinstance(v, dict):
        if 'textRun' in v:
            yield v['textRun'].get('content', '')
        for k, child in v.items():
            if k != 'textRun':
                yield from text_of(child)
    elif isinstance(v, list):
        for child in v:
            yield from text_of(child)
def chapter(n):
    for end, name in [(7,'overview'),(20,'city'),(28,'congregational'),(32,'methodist'),(37,'presbyterian'),(48,'firefighters'),(61,'investigations'),(75,'rebuilding'),(101,'gallery'),(102,'omit-blank')]:
        if n <= end: return name

def export():
    src = ROOT/'ignore/drive-review'
    out = ROOT/'sources/extracted'
    for name in ['excerpts','gazette','summaries']:
        d = unwrap(read(src/f'{name}.json'))
        write(out/f'{name}.json', d)
        (out/f'{name}.txt').write_text('\n\n'.join(p['text'] for p in d['paragraphs'])+'\n', encoding='utf-8')
    deck = unwrap(read(src/'raw-template.json'))
    rows=[]
    for n,s in enumerate(deck['slides'],1):
        elements=[]
        for e in objects(s.get('pageElements',[])):
            # Temporary image URLs deliberately kept only in ignored original snapshot.
            item={k:v for k,v in e.items() if k in ['objectId','size','transform','title','description']}
            item['text']=''.join(text_of(e.get('shape',{})))
            for kind in ['image','video']:
                if kind in e:
                    item[kind]={k:v for k,v in e[kind].items() if k not in ['contentUrl']}
            elements.append(item)
        rows.append({'slide':n,'slide_id':s['objectId'],'chapter':chapter(n),
            'native_text':''.join(text_of(s.get('pageElements',[]))),
            'notes':''.join(text_of(s.get('slideProperties',{}).get('notesPage',{}))),
            'elements':elements,'status':'unreviewed',
            'instructions':'Extract all meaningful text/images; map article, audio, credits. Preserve native ID. Do not infer reading order from object order.'})
    write(out/'slide-worklist.json',{'revision':deck['revisionId'],'slides':rows})
    lines=['# Slide-by-slide extraction worklist','', 'Generated source index; put editorial decisions in content/ or docs, not here.','']
    for r in rows:
        lines.extend([f"## {r['slide']:03d} — {r['chapter']} — {r['slide_id']}",'',r['native_text'].strip() or '(No native text; inspect visual.)','',f"Objects: {len(r['elements'])}. Reference: ignore/pdf-review/slide-{r['slide']:03d}.jpg",''])
    (out/'slide-worklist.md').write_text('\n'.join(lines),encoding='utf-8')
    print(f'Exported {len(rows)} slides and three script documents to {out}')

def pdfs():
    import pymupdf
    manifest=read(ROOT/'docs/source-manifest.json')
    files=[('presentation',ROOT/'Kalamazoo Church Fires Presentation.pdf')]
    files += [(f'newspaper-{i:02d}',Path(manifest['source_root'])/r['source_path']) for i,r in enumerate([r for r in manifest['files'] if r['source_path'].endswith('.pdf')],1)]
    out=ROOT/'ignore/extraction'; out.mkdir(parents=True,exist_ok=True)
    index=[]
    for label,path in files:
        folder=out/label; folder.mkdir(exist_ok=True)
        d=pymupdf.open(path)
        pages=[]
        for n,page in enumerate(d,1):
            rendered=folder/f'page-{n:03d}.png'
            if not rendered.exists(): page.get_pixmap(dpi=120 if label=='presentation' else 180,alpha=False).save(rendered)
            images=[]
            for img in page.get_images(full=True):
                xref=img[0]; smask=img[1]
                data=d.extract_image(xref); digest=hashlib.sha256(data['image']).hexdigest()
                target=out/'images'/f"{digest}.{data['ext']}"; target.parent.mkdir(exist_ok=True)
                if not target.exists(): target.write_bytes(data['image'])
                images.append({'xref':xref,'smask':smask,'path':target.relative_to(ROOT).as_posix(),'sha256':digest,'width':data['width'],'height':data['height'],'warning':'Raw embedded image; inspect crop, mask, rotation and composition before use.'})
            pages.append({'page':n,'render':rendered.relative_to(ROOT).as_posix(),'images':images})
        index.append({'id':label,'source':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pages':pages})
        d.close()
    write(ROOT/'sources/extracted/pdf-index.json',index)
    print(f'Extracted/rendered {len(files)} PDFs; see sources/extracted/pdf-index.json')

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('command',choices=['text','pdf']); a=p.parse_args()
    export() if a.command=='text' else pdfs()
