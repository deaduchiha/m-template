"""Validate Marzban enum/string compatibility, states, and script-safe data."""
from pathlib import Path
from types import SimpleNamespace
from enum import Enum
import json,re,unittest
from jinja2 import Environment,FileSystemLoader,select_autoescape,StrictUndefined
ROOT=Path(__file__).resolve().parent.parent
class Status(str,Enum):
    active='active'
class TemplateTests(unittest.TestCase):
    def setUp(self):
        self.template=Environment(loader=FileSystemLoader(ROOT/'templates'),autoescape=select_autoescape(['html']),undefined=StrictUndefined).get_template('subscription/index.html')
    def render(self,**changes):
        values=dict(username='sample',status='active',used_traffic=0,data_limit=None,expire=None,subscription_url='/sub/sample',links=[])
        values.update(changes)
        page=self.template.render(user=SimpleNamespace(**values))
        payload=re.search(r'<script id="subscription-data" type="application/json">(.*?)</script>',page,re.S).group(1)
        return page,json.loads(payload)
    def test_all_states(self):
        for state in ['active','on_hold','expired','limited','disabled']:
            with self.subTest(state=state):
                _,data=self.render(status=state)
                self.assertEqual(data['status'],state)
    def test_enum_and_optional_fields(self):
        _,data=self.render(status=Status.active,data_limit_reset_strategy=Status.active)
        self.assertEqual(data['status'],'active')
        self.assertEqual(data['reset'],'active')
        self.assertIsNone(data['limit'])
    def test_script_and_html_injection(self):
        attack='</script><img src=x onerror=alert(1)>'
        page,data=self.render(username=attack,links=[attack])
        self.assertNotIn(attack,page)
        self.assertIn('&lt;/script&gt;',page)
        self.assertEqual(data['username'],attack)
    def test_no_external_runtime_assets(self):
        page,_=self.render()
        self.assertNotRegex(page,r'<script[^>]+src=')
        self.assertNotRegex(page,r'<link[^>]+rel="stylesheet"')
        self.assertNotIn('@@',page)
    def test_usage_values(self):
        _,data=self.render(used_traffic=1024**3,data_limit=100*1024**3)
        self.assertEqual(data['used'],1024**3)
        self.assertEqual(data['limit'],100*1024**3)
if __name__=='__main__':unittest.main()
