"""Authoring helpers: a compact Python layer that emits the pack's JSON (skills, generators, banks, paths).

The pack under courses/pl-primary-math is the artifact; this directory is its source.  Run `python3 -I build.py`.
Everything is plain data at the end - no Python runs in the app.
"""
import json
import os
import pathlib

# COGNIO_PACK lets tools/coursegen.py build another course (or a scratch pack) with the same helpers.
PACK = pathlib.Path(os.environ.get('COGNIO_PACK') or pathlib.Path(__file__).resolve().parent.parent / 'courses' / 'pl-primary-math')

SKILLS, GENS, BANKS, PATHS, QUESTS = {}, {}, {}, {}, {}
STAGE_DIR = {'I-III': 'I-III', 'IV-VI': 'IV-VI', 'VII-VIII': 'VII-VIII'}


# ----------------------------------------------------------------------------- answers
def _e(x):
    return {'$expr': str(x)}


def E(x): return _e(x)
def Int(e): return {'type': 'int', 'value': _e(e)}
def Dec(e): return {'type': 'decimal', 'value': _e(e)}
def Rat(n, d, lowest=True): return {'type': 'rational', 'num': _e(n), 'den': _e(d), 'form': 'lowest' if lowest else 'any'}
def Mixed(w, n, d): return {'type': 'mixed', 'whole': _e(w), 'num': _e(n), 'den': _e(d)}
def Qty(e, unit, unit_expr=False): return {'type': 'quantity', 'value': _e(e), 'unit': _e(unit) if unit_expr else unit}
def Choice(e): return {'type': 'choice', 'value': _e(e)}
def Seq(e): return {'type': 'sequence', 'value': _e(e)}
def Set(e): return {'type': 'set', 'value': _e(e)}
def Time(e): return {'type': 'time', 'value': _e(e)}
def Pt(x, y): return {'type': 'point', 'x': _e(x), 'y': _e(y)}


# ----------------------------------------------------------------------------- tasks
def _steps(steps):
    out = []
    for s in steps:
        if isinstance(s, tuple):
            out.append({'kind': s[0], 'text': s[1]})
        else:
            out.append({'text': s})
    return out


def task(kind, prompt, answer, steps, *, options=None, input=None, media=None, errors=(), equivalent=(), tags=(), constraints=()):
    """errors: (id, answer, feedback) or (id, answer, feedback, when_expr)."""
    t = {'kind': kind, 'prompt': prompt, 'answer': answer, 'steps': _steps(steps)}
    if options:
        t['options'] = options
    if input:
        t['input'] = input
    if media:
        t['media'] = media
    if errors:
        t['errorRules'] = []
        for e in errors:
            r = {'id': e[0], 'answer': e[1], 'feedback': e[2]}
            if len(e) > 3:
                r['when'] = e[3]
            t['errorRules'].append(r)
    if equivalent:
        t['equivalent'] = [{'answer': a, 'verdict': 'almost', 'feedbackKey': k} for a, k in equivalent]
    if tags:
        t['tags'] = list(tags)
    t['_constraints'] = list(constraints)
    return t


def number(prompt, answer, steps, **kw):
    return task('number-input', prompt, Int(answer), steps, **kw)


def decimal(prompt, answer, steps, **kw):
    return task('decimal-input', prompt, Dec(answer), steps, **kw)


def fraction(prompt, n, d, steps, lowest=True, **kw):
    return task('fraction-input', prompt, Rat(n, d, lowest), steps, **kw)


def quantity(prompt, expr, unit, steps, decimals=None, unit_expr=False, **kw):
    """unit: literal unit text, or (unit_expr=True) a DSL expression giving it."""
    inp = {'unit': _e(unit) if unit_expr else unit}
    if decimals is not None:
        inp['decimals'] = decimals
    return task('quantity-input', prompt, Qty(expr, unit, unit_expr), steps, input=inp, **kw)


