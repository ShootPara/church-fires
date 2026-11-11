## Latest replacement run - 2026-11-11

- New video: `ignore/YTDown.com_YouTube_Media_vpE_LWm_Y08_DRAFT-The-Four-Churches-First-Test_004_720p.mp4`. 13,686,864 bytes; H.264 1280x720 plus non-silent AAC; 60.116 seconds. Replaces the old 62.6 MB TEST file. Builder removes obsolete hashed output assets, preserving originals.
- Explicit labels for all 101 displayed slides: `sources/slide-titles.json`. HTML separator uses an entity to avoid encoding corruption. Do not derive menu titles from the first sentence or abbreviations such as FCC/MEC/Pres.
- Article scripts: `sources/narration/articles.json` and `article-01.txt` through `article-26.txt`. The first 25 come from the approved Gazette Article Contents export without historical rewriting. Script 26 was manually transcribed from the named slide 73 clipping, checked against the image, then appended to the live Google Doc at Brian's explicit request. Readback confirmed the prior text was unchanged. See `sources/narration/document-update.json`.
- Brian approved fixing the original audio mismatch: article 16 on slide 51; article 17 on slide 52. All 26 articles now have intended placements on 25 slides (two clips on slide 44). Slide 1's existing opening recording remains separate and unchanged.
- `python scripts/generate_articles.py --generate` produces paid OpenAI Cedar replacements with exact chunk scripts, request receipts and normalized MP3s under `sources/audio/articles/`. Completed chunks are checked and reused. Ambiguous pending requests stop instead of retrying. `--only article-NN` is available for an isolated unfinished article.
- `python scripts/select_article_audio.py` selects complete replacements and retains original archive paths. `python scripts/build_site.py` emits the portable local site. Article panels show individual matching scripts; slide 44 switches text with its recording selector.
- The narration key is in ignored `dev.vars`. Never print it or copy it to the site. Original MP3 archive is untouched. No runtime API calls.
- Historical transcriptions retain source wording, including the 1963 clipping's apparent typesetting errors. The retrospective identifies arson as a contemporary suspicion and quotes the subsequent denial; do not rewrite suspicion as established fact.

Current completed audio implementation and validation: `docs/AUDIO_IMPLEMENTATION_RESULTS.md`. Opening narration generated successfully; no credential blocker remains.

## Audio/video update — 2026-11-11 (latest user direction)

- Slide 75 uses `G:/My Drive/2024 Videos/The Four Churches First Test.mp4` (60.06 seconds, H.264/AAC, 640×360). Copied locally by the builder; no streaming dependency.
- Native audio assignments are recorded in `sources/audio-assignments.json`: 25 recordings on 24 original slides, including two on slide 44. Archive clip 17 has no native audio placement and is not added. Continuation pages do not automatically receive audio.
- Brian explicitly approves Gazette Article Contents as accurate scripts. Do not re-OCR or rewrite them. Original recordings remain intact and are used for these assignments.
- The ONE added assignment is slide 1: the complete `sources/extracted/excerpts.txt` (Article Text to be Read Verbatim), read by a paid AI voice. Large speaker below the title card and the footer speaker control the same recording.
- Previous/Next and enter/exit fullscreen use SVG icons with accessible labels. The footer speaker remains visible and disabled/grey on silent slides. One fixed bottom row remains required.
- `scripts/generate_opening.py --generate` uses the private ignored `dev.vars` key, writes per-chunk scripts and receipts under `sources/audio`, then joins and normalizes to `opening-reading.mp3`. It resumes completed chunks but refuses ambiguous interrupted attempts. Do not print or commit credentials. Paid requests have no automatic retries.
- Voice: OpenAI Cedar, measured documentary delivery. Documentation consulted: https://developers.openai.com/api/docs/guides/text-to-speech . Speech API model is available now but retires January 6, 2027; existing generated MP3s remain standalone. Review the generator before future regeneration after that date.
- Full Gazette source collection is available in the article panel on narrated slides; individual per-clip transcript segmentation remains unimplemented. No claim of clip-specific transcript matching is made.

# Paid narration production

Brian's latest audio direction: show audio controls only for slides with an assigned available recording. Slide 1 has no narration. Do not narrate a whole newspaper page merely because its image appears. Use original slide/clip associations and verified scripts. Never display Narration pending, missing-source warnings or implementation status on visitor-facing slides or controls. Record unresolved work in project documentation.

Brian explicitly requests paid generations using modern AI readers. No paid generation was performed in this planning pass. Old MP3s stay untouched at `G:\My Drive\Church Fires Presentation\Gazette Article Audios`.

## Script inputs

- `sources/extracted/gazette.txt`: complete available Gazette transcription source, with paragraph-indexed `.json` companion.
- `sources/extracted/excerpts.txt`: selected verbatim passages for the three main fires, not scripts for all 26 recordings.
- `sources/extracted/summaries.txt`: explanatory draft; NOT a substitute for an article's words.
- `docs/AUDIO_MAP.md` and `.json` counterpart `audio-mapping.json`: all 26 original filenames and candidate slide/newspaper matches. Candidate means not yet auditioned or text-verified. Clip 07 and 22 share similar headlines but refer to different presentation passages; do not deduplicate by title.

