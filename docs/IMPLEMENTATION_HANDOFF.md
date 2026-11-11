## Latest replacement run - 2026-11-11

- New video: `ignore/YTDown.com_YouTube_Media_vpE_LWm_Y08_DRAFT-The-Four-Churches-First-Test_004_720p.mp4`. 13,686,864 bytes; H.264 1280x720 plus non-silent AAC; 60.116 seconds. Replaces the old 62.6 MB TEST file. Builder removes obsolete hashed output assets, preserving originals.
- Explicit labels for all 101 displayed slides: `sources/slide-titles.json`. HTML separator uses an entity to avoid encoding corruption. Do not derive menu titles from the first sentence or abbreviations such as FCC/MEC/Pres.
- Article scripts: `sources/narration/articles.json` and `article-01.txt` through `article-26.txt`. The first 25 come from the approved Gazette Article Contents export without historical rewriting. Script 26 was manually transcribed from the named slide 73 clipping, checked against the image, then appended to the live Google Doc at Brian's explicit request. Readback confirmed the prior text was unchanged. See `sources/narration/document-update.json`.
- Brian approved fixing the original audio mismatch: article 16 on slide 51; article 17 on slide 52. All 26 articles now have intended placements on 25 slides (two clips on slide 44). Slide 1's existing opening recording remains separate and unchanged.
- `python scripts/generate_articles.py --generate` produces paid OpenAI Cedar replacements with exact chunk scripts, request receipts and normalized MP3s under `sources/audio/articles/`. Completed chunks are checked and reused. Ambiguous pending requests stop instead of retrying. `--only article-NN` is available for an isolated unfinished article.
- `python scripts/select_article_audio.py` selects complete replacements and retains original archive paths. `python scripts/build_site.py` emits the portable local site. Article panels show individual matching scripts; slide 44 switches text with its recording selector.
- The narration key is in ignored `dev.vars`. Never print it or copy it to the site. Original MP3 archive is untouched. No runtime API calls.
- Historical transcriptions retain source wording, including the 1963 clipping's apparent typesetting errors. The retrospective identifies arson as a contemporary suspicion and quotes the subsequent denial; do not rewrite suspicion as established fact.

## Audio/video update — 2026-11-11 (latest user direction)

- Slide 75 uses `G:/My Drive/2024 Videos/The Four Churches First Test.mp4` (60.06 seconds, H.264/AAC, 640×360). Copied locally by the builder; no streaming dependency.
- Native audio assignments are recorded in `sources/audio-assignments.json`: 25 recordings on 24 original slides, including two on slide 44. Archive clip 17 has no native audio placement and is not added. Continuation pages do not automatically receive audio.
- Brian explicitly approves Gazette Article Contents as accurate scripts. Do not re-OCR or rewrite them. Original recordings remain intact and are used for these assignments.
- The ONE added assignment is slide 1: the complete `sources/extracted/excerpts.txt` (Article Text to be Read Verbatim), read by a paid AI voice. Large speaker below the title card and the footer speaker control the same recording.
- Previous/Next and enter/exit fullscreen use SVG icons with accessible labels. The footer speaker remains visible and disabled/grey on silent slides. One fixed bottom row remains required.
- `scripts/generate_opening.py --generate` uses the private ignored `dev.vars` key, writes per-chunk scripts and receipts under `sources/audio`, then joins and normalizes to `opening-reading.mp3`. It resumes completed chunks but refuses ambiguous interrupted attempts. Do not print or commit credentials. Paid requests have no automatic retries.
- Voice: OpenAI Cedar, measured documentary delivery. Documentation consulted: https://developers.openai.com/api/docs/guides/text-to-speech . Speech API model is available now but retires January 6, 2027; existing generated MP3s remain standalone. Review the generator before future regeneration after that date.
- Full Gazette source collection is available in the article panel on narrated slides; individual per-clip transcript segmentation remains unimplemented. No claim of clip-specific transcript matching is made.

# Implementation handoff — start here

