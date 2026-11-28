import concurrent.futures
import pathlib
import time
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit
root = pathlib.Path('docs')
origin = 'https://lab.bixcore.de/'
def get(url):
    request = urllib.request.Request(url, headers={'User-Agent':'BiXCore public deployment verification','Cache-Control':'no-cache','Accept-Encoding':'identity'})
    with urllib.request.urlopen(request, timeout=20) as r:
        if r.status != 200 or urlsplit(r.geturl()).scheme != 'https':
            raise RuntimeError(f'{url}: unexpected HTTP status or scheme')
        return r.read()
def check(url):
    relative = urlsplit(url).path.lstrip('/')
    path = root / (relative + 'index.html' if not relative or relative.endswith('/') else relative)
    expected = path.read_bytes()
    for attempt in range(3):
        try:
            actual = get(url)
            if actual != expected:
                raise RuntimeError('Published bytes differ from checked release')
            return None
        except Exception as e:
            if attempt == 2:
                return f'{url}: {e}'
            time.sleep(3)
ns = {'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'}
expected_urls = [x.text for x in ET.parse(root/'sitemap.xml').findall('.//sm:loc', ns)]
live = get(origin+'sitemap.xml')
actual_urls = [x.text for x in ET.fromstring(live).findall('.//sm:loc', ns)]
assert len(expected_urls)==117 and set(actual_urls)==set(expected_urls) and len(actual_urls)==117, 'Live sitemap mismatch'
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    failures = [r for r in pool.map(check, expected_urls) if r]
for f in failures:
    print('FAIL:', f)
assert not failures, f'{len(failures)} public pages failed'
for asset in ['styles.css','favicon.svg','assets/barox-gui-public.webp','assets/felix-portrait.webp','robots.txt']:
    assert get(origin+asset)==(root/asset).read_bytes(), f'Asset mismatch: {asset}'
print('PASS: all 117 public HTTPS pages and 5 shared assets match the generated release; sitemap has 117 URLs.')
