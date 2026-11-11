# Agent instructions

## Mission

Turn Brian Ream's Google Slides presentation, **1925–1926 Kalamazoo Church Fires**, into a self-contained historical website that delivers the same information in a clearer, more accessible form.

The finished project must be cloneable and usable without Google Slides, Google Drive, Blender, a database, an API, a hosted backend, or any proprietary server. All content needed at runtime—including text, images, 3D assets, video, captions, and narration—must live in the repository or in a documented release artifact generated from repository sources.

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

The current presentation has 103 slides and follows this broad arc:

1. Scope and summary of the 1925–1926 fire series.
2. Kalamazoo and the three major church buildings before the fires.
3. The First Congregational fire of December 29, 1925.
4. The First Methodist Episcopal fire of March 14, 1926, including the deaths of firefighters Claus Slater and John Morren.
5. The First Presbyterian fire of July 7, 1926.
6. Investigations, known/claimed causes, and contemporary arson suspicion.
7. Community response, memorials, family relief, and rebuilding.
8. The replacement churches and First Congregational Church visualizer/model sequence.
9. Historical image-source appendix.

The website should not mechanically reproduce 103 slide-sized screens. Preserve the information and evidence while reorganizing it into readable chapters, a timeline, article/source views, transcripts, and optional media experiences.

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