Latest control direction from Brian: use ONE bottom control row. Previous and Next must be adjacent, followed by chapter/slide selectors, reading controls, fullscreen and audio. This supersedes all earlier two-row footer instructions. Reserve 64px for the bar. On narrow screens the single row may scroll horizontally so controls remain reachable.

## Binding source contract and rejected implementation

Brian explicitly rejected the PDF-derived shortcut on 2026-11-11. This section supersedes older extraction fallback and layout advice throughout the handoff.

- Visible historical images, newspaper clippings, headline strips and date strips must use the individually renamed files in `ignore/Deconstructed Original Slides/media/`, or documented optimized derivatives of those files. Preserve exact source filenames and SHA-256 hashes in the asset manifest.
- Use `sources/slide-layouts.json` to assign each visible element a source asset ID and explicit position, size, crop, rotation and stacking order. Reused images keep explicit slide associations. Source filename ordering alone cannot define a composition.
- Use native Slides text and the exported Docs for editable text. Rebuild panels, arrows, borders and labels as authored HTML/CSS or small SVG annotations. The PDF supplies visual measurements and comparison evidence only.
- Do not use presentation-PDF image extraction, `page.get_svg_image()`, PDF-to-SVG page conversion, rasterized slide backgrounds, full-page screenshots, or crops of rendered slides as visitor-facing slide content. Putting named media in a hidden or continuous-reading section does not satisfy the visible presentation requirement. Merely renaming PDF-derived files does not change their provenance.
- A missing named asset must produce a specific unresolved item identifying the slide and role. Continue other work. Obtain Brian's explicit agreement before substituting a presentation-PDF-derived asset. Existing standalone newspaper PDFs may support transcript verification, but do not silently replace his supplied clippings.
- Preserve all supplied media files. Optimization outputs belong in a separate location with recorded transformations.

### Required recovery sequence

1. Read `docs/PDF_MATCH_PLAN.md` and `design/PRESENTATION_LAYOUT.md`, including the control defect reference. The original slide-by-slide table remains the visual worklist.
2. Replace the current `scripts/build_site.py` integration of `scripts/pdf_layout.py`. Remove the PDF-derived foreground and the CSS that hides named media in presentation mode. The default site build must consume the explicit layout and named-asset records. Keep any retained rejected experiment clearly outside the build/import path.
3. Implement the PDF plan's representative pilot slides and the styled control bar using named assets. Render and inspect them before applying the approach to the full deck.
4. Complete all 101 content slides, preserve stable IDs, and record blank page 102. Run the source-provenance gate below alongside bounded visual and interaction checks.

### Source-provenance acceptance gate

For every visible image on every presentation page, record slide ID, element ID, exact named source file, source SHA-256, output path/hash and any transformation. Include all image-bearing elements, including CSS backgrounds and SVG image references. An unchanged copy must match the source hash. An optimized derivative must have a reproducible transformation record. Decorations and video posters need their own explicit provenance or authored classification.

Check the rendered presentation, not only the manifest. Inspect slides 10, 21, 24 and 98 at minimum to verify that the actual displayed image URLs resolve to the named assets. Reject any PDF-derived visual overlay that obscures those assets. Every slide requires a visual comparison against its PDF reference. File counts, successful builds, valid URLs, or a visually similar PDF conversion cannot establish compliance.

Report implementation, source verification and browser verification separately in `docs/PDF_MATCH_RESULTS.md`. A pending check must remain pending. Do not call the correction complete until the source gate, slide comparisons and fixed-control checks pass.

Brian selected `design/presentation-concept.html`, including the bounded slide layout and bottom audio/control bar. Use `design/presentation-layout.css` as the styling reference, refined by the later per-slide composition plan. The current PDF-derived implementation was rejected. Full compliant implementation and browser acceptance remain pending.

The primary supplied visual assets are now in `ignore/Deconstructed Original Slides/media/`, named by source slide and content. Use these individual clippings and images. The older `site/` and `ignore/preview/` prototype uses cropped slide screenshots and is superseded visually. Reconcile supplied filenames with native slide IDs and preserve provenance when promoting assets into the final site. The native object-count folder inventory includes decorative and audio-icon objects and must not dictate the number of visitor-facing clippings.

