"""Render sample data locally. Never use real subscriber links in public previews."""
from pathlib import Path
from types import SimpleNamespace
import time, json
from jinja2 import Environment, FileSystemLoader, select_autoescape
ROOT=Path(__file__).resolve().parent.parent
env=Environment(loader=FileSystemLoader(ROOT/'templates'),autoescape=select_autoescape(['html']))
user=SimpleNamespace(username='alex.circle',status='active',used_traffic=32.4*1024**3,data_limit=100*1024**3,expire=int(time.time()+23*86400),data_limit_reset_strategy='no_reset',subscription_url='https://example.com/sub/demo-only',links=[f'vless://00000000-0000-4000-8000-000000000000@{host}.example.com:443?security=tls&type=ws#{name}' for host,name in [('de','Germany · Frankfurt'),('nl','Netherlands · Amsterdam'),('fi','Finland · Helsinki')]])
page=env.get_template('subscription/index.html').render(user=user)
page=page.replace('"username":', '"demo":true,"username":',1)
(ROOT/'preview').mkdir(exist_ok=True)
(ROOT/'preview/index.html').write_text(page)
print('Preview rendered: preview/index.html')