Create `content/audio/article-NN/transcript.txt`, `spoken.txt`, `corrections.json`, and `job.json` after comparing the scan, displayed crop and source text. The displayed transcript and spoken content must agree in meaning and coverage. Allowed recorded differences are spoken dates, amounts, abbreviations and pronunciation. Do not silently shorten articles. Include titles/dates consistently and mark them as editorial introductions if not part of the passage. Long readings can cover multiple source slides; model that explicitly rather than generating the whole article again for each page.

Pronunciation review list: Kalamazoo, Claus Slater, John Morren, Stoops, Triestram, VanHaaften, DeRight, Boudeman, Herfendahl, Batterson. Confirm names and pronunciations rather than inventing phonetics. Preserve the original written spelling in the transcript.

## Provider and cost

Use paid ElevenLabs TTS as the concrete prepared route. The API supports explicit voice/model selection and MP3 output. Check available models and the account's licensed voices at production time. Use the current high-quality narration model; compare a modern expressive reader (e.g. available Eleven v3 or successor) with the established Multilingual v2 baseline using the same 30–45 second historical passage. Choose restrained documentary delivery, natural pace and clear names. Model availability changes: do not assume a model exists because its name is in a plan.

The supplied Python generator accepts an explicit model and voice, rather than hardcoding a stale choice. Credentials go only in `ELEVENLABS_API_KEY`, never source, logs, browser code or job JSON. Existing user authorization covers paid narration intent; actual production still needs available credentials and an account/cost basis. Do not invent account access or silently subscribe to a plan.

Before a full batch, total reviewed script characters and apply the account's current model-specific rate/credits. Record the source/date of pricing, expected spend and a bounded allowance for two samples and targeted corrections in `docs/AUDIO_COSTS.md`. If budget/account constraints are missing, identify the specific missing information; finish script preparation meanwhile. Do not make repeated samples to chase subjective perfection.

Official API checked 2026-11-11: https://elevenlabs.io/docs/api-reference/text-to-speech/convert ; model/voice selection and response format are documented there. Quickstart: https://elevenlabs.io/docs/eleven-api/quickstart/ . MP3 44.1kHz/128kbps is supported. Deterministic script/hash does not mean deterministic generated audio.

## Job contract and commands

All paths below are repository-relative. A job has this shape (replace every placeholder):

```json
{
  "script": "content/audio/article-01/chunk-01.txt",
  "script_sha256": "SHA256_OF_EXACT_UTF8_FILE_BYTES",
  "review_status": "approved",
  "voice_id": "SELECTED_LICENSED_VOICE_ID",
  "model_id": "VERIFIED_AVAILABLE_MODEL_ID",
  "pronunciation_notes": "Document checked names and normalization here",
  "output": "ignore/audio-generated/article-01-chunk-01.mp3"
}
```

Optional `voice_settings` is passed verbatim; use only settings supported by the chosen model. Chunk at paragraph boundaries, at most 3000 characters per prepared request. Never split a name or sentence midstream. Keep ordered chunk files and an article-level manifest; the concatenated spoken text must equal the reviewed script. This conservative size is a local limit, not a claim about the provider's maximum. The generator makes one request per job, not an unlimited batch.

```powershell
python scripts/generate_narration.py content/audio/article-01/job.json
# Above is dry-run: hash/review checks and character count; no credentials needed.
python scripts/generate_narration.py content/audio/article-01/job.json --generate
python scripts/normalize_audio.py ignore/audio-generated/article-01-chunk-01.mp3 ignore/audio-normalized/article-01-chunk-01.mp3
```

For a multi-chunk article, join accepted chunks with FFmpeg concat after making a local list of ordered paths; normalize the joined article once. Check each seam. Retain the raw chunks and generation receipts. Normalize toward -16 LUFS integrated and -1.5 dBTP; inspect measured results rather than assuming the filter attained targets. The normalizer uses two passes and saves measurements. No automatic silence trimming: pauses can be intentional.

The paid generator refuses overwriting output and writes a pending receipt before network activity. On a timeout, inspect provider history before retrying: completion may have occurred and been charged. Never delete the pending marker merely to bypass this protection. Record recovery decisions. Generation returns a receipt with script hash, model/voice, UTC date, audio hash and request ID when provided. Add license/attribution and acceptance notes to the final asset manifest.

## Bounded review

Listen to each final clip once against its transcript: no omissions, repeated passages, invented words, clipped beginnings/endings or wrong names. Inspect FFprobe duration and normalization measurements. Spot-check seams after concatenation. One targeted regeneration for an observed defect; if still wrong, record it and decide an explicit correction instead of looping. Do not regenerate accepted clips because another part of the website changed. No runtime TTS and no autoplay.

Generation code is dry-run verified only; real provider credentials, paid requests and voice quality were not tested during planning.