## Read in order (do not reread all raw exports)

1. This file: work sequence and acceptance gates.
2. `docs/PDF_MATCH_PLAN.md` and `design/PRESENTATION_LAYOUT.md`: per-slide correction worklist, source rules and control requirements. Then `docs/EXTRACTION_GUIDE.md` for reference extraction commands and recovery.
3. `docs/AUDIO_PRODUCTION.md` and `docs/AUDIO_MAP.md`: paid generation and script mapping.
4. `docs/WEBSITE_PLAN.md`: viewport design and chapter map.
5. `docs/SOURCE_REVIEW.md`: historical context; its 103-slide count is superseded by 102.
6. Work only on the relevant entries in `sources/extracted/slide-worklist.md` and `.json`.

## Source hierarchy and fidelity

The native deck and supplied PDF both have 102 pages. Preserve the story and meaningful evidence, not PDF export defects. Brian reports damaged text in the PDF. Use native Slides text for editable text, original newspaper scan for newspaper quotations, and native Slides appearance when PDF layout is ambiguous. Never copy malformed PDF line breaks or recreate illegible newspaper typography as body text. The PDF is a layout/evidence reference, not the authoritative text source.

All original native text and three Docs are exported under `sources/extracted/`. Do not overwrite those with editorial corrections. Native text order is object order, not guaranteed reading order. New content uses readable HTML. Keep quotation wording and editorial commentary distinct. Do not repair uncertain names or dates by guessing.

## What every source slide must produce

For slides 1–101, record: native slide ID; final chapter/page ID(s); all meaningful text; each meaningful image/object ID and resulting local asset; source credit and rights decision; article ID/transcript if present; audio mapping if present; alt text; any intentional consolidation or omission and why. Slide 102 is blank: mark omitted-blank. The generated worklist lists every object, native text, available notes, geometry and image crop properties.

Repeated nav labels and decorative corners need not become content assets. Repeated photos should share one asset after byte-hash/visual deduplication. A composed comparison (e.g. slide 24 roof details with arrows, slide 65 interiors) must preserve its explanation; do not extract only the main image and lose the annotations. Slide 14 includes a historical table: transcribe it as a real table or retain a source image plus complete reading alternative. Slides 19/20/75 need video/caption decisions; 28/74 use the local spins. Gallery 76–101 retains titles and sources, including both images on 98 and apparent duplicates 96/97 pending visual comparison.

## Fixed implementation choices

Use static HTML/CSS and small plain JavaScript. A dependency-free Node build is acceptable to generate pages from structured data. No framework, database, account system or runtime service. Emit full content into HTML; do not rely on fetch for initial file-open use. Use relative asset URLs for GitHub Pages subpaths and local files. Optional 3D can be deferred until the story works; vendor and pin its viewer dependency if introduced.

Default page controls: Previous/Next, chapter selector, current page title/count, fullscreen when available, reading-view toggle. Keyboard arrows only outside interactive controls. Stable URL fragments with browser history. The presentation canvas fits uniformly inside the available width and height, with fixed bottom controls. Reading and zoom views provide readable small-screen alternatives. Native audio controls, transcript next to player, no autoplay; stop audio on page change. Scan zoom has reset and keyboard controls. Reduced motion and no-JavaScript continuous reading are required.

## Work packages and completion gates

### 1. Finish evidence mapping before building

Use generated files; no need to repeat full extraction unless sources changed. Create `content/pages.json`, `content/articles/`, `content/audio/`, `content/assets.json` and `docs/CONTENT_DECISIONS.md`. Keep schema simple:

- Page: `id, chapter, title, sourceSlideIds[], body, assetIds[], articleIds[], audioIds[]`.
- Asset: `id, source, sourceSha256, output, outputSha256, transform, attribution, rightsStatus, alt`.
- Article: `id, newspaper, publicationDate, page, sourceScan, crop, originalText, correctedText, corrections[], certainty`.
- Audio: `id, articleId, pageIds[], displayTranscript, spokenScript, pronunciationChanges[], originalPath, generationJob, reviewStatus`.

