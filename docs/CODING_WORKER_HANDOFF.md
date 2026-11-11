# Coding worker handoff

## Accepted state and scope

This is an implemented, approved presentation, not an unstarted design brief. Preserve the PDF-like compositions and Brian's named images. Old preview directories and PDF extraction proposals are not the baseline. Current instructions in AGENTS.md and this document supersede historical plans.

A normal task starts with `git status`, reading the requested files, `python scripts/build_site.py --output dist`, and `python scripts/validate_site.py dist`. Build/deploy never requires narration credentials or paid services. Do not repeat OCR or external research for approved content.

## Source ownership

| Change | Owning source |
| --- | --- |
| Menu titles for every slide | `sources/slide-titles.json` |
| Positions, dimensions, text runs, crops, borders and rotations | `sources/slide-layouts.json` |
| Named newspaper images and photographs | `sources/media/` |
| Local videos on slides 28, 74, 75 | `sources/video/`; `spins` in `scripts/build_site.py` |
| YouTube IDs, URLs and start times on 19/20 | `sources/external-videos.json` |
| Slide-to-audio assignments | `sources/audio-assignments.json` |
| Individual approved article scripts | `sources/narration/article-NN.txt`; index `articles.json` |
| Opening script | `sources/extracted/excerpts.txt` |
| Final article MP3s | `sources/audio/articles/article-NN/reading.mp3` |
| Opening MP3 | `sources/audio/opening-reading.mp3` |
| HTML shell and control order | `site/presentation.html` |
| Navigation, fullscreen, audio and video behavior | `site/presentation.js` |
| Current layout/controls styling | `site/presentation.css` (overrides base design CSS) |
| Base approved style | `design/presentation-layout.css` |
| Explicit-layout rendering | `scripts/render_slide_layout.py` |
| Static composition, copy and provenance | `scripts/build_site.py` |
| Last-page GitHub link | `project_link` in `scripts/build_site.py` |
| Deployment | `.github/workflows/pages.yml` |

`build_site.py` writes hashed assets plus `asset-manifest.json` and `visible-assets.json`. It prunes only obsolete hashed assets in the chosen output's assets directory. It does not edit source media. Use `--output dist` for production; the default `ignore/named-presentation` supports Brian's old preview link. Never hand-edit either output.

## Implementing a bounded change

1. Identify the source row/slide/asset affected. Read the original PDF and named image if visual placement matters, without extracting replacement website images from the PDF.
2. Make the smallest source change. Keep all visible content within a common 16:9 canvas. The footer reserves 64px, remains in one row, and may scroll horizontally on small screens. Images use explicit positions/crops, not arbitrary responsive grids in presentation mode.
3. Preserve existing accessible labels, focus styles, keyboard navigation, continuous reading and transcripts. SVG icons need accessible button names; silent speakers stay disabled/grey.
4. Build and run the standard-library validator. Inspect the changed slide in a browser. Check a neighboring slide and fullscreen; broaden tests only if the change affects shared behavior.
5. For audio/control changes, `scripts/check_audio.py` is the existing bounded Playwright smoke test. It expects Python Playwright and Edge at Brian's Windows path, so either install an explicitly pinned QA dependency for your environment or adapt the executable path deliberately. Browser QA is not a runtime/build dependency. Do not install unrelated tools or launch giant test sweeps.
6. Record actual tests and limits. Commit source, relevant assets and documentation, not disposable screenshots or credentials. Publish only when requested/authorized.

## Narration maintenance

There are 26 article recordings on 25 article slides, with two clips on slide 44, plus the opening reading on slide 1. Brian approved the correction placing article 16 on 51 and article 17 on 52. Do not narrate continuation slides merely because an article continues there. The two slide 44 recordings switch their matching transcript when selected.

The first 25 scripts come from the approved Gazette Article Contents. The 26th is the June 29, 1963 Terry Brown retrospective transcribed from the named clipping and appended to the Google Doc with explicit permission. `sources/narration/document-update.json` records the guarded update and readback. The newspaper's wording can contain typographical errors and historical claims; preserve them as source claims rather than silently improving history. Metadata records AI voice/provider/settings and exact source hashes.

New audio generation is a separate paid production step and requires a request for new/replacement narration. Keep old originals in the source archive. `generate_articles.py` and `generate_opening.py` verify and reuse existing final files, keep per-chunk receipts, and stop on ambiguous pending requests. Existing finals and receipts are committed; charged raw intermediate MP3s are ignored. Never remove receipts just to force a retry. For a deliberately revised recording, prepare a new versioned output job rather than overwrite accepted audio blindly. The current Speech API model has a documented retirement date of January 6, 2027; consult current official docs before future generation, not before ordinary builds.

## External videos and last page

YouTube 19 starts at 1093 seconds; YouTube 20 at 110 seconds. An authored Play card replaces the JPG. Click creates a privacy-enhanced embed; slide changes remove it to stop playback. A direct link remains available, including without JavaScript. This is an explicit exception to the original all-local-media goal. Do not add autoplay on page load or new external services. Slide 75 is the user-supplied 13.7 MB MP4 with non-silent audio, not the older 62.6 MB TEST.

Slide 101's repository link lets viewers clone the project. Keep it within slide bounds. If deploying a fork, update this link and README/deployment URLs together.

## Verification limits

All final narration files decoded; scripts were matched exactly to generated chunk inputs. That is not a human word-for-word listening audit of 81.8 minutes. Desktop browser playback, titles, key transcripts, fixed bounds at desktop/phone viewport sizes and named-image hashes were checked. Physical-phone behavior and unrestricted YouTube embedding on every visitor's network are not established. Production deployment evidence belongs in `docs/DEPLOYMENT_STATUS.md`.
