#!/usr/bin/env python3
"""Generate a Cognio course by prompting Claude, with deterministic acceptance gates between the stages.

  python3 -I tools/coursegen.py new <course> --language pl --title "…" --prefix xx
  python3 -I tools/coursegen.py source   <course> <url-or-file>... [--note "legal basis"]   G1  curriculum.json
  python3 -I tools/coursegen.py plan     <course>                                           G2  plan.json (skills, units)
  python3 -I tools/coursegen.py author   <course> [--batch-size 8] [--rounds 3]             G3  content-src modules
  python3 -I tools/coursegen.py validate <course> [--sample 3] [--repair-rounds 2]          G4+G5 build, lint, blind solve, pack
  python3 -I tools/coursegen.py all      <course> <source>...                               everything above
  python3 -I tools/coursegen.py status   <course>

Gates only (no model, free): check-source | check-plan | check-batch <module> | build | gates
Global flags: --dry-run (write the prompts to course-work/<course>/logs and stop), --model <name>.
Environment: COGNIO_CLAUDE (command, default `claude`), COGNIO_CLAUDE_ARGS (extra flags for every call).

Requirements and workflow: docs/07-course-generation.md; the gate list shown to the model: tools/coursegen/gates.md.
Run from the project root. Needs: the `claude` CLI, python `jsonschema` (like cognio.py), `pdftotext` for PDF sources.
"""
import argparse, datetime, hashlib, html.parser, json, os, pathlib, random, re, shlex, shutil, subprocess, sys, unicodedata
import urllib.request
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / 'tools'
CG = TOOLS / 'coursegen'
WORK = ROOT / 'course-work'
STAGES = ('I-III', 'IV-VI', 'VII-VIII')
SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
OBJ_ID = re.compile(r'^(I-III|IV-VI|VII-VIII)\.\d+\.(\d+|[a-z])(\.[a-z])?$')


