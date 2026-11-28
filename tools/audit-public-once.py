import concurrent.futures, pathlib, urllib.request, urllib.error, ssl, time, xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlsplit
root = pathlib.Path('docs')
origin = 'https://lab.bixcore.de/'
def fetch(url,timeout=18):
    request = urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; BiXCore deployment audit)','Cache-Control':'no-cache','Accept-Encoding':'identity'})
    with urllib.request.urlopen(request,timeout=timeout) as r:
        return r.status,r.geturl(),r.read(),dict(r.headers)
ns={'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[x.text for x in ET.parse(root/'sitemap.xml').findall('.//sm:loc',ns)]
assert len(urls)==117
def check(url):
    path=urlsplit(url).path.lstrip('/')
    path=root/(path+'index.html' if not path or path.endswith('/') else path)
    for attempt in range(2):
        try:
            status,end,body,headers=fetch(url)
            assert status==200 and urlsplit(end).scheme=='https' and body==path.read_bytes(), 'content or status mismatch'
            return ('PASS',url)
        except Exception as e:
            if attempt==1:return ('FAIL',url,str(e))
            time.sleep(2)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results=list(pool.map(check,urls))
bad=[x for x in results if x[0]!='PASS']
print('PUBLIC_PAGES',len(results),'PASS',len(results)-len(bad),'FAIL',len(bad))
for b in bad: print(b)
assert not bad
for asset in ['sitemap.xml','robots.txt','styles.css','favicon.svg','assets/barox-gui-public.webp','assets/felix-portrait.webp']:
    status,end,data,h=fetch(origin+asset)
    assert status==200 and data==(root/asset).read_bytes(),asset
print('ASSETS 6/6 EXACT')
for url in [origin,origin+'de/',origin+'ru/',origin+'index.html',origin+'de/index.html',origin+'ru/index.html','http://lab.bixcore.de/']:
    try:
        s,end,b,h=fetch(url)
        keys=['Content-Type','Content-Encoding','Strict-Transport-Security','Content-Security-Policy','X-Content-Type-Options','X-Frame-Options','Referrer-Policy','Permissions-Policy','Cache-Control']
        print('HTTP',url,s,end,{k:next((v for a,v in h.items() if a.lower()==k.lower()),None) for k in keys})
    except Exception as e: print('HTTP_ERROR',url,str(e))
class Links(HTMLParser):
    def __init__(self): super().__init__();self.urls=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a' and a.get('href','').startswith('https://'):self.urls.add(a['href'])
links=Links()
for p in root.rglob('*.html'):links.feed(p.read_text('utf-8'))
for url in sorted(links.urls):
    try:
        s,end,b,h=fetch(url)
        print('EXTERNAL',s,url,end)
    except Exception as e:print('EXTERNAL_UNVERIFIED',url,str(e))
