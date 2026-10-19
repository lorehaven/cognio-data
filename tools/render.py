"""Reference renderer for task media (figures, charts, tables).

A compiled task carries `media: [{type, kind, params, alt}]` (concrete JSON, expressions already resolved).
`scene(media)` turns one media item into a *scene*: a flat, theme-free list of drawing primitives in a
fixed coordinate space. The app draws a scene with its own canvas (Compose `DrawScope`); `to_svg` is the
reference drawing used for tests, previews and the gallery.

Scene = {"w": W, "h": H, "items": [...]}; y grows downwards. Item types (all numbers rounded to 2 places):
  line   {t, x1, y1, x2, y2, c, w, dash?}
  rect   {t, x, y, w, h, fill?, c?, sw?}
  circle {t, cx, cy, r, fill?, c?, sw?}
  arc    {t, cx, cy, r, a0, a1, c, sw}     degrees, counter-clockwise from +x, drawn a0 -> a1
  poly   {t, pts, fill?, c?, sw?, close}   pts = [[x, y], ...]
  text   {t, x, y, s, size, anchor, c, bold?}   (x, y) = anchor point, vertically centred
Colours are semantic roles: ink, muted, grid, accent, accent2, fill, fill2, good, bad, bg (the theme maps them).
Engine ports (cognio-render/) must produce the same scenes (tests/conformance/scenes.json).
"""
import math

W, H = 320, 200


def r2(v):
    return round(float(v) + 0.0, 2)


def fnum(v):
    """Number as shown to a Polish reader: decimal comma, minimal digits."""
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        return f"{int(v['num'])}/{int(v['den'])}"
    f = float(v)
    if abs(f - round(f)) < 1e-9:
        s = str(int(round(f)))
    else:
        s = ('%.4f' % f).rstrip('0').rstrip('.')
    return s.replace('-', '−').replace('.', ',')


def val(v):
    if isinstance(v, dict) and 'num' in v:
        return v['num'] / v['den']
    return float(v)


class S:
    def __init__(self, w=W, h=H):
        self.w, self.h, self.items = w, h, []

    def line(self, x1, y1, x2, y2, c='ink', w=1.5, dash=None):
        d = {'t': 'line', 'x1': r2(x1), 'y1': r2(y1), 'x2': r2(x2), 'y2': r2(y2), 'c': c, 'w': w}
        if dash:
            d['dash'] = dash
        self.items.append(d)

    def rect(self, x, y, w, h, fill=None, c=None, sw=1.5):
        d = {'t': 'rect', 'x': r2(x), 'y': r2(y), 'w': r2(w), 'h': r2(h)}
        if fill:
            d['fill'] = fill
        if c:
            d['c'] = c
            d['sw'] = sw
        self.items.append(d)

    def circle(self, cx, cy, r, fill=None, c=None, sw=1.5):
        d = {'t': 'circle', 'cx': r2(cx), 'cy': r2(cy), 'r': r2(r)}
        if fill:
            d['fill'] = fill
        if c:
            d['c'] = c
            d['sw'] = sw
        self.items.append(d)

    def arc(self, cx, cy, r, a0, a1, c='accent', sw=1.5):
        self.items.append({'t': 'arc', 'cx': r2(cx), 'cy': r2(cy), 'r': r2(r), 'a0': r2(a0), 'a1': r2(a1), 'c': c, 'sw': sw})

    def poly(self, pts, fill=None, c=None, sw=1.5, close=True):
        d = {'t': 'poly', 'pts': [[r2(x), r2(y)] for x, y in pts], 'close': close}
        if fill:
            d['fill'] = fill
        if c:
            d['c'] = c
            d['sw'] = sw
        self.items.append(d)

    def text(self, x, y, s, size=12, anchor='middle', c='ink', bold=False):
        d = {'t': 'text', 'x': r2(x), 'y': r2(y), 's': str(s), 'size': size, 'anchor': anchor, 'c': c}
        if bold:
            d['bold'] = True
        self.items.append(d)

    def out(self):
        return {'w': self.w, 'h': self.h, 'items': self.items}


class Fit:
    """Maps model coordinates (y up) into a box of the canvas, preserving aspect ratio."""
    def __init__(self, xs, ys, box, pad=0.0):
        x0, y0, x1, y1 = box
        self.minx, self.maxx, self.miny, self.maxy = min(xs), max(xs), min(ys), max(ys)
        dx = max(self.maxx - self.minx, 1e-9)
        dy = max(self.maxy - self.miny, 1e-9)
        self.k = min((x1 - x0) / dx, (y1 - y0) / dy)
        self.ox = x0 + ((x1 - x0) - dx * self.k) / 2
        self.oy = y0 + ((y1 - y0) - dy * self.k) / 2

    def __call__(self, x, y):
        return (self.ox + (x - self.minx) * self.k, self.oy + (self.maxy - y) * self.k)


def shown(lst):
    """entries of a params list; an entry with show=false (resolved from an expression) is dropped"""
    return [e for e in lst if not isinstance(e, dict) or e.get('show', True)]