def choice(prompt, correct, wrongs, steps, *, fmt=None, errors=(), fixed_order=False, extra_constraints=(), **kw):
    """Multiple choice. correct / wrongs are DSL expressions (values) rendered with filter `fmt` (None = raw text).
    The app shuffles the options unless input.fixedOrder is set. Distinctness of all values is added as a constraint."""
    vals = [correct] + list(wrongs)
    f = f'|{fmt}' if fmt else ''
    options = [{'id': 'abcdefgh'[i], 'text': f'@{{{x}{f}}}', **({'correct': 'true'} if i == 0 else {'correct': 'false'})}
               for i, x in enumerate(vals)]
    cons = [f'({vals[i]}) != ({vals[j]})' for i in range(len(vals)) for j in range(i + 1, len(vals))]
    inp = {'fixedOrder': True} if fixed_order else None
    return task('multiple-choice', prompt, Choice("'a'"), steps, options=options, input=inp, errors=errors,
                constraints=cons + list(extra_constraints), **kw)


def choice_text(prompt, options, correct_ids, steps, *, errors=(), fixed_order=False, multi=False, **kw):
    """Options with explicit text templates and boolean correctness expressions: options=[(text, 'expr'), ...]."""
    opts = [{'id': 'abcdefgh'[i], 'text': t, 'correct': c} for i, (t, c) in enumerate(options)]
    inp = {'fixedOrder': True} if fixed_order else None
    ids = ' + '.join(f"(['{'abcdefgh'[i]}'] if ({c}) else [])" for i, (_, c) in enumerate(options))
    if multi:
        flags = '[' + ', '.join(c for _, c in options) + ']'
        return task('multi-select', prompt, Set(f"({ids})"), steps, options=opts, input=inp, errors=errors,
                    constraints=[f'count({flags}, true) >= 1', f'count({flags}, false) >= 1'], **kw)
    return task('multiple-choice', prompt, Choice(f"({ids})[0]"), steps, options=opts, input=inp, errors=errors, **kw)


def order(prompt, xs, n, steps, *, fmt='dec', descending='false', math=False, **kw):
    """Order n distinct values from list expression xs (ids are str(value)); `descending` is a DSL boolean expression."""
    wrap = '$' if math else ''
    items = [{'id': _e(f'str({xs}[{i}])'), 'text': f'{wrap}@{{{xs}[{i}]|{fmt}}}{wrap}'} for i in range(n)]
    ans = f'(reverse(sorted({xs})) if {descending} else sorted({xs}))'
    cons = [f'len({xs}) == {n}'] + [f'{xs}[{i}] != {xs}[{j}]' for i in range(n) for j in range(i + 1, n)]
    return task('order-items', prompt, Seq(ans), steps, input={'items': items}, constraints=cons, **kw)


# ----------------------------------------------------------------------------- skills
def lvl(label, caps=None, md=None, **vars):
    """One difficulty level: label, optional regulation cap note, md = minimum distinct tasks (lint), then level constants."""
    return {'label': label, 'caps': caps, 'md': md, 'vars': {k: str(x) for k, x in vars.items()}}


