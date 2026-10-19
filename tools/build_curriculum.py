"""Build courses/pl-primary-math/curriculum.json and docs/curriculum/stage-*.md
from the JSON produced by parse_regulation.py (Dz.U. 2026 poz. 378).

usage: python3 -I tools/build_curriculum.py parsed.json
"""
import json, re, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
d = json.load(open(sys.argv[1], encoding='utf-8'))

FIN = re.compile(r'\s*[–-]\s*moduł ekonomiczno-\s*-?finansowy')
KUL = re.compile(r'\s*[–-]\s*moduł kultura')

def tidy(t):
    return re.sub(r'ekonomiczno- -finansowy', 'ekonomiczno-finansowy', t)

def flags(text):
    f = []
    if FIN.search(tidy(text)): f.append('finance')
    if KUL.search(tidy(text)): f.append('culture')
    return f

def split_experiences(raw):
    t = ' '.join(raw)
    t = re.sub(r'\s+', ' ', t)
    out = {}
    m46 = re.search(r'W przypadku klas IV–VI uczeń: (.*?) W przypadku klas VII i VIII uczeń: (.*)$', t)
    for key, blob in (('IV-VI', m46.group(1)), ('VII-VIII', m46.group(2))):
        items = re.split(r'\s(?=\d\)\s)', ' ' + blob)
        items = [re.sub(r'^\s*\d\)\s*', '', i).strip() for i in items if i.strip()]
        out[key] = items
    return out

exp = split_experiences(d['experiences_raw'])

def objective(stage, area_key, item):
    oid = f"{stage}.{area_key}.{item['no']}"
    text = tidy(item['text'])
    return {
        'id': oid, 'ref': f"{area_key}.{item['no']}", 'text': text, 'flags': flags(text),
        'parts': [{'id': f"{oid}.{s['k']}", 'key': s['k'], 'text': tidy(s['text'])} for s in item['sub']],
    }

def ew_objective(area_no, s):
    oid = f"I-III.{area_no}.{s['k']}"
    text = tidy(s['text'])
    return {'id': oid, 'ref': f"5.{area_no}{s['k']}", 'text': text, 'flags': flags(text), 'parts': []}

stages = []
stages.append({
    'id': 'I-III', 'title': 'Etap I (klasy I–III) – Edukacja matematyczna', 'grades': [1, 2, 3],
    'source': 'Dz.U. 2026 poz. 378, edukacja wczesnoszkolna, pkt 5 „Edukacja matematyczna”',
    'goals': [], 'experiences': [],
    'areas': [{'id': f"I-III.{a['no']}", 'no': a['no'], 'name': a['name'],
               'objectives': [ew_objective(a['no'], s) for s in a['items']]} for a in d['ew']]})
for key, title, grades, areas, goals in (
        ('IV-VI', 'Etap II (klasy IV–VI) – Matematyka', [4, 5, 6], d['iv_vi'], d['goals_iv_vi']),
        ('VII-VIII', 'Etap II (klasy VII–VIII) – Matematyka', [7, 8], d['vii_viii'], d['goals_vii_viii'])):
    goals = [re.sub(r'\s*Treści nauczania.*$', '', g) for g in goals]
    stages.append({
        'id': key, 'title': title, 'grades': grades,
        'source': 'Dz.U. 2026 poz. 378, Matematyka, klasy ' + ('IV–VI' if key == 'IV-VI' else 'VII i VIII'),
        'goals': goals, 'experiences': exp[key],
        'areas': [{'id': f"{key}.{a['no']}", 'no': a['no'], 'name': a['name'],
                   'objectives': [objective(key, a['no'], it) for it in a['items']]} for a in areas]})

cur = {'formatVersion': '1.0', 'kind': 'curriculum', 'curriculumId': 'pl-podstawa-matematyka-2026',
       'legalBasis': 'Rozporządzenie Ministra Edukacji z dnia 11 marca 2026 r. (Dz.U. 2026 poz. 378)',
       'note': 'Texts are verbatim from the regulation (whitespace/hyphenation normalised). The regulation defines stages, not school years.',
       'stages': stages}
(root / 'courses/pl-primary-math/curriculum.json').write_text(json.dumps(cur, ensure_ascii=False, indent=1), encoding='utf-8')

# ---- markdown
out = root / 'docs/curriculum'
def md_stage(st):
    L = [f"# {st['title']}", '',
         f"**Source:** {cur['legalBasis']} — {st['source']}.  ",
         f"**Grades covered:** {', '.join(map(str, st['grades']))} — the regulation does **not** assign requirements to individual years inside the stage.  ",
         "**Generated** by `tools/build_curriculum.py` from the regulation text; do not edit by hand.", '',
         "IDs below are the objective IDs used in `courses/pl-primary-math/curriculum.json` and referenced by skills in course packs. Tags: 💰 = moduł ekonomiczno-finansowy, 🎨 = moduł kultura.", '']
    if st['goals']:
        L += ['## Cele kształcenia – wymagania ogólne', '']
        L += [f"{i}. {g}" for i, g in enumerate(st['goals'], 1)] + ['']
    L += ['## Treści nauczania – wymagania szczegółowe', '']
    for a in st['areas']:
        L += [f"### {a['no']}. {a['name'][0].upper() + a['name'][1:]}", '']
        for o in a['objectives']:
            tag = ' 💰' if 'finance' in o['flags'] else ''
            tag += ' 🎨' if 'culture' in o['flags'] else ''
            L.append(f"- **`{o['id']}`**{tag} {o['text']}")
            for p in o['parts']:
                L.append(f"    - `{p['id']}` {p['text']}")
        L.append('')
    if st['experiences']:
        L += ['## Doświadczenia edukacyjne', '']
        L += [f"{i}. {e}" for i, e in enumerate(st['experiences'], 1)] + ['']
    return '\n'.join(L)

names = {'I-III': 'stage-I-III.md', 'IV-VI': 'stage-IV-VI.md', 'VII-VIII': 'stage-VII-VIII.md'}
for st in stages:
    (out / names[st['id']]).write_text(md_stage(st), encoding='utf-8')
for st in stages:
    print(st['id'], {a['name']: len(a['objectives']) for a in st['areas']}, len(st['goals']), len(st['experiences']))
