# Task media — figures, charts, tables (v1.0)

A task may carry `media[]`: drawings that illustrate or define the problem. The pack contains **data only**; the app turns each media item into a *scene* (a flat list of drawing primitives) with a built-in renderer and draws it on a canvas. Reference implementation: `tools/render.py` (Python, + SVG export for previews); the engine port `cognio-render/` produces identical scenes (`tests/conformance/scenes.json`, 375 cases, checked by `cognio-render/src/test/kotlin/Conformance.kt`) and `cognio-render/compose/SceneCanvas.kt` draws them with Jetpack Compose.

```jsonc
"media": [{ "type": "figure", "kind": "right-triangle", "essential": false,
            "alt": "Trójkąt prostokątny; znak zapytania oznacza szukany bok.",
            "params": { "a": 24, "b": 7, "labels": { "a": "24 cm", "b": "7 cm", "c": "?" } } }]
```

* `essential: true` — the task cannot be solved without the picture; if the renderer is missing or fails, skip the task. `false` — the prompt alone is enough; on failure show `alt`.
* `alt` — text for screen readers and fallback. It must never reveal the answer.
* In *generator templates* params are expressions (`{"$expr": "a"}`), strings may contain `@{…}`, and an item may have `"when": "<expr>"` (attach only if true). Inside list entries `"show": <expr>` hides one entry (point, polygon, side label…). A compiled task has concrete values only.
* Numbers may be numbers or exact decimal strings. A label `"?"` marks the unknown; a figure never shows the answer.
* Figures are **illustrations**: shapes are drawn proportionally where the data allow it, but lengths are clamped to a readable ratio and angle drawings are normalised (the task text, not the ruler, defines the values).

## Scene format

`{"w": 320, "h": 200, "items": [...]}`; y grows downwards; numbers rounded to 2 places. Items:

| `t` | fields |
|---|---|
| `line` | `x1 y1 x2 y2 c w dash?` |
| `rect` | `x y w h fill? c? sw?` |
| `circle` | `cx cy r fill? c? sw?` |
| `arc` | `cx cy r a0 a1 c sw` — degrees, counter-clockwise from +x, drawn from `a0` to `a1` |
| `poly` | `pts [[x,y]…] close fill? c? sw?` |
| `text` | `x y s size anchor(start|middle|end) c bold?` — (x, y) = anchor point, vertically centred |

Colours are roles (`ink muted grid accent accent2 fill fill2 good bad bg`); the theme maps them to real colours, so figures follow the app's look and dark mode. Texts use the Polish decimal comma and U+2212 for minus.

## Figure kinds (`type: "figure"`)

| kind | params |
|---|---|
| `clock` | `hour minute` |
| `number-line` | `min max tick labelEvery? points[{label, at}]`; or `partsPerUnit` (ticks every 1/d, integers labelled); `at` = number or `{num, den}` |
| `fraction-bar` | `parts shaded` (more shaded than parts → several bars) |
| `angle` | `degrees startDeg? labels?[vertex, ray1, ray2]` (90° gets a square mark) |
| `protractor` | `degrees mirrored` — base arm on the 0 of the outer scale |
| `ruler` | `startMm lengthMm unit` — an object lies on the ruler from `startMm` |
| `thermometer` | `value min max` |
| `rect` | `w h unit` (a square is labelled once) |
| `triangle` | `A B C` (model coordinates), `feet[{label, x}]` (dashed altitudes onto the base line), `baseLabel?`, `names?` |
| `triangle-angles` | `angles[A,B,C]` (sum 180), `labels[tA,tB,tC]` (e.g. `"?"`, `"40°"`), `names?`, `sides?` |
| `triangle-sides` | `sides[a,b,c]` (must form a triangle), `labels?[ta,tb,tc]`, `names?` |
| `right-triangle` | `a b` (leg proportions), `labels{a,b,c}` (texts), `names?` |
| `polygon` | `pts[[x,y]…]` (counter-clockwise, model coords), `names?`, `sides[{i,text}]` (side *i* = pts[i]→pts[i+1]), `angles[{i,text}]`, `rightAt[i…]`, `diagonals[[i,j]…]`, `segments[{from,to,text}]` (dashed, e.g. heights), `extras[{pts,fill}]` (additional polygons) |
| `regular-polygon` | `n` + the `polygon` marks |
| `circle` | `draw[radius|diameter|chord…]`, `labels{radius,diameter,chord,center}` |
| `arch` | `w h`, `labels{w,h,r}` — rectangle topped with a semicircle (window, gate) |
| `cuboid` | `a b c` (proportions), `labels{a,b,c}` — oblique projection, hidden edges dashed |
| `solid` | `kind: prism|pyramid`, `n` (base polygon, 3–8), `show[height|slant]`, `labels{h,s,e}` |
| `net` | `a b c`, `labels{a}` — net of a cuboid |
| `grid-shape` | `cols rows cells[[c,r]…]`, `poly[[x,y]…]`, `axis{type: v|h, at}` |
| `coordinate-plane` | `xMin xMax yMin yMax` (or `min max`), `points[{label,x,y}]`, `polygons[{pts,fill?}]`, `lines[{from,to,dash?}]` |
| `balance` | `left[texts] right[texts]` |

## Charts and tables

| type / kind | params |
|---|---|
| `chart` / `bar` | `labels values title? yMin?` (`yMin` = where the value axis starts; a non-zero start exaggerates differences — used on purpose in the "misleading chart" quest) |
| `chart` / `line` | `x y xLabel? yLabel? title? yMin?` |
| `chart` / `pie` | `labels values showValues?` |
| `chart` / `pictogram` | `labels counts per?` |
| `table` / `table` | `headers? rows` |

## Quality gates

`cognio.py lint` renders the media of every generated task (200 seeds per level) and fails when a kind is unknown, a parameter is malformed, or something is drawn outside the canvas. Visual review: `python3 -I tools/gallery.py courses/pl-primary-math gallery.html` renders every media-bearing skill to an HTML contact sheet.
