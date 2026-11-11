# Deployment and fresh-clone guide

## What is being published

Repository: https://github.com/ShootPara/church-fires . Production: https://shootpara.github.io/church-fires/ . The default branch is `main`. The workflow is `.github/workflows/pages.yml`; it builds and validates `dist/`, then uploads only that directory to GitHub Pages. Python 3.12 is pinned in CI; actions are pinned to reviewed commit hashes. There are no third-party Python or Node build dependencies.

The site includes 101 presentation pages, named historical images, 27 final audio files (26 article readings and one opening reading), and three local MP4s. Only the two explicitly requested YouTube players need internet. They start at 1093 and 110 seconds and load after a visitor clicks Play. Both have a direct YouTube link in case privacy settings, embedding restrictions or offline conditions prevent playback. External videos are not part of the offline guarantee.

## A church member starting from scratch

1. Install Git and Python 3.12 or later. Open Terminal/PowerShell in a folder where you want the project.
2. Run `git clone https://github.com/ShootPara/church-fires.git`, then `cd church-fires`.
3. Open this folder in Codex. Ask it: "Read AGENTS.md, docs/DEPLOYMENT.md and docs/CODING_WORKER_HANDOFF.md. Check repository status, build and validate the existing website, then make only the change I describe. Do not redesign it or regenerate narration."
4. Run `python scripts/build_site.py --output dist` and `python scripts/validate_site.py dist`. No API key or Google account is needed. If `python` is not found, use `py -3` on Windows or `python3` on macOS/Linux.
5. Run `python -m http.server 8000 --directory dist`. Open http://localhost:8000 . Stop the server with Ctrl+C. This server is for preview only; production is static.
6. For a portable copy, share the entire `dist` folder, including `assets`, not just `index.html`. For another static host, upload the contents of `dist`. All site asset paths are relative, so GitHub project subpaths work.

Do not copy anything from another person's G: drive. Do not download Google Docs to perform a normal build. `sources/media`, `sources/video`, final `sources/audio` files, layout JSON and transcript files are committed. `ignore/` and `dist/` are disposable. Older discovery scripts that refer to Brian's Drive are research tools, not build requirements.

## Publish changes to this repository

You need GitHub write access to ShootPara/church-fires. A fresh clone does not grant it. Authenticate Git or GitHub CLI using your own account; do not copy Brian's `dev.vars` or credentials. A maintainer can instead review your pull request.

1. Read `git status`, create a branch for the work, edit the source files described in the handoff, and build/validate.
2. Review `git diff` and `git diff --cached`. Never stage credentials, generated `dist`, old audio intermediates or unrelated local files. Add the intended source/docs/assets explicitly.
3. Commit and push the branch, then open a pull request to `main`. After authorized review/merge, the push to `main` triggers deployment. Direct pushes are suitable only when the owner has authorized that workflow.
4. In GitHub, open **Actions → Deploy GitHub Pages** and watch the newest run. Both validation and deployment must succeed. The `github-pages` environment displays the deployed URL.
5. Verify the public URL in a fresh browser tab. Check slide 1, one article speaker and transcript, both slide 44 recordings, corrected slides 51/52, the retrospective on 73, local video on 75, the YouTube links on 19/20 and the repository link on 101. Enter/exit fullscreen and confirm the footer remains at the bottom. Check the network panel for missing local files.
6. Record the commit, Actions run URL, hosted checks and limits in `docs/DEPLOYMENT_STATUS.md`. Do not claim a deployment merely because the push succeeded.

CLI equivalents, when `gh` is installed and authenticated:

```sh
gh run list --workflow pages.yml --limit 5
gh run view RUN_ID
gh run view RUN_ID --log-failed
gh workflow run pages.yml --ref main
```

The final command redeploys the current `main` without changing content. On Brian's Windows machine GitHub CLI may be at `C:/Program Files/GitHub CLI/gh.exe` if it is missing from PATH; other machines should use their installed `gh`.

## Enable Pages on a fork or new owner repository

1. Fork/import the complete repository, including binary media. Enable Actions if GitHub asks.
2. In **Settings → Pages → Build and deployment**, select **GitHub Actions** as Source. Do not select `/docs` branch deployment; `/docs` contains maintainer documents, not the generated website.
3. Check **Settings → Environments → github-pages** for required reviewers or allowed branches. Approve deployment if your organization requires it.
4. Run the workflow manually or push an approved change to `main`.
5. Update README's production/repository URLs and the `project_link` in `scripts/build_site.py` to the new owner/repository. Update the hardcoded expected repository URL in `scripts/validate_site.py` as well.
6. Use the URL returned by Pages. A fork normally uses `https://OWNER.github.io/REPOSITORY/`. No custom domain is configured here.

## Rollback

Prefer `git revert BAD_COMMIT` on a reviewed branch, merge/push to `main`, and let the workflow deploy the reversal. If several commits must be rolled back, identify the last known good revision and review the revert range. Do not force-push or reset shared history. Verify the resulting public site and record the rollback. A successful old Actions run alone does not prove its media remains available; rebuilding from that commit is the reproducible recovery path.

## Troubleshooting

- **Missing local source file:** verify the clone completed and `git status`/`git ls-files` includes the required source. Restore the tracked file; do not replace it with a PDF screenshot. The build should never depend on `ignore` or G:.
- **Pages 404 / configure-pages error:** enable Pages with GitHub Actions as Source, check repository visibility/plan and environment permissions, then rerun the workflow. Do not change repository visibility without owner authorization.
- **403 / Actions deployment failure:** check write access and the workflow's `pages: write`, `id-token: write`, `contents: read` permissions. Inspect the actual failing run; do not rotate credentials blindly.
- **Old website:** wait for the latest successful Pages deployment, hard-refresh or use a new tab. Check the run's commit SHA. Do not regenerate assets as a cache workaround.
- **YouTube unavailable:** use the direct timestamped link. Local-file previews may lack the referrer YouTube expects. Do not claim an embedded video played when only its frame loaded.
- **Narration fails:** inspect the local MP3 URL and asset manifest, verify the final recording exists, and rebuild. Do not make a paid API request to fix a missing deployment file.

Reference: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages .
