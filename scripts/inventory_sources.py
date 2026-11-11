"""Read-only source manifest. Run from repository root; originals are never copied."""
import hashlib
import json
from pathlib import Path

root = Path('G:/My Drive/Church Fires Presentation')
records = []
for path in sorted(root.rglob('*')):
    if not path.is_file():
        continue
    pointer = path.suffix.lower() in {'.gdoc', '.gslides'}
    digest = None
    if not pointer:
        with path.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    records.append({
        'source_path': path.relative_to(root).as_posix(),
        'bytes': path.stat().st_size,
        'sha256': digest,
        'checksum_note': 'Native Google pointer; content captured separately' if pointer else None,
        'rights': 'unreviewed', 'attribution': None,
        'transformation': 'none; inventory only', 'output_path': None,
    })
out = Path('docs/source-manifest.json')
out.write_text(json.dumps({'source_root': str(root), 'files': records}, indent=2) + '\n', encoding='utf-8')
print(f'{len(records)} files; {sum(r["bytes"] for r in records):,} bytes; manifest: {out}')