def skill(id, stage, title, objectives, levels, vars, task_, *, constraints=(), selfCheck=(), intro=None, ideas=(),
          prereq=(), tags=('no-calculator',), area=None, desc=None, min_distinct=None, order=None, extra_sources=()):
    """One skill with its own generator (generator id == skill id)."""
    assert id not in SKILLS, f'duplicate skill {id}'
    task_ = dict(task_)
    cons = list(constraints) + task_.pop('_constraints', [])
    gen = {'formatVersion': '1.0', 'id': id, 'levels': [],
           'vars': [({'name': v[0], 'expr': str(v[1]), 'require': True} if len(v) > 2 else {'name': v[0], 'expr': str(v[1])}) for v in vars]}
    if desc:
        gen['description'] = desc
    for i, l in enumerate(levels, 1):
        g = {'level': i}
        if l['vars']:
            g['vars'] = l['vars']
        if l['caps']:
            g['capsNote'] = l['caps']
        if l.get('md'):
            g['minDistinct'] = l['md']
        gen['levels'].append(g)
    if cons:
        gen['constraints'] = cons
    if selfCheck:
        gen['selfCheck'] = list(selfCheck)
    if min_distinct:
        gen['minDistinct'] = min_distinct
    gen['task'] = task_
    GENS[id] = gen
    sk = {'formatVersion': '1.0', 'id': id, 'stage': stage, 'title': {'pl': title}, 'objectives': list(objectives),
          'tags': list(tags),
          'levels': [{'level': i, 'label': {'pl': l['label']}, **({'capsNote': l['caps']} if l['caps'] else {})}
                     for i, l in enumerate(levels, 1)],
          'taskSources': [{'type': 'generator', 'ref': f'generators/{id}.json', 'levels': list(range(1, len(levels) + 1))}]}
    sk['taskSources'] += list(extra_sources)
    if area:
        sk['area'] = area
    if desc:
        sk['description'] = {'pl': desc}
    if prereq:
        sk['prerequisites'] = list(prereq)
    tutor = {}
    if intro:
        tutor['intro'] = {'pl': intro}
    if ideas:
        tutor['keyIdeas'] = [{'pl': i} for i in ideas]
    if tutor:
        sk['tutor'] = tutor
    SKILLS[id] = sk
    return id


def bank_skill(id, stage, title, objectives, tasks, *, levels=None, intro=None, ideas=(), prereq=(), tags=(), area=None, desc=None):
    """A skill whose tasks are hand-written (bank). tasks: list of compiled-task dicts (without id/skill/provenance)."""
    assert id not in SKILLS, f'duplicate skill {id}'
    fn = f'{id}.jsonl'
    lv_nums = sorted({t.get('level', 1) for t in tasks})
    levels = levels or [f'Poziom {n}' for n in lv_nums]
    out = []
    for i, t in enumerate(tasks, 1):
        t = dict(t)
        t.pop('_constraints', None)
        t.setdefault('level', 1)
        t.update({'id': f'bank/{id}/{i}', 'skill': id, 'provenance': {'source': 'bank-human', 'verifiedBy': 'human', 'createdAt': '2026-10-18'}})
        t['answer'] = _plain_answer(t['answer'])
        out.append(t)
    BANKS[fn] = out
    sk = {'formatVersion': '1.0', 'id': id, 'stage': stage, 'title': {'pl': title}, 'objectives': list(objectives),
          'tags': list(tags), 'levels': [{'level': n, 'label': {'pl': levels[i]}} for i, n in enumerate(lv_nums)],
          'taskSources': [{'type': 'bank', 'ref': f'banks/{fn}'}]}
    if area:
        sk['area'] = area
    if desc:
        sk['description'] = {'pl': desc}
    if prereq:
        sk['prerequisites'] = list(prereq)
    if intro or ideas:
        sk['tutor'] = {**({'intro': {'pl': intro}} if intro else {}), **({'keyIdeas': [{'pl': i} for i in ideas]} if ideas else {})}
    SKILLS[id] = sk
    return id


def _plain_answer(a):
    """Bank answers are literal values: unwrap {"$expr": "'x'"} / numbers written as python values."""
    out = {}
    for k, v in a.items():
        if isinstance(v, dict) and '$expr' in v:
            v = eval(v['$expr'], {}, {})
        out[k] = str(v) if k in ('value', 'num', 'den', 'whole', 'x', 'y') and not isinstance(v, (list, bool)) else v
    return out


