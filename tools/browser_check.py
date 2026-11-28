#!/usr/bin/env python3
"""Browser regressions on the complete, locally served static site."""
import argparse, functools, http.server, re, threading
from collections import defaultdict
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as BrowserTimeout
parser=argparse.ArgumentParser()
parser.add_argument('site',type=Path)
args=parser.parse_args()
root=args.site.resolve()
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
origin=f'http://127.0.0.1:{server.server_port}'
widths=(320,390,550,651,768,1024,1101,1280,1440,1920)
errors=[]; count=0; table_count=0; anchor_count=0
titles=defaultdict(set); descriptions=defaultdict(set)
joined=re.compile(r'(?<=[^\W_])(?:</(?:a|em|strong|code|b|i)>|<(?:a|em|strong|code|b|i)\b[^>]*>)(?=[^\W_])')
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch()
        page=browser.new_page()
        page.on('pageerror', lambda error: errors.append(f'{page.url}: JavaScript error: {error}'))
        page.on('console', lambda message: errors.append(f'{page.url}: {message.text}') if message.type=='error' and 'Content Security Policy' in message.text else None)
        for f in sorted(root.rglob('*.html')):
            path=f.relative_to(root).as_posix()
            lang=path.split('/')[0] if path.startswith(('de/','ru/')) else 'en'
            url=origin+'/'+(path.removesuffix('index.html') if f.name=='index.html' else path)
            if lang!='en':
                for block in re.findall(r'<(?:p|li)\b[^>]*>.*?</(?:p|li)>',f.read_text('utf-8'),re.S):
                    if joined.search(block): errors.append(f'{path}: missing inline word separator')
            for width in widths:
                page.set_viewport_size({'width':width,'height':900})
                response=page.goto(url,wait_until='load')
                count+=1
                if not response or response.status!=200: errors.append(f'{path}: HTTP failure')
                # A lazy image below the fold is not broken. Force loading in
                # the test only, then still check that the real resource decoded.
                page.evaluate("""async () => {
                  const images=[...document.images];
                  images.forEach(img=>img.loading='eager');
                  await Promise.allSettled(images.map(img=>img.decode()));
                  return images.length;
                }""")
                result=page.evaluate("""() => {
                  const doc=document.documentElement;
                  const sw=document.querySelector('.language-switch');
                  const nav=document.querySelector('.top-nav');
                  const box=e=>e.getBoundingClientRect();
                  const overlap=(a,b)=>a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top;
                  const svg=[];
                  for (const graphic of document.querySelectorAll('svg.graphic-svg')) {
                    const bounds=graphic.viewBox.baseVal;
                    for(const t of graphic.querySelectorAll('text')) {
                      const b=t.getBBox();
                      if(b.x<bounds.x-1||b.x+b.width>bounds.x+bounds.width+1) svg.push(t.textContent);
                      const x=Number(t.getAttribute('x')), y=Number(t.getAttribute('y'));
                      const rects=[...graphic.querySelectorAll('rect')].filter(r=>{
                        const q=r.getBBox();return x>=q.x&&x<=q.x+q.width&&y>=q.y&&y<=q.y+q.height;
                      }).sort((a,b)=>a.getBBox().width-b.getBBox().width);
                      if(rects.length){const q=rects[0].getBBox();if(b.x<q.x+1||b.x+b.width>q.x+q.width-1) svg.push(t.textContent);}
                    }
                  }
                  return {overflow:doc.scrollWidth>innerWidth+1, overlap:!!(sw&&nav&&overlap(box(sw),box(nav))),
                    images:[...document.images].filter(x=>!x.complete||!x.naturalWidth).length,svg,
                    tables:[...document.querySelectorAll('.table-wrap')].every(x=>x.tabIndex===0&&x.getAttribute('aria-label')&&x.getAttribute('role')==='region'),
                    headers:[...document.querySelectorAll('thead th')].every(x=>x.getAttribute('scope')==='col')};
                }""")
                if result['overflow'] or result['overlap'] or result['images'] or result['svg'] or not result['tables'] or not result['headers']:
                    errors.append(f'{path}@{width}: {result}')
            table_count+=page.locator('.table-wrap').count()
            if page.locator('meta[http-equiv="Content-Security-Policy"]').count()!=1:
                errors.append(f'{path}: missing or duplicate CSP')
            title=page.title()
            meta=page.locator('meta[name=description]')
            if meta.count()!=1:
                errors.append(f'{path}: expected exactly one meta description')
                continue
            desc=meta.get_attribute('content')
            if title in titles[lang]: errors.append(f'{path}: duplicate title {title}')
            if desc in descriptions[lang]: errors.append(f'{path}: duplicate description {desc}')
            titles[lang].add(title); descriptions[lang].add(desc)
            anchor=page.locator('main [id]').first
            if anchor.count():
                ident=anchor.get_attribute('id')
                page.evaluate('(id)=>{location.hash=encodeURIComponent(id)}',ident)
                try:
                    page.wait_for_function("() => Array.from(document.querySelectorAll('.language-switch a')).every(a=>a.hash===location.hash)",timeout=3000)
                    anchor_count+=1
                except BrowserTimeout:
                    errors.append(f'{path}: language switch did not preserve section #{ident}')
        browser.close()
finally:
    server.shutdown()
print(f'Browser checks: {count}; table regions: {table_count}; section-preserving language checks: {anchor_count}; errors: {len(errors)}')
if errors:
    print('\n'.join(errors[:100]))
    raise SystemExit(1)
