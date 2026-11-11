# Website discovery and implementation plan

## Current direction supersedes this discovery proposal

Use `docs/IMPLEMENTATION_HANDOFF.md`, `docs/PDF_MATCH_PLAN.md` and `design/PRESENTATION_LAYOUT.md` for implementation. Brian requires his renamed individual media arranged slide by slide. The presentation PDF is reference-only. PDF-to-SVG pages, extracted presentation-PDF images and slide screenshots/crops are prohibited as visible presentation content. The current PDF-derived build was rejected.

Preserve pages 1–101 and account for blank page 102. Fit compositions inside fixed bounds above styled bottom navigation and adjacent audio controls. Provide reading/zoom views for smaller screens. This historical discovery proposal does not authorize page consolidation, a different control layout or alternative visual sources. Follow the handoff's source-provenance and browser acceptance gates.

Date: 2026-11-11. Status: source discovery complete enough to plan; content reconciliation and implementation pending.

## Verified starting point

The checkout points to https://github.com/ShootPara/church-fires.git. Before this pass it contained README.md, AGENTS.md, and docs/SOURCE_REVIEW.md, with no site implementation. No source Google files have been edited.

The live native presentation and Brian's newly supplied PDF both contain **102 slides**, at 720 by 405 points (16:9). This supersedes the earlier 103-slide count. The last slide is visually blank. The PDF is 22,707,249 bytes. All 102 pages were rendered and inspected as contact sheets for composition, not for line-by-line historical accuracy.

Native slide data contains 260 image placements (not 260 unique historical images) and five video elements. Many newspaper passages exist as images, so native text extraction is not a complete transcript. PDF audio icons demonstrate another limitation: native API extraction does not expose a dependable clip mapping.

The mapped archive contains 65 substantive files, plus four desktop.ini files: 26 MP3s, 22 newspaper PDFs, seven GLBs, four Blender files, two MP4s, three native Docs pointers and one Slides pointer. docs/source-manifest.json records relative paths, sizes and SHA-256 checksums for non-pointer files. No large originals were copied into tracked assets.

Three native script documents were captured locally:
- Verbatim excerpts: 16,162 extracted characters.
- Gazette contents: 80,163 extracted characters.
- Slide summaries: 34,269 extracted characters.

These counts exclude paragraph separators. Presence is verified; completeness and audio equivalence are not. Treat Brian's intended contract as **audio reads the displayed text**, with separate labels if an optional explanatory narration is later retained. Do not substitute the summary script for a verbatim article reading.

## Available tools and their roles

- Google Slides connector and skill: read native text, object IDs, links, geometry, video IDs and source references. The skill's design parser ran successfully. Its host file-transfer helpers assume POSIX paths; the raw connector response was saved directly with the available local file tool on Windows.
- Google Docs connector: read scripts with paragraph indexes and preserve source snapshots.
- Local PDF tools: pdfinfo and pdftoppm successfully inspected and rendered the supplied export. No new export is needed for this revision.
- Python standard library: reproducible inventory and checksums. Pillow: visual contact sheets.
- Node: available for a small static build if needed; no visitor dependency.
- Local coding worker: consider later for bounded routine implementation. This discovery pass involved source interpretation and architecture, so no inference was delegated.
- Sites skill reviewed for routing. This task is planning in Brian's existing GitHub checkout; no Site registration, hosting, or publication was initiated.

## Proposed visitor experience

A guided, deck-like presentation is the primary interface. Use real HTML text and local media inside a roomy viewport, with a persistent control strip outside the content.

Desktop composition:
- Header: title and chapter chooser.
- Main viewport: historical image, article excerpt, comparison, timeline, or optional model.
- Controls: Previous, page number/title, Next, and optional fullscreen.
- Adjacent or lower panel: Listen, playback position/speed, displayed transcript, image/source credits.
- Read continuously toggle: the same content in a normal document flow.

Keep 16:9 framing for images where it helps, but allow text to reflow. On phones, stack the media, readable text and controls; do not shrink a newspaper page to fit the screen. Provide zoom/pan for scans and a corrected text view. Images retain their aspect ratio. Long articles may have multiple guided pages with one article identity and an explicit clip/page relationship.

Navigation: buttons, chapter menu, URL fragment deep links, browser Back/Forward, and keyboard arrows when focus is not in a player, form, or zoom control. Touch targets should be at least 44 CSS pixels. Swiping is optional and must not interfere with image panning. Announce page changes and move focus predictably. Never autoplay audio or advance pages unexpectedly. Changing page stops the previous clip; continuous playback across split article pages requires an explicit later design decision.

Use a restrained brick-red accent inspired by the source, warm paper backgrounds and high-contrast controls. The existing red deck has cramped navigation and tiny newspaper columns; the new layout should give the evidence more room. Keep all text legible at 200% zoom.

## Content map

