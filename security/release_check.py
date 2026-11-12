#!/usr/bin/env python3
"""Check the standalone portfolio files, local links and Git author metadata."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs'
ALLOWED_SUFFIXES = {'.md', '.html', '.css', '.webp', '.py', '.yml', '.yaml', '', '.gitignore'}
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
    if p.suffix in ('.html','.css','.md'):
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
  if len(pages)!=36: problems.append(f'Expected 36 site pages; found {len(pages)}')
  if (SITE/'pages'/'notes.html').read_text('utf-8').count('<article class="mini-card" id=') != 35:
    problems.append('Expected 35 troubleshooting cases')
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
  print(f'PASS: {len(pages)} HTML pages, 35 cases, valid local links and noreply-only Git history')
  return 0
if __name__=='__main__':
  sys.exit(check())