# ----------------------------------------------------------------------------- paths
class Unit:
    def __init__(self, stage, id, title, desc, icon, area=None):
        self.stage, self.id, self.title, self.desc, self.icon, self.area = stage, id, title, desc, icon, area
        self.lessons = []
        PATHS.setdefault(stage, []).append(self)

    def _add(self, kind, title, **kw):
        lid = f'{self.id}-{len(self.lessons) + 1:02d}'
        self.lessons.append({'id': lid, 'title': {'pl': title}, 'kind': kind, **kw})
        return self

    def _levels(self, skill_id, levels):
        return list(levels) if levels else [l['level'] for l in SKILLS[skill_id]['levels']]

    def learn(self, skill_id, title=None, levels=None, tasks=10):
        """New skill. levels = crowns (default: every level of the skill); the first level completes the lesson."""
        return self._add('learn', title or SKILLS[skill_id]['title']['pl'], skill=skill_id, levels=self._levels(skill_id, levels), tasks=tasks)

    def practice(self, skill_id, title=None, levels=None, tasks=10):
        return self._add('practice', title or SKILLS[skill_id]['title']['pl'], skill=skill_id, levels=self._levels(skill_id, levels), tasks=tasks)

    def _mix(self, skill_ids, level):
        out = []
        for s in skill_ids:
            top = max(l['level'] for l in SKILLS[s]['levels'])
            out.append({'skill': s, 'level': min(level, top)})
        return out

    def quest(self, skill_id, title=None):
        """A story-driven multi-step activity (a skill whose task source is a quest)."""
        return self._add('quest', title or SKILLS[skill_id]['title']['pl'], skill=skill_id, levels=[1], tasks=len(QUESTS[skill_id]['steps']))

    def review(self, title, skill_ids, tasks=12, level=1):
        return self._add('review', title, mix=self._mix(skill_ids, level), tasks=tasks)

    def checkpoint(self, skill_ids, title='Sprawdzian działu', tasks=15, level=2):
        return self._add('checkpoint', title, mix=self._mix(skill_ids, level), tasks=tasks, passRatio=0.8)

    def to_json(self):
        d = {'id': self.id, 'title': {'pl': self.title}, 'description': {'pl': self.desc}, 'icon': self.icon,
             'lessons': self.lessons, 'testOut': {'tasks': 15, 'passRatio': 0.9}}
        if self.area:
            d['area'] = self.area
        return d


