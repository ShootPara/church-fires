# Agent start here

This is the accepted 101-slide Kalamazoo Church Fires website. Brian approved the presentation and requested publication. Do not restart design or revive rejected prototypes.

1. Read `docs/DEPLOYMENT.md` for fresh-clone setup, build, verification, publishing and rollback.
2. Read `docs/CODING_WORKER_HANDOFF.md` before changing content or code.
3. Inspect Git status and preserve unrelated user work. Use the current checkout unless a new worktree is requested.

## Current contracts

- Build with Python 3.12+ standard library: `python scripts/build_site.py --output dist`. No npm install, API key, Drive access or paid generation is needed. Validate with `python scripts/validate_site.py dist`.
- GitHub Pages deploys `dist/` through `.github/workflows/pages.yml` on pushes to `main`. Publication must be explicitly authorized; Brian authorized this initial deployment.
- Runtime sources are committed: named images in `sources/media/`, MP4s in `sources/video/`, final narration in `sources/audio/`. `ignore/` and `dist/` are disposable, not required sources.
- Use Brian's individual named images. Never replace the slides with PDF screenshots, extracted PDF images, page SVGs or a hidden screenshot foreground. The PDF is reference only.
- Preserve explicit compositions, centered cream cards, brick/cream colors, slide order, bounded 16:9 canvas and a fixed single bottom control row. Previous/Next are adjacent icons. Fullscreen uses enter/exit icons. Speaker remains grey/disabled when a slide has no audio.
- Use `sources/slide-titles.json` for concise menu labels. Do not derive titles from the first text sentence or FCC/MEC/Pres abbreviations.
- Narration follows `sources/audio-assignments.json`. Slide 1 is the explicitly approved extra opening reading. Brian also approved correcting article 16 to slide 51 and article 17 to slide 52. Slide 44 has two recordings. Do not add narration to continuation slides automatically.
- All 26 article recordings are paid Cedar replacements. Scripts 1-25 are approved Gazette text; script 26 was transcribed from the named 1963 clipping and appended to the Google Doc at Brian's request. Preserve historical wording and distinguish contemporary arson suspicion from established fact.
- YouTube slides 19/20 are an explicit user-approved external-media exception. They load only after Play, start at 1093/110 seconds, and provide direct timestamped links. Do not download these videos or silently substitute thumbnails. The rest of the presentation works offline; these two videos require internet and YouTube availability.
- Slide 101 links to the GitHub project for cloning. Do not add Brian's visible name, pending narration labels or implementation status to the slides.
- Never read credentials into logs or commit `dev.vars`/`.env`. Do not regenerate paid audio for a build/deploy. Paid generation requires a request to generate audio; no automatic retries after an ambiguous charged request.
- Do not edit native Google sources unless explicitly requested. The latest authorized change appended the missing retrospective; preserve the rest.
- Run bounded checks appropriate to changes. Report what was actually tested; successful audio decoding is not a complete listening review. No physical-phone acceptance has been claimed.

Older plans, prototypes and extraction instructions are historical. `docs/HISTORICAL_AGENT_NOTES.md` preserves earlier instructions for context. Current rules above and the two entry-point docs take precedence.