| Source slides | Role | Proposed treatment |
| --- | --- | --- |
| 1–7 | Overview, losses, deaths, causes, rebuilding | Opening chapter with sourced claims and uncertainty labels |
| 8–18 | City and buildings before the fires | Context gallery and concise building profiles |
| 19–20 | Recollections on video | Optional captioned evidence with provenance |
| 21–28 | Congregational fire and building | Guided church chapter; article reading and image comparisons |
| 29–32 | Methodist fire | Guided church chapter with article text |
| 33–37 | Presbyterian incidents and destruction | Guided church chapter distinguishing earlier fires |
| 38–48 | Deaths, memorials and family support | Dedicated chapter; retain full evidence in source library |
| 49–61 | Investigations, cornerstone and aftermath | Separate cause evidence from cornerstone/community history |
| 62–75 | Rebuilding and models | Rebuilding chapter and optional locally hosted model/video experience |
| 76–101 | Historical image appendix | Searchable/browsable source gallery linked from story pages |
| 102 | Blank closing slide | Omit from visitor sequence; retain mapping record |

This is a proposed editorial map, not a fixed new page count. Every meaningful source slide must have a destination or an explicit omission reason. Preserve the ability to trace new pages to native slide IDs.

## Media reconciliation

| Source slide | Video source | Required next check |
| --- | --- | --- |
| 19 | YouTube NymyXsB3Oi8, 1098–1160 seconds | Locate original in archive/account; establish rights and captions |
| 20 | YouTube OIm6NgBaB0c, 109–270 seconds | Locate original and identify speaker/context; captions |
| 28 | Drive 1nQFrNsmlHa4dqsHe0OO6FQfSIX-LAPDQ | Compare metadata/content to local MP4s |
| 74 | Drive 1FyNvU9j5qcEXCwSKgA-FQ4DyVr9KgnD5 | Compare metadata/content to local MP4s |
| 75 | YouTube vpE_LWm_Y08 | Locate Brian's original model/music/narration production |

Brian believes the production materials are in the Drive folder. Search and reconcile those before requesting anything again. Do not conclude that external video references prove their originals are missing. No runtime YouTube or Drive embeds in the final site.

## Implementation approach

Start with semantic HTML, CSS and small plain JavaScript modules, without a frontend framework. If duplication makes authoring difficult, use a dependency-free Node build to generate static HTML from structured content. Generate full reading content at build time; do not require fetch calls for basic file-open use.

Proposed directories:
- content/pages/: page IDs, chapter, text, source slide IDs, media references.
- content/articles/: original transcription, corrected transcription, citations and editorial notes.
- content/audio/: deterministic scripts and production metadata.
- assets/: approved optimized images, audio, video, poster images and optional GLBs.
- scripts/: inventory, build and validation.
- docs/: provenance, mapping, claim review and test results.
- dist/: complete portable production output.

Metadata for each approved asset: source path/ID, checksum, rights status, credit, transformations, output path and output checksum. A source-file hash does not establish redistribution rights. Raw connector snapshots and renders remain in ignore/. Source images need deduplication before optimization.

Initial proposed budgets, to be measured on a prototype: initial page at most 2 MB; shell JavaScript at most 50 KB compressed excluding optional 3D; audio/video use metadata-only or no preload; 3D loads only on request. Archival originals stay out of ordinary Git until rights and release strategy are resolved. Final runtime files must ship in the repository or a documented downloadable release bundle.

## Definition of success

1. All 102 source slides accounted for; meaningful material preserved, appendix integrated, blank slide explicitly omitted.
2. Every public historical claim and quotation traceable to evidence; contradictory dates, names, dollar amounts and cause claims flagged and resolved or labeled uncertain.
3. Every clip mapped to its displayed text and source article. Exact wording, omissions, split pages and pronunciation changes documented. Review old audio before replacement; preserve originals.
4. Viewport paging, chapter jumps, deep links, browser history, audio controls and article zoom work with keyboard and touch.
5. Full story remains readable without JavaScript, audio, motion or WebGL; media has appropriate alternatives.
6. Every shipped asset has provenance and a rights decision. No third-party runtime requests.
7. Production output passes disconnected-browser checks, file-open and ordinary static-server checks, narrow/mobile layout, 200% zoom, reduced motion, keyboard and screen-reader checks.
8. A clean clone/build or documented release download reproduces the visitor experience without Google, Blender or a backend.

## Next implementation milestone

Build one representative vertical slice: overview, one image-led building page, the two-page Congregational article with matched transcript/audio, and an investigation page. This tests the hard layout and media cases before converting the full collection.

Before that slice: reconcile video originals; map all 26 MP3s to scripts and displayed scans; extract/deduplicate images with citations; compare quoted text to newspaper scans. Review the family details and collapse descriptions in the summary script, which vary internally, rather than treating generated prose as primary evidence.

## Current limits

No website, audio replacements, full transcription verification or public release was produced in this discovery pass. Visual review was at contact-sheet scale; fine-print and full-resolution scan review remain pending. No audio was auditioned. No five-video/local-file equivalence was established. Existing source review remains historical context with the live-count correction above.

