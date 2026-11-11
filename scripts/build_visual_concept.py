from pathlib import Path
from PIL import Image
import io, base64, html

root = Path(__file__).resolve().parents[1]
media = root / 'ignore/Deconstructed Original Slides/media'
out = root / 'design'
out.mkdir(exist_ok=True)
assets = []
for path in sorted(media.glob('SLIDE 021*'), key=lambda p: (0 if 'Headline' in p.name else 1, p.name)):
    if 'Audio icon' in path.name or ' Date ' in path.name:
        continue
    with Image.open(path) as im:
        im.thumbnail((850, 800))
        buffer = io.BytesIO()
        im.convert('RGB').save(buffer, format='JPEG', quality=75)
    assets.append('<img alt="'+html.escape(path.stem)+'" src="data:image/jpeg;base64,'+base64.b64encode(buffer.getvalue()).decode()+'">')
photo = next(media.glob('SLIDE 010*'))
with Image.open(photo) as im:
    im.thumbnail((800,600)); buffer=io.BytesIO(); im.convert('RGB').save(buffer,format='JPEG',quality=75)
photo_html='<img alt="First Congregational Church postcard" src="data:image/jpeg;base64,'+base64.b64encode(buffer.getvalue()).decode()+'">'
text=(root/'sources/extracted/excerpts.txt').read_text(encoding='utf-8').split('\n\n')[2]
css='''#church-concept{--brick:#ac3025;--paper:#f9f4e9;color:#241d19;font-family:Arial,sans-serif}#church-concept *{box-sizing:border-box}#church-concept .stage{background:var(--brick);padding:24px}#church-concept header{color:white;display:flex;justify-content:space-between;gap:20px;padding-bottom:18px;font-size:14px;letter-spacing:.04em}#church-concept h2{font:700 32px/1.1 Georgia,serif;margin:0}#church-concept .heading{background:var(--paper);padding:18px 22px;margin-bottom:16px}#church-concept .heading p{margin:8px 0 0;font-size:14px}#church-concept .evidence{display:flex;justify-content:center;align-items:flex-start;flex-wrap:wrap;gap:10px;min-height:320px}#church-concept img{max-width:100%;object-fit:contain;max-height:390px}#church-concept .evidence img{max-width:31%}#church-concept .evidence img:first-child{max-width:100%}#church-concept .photo img{max-width:100%}#church-concept footer{display:flex;flex-wrap:wrap;gap:8px;align-items:center;background:#75241d;padding:12px;color:white}#church-concept button,#church-concept select{font:14px Arial;padding:10px 14px;min-height:44px;border:1px solid #d2b4a7;background:var(--paper);color:#331e18;border-radius:3px}#church-concept .count{margin-right:auto}#church-concept .transcript{background:var(--paper);padding:22px;font:18px/1.6 Georgia,serif}#church-concept [hidden]{display:none!important}#church-concept:fullscreen{overflow:auto;background:var(--brick)}#church-concept:fullscreen .evidence{min-height:60vh}#church-concept:fullscreen img{max-height:65vh}@media(max-width:600px){#church-concept .stage{padding:12px}#church-concept h2{font-size:26px}#church-concept .evidence img{max-width:48%}}'''
markup='''<div id="church-concept"><style>CSS</style><div class="stage"><header><span>KALAMAZOO CHURCH FIRES</span><span>1925—1926</span></header><div class="heading"><h2>First Congregational Church burns</h2><p>December 29, 1925 · The Kalamazoo Gazette</p></div><div class="evidence">ASSETS</div><div class="photo" hidden>PHOTO</div><section class="transcript" hidden><h3>Article text</h3><p>TEXT</p><p><small>Opening excerpt · transcription review pending</small></p></section></div><footer><button data-action="previous">← Previous</button><span class="count" aria-live="polite">21 / 102</span><button data-action="text" aria-expanded="false">Read article</button><button data-action="full">Fullscreen</button><button data-action="next">Next →</button></footer><script>(()=>{const r=document.getElementById('church-concept');let article=true;const show=()=>{r.querySelector('.evidence').hidden=!article;r.querySelector('.photo').hidden=article;r.querySelector('h2').textContent=article?'First Congregational Church burns':'Before the fire';r.querySelector('.heading p').textContent=article?'December 29, 1925 · The Kalamazoo Gazette':'First Congregational Church · historic postcard';r.querySelector('.count').textContent=article?'21 / 102':'10 / 102';r.querySelector('.transcript').hidden=true;r.querySelector('[data-action=text]').disabled=!article;r.querySelector('[data-action=text]').setAttribute('aria-expanded','false')};r.querySelectorAll('[data-action]').forEach(b=>b.onclick=async()=>{if(b.dataset.action==='text'){const t=r.querySelector('.transcript');t.hidden=!t.hidden;b.setAttribute('aria-expanded',String(!t.hidden))}else if(b.dataset.action==='full'){try{if(document.fullscreenElement)await document.exitFullscreen();else await r.requestFullscreen()}catch{r.querySelector('.count').textContent='Fullscreen available in browser preview'}}else{article=!article;show()}});if(globalThis.Tweak){const state={brick:'#ac3025'};const t=new Tweak({container:r,onChange:()=>r.style.setProperty('--brick',state.brick)});t.addColorPicker(state,'brick',{label:'Slide background'})}})();</script></div>'''
css = (out / 'presentation-layout.css').read_text(encoding='utf-8')
markup = markup.replace('</footer>', '<div class="audio-slot"><span>Article audio</span><audio controls preload="none" aria-label="Article audio preview"></audio></div></footer>')
markup = markup.replace("const show=()=>{", "const show=()=>{r.querySelector('audio').pause();")
markup=markup.replace('CSS',css).replace('ASSETS',''.join(assets)).replace('PHOTO',photo_html).replace('TEXT',html.escape(text))
(out/'presentation-concept.html').write_text(markup,encoding='utf-8')
(out/'presentation-concept.css').write_text(css,encoding='utf-8')
print(len(markup), 'bytes;',len(assets),'article assets')
