#!/usr/bin/env python3
"""Build a static localized preview/release from the canonical English pages.

No network, client-side translator, external dependencies or automatic English fallback
in a release. The translation source fingerprint forces review when English changes.
"""
import argparse
import hashlib
import html
import json
import re
import shutil
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit
from collections import Counter
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'docs'
LOCALES=ROOT/'locales'
LANGS=('de','en','ru')
ORIGIN='https://lab.bixcore.de/'
TOKEN=re.compile(r'<[^>]+>|[^<]+')
ATTR=re.compile(r'\b(aria-label|alt|content)="([^"]*)"')
LINK=re.compile(r'\b(href|src)="([^"]*)"')
NEUTRAL={'BiX','BiXCore','GitHub ↗','OPNsense','Windows Server','Proxmox VE',
         'Felix Bistriker','BiXCore · Felix Bistriker','OPNsense · Windows Server · Proxmox · PKI',
         'PKI · EAP-TLS · RadSec','BiX Barox Config Tool','BiXCore RADIUS Control','Seele der KI',
         'generic_mbuf_dtor','mb_free_ext','iflib_completed_tx_reclaim','/','·','.',','}
COMMON={
 'de':{'Skip to content':'Zum Inhalt springen','BiXCore Lab, home':'BiXCore Lab, Startseite',
 'ENGINEERING LAB':'TECHNIKLABOR','Main navigation':'Hauptnavigation','Projects':'Projekte',
 'Troubleshooting':'Fehleranalyse','Hardware':'Hardware','Plans':'Ausblick','About me':'Über mich',
 'Home':'Startseite','/ About me':'/ Über mich','Portrait of Felix Bistriker':'Porträt von Felix Bistriker',
 'ABOUT ME':'ÜBER MICH','See the projects →':'Projekte ansehen →','← Home':'← Startseite',
 '← All projects':'← Alle Projekte','BiXCore · Personal network & security lab':'BiXCore · Privates Netzwerk- und IT-Sicherheitslabor'},
 'ru':{'Skip to content':'Перейти к содержанию','BiXCore Lab, home':'BiXCore Lab, главная',
 'ENGINEERING LAB':'ИНЖЕНЕРНАЯ ЛАБОРАТОРИЯ','Main navigation':'Основная навигация','Projects':'Проекты',
 'Troubleshooting':'Диагностика','Hardware':'Оборудование','Plans':'Планы','About me':'Обо мне',
 'Home':'Главная','/ About me':'/ Обо мне','Portrait of Felix Bistriker':'Портрет Феликса Бистрикера',
 'ABOUT ME':'ОБО МНЕ','See the projects →':'Посмотреть проекты →','← Home':'← Главная',
 '← All projects':'← Все проекты','BiXCore · Personal network & security lab':'BiXCore · Личная лаборатория сетей и IT-безопасности'}
}

