#!/usr/bin/env python3
"""Writes dist/index.json: the static index the Cognio app (and cognio-server) serves, for the packs in dist/courses/.

The repository is itself a pack source: the app can read `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/dist/` directly
(index.json + courses/*.cognio, urls relative to the index, sha256 verified by the app). Run it after every `pack`
(content-src/build.py and tools/coursegen.py do); `--check` fails when the committed index is out of date.

    python3 -I tools/make_index.py [--check]
"""
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
PACK_NAME = re.compile(r'^[a-z0-9][a-z0-9._-]{0,127}\.cognio$')
SEMVER = re.compile(r'^(\d+)\.(\d+)\.(\d+)$')


def semver_key(v):
    m = SEMVER.match(v)
    return tuple(int(x) for x in m.groups()) if m else (-1, -1, -1)


def build():
    models_src, models_dst = ROOT / 'models' / 'catalog.json', DIST / 'models' / 'catalog.json'
    if models_src.is_file():
        models_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(models_src, models_dst)
    packs = []
    for p in sorted((DIST / 'courses').glob('*.cognio')):
        if not PACK_NAME.match(p.name):
            continue
        try:
            with zipfile.ZipFile(p) as z:
                m = json.loads(z.read('course.json'))
            for k in ('id', 'version', 'formatVersion', 'language', 'title'):
                if k not in m:
                    raise ValueError(f"course.json has no '{k}'")
            if not SEMVER.match(str(m['version'])):
                raise ValueError(f"version '{m['version']}' is not x.y.z")
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as e:
            print(f'ignoring {p.name}: {e}', file=sys.stderr)
            continue
        packs.append((p, m))
    packs.sort(key=lambda t: (t[1]['id'], semver_key(t[1]['version'])))
    newest = {m['id']: m['version'] for _, m in packs}  # ascending order: the last one wins
    return {
        'formatVersion': '1.0',
        'courses': [
            {'id': m['id'], 'version': m['version'], 'latest': newest[m['id']] == m['version'], 'title': m['title'],
             'language': m['language'], 'formatVersion': m['formatVersion'], 'engine': m.get('engine', {}),
             'size': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'url': f'courses/{p.name}'}
            for p, m in packs
        ],
        'models': 'models/catalog.json' if models_dst.is_file() else None,
    }


if __name__ == '__main__':
    text = json.dumps(build(), ensure_ascii=False, indent=2) + '\n'
    out = DIST / 'index.json'
    if '--check' in sys.argv:
        if not out.is_file() or out.read_text() != text:
            sys.exit('dist/index.json is out of date: run python3 -I tools/make_index.py')
        print('dist/index.json is up to date')
    else:
        out.write_text(text)
        print(f'wrote {out.relative_to(ROOT)}: {len(json.loads(text)["courses"])} pack(s)')
