"""Package the deployment file, source, and licenses using an explicit allowlist.

Run scripts/build.py first. Outputs are placed in ignored dist/.
"""
from pathlib import Path
import hashlib
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True)
shutil.copyfile(ROOT / 'templates/subscription/index.html', DIST / 'index.html')
with zipfile.ZipFile(DIST / 'circleweb-marzban.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for folder in ['src', 'assets', 'vendor', 'templates', 'scripts', 'tests', 'docs']:
        for path in sorted((ROOT / folder).rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts:
                archive.write(path, path.relative_to(ROOT))
    for filename in ['README.md', 'requirements-dev.txt', '.gitignore', '.gitattributes', '.editorconfig']:
        archive.write(ROOT / filename, filename)
checksums = []
for filename in ['index.html', 'circleweb-marzban.zip']:
    digest = hashlib.sha256((DIST / filename).read_bytes()).hexdigest()
    checksums.append(f'{digest}  {filename}\n')
(DIST / 'SHA256SUMS').write_text(''.join(checksums))
print(f'Packaged deployment file, source ZIP, and SHA256SUMS in {DIST}')