# ----------------------------------------------------------------------------- workspace
class Course:
    def __init__(self, cid):
        self.id = cid
        self.work = WORK / cid
        self.pack = ROOT / 'courses' / cid
        self.cfg_file = self.work / 'course.cfg.json'

    @property
    def cfg(self):
        if not self.cfg_file.exists():
            sys.exit(f'unknown course {self.id}: run `coursegen.py new {self.id} --language … --title … --prefix …` first')
        return json.loads(self.cfg_file.read_text(encoding='utf-8'))

    def save_cfg(self, **kw):
        c = self.cfg_file.exists() and self.cfg or {}
        c.update(kw)
        self.work.mkdir(parents=True, exist_ok=True)
        self.cfg_file.write_text(json.dumps(c, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    source_txt = property(lambda s: s.work / 'source.txt')
    plan_file = property(lambda s: s.work / 'plan.json')
    src = property(lambda s: s.work / 'src')
    logs = property(lambda s: s.work / 'logs')
    curriculum = property(lambda s: s.pack / 'curriculum.json')

    def modules(self):
        return sorted(p.stem for p in self.src.glob('*.py'))

    def load_curriculum(self):
        return json.loads(self.curriculum.read_text(encoding='utf-8'))

    def load_plan(self):
        return json.loads(self.plan_file.read_text(encoding='utf-8'))


def rel(p):
    return str(pathlib.Path(p).resolve().relative_to(ROOT))


# ----------------------------------------------------------------------------- calling Claude
def render_prompt(name, **kw):
    t = (CG / 'prompts' / f'{name}.md').read_text(encoding='utf-8')
    kw.setdefault('gates', (CG / 'gates.md').read_text(encoding='utf-8'))
    for k, v in kw.items():
        t = t.replace('{{' + k + '}}', str(v))
    left = re.findall(r'\{\{(\w+)\}\}', t)
    assert not left, f'prompt {name}: unfilled {left}'
    return t


def ask(course, name, prompt, args, tools='Read,Write,Edit,Glob,Grep,Bash(python3 -I tools/*)'):
    """One headless Claude call. Returns stdout, or None for --dry-run. tools=None -> no tools at all."""
    course.logs.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    pf = course.logs / f'{stamp}-{name}.prompt.md'
    pf.write_text(prompt, encoding='utf-8')
    if args.dry_run:
        print(f'  [dry-run] prompt written to {rel(pf)}')
        return None
    cmd = shlex.split(os.environ.get('COGNIO_CLAUDE', 'claude')) + ['-p', '--no-session-persistence']
    cmd += ['--permission-mode', 'acceptEdits'] + (['--allowedTools', tools] if tools else ['--tools', ''])
    if args.model:
        cmd += ['--model', args.model]
    cmd += shlex.split(os.environ.get('COGNIO_CLAUDE_ARGS', ''))
    print(f'  claude: {name} …', flush=True)
    r = subprocess.run(cmd, input=prompt, text=True, capture_output=True, cwd=ROOT)
    (course.logs / f'{stamp}-{name}.out.md').write_text(r.stdout + ('\n--- stderr ---\n' + r.stderr if r.stderr else ''), encoding='utf-8')
    if r.returncode:
        sys.exit(f'claude exited with {r.returncode}: {r.stderr[-400:]}')
    return r.stdout


def report(title, errors, limit=25):
    if errors:
        print(f'FAIL {title}: {len(errors)} problem(s)')
        for e in errors[:limit]:
            print('   -', e)
        if len(errors) > limit:
            print(f'   … and {len(errors) - limit} more')
    else:
        print(f'OK   {title}')
    return not errors


# ----------------------------------------------------------------------------- stage 1: source (G1)
class _Text(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        self.skip += tag in ('script', 'style')
        if tag in ('p', 'li', 'br', 'tr', 'div', 'h1', 'h2', 'h3', 'h4'):
            self.out.append('\n')

    def handle_endtag(self, tag):
        self.skip -= tag in ('script', 'style') and self.skip > 0

    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)


def fetch(src, dest):
    dest.mkdir(parents=True, exist_ok=True)
    if re.match(r'https?://', src):
        name = re.sub(r'[^A-Za-z0-9._-]+', '_', src.split('://', 1)[1])[-80:]
        f = dest / name
        req = urllib.request.Request(src, headers={'User-Agent': 'cognio-coursegen/1.0'})
        with urllib.request.urlopen(req, timeout=60) as r:
            f.write_bytes(r.read())
        return f
    f = dest / pathlib.Path(src).name
    shutil.copyfile(src, f)
    return f


def to_text(f):
    raw = f.read_bytes()
    if raw[:5] == b'%PDF-' or f.suffix.lower() == '.pdf':
        if not shutil.which('pdftotext'):
            sys.exit('pdftotext (poppler) is needed for PDF sources')
        return subprocess.run(['pdftotext', '-layout', str(f), '-'], capture_output=True, text=True, check=True).stdout
    text = raw.decode('utf-8', errors='replace')
    if f.suffix.lower() in ('.html', '.htm') or text.lstrip()[:15].lower().startswith(('<!doctype', '<html')):
        p = _Text()
        p.feed(text)
        return ''.join(p.out)
    return text


def clean_source(text):
    lines = [re.sub(r'[ \t]+', ' ', l.replace('\x0c', '').replace('﻿', '')).strip() for l in text.split('\n')]
    out = [l for l in lines if l]
    return '\n'.join(out) + '\n'


def key(s):
    """Comparison key for the verbatim gate: ignores whitespace, hyphens/dashes (line-break hyphenation), case of nothing else."""
    return re.sub(r'[\s\-‐‑–—­]+', '', unicodedata.normalize('NFKC', s))


def check_source(c):
    errs = []
    if not c.curriculum.exists():
        return [f'{rel(c.curriculum)} does not exist']
    try:
        cur = c.load_curriculum()
    except json.JSONDecodeError as e:
        return [f'curriculum.json is not valid JSON: {e}']
    src = key(c.source_txt.read_text(encoding='utf-8')) if c.source_txt.exists() else None
    if src is None:
        errs.append('no source.txt: run the `source` stage (the verbatim check needs the source text)')
    seen = set()
    stages = cur.get('stages') or []
    if not stages:
        errs.append('no stages')
    for st in stages:
        if st.get('id') not in STAGES:
            errs.append(f'stage id {st.get("id")!r} not one of {STAGES}')
        if not st.get('areas'):
            errs.append(f'stage {st.get("id")}: no areas')
        for a in st.get('areas', []):
            if not re.fullmatch(re.escape(str(st.get('id'))) + r'\.\d+', str(a.get('id'))):
                errs.append(f'area id {a.get("id")!r} should be {st.get("id")}.<n>')
            if not a.get('objectives'):
                errs.append(f'area {a.get("id")}: no objectives')
            for o in a.get('objectives', []):
                for item in [o] + o.get('parts', []):
                    oid = item.get('id', '?')
                    if not OBJ_ID.match(oid) or not oid.startswith(str(a.get('id')) + '.'):
                        errs.append(f'bad objective id {oid!r} (area {a.get("id")})')
                    if oid in seen:
                        errs.append(f'duplicate objective id {oid}')
                    seen.add(oid)
                    t = item.get('text', '')
                    if len(t) < 8:
                        errs.append(f'{oid}: text missing or too short')
                    elif src is not None and key(t) not in src:
                        errs.append(f'{oid}: text is not verbatim in source.txt: {t[:70]!r}')
    return errs


def scaffold_manifest(c):
    cfg, cur = c.cfg, c.load_curriculum()
    f = c.pack / 'course.json'
    if f.exists():
        return
    lang = cfg['language']
    man = {'formatVersion': '1.0', 'id': c.id, 'version': '0.1.0', 'language': lang, 'title': {lang: cfg['title']},
           'description': {lang: cfg['title']}, 'authors': [cfg.get('author', 'coursegen')], 'license': 'private',
           'engine': {'min': '1.0.0', 'features': []}, 'curriculum': 'curriculum.json',
           'stages': [{'id': st['id'], 'title': {lang: st['title']}, 'skills': []} for st in cur['stages']], 'files': []}
    f.write_text(json.dumps(man, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


def stage_source(c, args):
    cfg = c.cfg
    if args.sources:
        parts = []
        for s in args.sources:
            f = fetch(s, c.work / 'input')
            parts.append(f'### source: {s}\n' + clean_source(to_text(f)))
            print(f'  fetched {s} -> {rel(f)}')
        c.source_txt.write_text('\n'.join(parts), encoding='utf-8')
    if not c.source_txt.exists():
        sys.exit('give at least one url/file')
    if args.note:
        c.save_cfg(source_note=args.note)
    note = c.cfg.get('source_note', 'see source.txt')
    c.pack.mkdir(parents=True, exist_ok=True)
    p = render_prompt('source', course=c.id, language=cfg['language'], source_txt=rel(c.source_txt), source_note=note,
                      curriculum_out=rel(c.curriculum))
    if ask(c, 'source', p, args) is None:
        return False
    ok = report('G1 source', check_source(c))
    if ok:
        scaffold_manifest(c)
    return ok


# ----------------------------------------------------------------------------- stage 2: plan (G2)
def leaf_ids(cur):
    ids = {}
    for st in cur['stages']:
        for a in st['areas']:
            for o in a['objectives']:
                ids[o['id']] = (st['id'], a['id'], [p['id'] for p in o.get('parts', [])])
    return ids


def check_plan(c):
    if not c.plan_file.exists():
        return [f'{rel(c.plan_file)} does not exist']
    try:
        plan, cur = c.load_plan(), c.load_curriculum()
    except json.JSONDecodeError as e:
        return [f'plan.json is not valid JSON: {e}']
    errs, objs = [], leaf_ids(cur)
    parts = {p for _, _, ps in objs.values() for p in ps}
    areas = {a['id'] for st in cur['stages'] for a in st['areas']}
    skills = {}
    for s in plan.get('skills', []):
        sid = s.get('id', '?')
        if not (isinstance(sid, str) and SLUG.match(sid) and len(sid) <= 60):
            errs.append(f'skill id {sid!r} is not a slug <= 60 chars')
        if sid in skills:
            errs.append(f'duplicate skill {sid}')
        skills[sid] = s
        if s.get('stage') not in STAGES:
            errs.append(f'{sid}: bad stage')
        if s.get('area') not in areas:
            errs.append(f'{sid}: unknown area {s.get("area")}')
        if s.get('source') not in ('generator', 'bank'):
            errs.append(f'{sid}: source must be generator or bank')
        if not 1 <= len(s.get('levels', [])) <= 3:
            errs.append(f'{sid}: 1-3 levels required')
        if not s.get('title') or not s.get('tasks'):
            errs.append(f'{sid}: title and tasks description required')
        if not s.get('objectives'):
            errs.append(f'{sid}: no objectives')
        for o in s.get('objectives', []):
            if o not in objs and o not in parts:
                errs.append(f'{sid}: unknown objective {o}')
    used = {o for s in skills.values() for o in s.get('objectives', [])}
    for oid, (_, _, ps) in objs.items():
        if oid not in used and not any(p in used for p in ps):
            errs.append(f'objective {oid} is not covered by any skill')
    placed = {}
    units = plan.get('units', [])
    if not units:
        errs.append('no units')
    uids = set()
    for u in units:
        if not (isinstance(u.get('id'), str) and SLUG.match(u['id'])) or u['id'] in uids:
            errs.append(f'unit id {u.get("id")!r} invalid or duplicate')
        uids.add(u.get('id'))
        if len(u.get('skills', [])) < 2:
            errs.append(f'unit {u.get("id")}: needs >= 2 skills')
        if u.get('area') not in areas:
            errs.append(f'unit {u.get("id")}: unknown area')
        for sid in u.get('skills', []):
            if sid not in skills:
                errs.append(f'unit {u.get("id")}: unknown skill {sid}')
            elif sid in placed:
                errs.append(f'skill {sid} is in two units')
            elif skills[sid].get('stage') != u.get('stage'):
                errs.append(f'skill {sid}: stage differs from unit {u.get("id")}')
            placed[sid] = len(placed)
    for sid in skills:
        if sid not in placed:
            errs.append(f'skill {sid} is in no unit')
    for sid, s in skills.items():
        for p in s.get('prerequisites', []):
            if p not in skills:
                errs.append(f'{sid}: unknown prerequisite {p}')
            elif skills[p].get('stage') != s.get('stage'):
                errs.append(f'{sid}: prerequisite {p} is in another stage')
            elif sid in placed and p in placed and placed[p] >= placed[sid]:
                errs.append(f'{sid}: prerequisite {p} does not come earlier in the path')
    return errs


def stage_plan(c, args):
    cfg = c.cfg
    p = render_prompt('plan', course=c.id, language=cfg['language'], prefix=cfg['prefix'], curriculum_out=rel(c.curriculum),
                      plan_out=rel(c.plan_file))
    if ask(c, 'plan', p, args) is None:
        return False
    return report('G2 plan', check_plan(c))


# ----------------------------------------------------------------------------- building packs (G3/G4)
def build_pack(c, out, modules, plan_mode):
    """Run the course modules through dsl.py into `out` (fresh process: dsl keeps its state in module globals).
    plan_mode 'full' = paths from plan.json; 'batch' = one scratch unit per stage so lint can see lessons."""
    out.mkdir(parents=True, exist_ok=True)
    if out != c.pack:
        shutil.copyfile(c.pack / 'curriculum.json', out / 'curriculum.json')
        man = json.loads((c.pack / 'course.json').read_text(encoding='utf-8'))
        man['files'] = []
        (out / 'course.json').write_text(json.dumps(man, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    env = dict(os.environ, COGNIO_PACK=str(out))
    r = subprocess.run([sys.executable, '-I', str(TOOLS / 'coursegen.py'), '_build', c.id, plan_mode, ','.join(modules)],
                       env=env, capture_output=True, text=True, cwd=ROOT)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def _build(cid, plan_mode, modules):
    """Internal entry (subprocess): import modules, write the pack, add the path."""
    import importlib
    c = Course(cid)
    sys.path[:0] = [str(ROOT / 'content-src'), str(c.src)]
    import dsl
    for m in modules.split(','):
        importlib.import_module(m)
    plan = c.load_plan()
    have = set(dsl.SKILLS)
    if plan_mode == 'batch':     # prerequisites in other batches are checked by the full build
        for sk in dsl.SKILLS.values():
            sk['prerequisites'] = [p for p in sk.get('prerequisites', []) if p in have]
            if not sk['prerequisites']:
                sk.pop('prerequisites', None)
    for u in plan['units']:
        sk = [s for s in u['skills'] if s in have]
        if plan_mode == 'batch':
            continue
        if len(sk) != len(u['skills']):
            sys.exit(f'unit {u["id"]}: skills without content: {sorted(set(u["skills"]) - have)}')
        unit = dsl.Unit(u['stage'], u['id'], u['title'], u.get('description', ''), u.get('icon', 'star'), u.get('area'))
        for i, sid in enumerate(sk, 1):
            unit.learn(sid)
            if len(sk) >= 4 and i % 3 == 0 and i < len(sk):
                unit.review(f'Powtórka {i // 3}' if c.cfg['language'] == 'pl' else f'Review {i // 3}', sk[max(0, i - 3):i], tasks=8)
        unit.checkpoint(sk, tasks=12)
    if plan_mode == 'batch':     # scratch path: learn lessons of the batch's skills, 4 tasks each (the smallest legal lesson)
        for stage in STAGES:
            sk = [s for s in dsl.SKILLS if dsl.SKILLS[s]['stage'] == stage]
            if sk:
                unit = dsl.Unit(stage, f'scratch-{stage.lower()}', 'scratch', 'scratch', 'star')
                for sid in sk:
                    unit.learn(sid, tasks=4)
                unit.practice(sk[0], tasks=4)
    missing = [s['id'] for s in plan['skills'] if plan_mode == 'full' and s['id'] not in have]
    if missing:
        sys.exit(f'skills in the plan without content: {missing}')
    dsl.write_all()
    print(f'{len(dsl.SKILLS)} skills, {len(dsl.GENS)} generators, {sum(map(len, dsl.BANKS.values()))} bank tasks')


def run_cognio(*a):
    r = subprocess.run([sys.executable, '-I', str(TOOLS / 'cognio.py'), *map(str, a)], capture_output=True, text=True, cwd=ROOT)
    return r.returncode, r.stdout, r.stderr


def lint_failures(pack):
    rc, out, err = run_cognio('lint', pack)
    fails = [l[5:] for l in out.splitlines() if l.startswith('FAIL')]
    if err.strip() and not fails:
        fails.append(err.strip()[-500:])
    return fails


def check_batch(c, module):
    scratch = c.work / 'tmp' / module
    shutil.rmtree(scratch, ignore_errors=True)
    ok, msg = build_pack(c, scratch, [module], 'batch')
    if not ok:
        return [f'build failed: {msg[-600:]}'], scratch
    return lint_failures(scratch), scratch


def stage_author(c, args):
    cfg, plan, cur = c.cfg, c.load_plan(), c.load_curriculum()
    c.src.mkdir(parents=True, exist_ok=True)
    texts = {}
    for st in cur['stages']:
        for a in st['areas']:
            for o in a['objectives']:
                texts[o['id']] = o['text']
                texts.update({p['id']: p['text'] for p in o.get('parts', [])})
    order = []
    for u in plan['units']:                      # batches follow the path: consecutive skills of one stage, <= batch-size
        for sid in u['skills']:
            order.append((u['stage'], sid))
    batches, cur_b = [], []
    for stage, sid in order:
        if cur_b and (cur_b[0][0] != stage or len(cur_b) >= args.batch_size):
            batches.append(cur_b)
            cur_b = []
        cur_b.append((stage, sid))
    if cur_b:
        batches.append(cur_b)
    by_id = {s['id']: s for s in plan['skills']}
    allok = True
    for n, b in enumerate(batches, 1):
        stage = b[0][0]
        module = f'b{n:02d}_{stage.lower().replace("-", "_")}'
        mfile = c.src / f'{module}.py'
        if mfile.exists() and not args.redo:
            print(f'batch {n}/{len(batches)} {module}: exists (use --redo to rewrite)')
        else:
            skills = [by_id[sid] for _, sid in b]
            objs = {o: texts.get(o, '') for s in skills for o in s['objectives']}
            p = render_prompt('author', course=c.id, language=cfg['language'], curriculum_out=rel(c.curriculum), module_out=rel(mfile),
                              module_name=module, batch=json.dumps(skills, ensure_ascii=False, indent=1),
                              objectives=json.dumps(objs, ensure_ascii=False, indent=1), rounds=args.rounds)
            print(f'batch {n}/{len(batches)} {module}: {len(skills)} skills')
            if ask(c, f'author-{module}', p, args) is None:
                continue
        if args.dry_run:
            continue
        if not mfile.exists():
            allok = False
            print(f'FAIL {module}: Claude did not write {rel(mfile)}')
            continue
        for rnd in range(args.rounds + 1):
            fails, scratch = check_batch(c, module)
            if not fails or rnd == args.rounds:
                break
            p = render_prompt('repair', course=c.id, module_out=rel(mfile), module_name=module, scratch_pack=rel(scratch),
                              failures='\n'.join(fails[:40]), rounds=args.rounds)
            ask(c, f'repair-{module}-{rnd + 1}', p, args)
        allok &= report(f'G3 {module}', fails)
    return allok and not args.dry_run


# ----------------------------------------------------------------------------- stage 5: validate (G4 + G5)
def canon(a):
    """Canonical form of a typed answer value, for comparing the stored answer with the examiner's."""
    if a is None:
        return None
    t, num = a.get('type'), (lambda x: Fraction(str(x).replace(',', '.').replace(' ', '').replace(' ', '')))
    try:
        if t in ('int', 'decimal'):
            return num(a['value'])
        if t == 'rational':
            return num(a['num']) / num(a['den'])
        if t == 'mixed':
            return num(a['whole']) + num(a['num']) / num(a['den'])
        if t == 'quantity':
            return num(a['value'])
        if t in ('choice', 'time'):
            return str(a['value']).strip()
        if t == 'set':
            return tuple(sorted(map(str, a['value'])))
        if t == 'sequence':
            return tuple(map(str, a['value']))
        if t == 'bool':
            return str(a['value']).lower()
        if t == 'point':
            return (num(a['x']), num(a['y']))
        return str(a.get('value', '')).strip().casefold()
    except (KeyError, ValueError, ZeroDivisionError, TypeError):
        return ('invalid', json.dumps(a, sort_keys=True))


def answer_format(a):
    f = {k: ('…' if k not in ('type', 'form') else v) for k, v in a.items() if k != 'unit'}
    return f


def sample_tasks(c, pack, per_level):
    sys.path.insert(0, str(TOOLS))
    import cognio
    out = []
    for sf in sorted((pack / 'skills').rglob('*.json')):
        sk = json.loads(sf.read_text(encoding='utf-8'))
        for src in sk['taskSources']:
            ref = pack / src['ref']
            if src['type'] == 'generator':
                g = json.loads(ref.read_text(encoding='utf-8'))
                for lv in src['levels']:
                    for i in range(per_level):
                        seed = 1000 + 7919 * i + lv
                        out.append((sk['id'], lv, seed, cognio.generate(g, sk['id'], lv, seed)))
            elif src['type'] == 'bank':
                tasks = [json.loads(l) for l in ref.read_text(encoding='utf-8').splitlines()]
                random.Random(sk['id']).shuffle(tasks)
                for lv in sorted({t['level'] for t in tasks}):
                    out.extend((sk['id'], lv, 0, t) for t in [t for t in tasks if t['level'] == lv][:per_level])
    return out


def exam_view(t, rng):
    """What the examiner sees: no answer, no steps, no error rules, options shuffled."""
    v = {'id': t['id'], 'kind': t['kind'], 'prompt': t['prompt'], 'answerFormat': answer_format(t['answer'])}
    for k in ('input', 'media'):
        if t.get(k):
            v[k] = json.loads(json.dumps(t[k], ensure_ascii=False))
    if t.get('options'):
        opts = [{'id': o['id'], 'text': o['text']} for o in t['options']]
        rng.shuffle(opts)
        v['options'] = opts
    return v


def parse_json_object(text):
    m = re.search(r'\{.*\}', text, re.S)
    return json.loads(m.group(0)) if m else {}


def blind_solve(c, pack, args):
    """G5: independent examiner vs stored answers. Returns (mismatches, checked, skipped)."""
    sample = sample_tasks(c, pack, args.sample)
    rng = random.Random(7)
    views, truth, meta = [], {}, {}
    for sid, lv, seed, t in sample:
        tid = f'{sid}#L{lv}#s{seed}' if seed else t['id']
        t = dict(t, id=tid)
        views.append(exam_view(t, rng))
        truth[tid] = t['answer']
        meta[tid] = (sid, lv, seed, t)
    mism, checked, skipped = [], 0, 0
    for i in range(0, len(views), args.exam_batch):
        chunk = views[i:i + args.exam_batch]
        out = ask(c, f'solve-{i // args.exam_batch:03d}', render_prompt('solve', tasks=json.dumps(chunk, ensure_ascii=False, indent=1)),
                  args, tools=None)
        if out is None:
            return None
        try:
            got = parse_json_object(out)
        except json.JSONDecodeError:
            got = {}
        for v in chunk:
            tid = v['id']
            if tid not in got or got[tid] is None:
                skipped += 1
                continue
            checked += 1
            ans = got[tid] if isinstance(got[tid], dict) else {'type': truth[tid]['type'], 'value': got[tid]}
            if canon(ans) != canon(truth[tid]):
                sid, lv, seed, t = meta[tid]
                mism.append({'skill': sid, 'level': lv, 'seed': seed, 'task': tid, 'prompt': t['prompt'], 'stored': truth[tid],
                             'examiner': got[tid], 'options': t.get('options')})
    return mism, checked, skipped


def skill_module(c, skill_id):
    for m in c.modules():
        if re.search(rf"(skill|bank_skill)\(\s*'{re.escape(skill_id)}'", (c.src / f'{m}.py').read_text(encoding='utf-8')):
            return m


def mechanical_gates(c):
    """Everything that needs no model: build, lint, coverage."""
    ok, msg = build_pack(c, c.pack, c.modules(), 'full')
    if not ok:
        return [f'build failed: {msg[-800:]}']
    run_cognio('fit', c.pack)
    (c.work / 'tmp').mkdir(parents=True, exist_ok=True)
    run_cognio('pack', c.pack, c.work / 'tmp' / 'pre.cognio')      # refresh the hashes in course.json, then lint verifies them
    errs = lint_failures(c.pack)
    cur, used = c.load_curriculum(), set()
    for sf in (c.pack / 'skills').rglob('*.json'):
        used |= set(json.loads(sf.read_text(encoding='utf-8'))['objectives'])
    for oid, (_, _, ps) in leaf_ids(cur).items():
        if oid not in used and not any(p in used for p in ps):
            errs.append(f'coverage: objective {oid} has no skill')
    return errs


def stage_validate(c, args):
    errs = mechanical_gates(c)
    if not report('G4 build + lint + coverage', errs):
        return False
    for rnd in range(args.repair_rounds + 1):
        res = blind_solve(c, c.pack, args)
        if res is None:
            return False
        mism, checked, skipped = res
        (c.work / 'review.json').write_text(json.dumps(mism, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'  blind solve: {checked} checked, {skipped} unsolvable-without-picture, {len(mism)} mismatches (round {rnd + 1})')
        if not mism or rnd == args.repair_rounds:
            break
        by_skill = {}
        for m in mism:
            by_skill.setdefault(m['skill'], []).append(m)
        for sid, ms in by_skill.items():
            mod = skill_module(c, sid)
            if not mod:
                continue
            p = render_prompt('review-repair', course=c.id, module_out=rel(c.src / f'{mod}.py'), module_name=mod, skill=sid,
                              mismatches=json.dumps(ms, ensure_ascii=False, indent=1))
            ask(c, f'review-repair-{sid}', p, args)
        errs = mechanical_gates(c)
        if not report('G4 rebuild after repairs', errs):
            return False
    if mism:
        print(f'FAIL G5 blind solve: {len(mism)} mismatch(es), see {rel(c.work / "review.json")}')
        return False
    print('OK   G5 blind solve')
    version = json.loads((c.pack / 'course.json').read_text(encoding='utf-8'))['version']
    dist = ROOT / 'dist' / 'courses'
    dist.mkdir(parents=True, exist_ok=True)
    rc, out, err = run_cognio('pack', c.pack, dist / f'{c.id}-{version}.cognio')
    errs = lint_failures(c.pack)       # hashes are checked by lint
    if not errs:
        subprocess.run([sys.executable, '-I', str(ROOT / 'tools' / 'make_index.py')], check=False)
    return report(f'pack dist/courses/{c.id}-{version}.cognio', errs)


# ----------------------------------------------------------------------------- commands
def cmd_status(c):
    cfg = c.cfg
    print(f'course {c.id}  language={cfg["language"]}  prefix={cfg["prefix"]}')
    print('G1 source  :', 'ok' if not check_source(c) else 'not passed')
    if c.plan_file.exists():
        print('G2 plan    :', 'ok' if not check_plan(c) else 'not passed', f'({len(c.load_plan()["skills"])} skills)')
    print('G3 modules :', ', '.join(c.modules()) or '-')
    print('pack       :', 'built' if (c.pack / 'skills').exists() else '-')


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd')
    ap.add_argument('course')
    ap.add_argument('rest', nargs='*')
    ap.add_argument('--language', default='pl')
    ap.add_argument('--title')
    ap.add_argument('--prefix')
    ap.add_argument('--note')
    ap.add_argument('--model')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--batch-size', type=int, default=8)
    ap.add_argument('--rounds', type=int, default=3)
    ap.add_argument('--redo', action='store_true', help='author: rewrite modules that already exist')
    ap.add_argument('--sample', type=int, default=3, help='validate: tasks per skill level for the blind solve')
    ap.add_argument('--exam-batch', type=int, default=20)
    ap.add_argument('--repair-rounds', type=int, default=2)
    args = ap.parse_intermixed_args(argv[1:])
    args.sources = args.rest
    c = Course(args.course)
    if args.cmd == '_build':
        _build(args.course, args.rest[0], args.rest[1])
        return 0
    if args.cmd == 'new':
        if not (args.title and args.prefix and SLUG.match(args.prefix) and SLUG.match(args.course)):
            sys.exit('new needs --title and --prefix (slugs: a-z, 0-9, -) and a slug course id')
        c.save_cfg(language=args.language, title=args.title, prefix=args.prefix)
        for d in (c.work / 'input', c.src):
            d.mkdir(parents=True, exist_ok=True)
        print(f'workspace {rel(c.work)} created')
        return 0
    if args.cmd == 'status':
        cmd_status(c)
        return 0
    if args.cmd == 'check-source':
        return 0 if report('G1 source', check_source(c)) else 1
    if args.cmd == 'check-plan':
        return 0 if report('G2 plan', check_plan(c)) else 1
    if args.cmd == 'check-batch':
        fails, _ = check_batch(c, args.rest[0])
        return 0 if report(f'G3 {args.rest[0]}', fails) else 1
    if args.cmd == 'build':
        return 0 if report('G4 build + lint + coverage', mechanical_gates(c)) else 1
    if args.cmd == 'gates':
        ok = report('G1 source', check_source(c)) & report('G2 plan', check_plan(c)) & report('G4 build + lint + coverage', mechanical_gates(c))
        return 0 if ok else 1
    stages = {'source': [stage_source], 'plan': [stage_plan], 'author': [stage_author], 'validate': [stage_validate],
              'all': [stage_source, stage_plan, stage_author, stage_validate]}
    if args.cmd not in stages:
        sys.exit(f'unknown command {args.cmd}')
    for fn in stages[args.cmd]:
        if fn(c, args) is False and not args.dry_run:
            print(f'stopped: the gate of `{fn.__name__[6:]}` did not pass')
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
