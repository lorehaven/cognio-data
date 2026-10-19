"""Contact sheet of all task media of a pack:  python3 -I tools/gallery.py courses/pl-primary-math out.html [seeds=3]
One card per (skill, level, seed): the prompt and the drawn media.  For human review of figures and charts."""
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cognio  # noqa: E402
import render  # noqa: E402

pack, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
seeds = int(sys.argv[3]) if len(sys.argv) > 3 else 3
cards = []
for gf in sorted((pack / 'generators').glob('*.json')):
    g = json.loads(gf.read_text(encoding='utf-8'))
    if not g['task'].get('media'):
        continue
    for lv in g['levels']:
        for seed in range(1, seeds + 1):
            t = cognio.generate(g, g['id'], lv['level'], seed * 7)
            figs = ''.join(render.to_svg(render.scene(m), scale=1) for m in t.get('media', []))
            if figs:
                cards.append(f'<div class="c"><div class="h">{html.escape(g["id"])} · L{lv["level"]} · seed {seed * 7}</div>{figs}<p>{html.escape(t["prompt"])}</p></div>')
out.write_text('<!doctype html><meta charset="utf-8"><title>Cognio media gallery</title>'
               '<style>body{font:14px sans-serif;background:#eee;margin:12px}.c{display:inline-block;vertical-align:top;background:#fff;margin:6px;padding:8px;width:340px;border-radius:8px}'
               '.h{font-weight:bold;color:#555;font-size:12px}p{margin:4px 0;color:#333}</style>' + ''.join(cards), encoding='utf-8')
print(f'{len(cards)} cards -> {out}')
