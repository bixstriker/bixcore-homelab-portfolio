#!/usr/bin/env python3
"""Check the standalone portfolio files, local links and Git author metadata."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs'
ALLOWED_SUFFIXES = {'.md', '.html', '.css', '.webp', '.py', '.yml', '.yaml', '.svg', '.xml', '.txt', '', '.gitignore'}
PATTERNS = {
  'private IPv4': re.compile(r'(?<![\d.])(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})(?![\d.])'),
  'IPv6 ULA': re.compile(r'\b(?:fc|fd)[0-9a-f]{2}:(?:[0-9a-f]*:){1,7}[0-9a-f]*\b', re.I),
  'MAC': re.compile(r'\b(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}\b', re.I),
  'personal email': re.compile(r'[\w.+-]+@(?!(?:users\.noreply\.github\.com)\b)[\w.-]+\.[A-Za-z]{2,}', re.I),
  'secrets': re.compile(r'\b(?:api[_-]?key|secret|password|token)\s*[:=]\s*["\']?[A-Za-z0-9_/+]{12,}', re.I),
}
class Page(HTMLParser):
  def __init__(self):
    super().__init__()
    self.links=[]
    self.ids=set()
    self.alt_errors=0
    self.title=False
    self.main=False
  def handle_starttag(self,tag,attrs):
    d=dict(attrs)
    if tag=='title': self.title=True
    if tag=='main': self.main=True
    if d.get('id'): self.ids.add(d['id'])
    if tag in ('a','link') and d.get('href'): self.links.append(d['href'])
    if tag=='img':
      if 'alt' not in d: self.alt_errors+=1
      if d.get('src'): self.links.append(d['src'])

def check():
  problems=[]
  for p in ROOT.rglob('*'):
    if not p.is_file() or '.git' in p.parts:
      continue
    if p.suffix.lower() not in ALLOWED_SUFFIXES and p.name not in ('.gitignore','.nojekyll'):
      problems.append(f'Unexpected file type: {p.relative_to(ROOT)}')
    if p.suffix in ('.html','.css','.md','.svg','.xml','.txt'):
      content=p.read_text('utf-8')
      if 'github.com/bixstriker/bixcore-homelab"' in content or 'github.com/bixstriker/bixcore-homelab/' in content:
        problems.append(f'Old private repository link: {p.relative_to(ROOT)}')
      for label,pat in PATTERNS.items():
        if pat.search(content): problems.append(f'{label}: {p.relative_to(ROOT)}')
  pages={}
  for p in SITE.rglob('*.html'):
    parser=Page()
    parser.feed(p.read_text('utf-8'))
    pages[p.resolve()]=parser
    if not parser.main or not parser.title or parser.alt_errors:
      problems.append(f'HTML structure: {p.relative_to(ROOT)}')
  for p,parsed in pages.items():
    for ref in parsed.links:
      u=urlsplit(ref)
      if u.scheme or u.netloc or ref.startswith('//'): continue
      dest=(p.parent/unquote(u.path)).resolve() if u.path else p
      if not dest.is_relative_to(SITE.resolve()) or not dest.is_file():
        problems.append(f'Broken local link: {p.relative_to(ROOT)} -> {ref}')
      elif u.fragment and dest in pages and unquote(u.fragment) not in pages[dest].ids:
        problems.append(f'Missing fragment: {p.relative_to(ROOT)} -> {ref}')

  # Guard against old snapshot figures and publication metadata drifting apart.
  versions = {
    'pages/windows-server-v2.6.html': 'Windows Server Master v2.10',
    'pages/proxmox-v1.7.html': 'Proxmox Master v1.12',
    'pages/network-v3.8.html': 'Network Master v3.26',
  }
  for relative, version in versions.items():
    page=(SITE/relative).read_text('utf-8')
    if f'<h1>{version}: Project Index</h1>' not in page or f'<title>{version}: Project Index' not in page:
      problems.append(f'Index heading/title mismatch: {relative}: {version}')
  required = {
    'pages/hardware.html': ['Barox', 'failover', 'VPN recovery'],
    'pages/lab.html': ['18 virtual machines', 'twelve platforms'],
    'pages/work-index.html': ['12 router/firewall platforms', 'Network Infrastructure v3.26', 'radsec-mtls.html'],
    'pages/proxmox-firewall-lab.html': ['All 40 Proxmox chapters'],
    'pages/working-notes.html': ['Proxmox Master v1.12 notes'],
    'pages/proxmox-v1.6.html': ['Historical snapshot', 'Proxmox Master v1.12'],
    'pages/radius-control.html': ['v1.0.2', 'v1.0.1', 'Omada', 'radsec-mtls.html'],
    'pages/radsec-mtls.html': ['TLS 1.3', 'Let\'s Encrypt', 'ACME', 'exported PEM', 'certificate verification enabled'],
    'pages/notes.html': ['radsec-omada-certificate', 'radsec-unifi-das'],
  }
  for relative, phrases in required.items():
    page=(SITE/relative).read_text('utf-8')
    for phrase in phrases:
      if phrase not in page: problems.append(f'Missing portfolio fact: {relative}: {phrase}')
  stale = {
    'pages/hardware.html': ['Testing complete service recovery and failover is ongoing.'],
    'pages/lab.html': ['There are now 13 documented virtual machines'],
    'pages/phylan1.html': ['user-confirmed end-to-end results'],
    'pages/proxmox-v1.6.html': ['Current edition:', 'Proxmox Master v1.11 project index'],
  }
  for relative, phrases in stale.items():
    page=(SITE/relative).read_text('utf-8')
    for phrase in phrases:
      if phrase in page: problems.append(f'Outdated public wording: {relative}: {phrase}')
  site_root='https://lab.bixcore.de/'
  expected_urls=set()
  for p,parsed in pages.items():
    relative=p.relative_to(SITE).as_posix()
    expected=site_root if relative=='index.html' else site_root+relative
    expected_urls.add(expected)
    page=p.read_text('utf-8')
    tags=[
      f'<link rel="canonical" href="{expected}">',
      f'<meta property="og:url" content="{expected}">',
      '<meta property="og:title" content="',
      '<meta property="og:description" content="',
      '<meta name="twitter:card" content="summary">',
      '<link rel="icon" type="image/svg+xml" href="',
    ]
    for tag in tags:
      if tag not in page: problems.append(f'Missing publication metadata: {relative}: {tag}')
  try:
    xml=ET.parse(SITE/'sitemap.xml')
    ns={'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls=[el.text for el in xml.findall('.//sm:loc',ns)]
    if len(urls)!=len(set(urls)) or set(urls)!=expected_urls:
      problems.append('Sitemap URLs differ from published HTML pages')
  except Exception as exc:
    problems.append(f'Sitemap invalid: {exc}')
  if 'Sitemap: https://lab.bixcore.de/sitemap.xml' not in (SITE/'robots.txt').read_text('utf-8'):
    problems.append('robots.txt does not list sitemap')
  try:
    svg=ET.parse(SITE/'favicon.svg')
    if svg.getroot().tag!='{http://www.w3.org/2000/svg}svg':
      problems.append('Favicon is not valid SVG')
    raw=(SITE/'favicon.svg').read_text('utf-8').lower()
    if any(token in raw for token in ['<script', 'onload=', 'onclick=', 'javascript:', '<foreignobject']):
      problems.append('Favicon contains executable content')
  except Exception as exc:
    problems.append(f'Favicon invalid: {exc}')
  for p in ROOT.rglob('*.md'):
    content=p.read_text('utf-8')
    for match in re.finditer(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', content):
      ref=match.group(1)
      u=urlsplit(ref)
      if u.scheme or u.netloc or ref.startswith(('#','/')): continue
      dest=(p.parent/unquote(u.path)).resolve()
      if not dest.is_relative_to(ROOT.resolve()) or not dest.exists():
        problems.append(f'Broken Markdown link: {p.relative_to(ROOT)} -> {ref}')

  if len(pages)!=38: problems.append(f'Expected 38 site pages; found {len(pages)}')
  if (SITE/'pages'/'notes.html').read_text('utf-8').count('<article class="mini-card" id=') != 39:
    problems.append('Expected 39 troubleshooting cases')
  try:
    commit_count=int(subprocess.check_output(['git','rev-list','--count','HEAD'],cwd=ROOT,text=True).strip())
    authors=subprocess.check_output(['git','log','--format=%ae%n%ce'],cwd=ROOT,text=True).splitlines()
    if commit_count < 1: problems.append('Git repository has no commits')
    if any(e != '212264745+bixstriker@users.noreply.github.com' for e in authors):
      problems.append('Unexpected Git author or committer email')
  except Exception as exc: problems.append(f'History check failed: {exc}')
  if problems:
    print('\n'.join('BLOCK: '+p for p in problems))
    return 1
  print(f'PASS: {len(pages)} HTML pages, 39 cases, valid local links and noreply-only Git history')
  return 0
if __name__=='__main__':
  sys.exit(check())