def blob_sha(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def localizable(tag):
    return 'name="description"' in tag or 'property="og:title"' in tag or 'property="og:description"' in tag

def units(source):
    result=[]
    for token in TOKEN.findall(source):
        if token.startswith('<'):
            for a in ATTR.finditer(token):
                if a[1]=='content' and not localizable(token):
                    continue
                value=html.unescape(a[2]).strip()
                if value:
                    result.append(value)
        else:
            value=html.unescape(token).strip()
            if value:
                result.append(value)
    return list(dict.fromkeys(result))

def url_for(lang, page):
    path='' if page=='index.html' else page
    return ORIGIN + ('' if lang=='en' else lang+'/') + path

def local_path(lang,page):
    return page if lang=='en' else lang+'/'+page

def route_for(current,ref):
    # English source links are relative to the original page.
    u=urlsplit(html.unescape(ref))
    if u.scheme or u.netloc or not u.path or ref.startswith('/'):
        return None,u
    import posixpath
    dest=posixpath.normpath(posixpath.join(posixpath.dirname(current),u.path))
    return dest,u

def render(source,page,lang,mapping,available,preview):
    import posixpath
    def translate(value):
        if lang=='en' or not value.strip():
            return value
        core=value.strip()
        if core not in mapping:
            raise ValueError(f'{lang}/{page}: untranslated text: {core[:100]}')
        return value[:len(value)-len(value.lstrip())]+mapping[core]+value[len(value.rstrip()):]
    def attributes(token):
        def replace_attr(a):
            if a[1]=='content' and not localizable(token):
                return a[0]
            return a[1]+'="'+html.escape(translate(html.unescape(a[2])),quote=True)+'"'
        token=ATTR.sub(replace_attr,token)
        def replace_link(a):
            dest,u=route_for(page,a[2])
            if dest is None:
                return a[0]
            if dest.endswith('.html'):
                target=lang if dest in available[lang] else 'en'
                if target!=lang and not preview:
                    raise ValueError(f'Missing {lang} target: {dest}')
                new='/' + local_path(target,dest)
            else:
                new='/'+dest
            if u.query:
                new+='?'+u.query
            if u.fragment:
                new+='#'+u.fragment
            return a[1]+'="'+html.escape(new,quote=True)+'"'
        return LINK.sub(replace_link,token)
    if lang!='en':
        pieces=[]
        for token in TOKEN.findall(source):
            if token.startswith('<'):
                pieces.append(attributes(token))
            else:
                pieces.append(html.escape(translate(html.unescape(token)),quote=False))
        source=''.join(pieces)
    else:
        source=''.join(attributes(t) if t.startswith('<') else t for t in TOKEN.findall(source))
    source=source.replace('<html lang="en">',f'<html lang="{lang}">',1)
    canonical=url_for(lang,page)
    source=re.sub(r'(<link rel="canonical" href=")[^"]*"',lambda m:m[1]+canonical+'"',source)
    source=re.sub(r'(<meta property="og:url" content=")[^"]*"',lambda m:m[1]+canonical+'"',source)
    alternates=[l for l in LANGS if page in available[l]]
    tags=''.join(f'<link rel="alternate" hreflang="{l}" href="{url_for(l,page)}">\n' for l in alternates)
    tags+=f'<link rel="alternate" hreflang="x-default" href="{url_for("en",page)}">\n'
    source=source.replace('</head>',tags+'</head>',1)
    labels={'de':'Sprachauswahl','en':'Language selection','ru':'Выбор языка'}
    names={'de':'Deutsch','en':'English','ru':'Русский'}
    links=''.join(f'<a href="/{local_path(l,page)}" hreflang="{l}" lang="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{names[l]}</a>' for l in alternates)
    switch=f'<nav class="language-switch" aria-label="{labels[lang]}">{links}</nav>'
    source=source.replace('</nav>','</nav>'+switch,1)
    if preview and lang!='en':
        note={'de':'Vorschau: Noch nicht übersetzte Artikel verlinken auf die englische Originalfassung.',
              'ru':'Предпросмотр: ссылки на ещё не переведённые статьи ведут к английскому оригиналу.'}[lang]
        source=source.replace('</header>',f'</header><p class="translation-preview">{note}</p>',1)
    return source

def load():
    pages={p.relative_to(SITE).as_posix():p for p in SITE.rglob('*.html') if p.relative_to(SITE).parts[0] not in ('de','ru')}
    available={'en':set(pages),'de':set(),'ru':set()}
    translations={}
    for lang in ('de','ru'):
        for p in sorted((LOCALES/lang).glob('*.json')):
            payload=json.loads(p.read_text('utf-8'))
            page=payload['page']
            if page not in pages or page in available[lang]:
                raise ValueError(f'{lang}: invalid or duplicate page {page}')
            raw=pages[page].read_bytes()
            if blob_sha(raw)!=payload['source_blob']:
                raise ValueError(f'{lang}/{page}: English source changed; review the translation')
            source=raw.decode('utf-8')
            expected=set(units(source))
            mapping={x:x for x in NEUTRAL}
            mapping.update(COMMON[lang])
            local=payload['translations']
            if set(local)-expected:
                raise ValueError(f'{lang}/{page}: unknown translation keys {set(local)-expected}')
            if not all(isinstance(v,str) and v.strip() for v in local.values()):
                raise ValueError(f'{lang}/{page}: empty translation')
            mapping.update(local)
            missing=expected-set(mapping)
            if missing:
                raise ValueError(f'{lang}/{page}: {len(missing)} missing text units: {sorted(missing)[:4]}')
            # Check technical digits on each translated unit, including dates, versions and counters.
            # Decimal/grouping punctuation is ignored; words may be used for spelled-out quantities.
            for src in expected:
                dst=mapping[src]
                if Counter(re.findall(r'\d+',src))!=Counter(re.findall(r'\d+',dst)):
                    raise ValueError(f'{lang}/{page}: numeric values changed in {src[:100]}')
            translations[(lang,page)]=mapping
            available[lang].add(page)
    return pages,available,translations

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true',help='validate the staged translations')
    parser.add_argument('--require-complete',action='store_true',help='reject missing pages in either language')
    parser.add_argument('--output',type=Path,help='write a standalone site to a NEW directory outside docs')
    parser.add_argument('--preview',action='store_true',help='explicitly allow incomplete preview with labeled English links')
    args=parser.parse_args()
    pages,available,maps=load()
    total=len(pages)
    for lang in LANGS:
        print(f'{lang}: {len(available[lang])}/{total} complete pages')
    complete=all(len(available[l])==total for l in LANGS)
    if (args.require_complete or (args.output and not args.preview)) and not complete:
        raise ValueError('Release blocked: all 39 pages must exist in both translations')
    rendered={}
    for lang in LANGS:
        for page in sorted(available[lang]):
            rendered[local_path(lang,page)]=render(pages[page].read_text('utf-8'),page,lang,maps.get((lang,page),{}),available,not complete)
    if args.output:
        dest=args.output.resolve()
        if dest.exists() or dest==SITE.resolve() or SITE.resolve() in dest.parents:
            raise ValueError('Output must be a new directory outside the canonical docs tree')
        dest.mkdir(parents=True)
        for f in SITE.iterdir():
            if f.name in ('pages','index.html','sitemap.xml','de','ru'):
                continue
            if f.is_dir():
                shutil.copytree(f,dest/f.name)
            else:
                shutil.copy2(f,dest/f.name)
        css=dest/'styles.css'
        with css.open('a',encoding='utf-8') as f:
            f.write('\n.language-switch{display:flex;flex-wrap:wrap;gap:.45rem;align-items:center;font-size:.8rem}.language-switch a{padding:.25rem .4rem;border:1px solid currentColor;border-radius:.35rem;text-decoration:none}.language-switch a[aria-current=page]{font-weight:700;background:#153a48;color:#e9f4fc}.translation-preview{max-width:80rem;margin:.5rem auto;padding:0 1rem;font-size:.85rem}\n@media(max-width:900px){.header-inner{flex-wrap:wrap}.language-switch{margin-left:auto}}\n')
        for path,content in rendered.items():
            f=dest/path
            f.parent.mkdir(parents=True,exist_ok=True)
            f.write_text(content,encoding='utf-8')
        ns='http://www.sitemaps.org/schemas/sitemap/0.9'
        xhtml='http://www.w3.org/1999/xhtml'
        ET.register_namespace('',ns)
        ET.register_namespace('xhtml',xhtml)
        tree=ET.Element('{'+ns+'}urlset')
        for lang in LANGS:
            for page in sorted(available[lang]):
                node=ET.SubElement(tree,'{'+ns+'}url')
                ET.SubElement(node,'{'+ns+'}loc').text=url_for(lang,page)
                for l in LANGS:
                    if page in available[l]:
                        ET.SubElement(node,'{'+xhtml+'}link',rel='alternate',hreflang=l,href=url_for(l,page))
        ET.ElementTree(tree).write(dest/'sitemap.xml',encoding='utf-8',xml_declaration=True)
        print(f'Generated {len(rendered)} static pages into {dest}')
    print('PASS: translation source fingerprints, text coverage, numeric consistency and rendering')
if __name__=='__main__':
    try:
        main()
    except (ValueError,KeyError,OSError) as exc:
        print(f'BLOCK: {exc}',file=sys.stderr)
        sys.exit(1)
