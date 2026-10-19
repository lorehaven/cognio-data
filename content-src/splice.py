"""Dev helper: replace whole skill blocks in a content module.
usage: python3 -I splice.py <module.py> <blocks.py>   (blocks.py holds one or more `skill('id', ...)` / `bank_skill('id', ...)` blocks separated by blank lines)
A block runs from its `skill(` line to the next line starting at column 0 with `skill(`, `bank_skill(`, `un =`, `Unit(`, `#` or EOF."""
import pathlib, re, sys

mod, blocks_file = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
text = mod.read_text()
START = re.compile(r"^(skill|bank_skill)\('([^']+)'", re.M)
BOUND = re.compile(r"^(skill\(|bank_skill\(|un = |un\.|Unit\(|#|[A-Za-z_]+ = )", re.M)

def split_blocks(src):
    starts = [m for m in START.finditer(src)]
    out = []
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(src)
        out.append((m.group(2), src[m.start():end].rstrip() + '\n'))
    return out

for sid, blk in split_blocks(blocks_file.read_text()):
    m = re.search(rf"^(skill|bank_skill)\('{re.escape(sid)}'", text, re.M)
    if not m:
        print('not found, appending:', sid)
        text = text.rstrip() + '\n\n' + blk
        continue
    nxt = BOUND.search(text, m.end())
    end = nxt.start() if nxt else len(text)
    text = text[:m.start()] + blk + '\n' + text[end:]
    print('replaced', sid)
mod.write_text(text)
