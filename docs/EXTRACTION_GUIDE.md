# Extraction guide

Run commands in `C:\Projects\Church Fires GitHub Site`. Python 3.12 and FFmpeg are available. PyMuPDF 1.26.6 is pinned in `scripts/requirements-extraction.txt` for source review and reference rendering. Presentation-PDF renders and extracted images are reference material only. Brian rejected their use as visible site content. Use his renamed media under `ignore/Deconstructed Original Slides/media/` and follow the binding source contract in `docs/IMPLEMENTATION_HANDOFF.md`.

## Already available

- `sources/extracted/{excerpts,gazette,summaries}.txt`: human-readable native Docs text.
- Matching `.json`: document IDs, revision IDs and paragraph indexes for traceability.
- `sources/extracted/slide-worklist.{md,json}`: all 102 source slides, native text and object metadata.
- `docs/source-manifest.json`: archive paths, bytes and SHA-256 hashes. Four desktop.ini entries are system files, not content.
- `docs/slide-inventory.json`: earlier compact structural inventory.
- `Kalamazoo Church Fires Presentation.pdf`: supplied 102-page layout reference; text export defects reported by Brian.
- `ignore/pdf-review/`: 102 overview JPEGs and five contact sheets.
- `ignore/drive-review/raw-template.json`: complete connector snapshot, including short-lived native image URLs.
- `sources/extracted/pdf-index.json`: maps each extracted image/page to its original PDF and page number.
- `ignore/extraction/presentation/`: PDF slide renders.
- `ignore/extraction/newspaper-NN/`: rendered original newspaper pages; look up NN in pdf-index.json, not by guessing order.
- `ignore/extraction/images/`: original embedded image bytes named by SHA-256. These can include duplicate decorative assets, masks, or uncropped source images. They are not yet approved web assets.

## Repeatable commands

```powershell
python -m pip install -r scripts/requirements-extraction.txt
python scripts/extract_sources.py text
python scripts/extract_sources.py pdf
```

Text extraction overwrites generated `sources/extracted/` files, not edited content. PDF extraction caches page renders and image bytes. If a PDF changes, use a new output directory or move its old derived directory aside before rerunning; existing renders are not automatically invalidated. Do not repeatedly hash 716 MB of unchanged originals. `python scripts/inventory_sources.py` is only for a deliberate source inventory refresh.

## Image extraction order

1. Map Brian's renamed media to each slide and role. Record exact source filename, hash and output derivative. Use these assets in the visible presentation. Native-image download tooling may investigate missing sources, with any proposed replacement recorded separately.
2. If URLs expired, call the connected Google Drive `get_presentation` with presentation ID `14zyrIraeNE62MBTTteZxYaDqG_0T7kGfRWu1epeN5vE` and **omit fields**. Save the full response as UTF-8 JSON to `ignore/drive-review/raw-template.json` using the file tool. Then rerun failed image extraction once. Do not print the 1.5 MB response into chat or paste it by hand.
3. Record missing named assets by slide and role. Continue independent work. Do not substitute a presentation-PDF image, SVG page, screenshot or crop. A presentation-PDF-derived replacement requires Brian's explicit agreement.
4. Rebuild annotations over individual named assets using authored HTML/CSS/SVG. Use native geometry and PDF renders as positioning evidence. Do not crop a rendered slide to capture the composition.
5. Newspaper body text: original newspaper PDF render is the evidence; `gazette.txt` is the transcription starting point. Do not OCR if a faithful transcription is already present. Compare all selected quotations to the scan; if OCR is needed for a gap, label it uncorrected until proofread.
6. If the supplied PDF garbles a title, rebuild it from native text using HTML. Do not transcribe garbling or flatten the entire page into a background.

Use native transform/crop metadata as evidence, not an automatic guarantee of image placement. Nested groups carry transforms; the worklist records objects but does not compose nested transforms for you. The rendered slide/native editor is the visual check.

## Newspaper clips

All 22 originals are at `G:\My Drive\Church Fires Presentation\Gazettes`. The PDF index retains full filenames and hashes. Use them to verify newspaper text and attribution. Use Brian's named clipping files for the visible presentation, including the retrospective on slide 73. Article IDs must not simply equal PDF IDs.

For each used article record its named clipping file, source date/page, hash, optimization settings, text and attribution. Additional higher-resolution reading assets require documented provenance and must not silently replace the named presentation clipping. Preserve originals.

## Source refresh and failure limits

The three native Docs IDs are in AGENTS.md. Use `get_document_text`, save the complete response to the corresponding `ignore/drive-review/*.json`, then run the text exporter. Never read a .gdoc pointer as if it contained the document. Compare revision IDs before refreshing; do not redo unchanged source discovery.

One expired-link refresh and one retry are sufficient. If a source remains inaccessible, record its ID and affected pages, use verified local evidence where sufficient, and continue independent work. Do not repeatedly search the whole Drive or ask Brian for material already in this folder.
