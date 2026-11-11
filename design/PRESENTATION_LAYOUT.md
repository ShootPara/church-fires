# Presentation layout contract

Latest control direction from Brian: use ONE bottom control row. Previous and Next must be adjacent, followed by chapter/slide selectors, reading controls, fullscreen and audio. This supersedes all earlier two-row footer instructions. Reserve 64px for the bar. On narrow screens the single row may scroll horizontally so controls remain reachable.

## Current correction and bottom controls

Brian rejected the PDF-derived presentation and current control appearance on 2026-11-11. Use his renamed media and the binding source contract in `docs/IMPLEMENTATION_HANDOFF.md`. `docs/PDF_MATCH_PLAN.md` defines per-slide compositions within fixed outer bounds. Page-specific title placement supersedes the concept's universal header/title rows. Retain the selected colors, bottom controls and adjacent audio area.

`design/references/rejected-controls.png` is Brian's defect screenshot. Use `design/presentation-concept.html` and `design/presentation-layout.css` as styling references. Correct the default-looking buttons, oversized slide selector and loosely grouped second row.

- Apply one shared style to buttons and selects with consistent Arial typography, weight, line height, padding, border, corner radius and vertical alignment. Use warm paper surfaces, ink text and the dark brick footer.
- Give Previous and Next equal widths. Bound the chapter and slide selectors within a balanced navigation group. Long slide titles may truncate visually while retaining complete accessible labels. Avoid a slide selector consuming nearly the entire wide-screen row.
- Group Read article, Continuous reading and Fullscreen consistently in the second row. Reserve an aligned audio/player area beside that group, including on slides with unavailable narration. Pending audio uses readable subdued status in that reserved area.
- Provide distinct hover, pressed, keyboard-focus and disabled appearances. Disabled Read article remains legible and noninteractive. Use actual disabled semantics, visible focus, accessible selector labels and at least 44px touch targets.
- Keep footer height and control positions identical across slides, article toggles and audio availability at each viewport breakpoint. Desktop starts with the approved 112px two-row footer. Use a deterministic compact layout on mobile and short landscape screens. Reserve footer space before fitting the slide.
- Verify Previous/Next boundaries, selectors, article toggle, continuous view, fullscreen entry/exit and audio behavior. Capture the repaired bar at 1440×900, 390×844 and 844×390, including disabled and keyboard-focus states. Compare with the selected concept and defect screenshot. CSS edits alone do not establish visual acceptance.

These sizing/grouping requirements translate Brian's request to fix the pictured controls into implementation guidance. Tune exact widths using browser renders within the approved visual direction.

Selected by Brian on 2026-11-11 after reviewing the bounded slide concept with audio beside the bottom controls. This document and `presentation-layout.css` define the selected visual direction for implementation by any subsequent model.

## Files and sources

- `design/presentation-concept.html` is the self-contained interactive reference with embedded sample imagery.
- `design/presentation-layout.css` is the editable styling source. `presentation-concept.css` is generated from it.
- `scripts/build_visual_concept.py` rebuilds the reference with `python scripts/build_visual_concept.py` from the repository root.
- `ignore/Deconstructed Original Slides/media/` contains Brian's labeled image and clipping assets. Promote selected files to tracked optimized assets with a source manifest during implementation.
- `sources/extracted/` contains native text and document exports. The article excerpt in the concept is a sample awaiting verification.

## Visual specification

Brick background is #ac3025, paper panels are #f9f4e9, ink is #241d19, and the bottom bar is #75241d. Use Georgia bold for titles and Arial for navigation in this selected reference. Preserve these system-font choices unless Brian changes the style.

The reference shell is 660px tall in the conversation preview and fills the viewport in fullscreen. Its bottom bar always reserves 112px in two rows. The stage has 20px padding, a 34px header, a 100px title panel and a remaining media row, with 12px gaps. Exact mobile and short-screen adjustments are in the CSS. These dimensions are starting values for implementation, with stable bounds and readable controls taking priority during responsive fixes.

For the sample article, one headline spans four columns above four clippings. Build explicit per-slide arrangements for other compositions while retaining the same outer media bounds. Keep intrinsic image aspect ratios. Photos occupy the same media region. The header, title and controls maintain their positions when changing slides.

## Interaction and implementation boundaries

The demo Previous/Next buttons alternate between source slides 21 and 10. Implement real ordered navigation, chapter selection and deep links for the full site. The numbers 21 and 10 identify the sample source slides. The demo is not a completed 102-page presentation.

Read article opens a paper-colored overlay within the media region, with internal scrolling. Keep its toggle available in the control bar and provide a clear close state. The recording controls occupy the bottom bar's second row. Reserve the same space on pages without audio and display an appropriate unavailable state. Final recordings need verified transcripts and the production metadata specified in `docs/AUDIO_PRODUCTION.md`.

Fullscreen must keep the entire shell inside the viewport, including both control rows. Use the Fullscreen API with a visible fallback when unsupported. Handle exit with Escape and viewport resizing. Images must fit their cells without stretching or clipping. Navigation pauses active audio. The text overlay must not alter the shell height or media positions.

## Focused acceptance checks

Check the photo page and dense clipping page at desktop and mobile sizes, plus a short landscape viewport. Compare the control bar's position across page changes and text toggles. Confirm all images fit within the media bounds and all controls remain visible. In actual fullscreen, verify entry, page changes, article opening, resizing and Escape exit. Long transcripts scroll internally. Check keyboard navigation and preserve a readable no-JavaScript/continuous-reading route in the final site.

The concept was rebuilt successfully. Actual fullscreen behavior, mobile fit and keyboard interaction have not yet been browser-verified. Audio is an unconnected placement preview. User approval establishes the visual direction, while these functional checks remain implementation work.

All slides use the same content bounds and bottom control bar. The root uses a bounded height with a flexible stage row and a reserved 112px control row. Fullscreen changes the root height to 100dvh. The stage and its grid children allow shrinking with min-height: 0.

The header and title occupy reserved rows. Photos and article compositions occupy the same remaining row. Images use object-fit: contain and explicit cell dimensions. Article text overlays that row and scrolls within it. Opening text never changes the control bar position.

Audio playback occupies the second row of the bottom control bar. Reserve this space on every page. Stop playback when navigating. The concept currently shows an unconnected native audio control to demonstrate placement. Connect the reviewed recording in implementation.

Use presentation-layout.css as the editable layout source. build_visual_concept.py embeds it into the concept and exports presentation-concept.css. The preview contains two sample layouts. Fullscreen browser behavior and small-screen fit still require interaction verification.
