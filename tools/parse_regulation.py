"""Extract the maths requirements from the text of Dz.U. 2026 poz. 378.

  curl -L -o du378.pdf https://dziennikustaw.gov.pl/D2026000037801.pdf
  pdftotext -layout du378.pdf du378.txt
  python3 -I tools/parse_regulation.py du378.txt parsed.json
  python3 -I tools/build_curriculum.py parsed.json

NOTE: the line ranges near the bottom (`L[2250:2361]`, `L[9465:9483]` …) are specific to this
edition of the PDF text; re-check them if the regulation is amended/re-published.
"""
import re, json, sys
src, out = sys.argv[1], sys.argv[2]
L = open(src, encoding='utf-8').read().split('\n')

def clean(lines):
    res = []
    for l in lines:
        l = l.replace('﻿', '').replace('\x0c', '')
        if 'Dziennik Ustaw' in l or 'Poz. 378' in l: continue
        if re.fullmatch(r'[\s\–\-—0-9]*', l): continue
        res.append(re.sub(r'\s+', ' ', l).strip())
    return res

def join(parts):
    t = ' '.join(parts)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def parse_math(lines):
    """areas 'N. Name. Uczeń:' ; items 'N) ...' ; sub 'a) ...'"""
    areas = []; cur = None; item = None; sub = None
    for l in lines:
        m = re.match(r'^(\d+)\.\s+(.+?)\.\s+Uczeń:$', l)
        if m:
            cur = {'no': int(m.group(1)), 'name': m.group(2), 'items': []}; areas.append(cur); item = sub = None; continue
        if cur is None: continue
        m = re.match(r'^(\d+)\)\s*(.*)$', l)
        if m and (item is None or int(m.group(1)) == item['no'] + 1):
            item = {'no': int(m.group(1)), 'parts': [m.group(2)], 'sub': []}; cur['items'].append(item); sub = None; continue
        m = re.match(r'^([a-z])\)\s*(.*)$', l)
        if m and item is not None and (sub is None and m.group(1) == 'a' or sub is not None and ord(m.group(1)) == ord(sub['k']) + 1):
            sub = {'k': m.group(1), 'parts': [m.group(2)]}; item['sub'].append(sub); continue
        if sub is not None: sub['parts'].append(l)
        elif item is not None: item['parts'].append(l)
    for a in areas:
        for it in a['items']:
            it['text'] = join(it.pop('parts'))
            it['sub'] = [{'k': s['k'], 'text': join(s['parts'])} for s in it['sub']]
    return areas

def parse_ew(lines):
    """'N) name – uczeń:' then 'a) ...'"""
    areas = []; cur = None; sub = None
    for l in lines:
        m = re.match(r'^(\d+)\)\s+(.+?)\s+–\s+uczeń:$', l)
        if m:
            cur = {'no': int(m.group(1)), 'name': m.group(2), 'items': []}; areas.append(cur); sub = None; continue
        if cur is None: continue
        m = re.match(r'^([a-z])\)\s*(.*)$', l)
        if m and (sub is None and m.group(1) == 'a' or sub is not None and ord(m.group(1)) == ord(sub['k']) + 1):
            sub = {'k': m.group(1), 'parts': [m.group(2)]}; cur['items'].append(sub); continue
        if sub is not None: sub['parts'].append(l)
    for a in areas:
        for s in a['items']:
            s['text'] = join(s.pop('parts'))
    return areas

def goals(lines):
    g = []; 
    for l in lines:
        m = re.match(r'^(\d+)\.\s+(.*)$', l)
        if m and int(m.group(1)) == len(g) + 1: g.append([m.group(2)])
        elif g: g[-1].append(l)
    return [join(x) for x in g]

# 1-based line numbers found with grep
ew = clean(L[2250:2361])            # 5. Edukacja matematyczna .. before 6.
g46 = clean(L[9465:9483]);  g78 = clean(L[9484:9510])
iv = clean(L[9522:9744]);   vii = clean(L[9745:9897]); exp = clean(L[9897:9945])
data = {'ew': parse_ew(ew), 'iv_vi': parse_math(iv), 'vii_viii': parse_math(vii),
        'goals_iv_vi': goals(g46), 'goals_vii_viii': goals(g78), 'experiences_raw': exp}
json.dump(data, open(out, 'w'), ensure_ascii=False, indent=1)
for k in ('ew', 'iv_vi', 'vii_viii'):
    print(k, [(a['no'], a['name'], len(a['items'])) for a in data[k]])
print(len(data['goals_iv_vi']), len(data['goals_vii_viii']))
