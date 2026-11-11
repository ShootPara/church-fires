# Handoff validation — 2026-11-11

## Later status correction

The entries below record the original planning/extraction pass. Two later local builds exist. `ignore/presentation/` uses named media in generic grids. `ignore/pdf-presentation/` uses PDF-derived SVG foregrounds with extracted PDF images and hides named media during presentation mode. Brian rejected that approach. `scripts/build_site.py` currently builds the rejected version through `scripts/pdf_layout.py`.

File-existence checks and earlier extraction checks do not validate the required reconstruction. Compliant per-slide named-asset layouts, corrected controls and browser acceptance remain pending. Follow `docs/IMPLEMENTATION_HANDOFF.md` for correction and `docs/TEST_RESULTS.md` for current status.

## Historical planning-pass checks

At the time of this original pass, work comprised planning and extraction. The later implementation status is recorded above.

- Native deck read succeeded; refreshed snapshot has unchanged revision and 102 slides.
- Three Docs exported to readable UTF-8 text and paragraph-indexed JSON; 102-slide worklist generated. Draft/source text is not fact-checked merely by exporting it.
- 23 PDFs processed: supplied presentation (102 pages) plus all 22 newspaper originals (one page each).
- 241 unique embedded image byte files extracted. Every indexed render and image path checked to exist. PDF composition includes masks/crops; extracted image count is not a count of usable final web assets.
- All slide overview contact sheets reviewed in initial discovery. One original newspaper full-page render visually inspected in this pass; article cropping and line-by-line transcription review remain implementation work.
- Native-image sample initially failed with an expired URL; refreshing the full presentation resolved it. One image downloaded and hashed. Full native-image download not run; use the script as needed. Sample receipt: sources/extracted/native-image-sample.json.
- Both linked Drive spins matched local filenames and sizes through connector metadata. Remote content hashes were not supplied. Three YouTube originals remain unresolved.
- All 26 original MP3 filenames have candidate slide/scan mappings. Those mappings have NOT been accepted through full listening/transcription comparison. Final per-clip scripts are deliberately not marked approved.
- All Python scripts compiled successfully. Narration dry-run validated a fixture's script hash/review status and made zero network calls. Live paid API remains untested.
- Two-pass FFmpeg normalization ran against an original clip, saving a separate ignored output. Filter reports -16.00 LUFS and -1.50 dBTP. This is filter-stage evidence, not independent post-MP3-encode peak validation or listening acceptance. Recheck final encoded assets at production time.
- git diff --check passed. No commits or pushes performed.

Tool dependency: PyMuPDF 1.26.6 installed locally and pinned in scripts/requirements-extraction.txt. FFmpeg already available. Temporary outputs are under ignore/. Durable source text, worklists, mappings, scripts and instructions are in the project folder outside ignore/.

Known limitation: extractor caches existing render files and native downloads; for a changed source revision use a fresh derived output directory or move old derived files aside before rerunning. Never overwrite original Drive files. Source source-manifest hashes are from the initial inventory; do not infer current remote revision from them.
