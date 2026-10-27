"""Build a self-contained Marzban template; requires only Python 3."""
from pathlib import Path
import base64
ROOT = Path(__file__).resolve().parent.parent
page = (ROOT / 'src/page.html').read_text()
for key, path in {'CSS':'src/styles.css','JS':'src/app.js','QR':'vendor/qrcode.min.js','LOGO':'assets/logo.svg','SYMBOL':'assets/symbol.svg'}.items():
    page = page.replace('@@'+key+'@@', (ROOT / path).read_text())
fonts = ''
for family, filename in [('Inter','inter-medium.ttf'),('Poppins','poppins-semibold.ttf')]:
    encoded = base64.b64encode((ROOT/'assets'/filename).read_bytes()).decode()
    fonts += f"@font-face{{font-family:'{family}';font-style:normal;font-weight:400 700;font-display:swap;src:url(data:font/ttf;base64,{encoded}) format('truetype')}}"
arad = base64.b64encode((ROOT/'assets/AradNL-VF.woff2').read_bytes()).decode()
fonts += f"@font-face{{font-family:'AradNL';font-style:normal;font-weight:100 900;font-display:swap;src:url(data:font/woff2;base64,{arad}) format('woff2')}}"
page = page.replace('<style>', '<style>'+fonts, 1)
page = page.replace('@@FAVICON@@', base64.b64encode((ROOT/'assets/favicon.svg').read_bytes()).decode())
target = ROOT / 'templates/subscription/index.html'
target.parent.mkdir(parents=True,exist_ok=True)
target.write_text(page)
print(f'Built {target} ({len(page.encode()):,} bytes)')
