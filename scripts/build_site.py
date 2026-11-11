"""Build a portable local presentation from the labeled source archive."""
import argparse
import hashlib
import json
import re
from html import escape
from pathlib import Path
from shutil import copyfile
from render_slide_layout import render_layout

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--output", default="ignore/named-presentation")
args = parser.parse_args()
out = (root / args.output).resolve()
assets = out / "assets"
assets.mkdir(parents=True, exist_ok=True)
media = root / "sources/media"
slides = json.loads((root / "sources/extracted/slide-worklist.json").read_text(encoding="utf-8"))["slides"]
layouts = {row["slide"]: row for row in json.loads((root / "sources/slide-layouts.json").read_text(encoding="utf-8"))}
urls = {}
by_slide = {}
manifest = []
optimized = json.loads((root / 'sources/optimized-media/manifest.json').read_text(encoding='utf-8'))
for path in sorted(media.iterdir()):
    match = re.match(r"SLIDE (\d+) (.+)", path.stem)
    if not match or path.suffix.lower() not in {".jpg", ".png", ".jpeg"} or match[2].startswith("Audio icon"):
        continue
    source_digest = hashlib.sha256(path.read_bytes()).hexdigest()
    selected = path
    if path.name in optimized:
        record = optimized[path.name]
        assert source_digest == record['source_sha256'], f'Regenerate optimization for {path.name}'
        selected = root / 'sources/optimized-media' / record['file']
        assert hashlib.sha256(selected.read_bytes()).hexdigest() == record['sha256']
    digest = hashlib.sha256(selected.read_bytes()).hexdigest()
    url = f"assets/{digest[:20]}{selected.suffix.lower()}"
    copyfile(selected, out / url)
    urls[path.name] = url
    label = re.sub(r"\s+\d+ of \d+.*$", "", match[2]).partition(" - ")[2] or match[2]
    numbers = [int(match[1]), *(int(n) for n in re.findall(r"also SLIDE (\d+)", path.stem))]
    ordinal = re.search(r"(\d+) of \d+", path.stem)
    for number in numbers:
        by_slide.setdefault(number, []).append((int(ordinal[1]) if ordinal else 0, label, url))
    manifest.append({"slides": numbers, "source": path.name, "source_sha256": source_digest, "sha256": digest, "output": url,
                     "credit": "Brian Ream presentation archive", "rights": "review before publication"})