For each quote compare the full selected passage with the scan. Preserve unreviewed material as draft. The summary Doc is explanatory prose, not a source quotation. Verify Slater/Morren family counts, collapse mechanism, fire/event vs publication dates, Central Station date discrepancies, church-building dates, losses and inflation. Keep arson as contemporary suspicion except where evidence establishes an incident-specific finding. Resolve source conflicts individually; don't block unrelated pages.

Gate: 102 source rows accounted for; every included item has a destination or documented omission; all initial prototype claims/transcripts reviewed. Full collection can proceed chapter by chapter, but no unreviewed copy goes public.

### 2. Build one representative slice

Implement the pilot pages listed in `docs/PDF_MATCH_PLAN.md` with explicit layouts, named assets and the styled bottom controls. Include the existing draft transcript where available and keep its review status visible in content metadata. Make layout and navigation work before producing final audio for the entire site. Full-slide screenshots and PDF-derived foregrounds are prohibited even when an alternate text or media view exists.

Gate: correct text, readable 390px and desktop layout, keyboard paging, history, no-JS reading, scan zoom, no unwanted remote requests. One focused repair pass, then recheck only failures.

### 3. Convert remaining chapters

Use the same page components and metadata. Preserve chronology, firefighters, investigations, rebuilding and image appendix. Add the two local spin videos with posters and controls. YouTube originals are unresolved: search Drive by IDs/titles before asking Brian; a missing video can be represented by an explicitly documented transcript/still alternative only if it preserves the information and rights permit. Do not silently substitute unrelated video or hotlink YouTube.

Gate: mapping completeness and no missing local asset references. Do not redesign the shell per chapter.

### 4. Paid narration

Follow AUDIO_PRODUCTION.md. User has requested paid modern AI voices; do not substitute local/free robotic TTS. Prepare reviewed scripts first. Select an available paid provider voice using short samples, then batch accepted settings. Record costs from actual provider pricing/account rather than inventing a dollar figure. No generation has been purchased during planning. If credentials are unavailable, finish scripts and jobs and identify that specific blocker; continue independent implementation.

Gate: all final clips have script/hash, voice/model/settings/date, pronunciation notes, normalization report and listening review. Preserve old clips. No endless voice auditions: two candidate samples initially, one targeted regeneration per defective chunk before reporting the remaining issue.

### 5. One bounded release validation

Run a structural content checker once: unique IDs, referenced files exist, approved rights, transcripts for audio, every source slide mapped, no remote runtime asset URLs. Run build once. Browser cases: desktop 1440x900; mobile 390x844; keyboard-only paging and controls; 200% text zoom; reduced motion; JS disabled; disconnect network after loading local server, reload and traverse chapters/media; file-open check; static server under a subdirectory. Screen-reader spot check page announcements and audio controls. Physical phone only if available—report it untested otherwise.

Record exact outcomes in `docs/TEST_RESULTS.md`. Fix observed failures and rerun only affected cases plus build if code changed. No load tests, fuzzing, dependency churn, screenshots of all responsive permutations, repeated full scans, or benchmark campaign. Do not claim unperformed accessibility/physical-device tests. Offline failure blocks release. A remaining rights problem blocks that asset, not all independent development.

## Known state and next action

Three script exports are present; 26 original clips and 22 newspaper PDFs are inventoried. The retrospective clip's original newspaper scan has not been identified among those PDFs; source slide 73 contains the clipping image. Clip matches in AUDIO_MAP are hypotheses by headline/slide appearance, not verified listening matches. Two Drive videos match local MP4 names and sizes (not independently remote-hash verified). Three YouTube originals remain to locate.

Next implementation begins with the recovery sequence above. Layout/source correction and control styling take priority. Resume the article/audio work packages after those corrections are established.
