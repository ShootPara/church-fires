"""Optional asset preparation. Requires Pillow; ordinary builds use committed results."""
import hashlib,json
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
out=root/'sources/optimized-media';out.mkdir(exist_ok=True)
manifest={}
for source in sorted((root/'sources/media').glob('*.png')):
 if 'Audio icon' in source.name:continue
 target=out/(source.stem+'.webp')
 with Image.open(source) as image:
  image.save(target,'WEBP',lossless=True,exact=True,method=4)
  with Image.open(target) as check:
   assert check.size==image.size
   assert check.convert('RGBA').tobytes()==image.convert('RGBA').tobytes(),source.name
  dimensions=list(image.size)
 if target.stat().st_size>=source.stat().st_size:
  target.unlink();continue
 manifest[source.name]={'file':target.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'dimensions':dimensions,'pixel_identical':True}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Verified lossless assets:',len(manifest))