# ----------------------------------------------------------------------------- output
def write_all():
    for sub in ('skills', 'generators', 'banks', 'paths', 'quests'):
        d = PACK / sub
        d.mkdir(parents=True, exist_ok=True)
        for f in d.rglob('*'):
            if f.is_file():
                f.unlink()
    for sid, sk in SKILLS.items():
        d = PACK / 'skills' / sk['stage']
        d.mkdir(parents=True, exist_ok=True)
        (d / f'{sid}.json').write_text(json.dumps(sk, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for gid, g in GENS.items():
        (PACK / 'generators' / f'{gid}.json').write_text(json.dumps(g, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for qid, q in QUESTS.items():
        (PACK / 'quests' / f'{qid}.json').write_text(json.dumps(q, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for fn, tasks in BANKS.items():
        (PACK / 'banks' / fn).write_text('\n'.join(json.dumps(t, ensure_ascii=False) for t in tasks) + '\n', encoding='utf-8')
    for stage, units in PATHS.items():
        path = {'formatVersion': '1.0', 'stage': stage, 'entry': 'open', 'units': [u.to_json() for u in units]}
        (PACK / 'paths' / f'{stage}.json').write_text(json.dumps(path, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    man = json.loads((PACK / 'course.json').read_text(encoding='utf-8'))
    for st in man['stages']:
        st['skills'] = sorted(f'skills/{st["id"]}/{sid}.json' for sid, sk in SKILLS.items() if sk['stage'] == st['id'])
        st['path'] = f'paths/{st["id"]}.json' if st['id'] in PATHS else None
        if st['path'] is None:
            del st['path']
    man['engine']['features'] = sorted(set(man['engine'].get('features', [])) | {'order-items', 'multi-select', 'number-input', 'quantity-input'} | ({'quest'} if QUESTS else set()))
    (PACK / 'course.json').write_text(json.dumps(man, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


# ----------------------------------------------------------------------------- static (bank) task helpers
def bank_choice(prompt, options, steps, *, level=1, fixed=False, tags=(), multi=False):
    """options: [(text, is_correct)]. Exactly one correct unless multi=True."""
    ids = 'abcdefgh'
    opts = [{'id': ids[i], 'text': t, 'correct': bool(c)} for i, (t, c) in enumerate(options)]
    good = [o['id'] for o in opts if o['correct']]
    assert (len(good) >= 1) if multi else (len(good) == 1), (prompt, good)
    t = {'kind': 'multi-select' if multi else 'multiple-choice', 'prompt': prompt, 'options': opts,
         'answer': {'type': 'set', 'value': good} if multi else {'type': 'choice', 'value': good[0]},
         'steps': _steps(steps), 'level': level}
    if fixed:
        t['input'] = {'fixedOrder': True}
    if tags:
        t['tags'] = list(tags)
    return t


def bank_find_mistake(prompt, lines, wrong, steps, *, level=1, tags=('thinking',)):
    """lines: list of strings; wrong: 1-based index of the faulty line, or None if the solution is correct."""
    ids = [f'l{i}' for i in range(1, len(lines) + 1)]
    opts = [{'id': i, 'text': f'krok {n}'} for n, i in enumerate(ids, 1)] + [{'id': 'none', 'text': 'Nie ma błędu'}]
    return {'kind': 'find-the-mistake', 'prompt': prompt, 'input': {'lines': [{'id': i, 'text': t} for i, t in zip(ids, lines)]},
            'options': opts, 'answer': {'type': 'choice', 'value': 'none' if wrong is None else ids[wrong - 1]},
            'steps': _steps(steps), 'level': level, 'tags': list(tags)}


def bank_number(prompt, value, steps, *, level=1, tags=()):
    t = {'kind': 'number-input', 'prompt': prompt, 'answer': {'type': 'int', 'value': str(value)}, 'steps': _steps(steps), 'level': level}
    if tags:
        t['tags'] = list(tags)
    return t


# ----------------------------------------------------------------------------- figures (media) helpers
def fig(figure, alt, essential=False, when=None, **params):
    """A figure media item.  params values may contain E(...) expressions; `when` is an expression (attach only if true)."""
    m = {'type': 'figure', 'kind': figure, 'essential': essential, 'alt': alt, 'params': params}
    if when:
        m['when'] = when
    return m


def add_media(skill_id, *items):
    """Attach media items to the task template of an already defined skill (the figure layer lives in stage_media.py)."""
    task = GENS[skill_id]['task']
    task.setdefault('media', []).extend(items)


# ----------------------------------------------------------------------------- quests
def quest(id, stage, title, experience, intro, steps, vars, *, outro=None, media=(), constraints=(), selfCheck=(), objectives=(), prereq=(), area=None,
          tags=('thinking',), min_distinct=20, desc=None):
    """A quest (doświadczenie edukacyjne): a story with 4-10 ordinary tasks that share one set of random variables.
    The quest id doubles as the id of its skill (one level), so a path lesson of kind 'quest' can reference it."""
    assert id not in SKILLS, f'duplicate skill {id}'
    cons = list(constraints)
    st = []
    for t in steps:
        t = dict(t)
        cons += t.pop('_constraints', [])
        st.append(t)
    q = {'formatVersion': '1.0', 'id': id, 'title': {'pl': title}, 'experience': experience,
         'vars': [{'name': v[0], 'expr': str(v[1])} for v in vars], 'intro': intro, 'steps': st}
    if cons:
        q['constraints'] = cons
    if selfCheck:
        q['selfCheck'] = list(selfCheck)
    if media:
        q['media'] = list(media)
    if outro:
        q['outro'] = outro
    if min_distinct != 20:
        q['minDistinct'] = min_distinct
    QUESTS[id] = q
    sk = {'formatVersion': '1.0', 'id': id, 'stage': stage, 'title': {'pl': title}, 'objectives': list(objectives), 'tags': list(tags),
          'levels': [{'level': 1, 'label': {'pl': 'Misja'}}], 'taskSources': [{'type': 'quest', 'ref': f'quests/{id}.json'}],
          'tutor': {'intro': {'pl': desc or title}}}
    if area:
        sk['area'] = area
    if prereq:
        sk['prerequisites'] = list(prereq)
    SKILLS[id] = sk
    return id
