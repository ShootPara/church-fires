# Implementation status and verification

Latest verification is recorded in `docs/PDF_MATCH_RESULTS.md`. All 101 content slides received a visual comparison pass. Native crop reconstruction, 240 named-source placements and bounded browser interaction checks are now recorded there. The earlier pending statements below are historical.

The current build now produces `ignore/named-presentation/index.html`. See `docs/PDF_MATCH_RESULTS.md` for verified source identity and remaining acceptance work. The PDF-derived build described below is the rejected historical version.

Updated 2026-11-11 after Brian rejected the PDF-derived implementation. `python scripts/build_site.py` currently writes `ignore/pdf-presentation/index.html`. It imports `scripts/pdf_layout.py`, converts PDF pages into inline SVG, extracts embedded PDF images and displays that composition. Named media is copied into the output but hidden during ordinary presentation use. This approach fails Brian's required source/layout contract.

The earlier `ignore/presentation/index.html` uses named media in generic grids. It is the comparison baseline for `docs/PDF_MATCH_PLAN.md`. Compliant per-slide reconstruction remains pending.

The rejected build completed with 101 slides and blank slide 102 omitted. Its 442 local asset references were checked for file existence, and `git diff --check` passed. These checks establish build execution and file existence only. The 220-entry asset manifest does not cover all PDF-extracted images in the visible SVG. No complete visible-asset provenance verification was performed.

Follow the recovery sequence in `docs/IMPLEMENTATION_HANDOFF.md`. Replace the PDF build path with explicit named-media layouts and correct the controls against `design/PRESENTATION_LAYOUT.md` and the defect screenshot. Record source compliance, per-slide comparisons and actual browser checks in `docs/PDF_MATCH_RESULTS.md` during implementation. That results file has not yet been produced.

The site is a local review build. The Congregational excerpt is a draft. Remaining work includes transcription and historical claim verification, rights decisions, three embedded video originals, and narration. ElevenLabs credentials were unavailable. The footer reserves the narration area. Browser interaction, mobile, fullscreen and offline browser acceptance remain pending.
