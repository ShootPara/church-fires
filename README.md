# Kalamazoo Church Fires, 1925-1926

A static, slide-style historical presentation with real newspaper clippings, article transcripts, local AI narration and church-model videos.

- Website: https://shootpara.github.io/church-fires/
- Repository: https://github.com/ShootPara/church-fires
- **New maintainer or coding agent:** start at [AGENTS.md](AGENTS.md), then [deployment instructions](docs/DEPLOYMENT.md) and the [coding-worker handoff](docs/CODING_WORKER_HANDOFF.md).

## Build from a fresh clone

Install Git and Python 3.12 or newer, then:

```sh
git clone https://github.com/ShootPara/church-fires.git
cd church-fires
python scripts/build_site.py --output dist
python scripts/validate_site.py dist
python -m http.server 8000 --directory dist
```

Open http://localhost:8000 . On systems using `python3`, substitute that command. Windows can use `py -3` if `python` is unavailable. No dependencies need installing. You can also open `dist/index.html` directly; YouTube embeds work more reliably over HTTP/HTTPS.

All required images, final narration and local videos are included. No Google Drive connection, API key, database, npm or runtime server is required. Slides 19 and 20 explicitly use YouTube and require internet; the rest is local. The clone includes substantial historical media; allow time for the initial download.

Pushing approved changes to `main` runs the GitHub Pages build and deployment. The website uses only `dist/`; credentials, research files and generation scripts are not deployed. See the deployment guide before publishing a fork or changing the production site.
