## Latest replacement run - 2026-11-11

- New video: `ignore/YTDown.com_YouTube_Media_vpE_LWm_Y08_DRAFT-The-Four-Churches-First-Test_004_720p.mp4`. 13,686,864 bytes; H.264 1280x720 plus non-silent AAC; 60.116 seconds. Replaces the old 62.6 MB TEST file. Builder removes obsolete hashed output assets, preserving originals.
- Explicit labels for all 101 displayed slides: `sources/slide-titles.json`. HTML separator uses an entity to avoid encoding corruption. Do not derive menu titles from the first sentence or abbreviations such as FCC/MEC/Pres.
- Article scripts: `sources/narration/articles.json` and `article-01.txt` through `article-26.txt`. The first 25 come from the approved Gazette Article Contents export without historical rewriting. Script 26 was manually transcribed from the named slide 73 clipping, checked against the image, then appended to the live Google Doc at Brian's explicit request. Readback confirmed the prior text was unchanged. See `sources/narration/document-update.json`.
- Brian approved fixing the original audio mismatch: article 16 on slide 51; article 17 on slide 52. All 26 articles now have intended placements on 25 slides (two clips on slide 44). Slide 1's existing opening recording remains separate and unchanged.
- `python scripts/generate_articles.py --generate` produces paid OpenAI Cedar replacements with exact chunk scripts, request receipts and normalized MP3s under `sources/audio/articles/`. Completed chunks are checked and reused. Ambiguous pending requests stop instead of retrying. `--only article-NN` is available for an isolated unfinished article.
- `python scripts/select_article_audio.py` selects complete replacements and retains original archive paths. `python scripts/build_site.py` emits the portable local site. Article panels show individual matching scripts; slide 44 switches text with its recording selector.
- The narration key is in ignored `dev.vars`. Never print it or copy it to the site. Original MP3 archive is untouched. No runtime API calls.
- Historical transcriptions retain source wording, including the 1963 clipping's apparent typesetting errors. The retrospective identifies arson as a contemporary suspicion and quotes the subsequent denial; do not rewrite suspicion as established fact.

Current completed audio implementation and validation: `docs/AUDIO_IMPLEMENTATION_RESULTS.md`. Opening narration generated successfully; no credential blocker remains.

## Audio/video update â€” 2026-11-11 (latest user direction)

- Slide 75 uses `G:/My Drive/2024 Videos/The Four Churches First Test.mp4` (60.06 seconds, H.264/AAC, 640Ã—360). Copied locally by the builder; no streaming dependency.
- Native audio assignments are recorded in `sources/audio-assignments.json`: 25 recordings on 24 original slides, including two on slide 44. Archive clip 17 has no native audio placement and is not added. Continuation pages do not automatically receive audio.
- Brian explicitly approves Gazette Article Contents as accurate scripts. Do not re-OCR or rewrite them. Original recordings remain intact and are used for these assignments.
- The ONE added assignment is slide 1: the complete `sources/extracted/excerpts.txt` (Article Text to be Read Verbatim), read by a paid AI voice. Large speaker below the title card and the footer speaker control the same recording.
- Previous/Next and enter/exit fullscreen use SVG icons with accessible labels. The footer speaker remains visible and disabled/grey on silent slides. One fixed bottom row remains required.
- `scripts/generate_opening.py --generate` uses the private ignored `dev.vars` key, writes per-chunk scripts and receipts under `sources/audio`, then joins and normalizes to `opening-reading.mp3`. It resumes completed chunks but refuses ambiguous interrupted attempts. Do not print or commit credentials. Paid requests have no automatic retries.
- Voice: OpenAI Cedar, measured documentary delivery. Documentation consulted: https://developers.openai.com/api/docs/guides/text-to-speech . Speech API model is available now but retires January 6, 2027; existing generated MP3s remain standalone. Review the generator before future regeneration after that date.
- Full Gazette source collection is available in the article panel on narrated slides; individual per-clip transcript segmentation remains unimplemented. No claim of clip-specific transcript matching is made.

# Agent instructions

Brian requested removal of his visible name, leaving its space empty. Narration follows original slide assignments only. Never display pending-work messages on slides or controls.

Historical audio direction (superseded by the audio/video update above): previously only recorded slides had controls and slide 1 was silent. Do not narrate a whole newspaper page merely because its image appears. Use original slide/clip associations and verified scripts. Never display Narration pending, missing-source warnings or implementation status on visitor-facing slides or controls. Record unresolved work in project documentation.

Latest control direction from Brian: use ONE bottom control row. Previous and Next must be adjacent, followed by chapter/slide selectors, reading controls, fullscreen and audio. This supersedes all earlier two-row footer instructions. Reserve 64px for the bar. On narrow screens the single row may scroll horizontally so controls remain reachable.

## Mandatory correction from Brian â€” read before implementation

Brian rejected the PDF-derived presentation shortcut on 2026-11-11. Sol must implement `docs/IMPLEMENTATION_HANDOFF.md`'s source and acceptance contract and `docs/PDF_MATCH_PLAN.md` using Brian's individually renamed images in `ignore/Deconstructed Original Slides/media/`. The presentation PDF is a visual reference only. Do not extract its images for the visible site, convert its pages to SVG, or use slide screenshots/crops as the presentation. Do not hide the supplied images behind a PDF-derived foreground. CSS/SVG authored arrows and decorations are allowed.

The rejected historical build called `scripts/pdf_layout.py` and emitted `ignore/pdf-presentation/`. The current builder uses named media and explicit native layouts, emitting `ignore/named-presentation/`. See `docs/PDF_MATCH_RESULTS.md` for the latest review. It is not an accepted baseline or a completed implementation. Remove the PDF rendering path from the site build during correction. Use explicit per-slide layouts and native text. Asset existence checks alone cannot pass acceptance. Prove the images actually visible in presentation mode resolve to Brian's named media through recorded provenance.

Brian also rejected the current bottom controls' appearance. Follow the control-bar requirements in `design/PRESENTATION_LAYOUT.md`, including the defect reference `design/references/rejected-controls.png`. Keep navigation and audio together at the bottom, with consistent styled controls and stable bounds. Implement and visually verify the controls before claiming completion.

## Latest PDF fidelity review

Read `docs/PDF_MATCH_PLAN.md` before further presentation layout work. It contains 102 page-specific comparison rows, implementation order, and bounded acceptance checks. Its comparison describes the earlier `ignore/presentation/` build. The subsequent PDF-derived build was rejected. Preserve source slide order and compositions while retaining fixed bottom navigation/audio, optional article text and a bounded fullscreen shell. A continuous accessible reading route remains required.

## Implementation handoff â€” GPT-6.1 Sol starts here

Brian selected the latest presentation concept on 2026-11-11. Start with `design/PRESENTATION_LAYOUT.md` and the actual `design/presentation-concept.html` preview. `design/presentation-layout.css` is the editable visual specification. This selected design supersedes earlier layout suggestions and the older four-page preview in `site/`. New labeled source media is in `ignore/Deconstructed Original Slides/media/`. Use those individual images and clippings. Continue implementation when requested using the selected style, fixed slide bounds, bottom navigation and adjacent audio controls.

Read `docs/IMPLEMENTATION_HANDOFF.md` first, then `docs/EXTRACTION_GUIDE.md` and `docs/AUDIO_PRODUCTION.md`. These are the detailed execution plan, commands, acceptance gates and bounded testing policy. `docs/AUDIO_MAP.md` / `docs/audio-mapping.json` list all 26 clip candidates. `sources/extracted/slide-worklist.md` / `.json` account for all 102 current slides; the three script exports are alongside them. `sources/extracted/pdf-index.json` maps extracted newspaper/slide images to originals. Do not redo discovery or build before reviewing this handoff.

Implementation was authorized, followed by Brian's request to harden these handoffs after rejecting the shortcut. The current documentation correction does not establish implementation acceptance. Paid modern AI narration is requested after script verification. No audio has been purchased yet. Preserve native text. Candidate audio mappings are not verified transcripts. All large reference renders stay in ignored `ignore/`; durable text and maps are under `sources/extracted/`.

Start correction with the handoff's recovery sequence and the PDF plan's pilot slides. Finish layout and controls before expanding audio work. Use bounded checks and record unresolved sources while continuing independent work.

## Mission

Turn Brian Ream's Google Slides presentation, **1925â€“1926 Kalamazoo Church Fires**, into a self-contained historical website that delivers the same information in a clearer, more accessible form.

The finished project must be cloneable and usable without Google Slides, Google Drive, Blender, a database, an API, a hosted backend, or any proprietary server. All content needed at runtimeâ€”including text, images, 3D assets, video, captions, and narrationâ€”must live in the repository or in a documented release artifact generated from repository sources.

## Product constraints