titles = json.loads((root / "sources/slide-titles.json").read_text(encoding="utf-8"))
options, chapters, pages = [], {}, []
archive = root / "sources/video"
spins = {28: "3rd Church Spin0001-0120.mp4", 74: "4th Church Spin0001-0120.mp4"}
spins[75] = "four-churches.mp4"
external_videos = json.loads((root / "sources/external-videos.json").read_text(encoding="utf-8"))
audio_map = json.loads((root / 'sources/audio-assignments.json').read_text(encoding='utf-8'))
speaker_svg = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9h4l5-4v14l-5-4H3zM16 8a6 6 0 0 1 0 8M19 5a10 10 0 0 1 0 14"/></svg>'
excerpt = (root / "sources/extracted/excerpts.txt").read_text(encoding="utf-8").split("\n\n")
end = next(i for i, line in enumerate(excerpt) if i > 2 and "METHODIST" in line.upper() and len(line) < 100)
for slide in slides:
    n = slide["slide"]
    if n == 102:
        continue
    chapter = slide["chapter"].replace("-", " ").title()
    chapters.setdefault(chapter, n)
    raw = [s.strip() for s in slide["native_text"].splitlines() if s.strip() and s.strip().casefold() != "brian ream"]
    nav = {"summary", "timeline", "deaths", "investigations", "rebuilding"}
    lines = [s for s in raw if s.casefold() not in nav] or (raw if len(raw) == 1 else [])
    images = sorted(by_slide.get(n, []))
    title = titles[str(n)]
    options.append(f'<option value="{n}">{n:03} &#183; {escape(title)}</option>')
    body = "".join(f"<p>{escape(s)}</p>" for s in lines if s != title)
    evidence = "".join(f'<a href="{url}"><img loading="lazy" src="{url}" alt="{escape(label)}"></a>'
                       for _, label, url in images)
    video = ""
    if str(n) in external_videos:
        entry = external_videos[str(n)]
        embed = f'https://www.youtube-nocookie.com/embed/{entry["id"]}?start={entry["start"]}&autoplay=1'
        stamp = f'{entry["start"]//60}:{entry["start"]%60:02}'
        video = f'<div class="external-video"><button data-video="{escape(embed)}" aria-label="Play {escape(entry["label"])}"><span aria-hidden="true">&#9654;</span>Play video from {stamp}</button><a href="{escape(entry["url"])}" target="_blank" rel="noopener noreferrer">Watch on YouTube at {stamp}</a></div>'
        evidence = video
    if n in spins and (archive / spins[n]).is_file():
        source = archive / spins[n]
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        url = f"assets/{digest[:20]}.mp4"
        copyfile(source, out / url)
        poster = next((urls[element["source"]] for element in layouts[n]["elements"] if element["kind"] == "video" and element.get("source")), "")
        video = f'<video class="spin spin-{n}" controls preload="none" poster="{poster}" playsinline aria-label="{ "The Four Churches" if n == 75 else "Church model rotation" }" src="{url}"></video>'
        evidence += video
        manifest.append({"slides": [n], "source": source.name, "sha256": digest, "output": url,
                         "credit": "Brian Ream", "rights": "review before publication"})
    if not evidence and not body:
        body = ""
    audio_html = ''
    for assignment in audio_map.get(str(n), []):
        source = root / assignment['source']
        if not source.is_file():
            continue
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        url = f'assets/{digest[:20]}.mp3'
        copyfile(source, out / url)
        audio_html += f'<audio preload="none" data-title="{escape(assignment["title"])}" src="{url}"></audio>'
        manifest.append({'slides':[n], 'source':str(source), 'sha256':digest, 'output':url, 'credit':'Presentation audio archive', 'script':assignment['script']})
    cover_speaker = f'<button class="cover-speaker" data-narration aria-label="Play opening reading" title="Play opening reading" {"" if audio_html else "disabled"}>{speaker_svg}</button>' if n == 1 else ''
    reading = ""
    if n in {21,22}:
        reading = '<section class="transcript" aria-label="Article excerpt"><h3>December 29, 1925 &#183; The Kalamazoo Gazette</h3>'
        reading += "".join(f"<p>{escape(p)}</p>" for p in excerpt[2:end]) + "</section>"
    if n == 1 or audio_html:
        reading = '<section class="transcript" aria-label="Narration transcript">'
        for track, assignment in enumerate(audio_map.get(str(n), [])):
            script_text = (root / assignment['script']).read_text(encoding='utf-8-sig')
            reading += f'<section data-transcript="{track}"><h3>{escape(assignment["title"])}</h3><p class="voice-credit">AI-generated narration</p>'
            reading += ''.join(f'<p>{escape(p)}</p>' for p in script_text.split('\n\n')) + '</section>'
        reading += '</section>'
    project_link = '<a class="project-link" href="https://github.com/ShootPara/church-fires" target="_blank" rel="noopener noreferrer">View or clone this project on GitHub</a>' if n == 101 else ''
    pages.append(f'<article id="slide-{n}" data-source="{escape(slide["slide_id"])}" class="stage">'
                 f'<div class="slide-frame"><div class="slide-canvas">{render_layout(layouts[n], urls, video)}{cover_speaker}{project_link}</div></div>{audio_html}'
                 f'<header><span>Kalamazoo Church Fires</span><span>{escape(chapter)}</span></header>'
                 f'<div class="heading"><h2>{escape(title)}</h2></div>'
                 f'<div class="material">{body}<div class="media" style="--columns:{min(4,max(1,len(images)))}">{evidence}</div></div>'
                 f'{reading}</article>')
chapter_options = "".join(f'<option value="{n}">{escape(name)}</option>' for name,n in chapters.items())
template = (root / "site/presentation.html").read_text(encoding="utf-8")
(out / "index.html").write_text(template.replace("<!-- SLIDES -->", "".join(pages))
    .replace("<!-- OPTIONS -->", "".join(options)).replace("<!-- CHAPTERS -->", chapter_options), encoding="utf-8")
copyfile(root / "design/presentation-layout.css", out / "layout.css")
for file in ("presentation.css", "presentation.js"):
    copyfile(root / "site" / file, out / file)
(out / "asset-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
visible = [{"slide": row["slide"], "object": element["id"], **next(item for item in manifest if item["source"] == element["source"])}
           for row in layouts.values() for element in row["elements"] if element.get("source") and not (row["slide"] in [19,20] and element["kind"] == "video")]
(out / "visible-assets.json").write_text(json.dumps(visible, indent=2), encoding="utf-8")
# Retire only obsolete hashed build products, never original or user-named media.
used = {item['output'] for item in manifest}
for candidate in assets.iterdir():
    if candidate.is_symlink() or not candidate.is_file():
        continue
    if re.fullmatch(r'[0-9a-f]{20}\.(mp3|mp4|png|jpg|jpeg|webp)', candidate.name):
        assert candidate.resolve().parent == assets.resolve()
        if 'assets/' + candidate.name not in used:
            candidate.unlink()
print(f"{len(pages)} slides, {len(manifest)} assets. {out / 'index.html'}")

(out / ".nojekyll").touch()
