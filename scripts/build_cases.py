"""Render approved real cases into the homepage. Run: python3 scripts/build_cases.py.
Each case requires: region, work_type, problem, process, result, photos
([{src, alt, width, height}]), publication_approved=true, facts_verified=true.
Use broad regions, no customer identifiers or unverified performance claims.
"""
import json,re
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cases=json.loads((ROOT/'data/projects.json').read_text())['cases']
cards=[]
for item in cases:
 assert item.get('publication_approved') is True and item.get('facts_verified') is True
 for key in ['region','work_type','problem','process','result','photos']:assert item.get(key),key
 photos=[]
 for photo in item['photos']:
  assert photo['src'].startswith('/102-/assets/') and (ROOT/photo['src'].removeprefix('/102-/')).is_file()
  assert photo['width']>0 and photo['height']>0 and photo['alt']
  photos.append(f'<img src="{escape(photo["src"],quote=True)}" alt="{escape(photo["alt"],quote=True)}" width="{photo["width"]}" height="{photo["height"]}" loading="lazy">')
 details=''.join(f'<dt>{label}</dt><dd>{escape(item[key])}</dd>' for key,label in [('region','지역'),('work_type','공사 유형'),('problem','문제'),('process','과정'),('result','결과')])
 cards.append('<article class="case-card"><h3>'+escape(item['work_type'])+'</h3>'+''.join(photos)+'<dl>'+details+'</dl></article>')
content='<div class="case-grid">'+''.join(cards)+'</div>' if cards else '<div class="case-preparing"><h3>시공 사례를 정리하고 있습니다.</h3><p>공개가 승인된 실제 사진과 확인된 시공 내용을 차례로 소개하겠습니다.</p><a class="button" href="/102-/contact/">우리 공간 상담하기 ↗</a></div>'
p=ROOT/'index.html';html=p.read_text();html,count=re.subn(r'<!-- CASES:START -->.*?<!-- CASES:END -->','<!-- CASES:START -->'+content+'<!-- CASES:END -->',html,flags=re.S);assert count==1;p.write_text(html)