- Prefer a static site that can be opened from built files or served by any ordinary static host, including GitHub Pages.
- Node.js may be used for development/build tooling. Do not require Node.js, a package registry, or any server after the production build has been generated.
- Minimize dependencies. Pin any necessary development dependencies and explain why they exist.
- Do not load fonts, scripts, analytics, audio, images, models, maps, or other assets from third-party CDNs at runtime.
- Do not introduce accounts, authentication, a database, telemetry, or an external API.
- The story must remain understandable without audio, animation, WebGL, or JavaScript. Progressive enhancement is preferred.
- Provide responsive keyboard and touch navigation, semantic headings, visible focus, alt text, captions/transcripts, reduced-motion behavior, and strong contrast.
- Keep historical fact separate from contemporary speculation. In particular, present arson as an investigated contemporary suspicion unless a source conclusively establishes more.
- Preserve source attribution and licensing/provenance metadata for every historical image, newspaper scan, quotation, model, music track, and generated voice.

## Source material

The source folder is mapped locally at:

`G:\My Drive\Church Fires Presentation`

Important native Google files:

- Presentation: <https://docs.google.com/presentation/d/14zyrIraeNE62MBTTteZxYaDqG_0T7kGfRWu1epeN5vE/edit>
- Verbatim article excerpts: <https://docs.google.com/document/d/1Wb8qGWj0DTtP524oCi7Ix4hWECqU8YhbwlupRdxXCgA/edit>
- Gazette transcriptions: <https://docs.google.com/document/d/1-VtFJRzG7h7WN0zO37hNezaNp66vlPzbluVLFXgBlek/edit>
- Slide narration/summaries: <https://docs.google.com/document/d/17FimVlfApvYuJi40Q6Mvl6GvYwOqIWKSUBIEAzuAnEQ/edit>

Read `docs/SOURCE_REVIEW.md` before planning or importing content. The mapped Drive contains large binary sources; do not bulk-copy or commit them without first deciding on web formats, rights, size budgets, and Git LFS/release-asset strategy.

## Narrative spine

The current presentation has 102 slides (native and PDF verified 2026-11-11) and follows this broad arc:

1. Scope and summary of the 1925â€“1926 fire series.
2. Kalamazoo and the three major church buildings before the fires.
3. The First Congregational fire of December 29, 1925.
4. The First Methodist Episcopal fire of March 14, 1926, including the deaths of firefighters Claus Slater and John Morren.
5. The First Presbyterian fire of July 7, 1926.
6. Investigations, known/claimed causes, and contemporary arson suspicion.
7. Community response, memorials, family relief, and rebuilding.
8. The replacement churches and First Congregational Church visualizer/model sequence.
9. Historical image-source appendix.

The presentation view preserves source slides 1â€“101 in order and accounts for blank slide 102. Chapters, article/source views, transcripts and continuous reading provide additional ways to access the same information.

## Audio upgrade

The Drive contains 26 MP3 article readings totaling about 1 hour 15 minutes. Replace them with better AI narration only after the narration script is fact-checked and normalized against the source text.

- Keep one deterministic script/transcript per clip in the repository.
- Record voice/model/provider, generation date, settings, and pronunciation notes in metadata.
- Generate final web audio as local assets (prefer broadly supported compressed formats, with an optional second codec only if justified).
- Normalize loudness and peaks consistently; remove accidental silence and artifacts without changing the source meaning.
- Every clip needs an adjacent transcript and accessible controls.
- Do not make runtime TTS calls. Voice generation is a production step, never a website dependency.
- Preserve the old clips until replacements are reviewed and accepted; do not overwrite the source archive.

## Repository state established 2026-11-11

- The previously empty folder was initialized as a Git repository on branch `main`.
- `.gitignore` ignores `/ignore/`.
- `ignore/` exists as a local disposable drop-zone and is intentionally not tracked.
- GitHub CLI 2.103.3 was installed and authenticated as `ShootPara`.
- Source discovery and review were performed through both the mapped Drive and the connected Google Drive account.
- `docs/SOURCE_REVIEW.md` records the findings and migration implications.

## Working practices

- Put durable findings, plans, scripts, and generated manifests in this project folder so later agents can use them.
- Put disposable exports and intermediate renders in `ignore/`.
- Never edit the Google Slides or Drive sources unless Brian explicitly requests it.
- Avoid committing giant unoptimized originals. Keep a manifest with source path, checksum, rights, transformation, output path, and attribution.
- Before changing architecture, inspect the current repository and any existing plan/docs.
- Test a production build offline. A successful offline load is a release criterion.
- If a historical statement cannot be traced to a source, mark it as unresolved rather than smoothing it into fact.