def pol(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


# ---------------------------------------------------------------------------------------------- figures
def clock(p):
    s = S(W, H)
    cx, cy, R = 160, 100, 84
    s.circle(cx, cy, R, fill='fill', c='ink', sw=3)
    for i in range(60):
        a = 90 - i * 6
        r0 = R - (10 if i % 5 == 0 else 5)
        x0, y0 = pol(cx, cy, r0, a)
        x1, y1 = pol(cx, cy, R - 1, a)
        s.line(x0, y0, x1, y1, 'ink' if i % 5 == 0 else 'muted', 2 if i % 5 == 0 else 1)
    for n in range(1, 13):
        x, y = pol(cx, cy, R - 22, 90 - n * 30)
        s.text(x, y, n, 15, bold=True)
    h, m = int(p['hour']) % 12, int(p.get('minute', 0))
    ha = 90 - (h * 30 + m * 0.5)
    ma = 90 - m * 6
    x, y = pol(cx, cy, R * 0.5, ha)
    s.line(cx, cy, x, y, 'ink', 5)
    x, y = pol(cx, cy, R * 0.78, ma)
    s.line(cx, cy, x, y, 'accent', 3)
    s.circle(cx, cy, 4, fill='ink')
    return s.out()


def number_line(p):
    s = S(W, 90)
    lo, hi = val(p['min']), val(p['max'])
    if 'partsPerUnit' in p:
        d = int(p['partsPerUnit'])
        tick, every = 1.0 / d, d
    else:
        tick = val(p.get('tick', 1))
        every = int(p.get('labelEvery', 1))
    x0, x1, y = 24, 296, 52
    k = (x1 - x0) / (hi - lo)
    s.line(x0 - 10, y, x1 + 10, y, 'ink', 2)
    s.poly([(x1 + 10, y), (x1 + 4, y - 4), (x1 + 4, y + 4)], fill='ink')
    n = int(round((hi - lo) / tick))
    for i in range(n + 1):
        v = lo + i * tick
        x = x0 + (v - lo) * k
        big = i % every == 0
        s.line(x, y - (8 if big else 5), x, y + (8 if big else 5), 'ink', 1.5 if big else 1)
        if big:
            s.text(x, y + 22, fnum(round(v, 6)), 12)
    for pt in p.get('points', []):
        v = val(pt['at'])
        x = x0 + (v - lo) * k
        s.circle(x, y, 5, fill='accent', c='ink', sw=1)
        s.text(x, y - 20, pt.get('label', ''), 14, c='accent', bold=True)
    return s.out()


def fraction_bar(p):
    parts, shaded = int(p['parts']), int(p['shaded'])
    bars = max(1, -(-shaded // parts))
    s = S(W, 20 + 54 * bars)
    x0, w = 20, 280
    for b in range(bars):
        y = 14 + 54 * b
        for i in range(parts):
            idx = b * parts + i
            s.rect(x0 + i * w / parts, y, w / parts, 40, fill='accent' if idx < shaded else 'fill', c='ink', sw=1.5)
    return s.out()


def angle(p):
    s = S(W, H)
    deg = float(p['degrees'])
    start = float(p.get('startDeg', 12))
    vx, vy, L = 160, 108, 84
    labels = p.get('labels')
    a1, a2 = start, start + deg
    mid = (a1 + a2) / 2          # centre the opening of the angle upwards so the figure fits the canvas
    a1, a2 = a1 + (90 - mid), a2 + (90 - mid)
    x1, y1 = pol(vx, vy, L, a1)
    x2, y2 = pol(vx, vy, L, a2)
    s.line(vx, vy, x1, y1, 'ink', 3)
    s.line(vx, vy, x2, y2, 'ink', 3)
    if abs(deg - 90) < 1e-6:
        q = 18
        px, py = pol(vx, vy, q, a1)
        qx, qy = pol(vx, vy, q, a2)
        s.poly([(px, py), (px + qx - vx, py + qy - vy), (qx, qy)], c='accent', sw=2, close=False)
    else:
        s.arc(vx, vy, 34, a1, a2, 'accent', 2.5)
    s.circle(vx, vy, 3.5, fill='ink')
    if labels:
        s.text(vx - 12, vy + 12, labels[0], 14, bold=True)
        s.text(x1 + 10, y1 + 2, labels[1], 14, bold=True)
        s.text(x2 + 8, y2 - 6, labels[2], 14, bold=True)
    return s.out()


def protractor(p):
    s = S(W, 180)
    deg = float(p['degrees'])
    mirrored = bool(p.get('mirrored', False))
    cx, cy, R = 160, 150, 135
    s.poly([pol(cx, cy, R, a) for a in range(0, 181, 3)], fill='fill', c='ink', sw=2)
    s.line(cx - R - 8, cy, cx + R + 8, cy, 'ink', 2)
    for d in range(0, 181, 2):
        big = d % 10 == 0
        a = d
        x0, y0 = pol(cx, cy, R, a)
        x1, y1 = pol(cx, cy, R - (12 if big else (8 if d % 5 == 0 else 5)), a)
        s.line(x0, y0, x1, y1, 'ink', 1.2 if big else 0.8)
        if big:
            outer = d if not mirrored else 180 - d
            inner = 180 - d if not mirrored else d
            xo, yo = pol(cx, cy, R - 22, a)
            s.text(xo, yo, outer, 9)
            xi, yi = pol(cx, cy, R - 40, a)
            s.text(xi, yi, inner, 8, c='muted')
    s.circle(cx, cy, 4, fill='ink')
    base = 0 if not mirrored else 180
    ray = deg if not mirrored else 180 - deg
    xb, yb = pol(cx, cy, R + 8, base)
    xr, yr = pol(cx, cy, R + 8, ray)
    s.line(cx, cy, xb, yb, 'ink', 3)
    s.line(cx, cy, xr, yr, 'accent', 3)
    return s.out()


def ruler(p):
    start, length = float(p['startMm']), float(p['lengthMm'])
    end = start + length
    cm = int(-(-end // 10)) + 1
    s = S(W, 120)
    x0, x1 = 14, 306
    k = (x1 - x0) / (cm * 10)
    s.rect(x0 - 6, 62, x1 - x0 + 12, 44, fill='fill', c='ink', sw=1.5)
    for mm in range(0, cm * 10 + 1):
        x = x0 + mm * k
        big, half = mm % 10 == 0, mm % 5 == 0
        s.line(x, 62, x, 62 + (20 if big else (14 if half else 9)), 'ink', 1.4 if big else 0.9)
        if big:
            s.text(x, 96, mm // 10, 11)
    s.text(x1 - 6, 76, 'cm', 10, anchor='end', c='muted')
    xa, xb = x0 + start * k, x0 + end * k
    s.rect(xa, 30, xb - xa, 22, fill='accent', c='ink', sw=1.5)
    s.line(xa, 52, xa, 62, 'muted', 1, [2, 2])
    s.line(xb, 52, xb, 62, 'muted', 1, [2, 2])
    return s.out()


def thermometer(p):
    v, lo, hi = float(p['value']), float(p.get('min', -20)), float(p.get('max', 40))
    s = S(160, 220)
    cx, top, bot = 60, 16, 180
    k = (bot - top) / (hi - lo)
    s.rect(cx - 8, top - 6, 16, bot - top + 12, fill='fill', c='ink', sw=2)
    s.circle(cx, bot + 14, 17, fill='fill', c='ink', sw=2)
    y = bot - (v - lo) * k
    s.rect(cx - 4, y, 8, bot - y + 4, fill='bad')
    s.circle(cx, bot + 14, 13, fill='bad')
    t = lo
    while t <= hi + 1e-9:
        yy = bot - (t - lo) * k
        big = int(t) % 10 == 0
        s.line(cx + 8, yy, cx + (24 if big else 17), yy, 'ink', 1.3 if big else 0.9)
        if big:
            s.text(cx + 30, yy, fnum(t), 11, anchor='start')
        t += 2
    return s.out()


def rect_fig(p):
    w, h = float(p['w']), float(p['h'])
    unit = p.get('unit', '')
    s = S(W, H)
    f = Fit([0, w], [0, h], (60, 40, 270, 160))
    x0, y0 = f(0, h)
    x1, y1 = f(w, 0)
    s.rect(x0, y0, x1 - x0, y1 - y0, fill='fill', c='ink', sw=2.5)
    sq = abs(w - h) < 1e-9
    if sq:
        s.text((x0 + x1) / 2, y0 - 12, f"{fnum(w)} {unit}".strip(), 13, bold=True)
    else:
        s.text((x0 + x1) / 2, y1 + 16, f"{fnum(w)} {unit}".strip(), 13, bold=True)
        s.text(x0 - 10, (y0 + y1) / 2, f"{fnum(h)} {unit}".strip(), 13, anchor='end', bold=True)
    return s.out()


def _fit_poly(pts, box=(70, 34, 250, 168)):
    return Fit([q[0] for q in pts], [q[1] for q in pts], box)


def _right_mark(s, v, a, b, size=10):
    """right-angle square at screen vertex v between rays towards a and b."""
    def unit(p, q):
        dx, dy = q[0] - p[0], q[1] - p[1]
        n = math.hypot(dx, dy) or 1
        return dx / n, dy / n
    ua, ub = unit(v, a), unit(v, b)
    p1 = (v[0] + ua[0] * size, v[1] + ua[1] * size)
    p3 = (v[0] + ub[0] * size, v[1] + ub[1] * size)
    p2 = (p1[0] + ub[0] * size, p1[1] + ub[1] * size)
    s.poly([p1, p2, p3], c='accent', sw=1.6, close=False)


def triangle(p):
    A, B, C = p['A'], p['B'], p['C']
    feet = p.get('feet', [])
    xs = [A[0], B[0], C[0]] + [f['x'] for f in feet]  # feet: [{label, x}]
    ys = [A[1], B[1], C[1]] + ([0] if feet else [])
    s = S(W, H)
    fit = Fit(xs, ys, (30, 30, 290, 154))
    a, b, c = fit(*A), fit(*B), fit(*C)
    if feet:
        lx0, lx1 = fit(min(xs), 0), fit(max(xs), 0)
        s.line(lx0[0], lx0[1], lx1[0], lx1[1], 'muted', 1.5, [4, 3])
    s.poly([a, b, c], fill='fill', c='ink', sw=2.5)
    for i, f in enumerate(feet):
        fx = fit(f['x'], 0)
        s.line(c[0], c[1], fx[0], fx[1], 'accent', 1.8, [5, 3])
        s.circle(fx[0], fx[1], 2.5, fill='accent')
        s.text(fx[0], fx[1] + 14, f.get('label', ''), 13, bold=True, c='accent')
    if p.get('baseLabel'):
        s.text((a[0] + b[0]) / 2, a[1] + 32 if feet else a[1] + 16, p['baseLabel'], 13, bold=True)
    names = p.get('names', ['A', 'B', 'C'])
    s.text(a[0] - 12, a[1] + 4, names[0], 14, bold=True)
    s.text(b[0] + 12, b[1] + 4, names[1], 14, bold=True)
    s.text(c[0], c[1] - 12, names[2], 14, bold=True)
    return s.out()


def coordinate_plane(p):
    s = S(260, 260)
    x0 = float(p.get('xMin', p.get('min', -6)))
    x1 = float(p.get('xMax', p.get('max', 6)))
    y0 = float(p.get('yMin', p.get('min', -6)))
    y1 = float(p.get('yMax', p.get('max', 6)))
    pad = 24
    k = min((260 - 2 * pad) / (x1 - x0), (260 - 2 * pad) / (y1 - y0))
    ox = pad
    oy = 260 - pad

    def f(x, y):
        return ox + (x - x0) * k, oy - (y - y0) * k
    for i in range(int(x0), int(x1) + 1):
        a = f(i, y0)
        b = f(i, y1)
        s.line(a[0], a[1], b[0], b[1], 'grid', 0.8)
    for j in range(int(y0), int(y1) + 1):
        a = f(x0, j)
        b = f(x1, j)
        s.line(a[0], a[1], b[0], b[1], 'grid', 0.8)
    ax = f(x0, 0) if y0 <= 0 <= y1 else f(x0, y0)
    ay = f(0, y0) if x0 <= 0 <= x1 else f(x0, y0)
    xe = f(x1, 0 if y0 <= 0 <= y1 else y0)
    ye = f(0 if x0 <= 0 <= x1 else x0, y1)
    s.line(ax[0], ax[1], xe[0] + 6, xe[1], 'ink', 1.8)
    s.line(ay[0], ay[1], ye[0], ye[1] - 6, 'ink', 1.8)
    s.poly([(xe[0] + 8, xe[1]), (xe[0] + 1, xe[1] - 3.5), (xe[0] + 1, xe[1] + 3.5)], fill='ink')
    s.poly([(ye[0], ye[1] - 8), (ye[0] - 3.5, ye[1] - 1), (ye[0] + 3.5, ye[1] - 1)], fill='ink')
    s.text(xe[0] + 12, xe[1] - 10, 'x', 11, c='muted')
    s.text(ye[0] + 11, ye[1] - 2, 'y', 11, c='muted')
    step = 1 if (x1 - x0) <= 14 else 2
    for i in range(int(x0), int(x1) + 1):
        if i != 0 and i % step == 0:
            q = f(i, 0 if y0 <= 0 <= y1 else y0)
            s.text(q[0], q[1] + 11, fnum(i), 9, c='muted')
    for j in range(int(y0), int(y1) + 1):
        if j != 0 and j % step == 0:
            q = f(0 if x0 <= 0 <= x1 else x0, j)
            s.text(q[0] - 9, q[1], fnum(j), 9, anchor='end', c='muted')
    for pg in shown(p.get('polygons', [])):
        s.poly([f(*q) for q in pg['pts']], fill=pg.get('fill'), c='accent2', sw=2)
    for ln in shown(p.get('lines', [])):
        a, b = f(*ln['from']), f(*ln['to'])
        s.line(a[0], a[1], b[0], b[1], 'accent2', 2, ln.get('dash'))
    for pt in shown(p.get('points', [])):
        q = f(float(pt['x']), float(pt['y']))
        s.circle(q[0], q[1], 4.5, fill='accent', c='ink', sw=1)
        if pt.get('label'):
            s.text(q[0] + 9, q[1] - 9, pt['label'], 13, bold=True, c='accent')
    return s.out()


def polygon(p):
    """Generic polygon from abstract vertex coordinates, with optional marks.
    pts [[x,y]..] counter-clockwise; names ['A',..]; sides [{i, text}] (side i = pts[i]->pts[i+1]);
    rightAt [i,..]; angles [{i, text}]; diagonals [[i,j]..]; fill role."""
    pts = [tuple(map(float, q)) for q in p['pts']]
    s = S(W, H)
    allp = list(pts)
    for ex in shown(p.get('extras', [])):
        allp += [tuple(map(float, q)) for q in ex['pts']]
    for sg in shown(p.get('segments', [])):
        allp += [tuple(map(float, sg['from'])), tuple(map(float, sg['to']))]
    fit = _fit_poly(allp)
    sc = [fit(*q) for q in pts]
    n = len(sc)
    cxm = sum(q[0] for q in sc) / n
    cym = sum(q[1] for q in sc) / n
    s.poly(sc, fill=p.get('fill', 'fill'), c='ink', sw=2.5)
    for ex in shown(p.get('extras', [])):
        s.poly([fit(*map(float, q)) for q in ex['pts']], fill=ex.get('fill'), c='accent2', sw=2)
    for sg in shown(p.get('segments', [])):
        a, b = fit(*map(float, sg['from'])), fit(*map(float, sg['to']))
        s.line(a[0], a[1], b[0], b[1], 'accent', 1.8, [5, 3])
        if sg.get('text'):
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            if abs(b[0] - a[0]) > abs(b[1] - a[1]):
                s.text(mx, my - 11, sg['text'], 12, bold=True, c='accent')
            else:
                s.text(mx + 8, my, sg['text'], 12, anchor='start', bold=True, c='accent')
    for d in p.get('diagonals', []):
        a, b = sc[d[0]], sc[d[1]]
        s.line(a[0], a[1], b[0], b[1], 'accent2', 1.8, [5, 3])
    for i in p.get('rightAt', []):
        _right_mark(s, sc[i], sc[(i + 1) % n], sc[(i - 1) % n])
    for g in shown(p.get('angles', [])):
        i = g['i']
        v = sc[i]
        dx, dy = cxm - v[0], cym - v[1]
        m = math.hypot(dx, dy) or 1
        s.text(v[0] + dx / m * 30, v[1] + dy / m * 30, g['text'], 11, c='accent', bold=True)
        a0 = math.degrees(math.atan2(-(sc[(i + 1) % n][1] - v[1]), sc[(i + 1) % n][0] - v[0]))
        a1 = math.degrees(math.atan2(-(sc[(i - 1) % n][1] - v[1]), sc[(i - 1) % n][0] - v[0]))
        while a1 < a0:
            a1 += 360
        if a1 - a0 > 180:
            a0, a1 = a1, a0 + 360
        s.arc(v[0], v[1], 14, a0, a1, 'accent', 1.8)
    for sd in shown(p.get('sides', [])):
        i = sd['i']
        a, b = sc[i], sc[(i + 1) % n]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = mx - cxm, my - cym
        m = math.hypot(dx, dy) or 1
        ux, uy = dx / m, dy / m
        anc = 'end' if ux < -0.35 else ('start' if ux > 0.35 else 'middle')
        s.text(mx + ux * 9 + (0 if anc == 'middle' else ux * 4), my + uy * 11, sd['text'], 12, anchor=anc, bold=True)
    for i, nm in enumerate(p.get('names', [])[:n]):
        v = sc[i]
        dx, dy = v[0] - cxm, v[1] - cym
        m = math.hypot(dx, dy) or 1
        s.text(v[0] + dx / m * 13, v[1] + dy / m * 13, nm, 13, bold=True)
    return s.out()


def triangle_angles(p):
    """Triangle built from its three angles (degrees, sum 180). labels: text per vertex angle (e.g. '?', '40°')."""
    A, B, C = (float(v) for v in p['angles'])
    sa, sb, sc_ = (math.sin(math.radians(v)) for v in (A, B, C))
    pts = [(0.0, 0.0), (sc_, 0.0), (sb * math.cos(math.radians(A)), sb * math.sin(math.radians(A)))]
    lab = p.get('labels', ['', '', ''])
    q = {'pts': pts, 'names': p.get('names', []), 'angles': [], 'rightAt': []}
    for i, deg in enumerate((A, B, C)):
        if abs(deg - 90) < 1e-6:
            q['rightAt'].append(i)
        if lab[i]:
            q['angles'].append({'i': i, 'text': lab[i]})
    q['sides'] = p.get('sides', [])
    return polygon(q)


def triangle_sides(p):
    """Triangle from its side lengths a (BC), b (CA), c (AB); labels: texts for [a, b, c] (default: the numbers)."""
    a, b, c = (float(v) for v in p['sides'])
    x = (b * b + c * c - a * a) / (2 * c)
    y = math.sqrt(max(b * b - x * x, 0.0))
    q = {'pts': [(0.0, 0.0), (c, 0.0), (x, y)], 'names': p.get('names', []), 'sides': []}
    lab = p.get('labels', [fnum(a), fnum(b), fnum(c)])
    for i, t in ((0, lab[2]), (1, lab[0]), (2, lab[1])):
        if t:
            q['sides'].append({'i': i, 'text': t})
    return polygon(q)



def angle_pair(p):
    """Two lines (or two parallel lines and a transversal) with the angles alpha / beta marked.
    kind: adjacent | vertical | corresponding | alternate;  alpha in degrees (0 < alpha < 180)"""
    s = S(W, H)
    kind, al = p['kind'], float(p['alpha'])
    if kind in ('corresponding', 'alternate'):
        al = min(max(al, 22.0), 158.0)          # illustration only: keeps the transversal inside the canvas
    lab = p.get('labels', {})
    t_a, t_b = lab.get('alpha', '\u03b1'), lab.get('beta', '\u03b2')

    def mark(cx, cy, d0, d1, text, role, r=26):
        s.arc(cx, cy, r, d0, d1, role, 2.2)
        x, y = pol(cx, cy, r + 14, (d0 + d1) / 2)
        s.text(x, y, text, 14, c=role, bold=True)
    if kind in ('adjacent', 'vertical'):
        cx, cy, L = 160, 100, 100
        s.line(cx - L, cy, cx + L, cy, 'ink', 2.5)
        x, y = pol(cx, cy, L, al)
        x2, y2 = pol(cx, cy, L, al + 180)
        s.line(x, y, x2, y2, 'ink', 2.5)
        mark(cx, cy, 0, al, t_a, 'accent')
        if kind == 'adjacent':
            mark(cx, cy, al, 180, t_b, 'accent2', 34)
        else:
            mark(cx, cy, 180, 180 + al, t_b, 'accent2')
        s.circle(cx, cy, 3, fill='ink')
        return s.out()
    y1, y2, cx = 78, 122, 160
    # transversal direction in screen coordinates: up-right at angle alpha
    dx, dy = math.cos(math.radians(al)), -math.sin(math.radians(al))
    shift = (y2 - y1) / dy * dx / 2
    p1 = (cx - shift, y1)                                   # transversal meets the upper line ...
    p2 = (cx + shift, y2)                                   # ... and the lower line
    s.line(30, y1, 290, y1, 'ink', 2.5)
    s.line(30, y2, 290, y2, 'ink', 2.5)
    t0 = (y1 - 30 - p1[1]) / dy
    t1 = (y2 + 30 - p1[1]) / dy
    s.line(p1[0] + dx * t0, p1[1] + dy * t0, p1[0] + dx * t1, p1[1] + dy * t1, 'accent2', 2.5)
    if kind == 'corresponding':
        mark(p1[0], p1[1], 0, al, t_a, 'accent')
        mark(p2[0], p2[1], 0, al, t_b, 'accent')
    else:
        mark(p1[0], p1[1], 180 + al, 360, t_a, 'accent')
        mark(p2[0], p2[1], al, 180, t_b, 'accent')
    return s.out()



def regular_polygon(p):
    n = int(p['n'])
    pts = [(math.cos(math.radians(90 + 360 * i / n)), math.sin(math.radians(90 + 360 * i / n))) for i in range(n)]
    q = dict(p)
    q['pts'] = pts
    return polygon(q)


def right_triangle(p):
    """Right angle at the origin; legs along the axes. a = horizontal leg, b = vertical leg (lengths for the
    drawing); labels {a, b, c} are texts (so a leg can show '?')."""
    a, b = float(p['a']), float(p['b'])
    a, b = min(max(a, b / 2.2), b * 2.2), min(max(b, a / 2.2), a * 2.2)     # illustration: keep the legs in a readable ratio
    q = {'pts': [[0, 0], [a, 0], [0, b]], 'rightAt': [0], 'sides': [], 'names': p.get('names', [])}
    lab = p.get('labels', {})
    if 'a' in lab:
        q['sides'].append({'i': 0, 'text': lab['a']})
    if 'c' in lab:
        q['sides'].append({'i': 1, 'text': lab['c']})
    if 'b' in lab:
        q['sides'].append({'i': 2, 'text': lab['b']})
    return polygon(q)


def circle_fig(p):
    s = S(W, H)
    cx, cy, R = 160, 100, 78
    s.circle(cx, cy, R, fill='fill', c='ink', sw=2.5)
    draw = p.get('draw', ['radius'])
    lab = p.get('labels', {})
    if 'diameter' in draw:
        s.line(cx - R, cy, cx + R, cy, 'accent', 2.5)
        if 'diameter' in lab:
            s.text(cx + 40, cy - 12, lab['diameter'], 13, bold=True, c='accent')
    if 'radius' in draw:
        x, y = pol(cx, cy, R, 35)
        s.line(cx, cy, x, y, 'accent2', 2.5)
        if 'radius' in lab:
            s.text((cx + x) / 2 + 6, (cy + y) / 2 - 12, lab['radius'], 13, bold=True, c='accent2')
    if 'chord' in draw:
        x0, y0 = pol(cx, cy, R, 215)
        x1, y1 = pol(cx, cy, R, 325)
        s.line(x0, y0, x1, y1, 'accent', 2.5)
        if 'chord' in lab:
            s.text(cx, y0 + 14, lab['chord'], 13, bold=True, c='accent')
    s.circle(cx, cy, 3.5, fill='ink')
    if 'center' in lab:
        s.text(cx - 12, cy + 12, lab['center'], 13, bold=True)
    return s.out()


def cuboid(p):
    a, b, c = float(p['a']), float(p['b']), float(p['c'])
    s = S(W, H)
    dx, dy = 0.5 * b * math.cos(math.radians(35)), 0.5 * b * math.sin(math.radians(35))
    xs = [0, a, a + dx, dx]
    ys = [0, 0, dy, dy, c, c + dy]
    fit = Fit(xs, ys, (64, 30, 280, 172))
    P = lambda x, y: fit(x, y)
    f0, f1, f2, f3 = P(0, 0), P(a, 0), P(a, c), P(0, c)
    b0, b1, b2, b3 = P(dx, dy), P(a + dx, dy), P(a + dx, c + dy), P(dx, c + dy)
    s.poly([f0, f1, f2, f3], fill='fill', c='ink', sw=2.5)
    s.poly([f3, f2, b2, b3], fill='fill2', c='ink', sw=2.5)
    s.poly([f1, b1, b2, f2], fill='fill2', c='ink', sw=2.5)
    for u, v in ((f0, b0), (b0, b1), (b0, b3)):
        s.line(u[0], u[1], v[0], v[1], 'muted', 1.4, [4, 3])
    lab = p.get('labels', {})
    if 'a' in lab:
        s.text((f0[0] + f1[0]) / 2, f0[1] + 14, lab['a'], 13, bold=True)
    if 'b' in lab:
        s.text((f1[0] + b1[0]) / 2 + 14, (f1[1] + b1[1]) / 2 + 6, lab['b'], 13, bold=True)
    if 'c' in lab:
        s.text(f0[0] - 8, (f0[1] + f3[1]) / 2, lab['c'], 13, anchor='end', bold=True)
    return s.out()


def solid(p):
    """prism / pyramid with a regular n-gon base seen from above-front. labels: h (height), s (slant height),
    e (base edge), x (lateral edge); show: ['height','slant'] to draw those segments."""
    kind, n = p['kind'], int(p.get('n', 4))
    s = S(W, 220)
    cx, rx, ry = 160, 70, 22
    by, hgt = 168, 110 if kind == 'prism' else 130

    def base(y):
        return [(cx + rx * math.cos(math.radians(270 - 360 * i / n)), y + ry * math.sin(math.radians(270 - 360 * i / n)) * -1)
                for i in range(n)]
    bot = base(by)
    # front = vertices on or in front of the centre line (their lateral edges are visible)
    front = [i for i, q in enumerate(bot) if q[1] > by - 1e-6]
    strict = lambda i: bot[i][1] > by + 1e-6

    def edge_visible(i):
        j = (i + 1) % n
        return strict(i) or strict(j)
    top = [(q[0], q[1] - hgt) for q in bot] if kind == 'prism' else None
    apex = (cx, by - hgt)
    if kind == 'prism':
        s.poly(top, fill='fill2', c='ink', sw=2.2)
        for i in range(n):
            j = (i + 1) % n
            vis = edge_visible(i)
            s.line(bot[i][0], bot[i][1], bot[j][0], bot[j][1], 'ink' if vis else 'muted', 2.2 if vis else 1.3, None if vis else [4, 3])
        for i in range(n):
            vis = i in front
            s.line(bot[i][0], bot[i][1], top[i][0], top[i][1], 'ink' if vis else 'muted', 2.2 if vis else 1.3, None if vis else [4, 3])
        s.poly(top, fill=None, c='ink', sw=2.2)
    else:
        for i in range(n):
            j = (i + 1) % n
            vis = edge_visible(i)
            s.line(bot[i][0], bot[i][1], bot[j][0], bot[j][1], 'ink' if vis else 'muted', 2.2 if vis else 1.3, None if vis else [4, 3])
        for i in range(n):
            vis = i in front
            s.line(bot[i][0], bot[i][1], apex[0], apex[1], 'ink' if vis else 'muted', 2.2 if vis else 1.3, None if vis else [4, 3])
    lab = p.get('labels', {})
    show = p.get('show', [])
    ctr = (cx, by)
    if 'height' in show:
        top_pt = apex if kind == 'pyramid' else (cx, by - hgt)
        s.line(ctr[0], ctr[1], top_pt[0], top_pt[1], 'accent', 2.2, [5, 3])
        s.circle(ctr[0], ctr[1], 2.5, fill='accent')
        if 'h' in lab:
            s.text(cx + 12, by - hgt / 2, lab['h'], 13, anchor='start', bold=True, c='accent')
    if 'slant' in show and kind == 'pyramid':
        i = front[len(front) // 2]
        j = (i + 1) % n
        mid = ((bot[i][0] + bot[j][0]) / 2, (bot[i][1] + bot[j][1]) / 2)
        s.line(apex[0], apex[1], mid[0], mid[1], 'accent2', 2.2, [5, 3])
        s.circle(mid[0], mid[1], 2.5, fill='accent2')
        if 's' in lab:
            s.text((apex[0] + mid[0]) / 2 - 12, (apex[1] + mid[1]) / 2 + 8, lab['s'], 13, anchor='end', bold=True, c='accent2')
    if 'e' in lab:
        i = front[0]
        j = (i + 1) % n
        s.text((bot[i][0] + bot[j][0]) / 2, (bot[i][1] + bot[j][1]) / 2 + 15, lab['e'], 13, bold=True)
    return s.out()


def net(p):
    """net of a cuboid a x b x c: cross shape (bottom a x b in the middle)"""
    a, b, c = float(p['a']), float(p['b']), float(p['c'])
    s = S(W, 220)
    # layout: row of 4 (c, a, c, a) with the b-sized strip above and below the second
    w_units = c + a + c + a
    h_units = b + c + b
    fit = Fit([0, w_units], [0, h_units], (14, 14, 306, 206))
    def R(x, y, w, h, role='fill'):
        p0 = fit(x, y + h)
        p1 = fit(x + w, y)
        s.rect(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], fill=role, c='ink', sw=1.8)
    R(c, 0, a, b)                   # top flap
    R(0, b, c, c, 'fill2')          # left side
    R(c, b, a, c)                   # bottom face (middle)
    R(c + a, b, c, c, 'fill2')      # right side
    R(c + a + c, b, a, c)           # back
    R(c, b + c, a, b)               # lower flap
    lab = p.get('labels', {})
    if 'a' in lab:
        q = fit(c + a / 2, b + c / 2)
        s.text(q[0], q[1], lab['a'], 11, bold=True)
    return s.out()


def arch(p):
    """Rectangle w x h topped with a semicircle of diameter w (window, gate).  labels{w,h,r}."""
    w, h = float(p['w']), float(p['h'])
    s = S(W, H)
    fit = Fit([0, w], [0, h + w / 2], (70, 14, 250, 176))
    x0, y0 = fit(0, 0)
    x1, y1 = fit(w, h)
    cx, cy = fit(w / 2, h)
    rr = (x1 - x0) / 2
    pts = [(x0, y0), (x1, y0), (x1, y1)] + [pol(cx, cy, rr, a) for a in range(0, 181, 6)] + [(x0, y1)]
    s.poly(pts, fill='fill', c='ink', sw=2.5)
    s.line(x0, y1, x1, y1, 'muted', 1.4, [4, 3])
    lab = p.get('labels', {})
    if 'w' in lab:
        s.text(cx, y0 + 14, lab['w'], 13, bold=True)
    if 'h' in lab:
        s.text(x0 - 8, (y0 + y1) / 2, lab['h'], 13, anchor='end', bold=True)
    if 'r' in lab:
        s.line(cx, cy, cx + rr * 0.7, cy - rr * 0.7, 'accent', 2)
        s.text(cx + rr * 0.45, cy - rr * 0.75, lab['r'], 12, bold=True, c='accent')
    return s.out()



def grid_shape(p):
    cols, rows = int(p['cols']), int(p['rows'])
    s = S(W, H)
    cell = min(280 / cols, 170 / rows)
    x0 = (W - cell * cols) / 2
    y0 = (H - cell * rows) / 2
    for (c, r) in p.get('cells', []):
        s.rect(x0 + c * cell, y0 + (rows - 1 - r) * cell, cell, cell, fill='accent')
    for i in range(cols + 1):
        s.line(x0 + i * cell, y0, x0 + i * cell, y0 + rows * cell, 'grid', 1)
    for j in range(rows + 1):
        s.line(x0, y0 + j * cell, x0 + cols * cell, y0 + j * cell, 'grid', 1)
    if 'poly' in p:
        s.poly([(x0 + x * cell, y0 + (rows - y) * cell) for x, y in p['poly']], fill=p.get('fill'), c='ink', sw=2.5)
    ax = p.get('axis')
    if ax:
        if ax['type'] == 'v':
            x = x0 + ax['at'] * cell
            s.line(x, y0 - 6, x, y0 + rows * cell + 6, 'accent2', 2.2, [6, 3])
        elif ax['type'] == 'h':
            y = y0 + (rows - ax['at']) * cell
            s.line(x0 - 6, y, x0 + cols * cell + 6, y, 'accent2', 2.2, [6, 3])
    return s.out()


def balance(p):
    """scale: left / right = list of item texts"""
    s = S(W, 170)
    cx, top = 160, 150
    s.poly([(cx - 30, 160), (cx + 30, 160), (cx, 58)], fill='fill2', c='ink', sw=2)
    s.line(cx - 110, 58, cx + 110, 58, 'ink', 3)
    for side, items in ((-1, p.get('left', [])), (1, p.get('right', []))):
        x = cx + side * 110
        s.line(x, 58, x - 40, 100, 'muted', 1.4)
        s.line(x, 58, x + 40, 100, 'muted', 1.4)
        s.poly([(x - 48, 100), (x + 48, 100), (x + 38, 112), (x - 38, 112)], fill='accent2', c='ink', sw=1.8)
        n = max(len(items), 1)
        for i, t in enumerate(items):
            bw = min(40, 90 / n)
            bx = x - 45 + (i + 0.5) * 90 / n
            s.rect(bx - bw / 2, 100 - 24, bw, 22, fill='accent', c='ink', sw=1.2)
            s.text(bx, 87, t, 11, bold=True)
    return s.out()


# ---------------------------------------------------------------------------------------------- charts
def bar(p):
    labels, values = p['labels'], [float(v) for v in p['values']]
    s = S(W, 230)
    top = 30 if p.get('title') else 14
    if p.get('title'):
        s.text(160, 12, p['title'], 12, bold=True)
    base = float(p.get('yMin', 0))
    mx = max(values) - base
    step = 1 if mx <= 10 else (2 if mx <= 20 else (5 if mx <= 50 else (10 if mx <= 100 else (50 if mx <= 500 else 100))))
    ymax = math.ceil(mx / step) * step
    x0, x1, y0, y1 = 40, 306, 190, top + 6
    k = (y0 - y1) / ymax
    for t in range(0, int(ymax) + 1, step):
        y = y0 - t * k
        s.line(x0, y, x1, y, 'grid', 0.8)
        s.text(x0 - 5, y, fnum(base + t), 10, anchor='end', c='muted')
    s.line(x0, y0, x0, y1 - 4, 'ink', 1.8)
    s.line(x0, y0, x1, y0, 'ink', 1.8)
    n = len(values)
    bw = (x1 - x0) / n
    for i, v in enumerate(values):
        h = (v - base) * k
        s.rect(x0 + i * bw + bw * 0.18, y0 - h, bw * 0.64, h, fill='accent', c='ink', sw=1.2)
        s.text(x0 + (i + 0.5) * bw, y0 + 13, labels[i], 10 if n <= 6 else 8)
    return s.out()


def line_chart(p):
    xs, ys = [float(v) for v in p['x']], [float(v) for v in p['y']]
    s = S(W, 230)
    top = 30 if p.get('title') else 14
    if p.get('title'):
        s.text(160, 12, p['title'], 12, bold=True)
    x0, x1, y0, y1 = 44, 304, 186, top + 6
    lo = float(p['yMin']) if 'yMin' in p else min(0.0, min(ys))
    hi = max(ys)
    span = hi - lo
    step = next(t for t in (1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 5000) if span / t <= 8)
    ylo = math.floor(lo / step) * step
    yhi = math.ceil(hi / step) * step
    ky = (y0 - y1) / (yhi - ylo)
    kx = (x1 - x0 - 16) / (xs[-1] - xs[0]) if xs[-1] != xs[0] else 1
    t = ylo
    while t <= yhi + 1e-9:
        y = y0 - (t - ylo) * ky
        s.line(x0, y, x1, y, 'grid', 0.8)
        s.text(x0 - 5, y, fnum(t), 10, anchor='end', c='muted')
        t += step
    s.line(x0, y0, x0, y1 - 4, 'ink', 1.8)
    s.line(x0, y0, x1, y0, 'ink', 1.8)
    pts = [(x0 + 8 + (x - xs[0]) * kx, y0 - (y - ylo) * ky) for x, y in zip(xs, ys)]
    s.poly(pts, c='accent', sw=2.5, close=False)
    for (px, py), x in zip(pts, xs):
        s.circle(px, py, 3.5, fill='accent', c='ink', sw=1)
        s.line(px, y0, px, y0 + 4, 'ink', 1)
        s.text(px, y0 + 13, fnum(x), 10)
    if p.get('xLabel'):
        s.text(x1, y0 + 26, p['xLabel'], 10, anchor='end', c='muted')
    if p.get('yLabel'):
        s.text(x0 + 4, y1 - 8, p['yLabel'], 10, anchor='start', c='muted')
    return s.out()


def pie(p):
    labels, values = p['labels'], [float(v) for v in p['values']]
    s = S(W, 200)
    cx, cy, R = 100, 100, 80
    tot = sum(values)
    roles = ['accent', 'accent2', 'good', 'bad', 'fill2', 'muted']
    a = 90.0
    for i, v in enumerate(values):
        sweep = 360 * v / tot
        pts = [(cx, cy)] + [pol(cx, cy, R, a - t * sweep / 24) for t in range(25)]
        s.poly(pts, fill=roles[i % len(roles)], c='ink', sw=1.5)
        a -= sweep
    for i, lb in enumerate(labels):
        y = 40 + i * 24
        s.rect(210, y - 8, 14, 14, fill=roles[i % len(roles)], c='ink', sw=1)
        txt = lb + (f" ({fnum(values[i])})" if p.get('showValues') else '')
        s.text(230, y, txt, 12, anchor='start')
    return s.out()


def pictogram(p):
    labels, counts = p['labels'], [int(v) for v in p['counts']]
    per = int(p.get('per', 1))
    s = S(W, 20 + 30 * len(labels))
    for i, (lb, n) in enumerate(zip(labels, counts)):
        y = 22 + 30 * i
        s.text(10, y, lb, 12, anchor='start')
        for j in range(n):
            s.circle(110 + j * 22, y, 8, fill='accent', c='ink', sw=1)
    s.text(W - 10, 12, f"● = {per}", 11, anchor='end', c='muted')
    return s.out()


def table(p):
    headers, rows = p.get('headers', []), p['rows']
    ncol = len(headers) if headers else len(rows[0])
    allr = ([headers] if headers else []) + [[str(c) for c in r] for r in rows]
    widths = [max(len(str(r[i])) for r in allr) * 7 + 18 for i in range(ncol)]
    tw = sum(widths)
    rh = 26
    s = S(max(tw + 4, 120), rh * len(allr) + 4)
    y = 2
    for ri, r in enumerate(allr):
        x = 2
        for ci, c in enumerate(r):
            head = bool(headers) and ri == 0
            s.rect(x, y, widths[ci], rh, fill='fill2' if head else 'fill', c='ink', sw=1.2)
            s.text(x + widths[ci] / 2, y + rh / 2, c, 12, bold=head)
            x += widths[ci]
        y += rh
    return s.out()


KINDS = {
    ('figure', 'clock'): clock, ('figure', 'number-line'): number_line, ('figure', 'fraction-bar'): fraction_bar,
    ('figure', 'angle'): angle, ('figure', 'protractor'): protractor, ('figure', 'ruler'): ruler,
    ('figure', 'thermometer'): thermometer, ('figure', 'rect'): rect_fig, ('figure', 'triangle'): triangle,
    ('figure', 'coordinate-plane'): coordinate_plane, ('figure', 'polygon'): polygon,
    ('figure', 'regular-polygon'): regular_polygon, ('figure', 'triangle-angles'): triangle_angles, ('figure', 'triangle-sides'): triangle_sides, ('figure', 'angle-pair'): angle_pair, ('figure', 'right-triangle'): right_triangle,
    ('figure', 'circle'): circle_fig, ('figure', 'cuboid'): cuboid, ('figure', 'solid'): solid,
    ('figure', 'net'): net, ('figure', 'grid-shape'): grid_shape, ('figure', 'balance'): balance, ('figure', 'arch'): arch,
    ('chart', 'bar'): bar, ('chart', 'line'): line_chart, ('chart', 'pie'): pie, ('chart', 'pictogram'): pictogram,
    ('table', 'table'): table,
}


def scene(m):
    """media item (compiled) -> scene dict"""
    fn = KINDS.get((m['type'], m['kind']))
    if fn is None:
        raise KeyError(f"no renderer for {m['type']}/{m['kind']}")
    return fn(m.get('params', {}))


def problems(sc):
    """Sanity check of a scene: everything must lie inside the canvas (small tolerance) and no number may be NaN."""
    out, w, h = [], sc['w'], sc['h']

    def bad(x, y):
        return not (-4 <= x <= w + 4 and -4 <= y <= h + 4) or x != x or y != y
    for it in sc['items']:
        t = it['t']
        if t == 'line' and (bad(it['x1'], it['y1']) or bad(it['x2'], it['y2'])):
            out.append(f"line outside canvas: {it}")
        elif t == 'rect' and (bad(it['x'], it['y']) or bad(it['x'] + it['w'], it['y'] + it['h'])):
            out.append(f"rect outside canvas: {it}")
        elif t == 'circle' and bad(it['cx'], it['cy']):
            out.append(f"circle outside canvas: {it}")
        elif t == 'poly' and any(bad(x, y) for x, y in it['pts']):
            out.append('poly outside canvas')
        elif t == 'text':
            half = len(it['s']) * it['size'] * 0.3
            lo = it['x'] - (half if it['anchor'] == 'middle' else (0 if it['anchor'] == 'start' else 2 * half))
            hi = it['x'] + (half if it['anchor'] == 'middle' else (2 * half if it['anchor'] == 'start' else 0))
            if bad(it['x'], it['y']) or lo < -4 or hi > w + 4:
                out.append(f"text outside canvas: {it['s']!r}")
    return out


# ---------------------------------------------------------------------------------------------- SVG
THEME = {'ink': '#1f2933', 'muted': '#7b8794', 'grid': '#d9e2ec', 'accent': '#e8590c', 'accent2': '#1c7ed6',
         'fill': '#fff9db', 'fill2': '#e7f5ff', 'good': '#2f9e44', 'bad': '#e03131', 'bg': '#ffffff'}


def _c(role, theme):
    return theme.get(role, role)


def to_svg(sc, theme=THEME, scale=2):
    from xml.sax.saxutils import escape
    w, h = sc['w'], sc['h']
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * scale}" height="{h * scale}" viewBox="0 0 {w} {h}" font-family="DejaVu Sans, sans-serif">',
           f'<rect width="{w}" height="{h}" fill="{theme["bg"]}"/>']
    for it in sc['items']:
        t = it['t']
        st = ''
        if 'fill' in it or t in ('rect', 'circle', 'poly'):
            st += f' fill="{_c(it["fill"], theme) if "fill" in it else "none"}"'
        if it.get('c') and t != 'text':
            st += f' stroke="{_c(it["c"], theme)}" stroke-width="{it.get("sw", it.get("w", 1.5))}" stroke-linejoin="round" stroke-linecap="round"'
        if t == 'line':
            d = f' stroke-dasharray="{" ".join(map(str, it["dash"]))}"' if it.get('dash') else ''
            out.append(f'<line x1="{it["x1"]}" y1="{it["y1"]}" x2="{it["x2"]}" y2="{it["y2"]}"{st}{d}/>')
        elif t == 'rect':
            out.append(f'<rect x="{it["x"]}" y="{it["y"]}" width="{it["w"]}" height="{it["h"]}"{st}/>')
        elif t == 'circle':
            out.append(f'<circle cx="{it["cx"]}" cy="{it["cy"]}" r="{it["r"]}"{st}/>')
        elif t == 'poly':
            pts = ' '.join(f'{x},{y}' for x, y in it['pts'])
            tag = 'polygon' if it.get('close', True) else 'polyline'
            out.append(f'<{tag} points="{pts}"{st}/>')
        elif t == 'arc':
            x0, y0 = pol(it['cx'], it['cy'], it['r'], it['a0'])
            x1, y1 = pol(it['cx'], it['cy'], it['r'], it['a1'])
            large = 1 if (it['a1'] - it['a0']) % 360 > 180 else 0
            out.append(f'<path d="M {x0:.2f} {y0:.2f} A {it["r"]} {it["r"]} 0 {large} 0 {x1:.2f} {y1:.2f}" fill="none"{st}/>')
        elif t == 'text':
            anc = {'start': 'start', 'middle': 'middle', 'end': 'end'}[it['anchor']]
            wt = ' font-weight="bold"' if it.get('bold') else ''
            out.append(f'<text x="{it["x"]}" y="{it["y"]}" font-size="{it["size"]}" text-anchor="{anc}" dominant-baseline="central" fill="{_c(it["c"], theme)}"{wt}>{escape(it["s"])}</text>')
    out.append('</svg>')
    return '\n'.join(out)
