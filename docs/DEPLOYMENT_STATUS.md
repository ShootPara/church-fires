# Deployment status - November 11, 2026

- Live site: https://shootpara.github.io/church-fires/
- Repository: https://github.com/ShootPara/church-fires
- Deployed content commit: `ae07f302d68740614a7f7f2ecc6da4b36d4af3f1`
- Successful GitHub Actions run: https://github.com/ShootPara/church-fires/actions/runs/43058904242
- Pages configuration: GitHub Actions workflow, public HTTPS, no custom domain.

## Verified

A new local Git clone containing only committed files built and passed `scripts/validate_site.py dist`. No credentials, Drive mount, ignored exports or third-party Python packages were used. The same build/validator passed on the GitHub Linux runner. Actions upload and Pages deployment completed successfully.

The public HTTPS site passed browser checks for the opening speaker, replacement article playback, silence on continuation slide 22, both slide 44 recordings and selected transcripts, corrected slides 51/52, slide 73 text, slide 75 MP4 playback at 1280x720, clean slide 6 label and enter/exit fullscreen icons. Local browser checks also verified the exact YouTube starts, no replacement JPG in those player areas, click-only iframe loading, iframe removal on slide changes and the last-page GitHub link inside slide bounds. YouTube network playback was not asserted; the direct timestamped links remain available if embedding fails.

The tracked source tree is about 259 MB; published files about 234 MB. Every individual committed file is below 100 MiB. Credentials and generated audio intermediates are excluded. All final media required for ordinary build/playback is committed, apart from the two explicitly external YouTube videos.

Limits: no physical-phone acceptance, complete human listening review of the article recordings, or guarantee of YouTube availability on visitor networks. Existing desktop and simulated phone viewport checks are documented in the prior results.

This status-only documentation commit does not change deployed site content and uses `[skip ci]` to avoid rebuilding the identical artifact. Future site changes should use the normal workflow.
