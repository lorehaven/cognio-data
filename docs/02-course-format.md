# Course pack format — v1.0

**Purpose.** All learning content lives in a *course pack* — a **`.cognio` file** (a zip; a plain folder works too during authoring) of JSON/JSONL files. The app contains **no course content and no course-specific code**; it loads packs, interprets them, and runs sessions. Packs can be side-loaded now and downloaded from a server later without changing the app.

**Status:** draft v1.0, with a working reference implementation (`tools/cognio.py`), JSON Schemas (`schemas/`), a first sample course (`courses/pl-primary-math/`) and conformance vectors (`tests/conformance/vectors.json`).

## 1. Hierarchy

```
Course                      pl-primary-math                      (course.json)
 └─ Stage                   I–III · IV–VI · VII–VIII             (official stages; NOT school years)
     └─ Area (dział)        Liczby · Miary · Algebra · Figury …  (curriculum.json, official)
         └─ Objective       IV-VI.1.19  "skraca i rozszerza…"    (curriculum.json, verbatim from the regulation)
             └─ Skill       frac-simplify  = one class of problems the child trains   (skills/<stage>/<id>.json)
                 └─ Level   1, 2, …  (difficulty steps respecting the regulation's caps)
                     └─ Task source:  generator | bank | llm      (how tasks for this skill come into existence)
                         └─ Task      the compiled unit rendered by the app (task.schema.json)
```

* **Curriculum layer** (what the law says) is separate from the **skill layer** (how we train it). One objective can have several skills (different problem types); one skill can serve several objectives. Coverage is measurable (`cognio.py coverage`).
* The curriculum for the Polish course is **generated from the regulation text** (`tools/parse_regulation.py`, `tools/build_curriculum.py`) so it stays verbatim: 176 objectives (I–III: 43, IV–VI: 86, VII–VIII: 47). Human-readable copy: `docs/curriculum/stage-*.md`.
* A *course* is language/country specific, but the format is not: another course (e.g. English vocabulary, programming) only needs another `curriculum.json` (any stage/area structure with objective ids) plus skills and task kinds the app supports.

## 2. Pack layout

```
pl-primary-math/
  course.json                 manifest (id, version, engine requirements, stage → skill list, file hashes)
  curriculum.json             official structure: stages → areas → objectives (→ parts)
  skills/<stage>/<skill-id>.json
  generators/<generator-id>.json     declarative, deterministic task generators (pure data)
  banks/<name>.jsonl                 pre-made tasks, one JSON object per line
  paths/<stage>.json                 the learning path of a stage: units → lessons + unlock rules (§2.3)
  quests/<id>.json                   story-driven multi-step activities (§3.1)
  authoring/<spec-id>.llm.json       instructions for a model that WRITES tasks (not shipped to phones by default)
  assets/…                           images/figures referenced by tasks (optional)
```

Schemas: `schemas/{common,course,skill,generator,task,llm-spec,path,quest,model-catalog}.schema.json` (JSON Schema 2020-12).

### 2.1 `course.json` (manifest)
`formatVersion` (major = breaking; the app refuses unknown majors), `id`, `version` (semver), `language`, `title`, `engine.min` + `engine.features` (task kinds etc. the pack needs — the app can say "update the app"), `curriculum`, `stages[].skills[]`, `files[]` (path, sha256, size), optional `replaces[]` (skill renames) and `signature` (ed25519, reserved for server distribution).

### 2.2 `skills/*.json`
`id` (stable slug), `stage`, `area`, `title`/`description` (localized), `objectives[]` (ids from `curriculum.json`), `prerequisites[]`, `tags` (`finance`, `thinking`, `no-calculator`…), `order` (soft hint), `levels[]` (label + which regulation cap it respects), `taskSources[]`, `tutor` (intro, key ideas, common errors — grounding for hints and for the optional LLM).

**Ordering inside a stage.** The regulation fixes no order, and we don't know her school's. The engine orders by `prerequisites` + learner state + `order`; a parent can pick a *focus area* or pin skills. Never hard-code "grade 4 = these skills".

### 2.3 `paths/<stage>.json` — the Duolingo-style path

The *curriculum* says what must be learnt; the *path* says in which order the learner walks through it. One file per stage; every stage has `"entry": "open"`, i.e. **its first lesson is unlocked from the very start** — a learner never has to finish I–III to begin IV–VI.

* `units[]`: a themed group (icon, title, optional `area`), each with `lessons[]` and an optional `testOut` (a Duolingo-style jump-ahead test: passing it completes the whole unit).
* Lesson `kind`: `learn` (a new skill; the app first shows the skill's `tutor.intro`, which lint requires for every `learn` lesson), `practice`, `review` (mix of earlier skills), `checkpoint` (end-of-unit test, `passRatio` 0.8), `quest` (a story-driven multi-step activity, §3.1).
* A lesson draws its tasks from one `skill` (+ `levels` = "crowns": level 1 completes the lesson, higher levels are optional replays) or from a `mix` of `{skill, level, weight}`.
* **Unlocking:** by default a lesson unlocks when the previous lesson of the path is complete; `requires[]` overrides this. Units unlock their first lesson when the previous unit's `checkpoint` is passed (or via `testOut`).
* Lint guarantees: every skill of the course appears in some lesson, every lesson references existing skills and levels, every `learn` lesson has an intro, and **the sources can supply the lesson without repeating a task**: a bank must hold at least `tasks` tasks, a generator level must yield at least `2 × tasks` distinct tasks (and ≥ 8 in any case). `cognio.py fit` lowers `tasks` of lessons whose skill has a naturally small task space (e.g. the 100 facts of the multiplication table); the build runs it automatically.

Current Polish course: I–III 11 units / 88 lessons, IV–VI 30 / 231, VII–VIII 17 / 100 (the last unit of IV–VI and VII–VIII holds the quests).

## 3. Task sources — three ways to get tasks

| Type | What it is | When to use | Runs on device? |
|---|---|---|---|
| `generator` | Declarative template: random parameters (seeded) → prompt, exact answer, steps, buggy rules | Anything computational: arithmetic, fractions, units, perimeter, equations… | Yes (tiny interpreter, no model) |
| `bank` | JSONL of finished tasks | Hand-written or model-written tasks that can't be parameterised: find-the-mistake, reasoning puzzles, word problems with stories, figure-based tasks | Yes |
| `llm` | Instructions + verifier for a model that writes tasks | Producing **large, varied banks** of word problems, stories, puzzles | **Authoring-time on a PC** (default); device mode is optional/restricted |

A fourth source type, `quest`, is described in §3.1.

A skill may combine sources with `weight`s (e.g. 2 parts generator, 1 part LLM-written bank). Everything the child sees is a compiled **task**, so UI, checker, adaptive engine and tutor don't care where it came from (`provenance` records it).

> **Cheap-device decision.** Tasks are *not* generated by a language model on the phone. Banks are produced offline by a strong model, **verified by deterministic code**, and shipped as data. The phone model (if any) is limited to optional phrasing of hints. This keeps correctness at 100 %, speed instant, and RAM small.

### 3.1 Quests (`quests/<id>.json`, `quest.schema.json`)
A *quest* realises one of the regulation's "doświadczenia edukacyjne" (practical experiences): a short story with 4–10 ordinary tasks answered one after another, e.g. "class-trip budget", "plan of the classroom in a scale", "which deposit is better?", "the same chart, two stories". The quest's random variables are drawn **once** and shared by every step, so later steps can build on earlier results; each step is a normal task template (any kind, own answer, hints, error rules, media). `intro`/`outro` are templates; `media` at quest level (e.g. an offers table) stays visible during the steps; `experience` points at `stages[].experiences[]` of `curriculum.json`.

A quest doubles as a skill (id = quest id, one level, source `{"type":"quest","ref":"quests/<id>.json"}`), so a path lists it as a lesson of kind `quest`. The reference interpreter: `generate_quest(quest, skill, seed)`; `cognio.py quest <pack> <id> [seed]` prints an instance. Lint draws 100 seeds, checks every step like any task (answers, options, media rendering, no unresolved templates) and requires ≥ 20 distinct instances. The sample course has 9 quests: 4 for IV–VI (water usage data, trip budget, room plan in a scale, school garden) and 5 for VII–VIII (arched window, deposits, a take-away game, misleading charts, bike ramp).

## 4. The compiled task (`task.schema.json`)

Key fields: `id`, `skill`, `level`, `kind`, `prompt` (Polish, math markup §5), `media[]`, `input` (kind-specific config), `options[]` (choice kinds), **`answer`** (typed value), `equivalent[]` (right value but softer verdict), **`errorRules[]`** (answer a child gives when applying a wrong procedure + feedback), **`steps[]`** (structured worked solution = grounding for hints/LLM), `estimatedSeconds`, `tags`, `provenance`.

### 4.1 Task kinds
| Kind | Input | Status in v1 |
|---|---|---|
| `number-input`, `decimal-input`, `fraction-input`, `mixed-number-input`, `quantity-input` (value + unit) | keypad / fraction widget | **MVP** |
| `multiple-choice`, `multi-select`, `order-items`, `find-the-mistake`, `word-problem` (stepped) | taps / drag | **MVP** |
| `number-line-tap`, `column-arithmetic`, `matching`, `shade-fraction`, `equation-solve` | specialised widgets | planned |
| `coordinate-plot`, `geometry-measure`, `geometry-classify`, `free-text-explain` | canvas / text | planned |

A pack lists the kinds it needs in `engine.features`; unknown kinds make the app skip that source and report it.

### 4.2 Typed answer values (`common.schema.json#/$defs/value`)
`int`, `decimal` (string with a **dot**, exact; UI shows a comma), `rational` (`num`,`den`, `form: any|lowest`), `mixed`, `quantity` (`value`,`unit`), `text`, `choice` (option id), `set`, `sequence`, `point`, `bool`. All numbers are **strings** (exactness, big integers).

### 4.3 Checker semantics (implemented by the engine, not by the pack)
1. Parse the child's input into the answer's type (accepts `0,5`/`0.5`, `½`, spaces as thousands separators).
2. Equal to `answer` ⇒ **correct** (for `rational` with `form: lowest`: equal in value but not reduced ⇒ **almost**, feedbackKey `not_simplified`).
3. Matches an `equivalent[]` entry ⇒ **almost** (+ its feedbackKey).
4. Matches an `errorRules[].answer` ⇒ **wrong with diagnosis** `id` (+ its feedback text).
5. Otherwise ⇒ **wrong, unknown error**. Hints use `steps[]` one at a time.
Rules whose buggy answer coincides with the correct one for this task are dropped at generation time.

## 5. Math markup in text
Plain Polish text with LaTeX *subset* between `$…$`: `\frac{a}{b}`, mixed number `2\frac{1}{3}`, `^`, `_`, `\sqrt{}`, `\sqrt[3]{}`, `\cdot`, `:`, `\%`, `\overline{3}` (repeating decimals), `^\circ`, `\angle`, `\parallel`, `\perp`, `\mathrm{km/h}`. Decimal comma inside math is written `{,}` (`3{,}75`). The app renders it with its own lightweight renderer (no WebView). LLM authors know LaTeX well, which is why we chose it.

## 6. The generator DSL (pure data, no code)

A generator is JSON; the engine interprets it. **No downloadable code ever executes** (safety, store policy, determinism).

```jsonc
{ "id": "frac-simplify",
  "levels": [ { "level": 1, "vars": { "max_b": "10", "max_g": "5" } }, … ],   // per-level constants (no randomness here)
  "vars":  [ { "name": "a", "expr": "randint(1, max_b - 1)" }, … ],            // evaluated top to bottom
  "constraints": [ "gcd(a, b) == 1" ],                                          // redraw `vars` until all true (≤ 1000 tries)
  "task": { "kind": "fraction-input", "prompt": "Skróć ułamek $\\frac{@{num}}{@{den}}$ …",
            "answer": { "type": "rational", "num": {"$expr": "a"}, "den": {"$expr": "b"}, "form": "lowest" },
            "errorRules": [ … ], "steps": [ … ] } }
```

### 6.1 Determinism (normative — every engine port (the app\'s Dart engine) must match `tests/conformance/vectors.json`)
* A task is `(generator, level, seed)`; `seed` is an unsigned 64-bit integer.
* PRNG = **SplitMix64** seeded with `seed`. `randint(lo, hi)` = `lo + next_u64 % (hi-lo+1)`; `choice(list)` = `list[next_u64 % len]`.
* `vars` are evaluated top-to-bottom, expressions left-to-right; every `randint`/`choice` call consumes exactly one `next_u64`. On constraint failure the *whole* `vars` list is re-evaluated, **continuing** the same stream (no re-seed).
* Arithmetic is exact (big rationals). `/` is exact division. `//` and `%` require integers.

### 6.2 Expression language
A Python-expression subset: integer and decimal literals (exact), strings, list literals `[…]`, indexing `x[i]`, `+ - * /`, `// %`, unary `- not`, comparisons (chained) and `in`/`not in`, `and`/`or`, ternary `A if C else B`, and function calls. **Functions (v1.1):**
* randomness: `randint, choice, sample(lo, hi, n)` (n distinct values, unordered), `shuffle(list)`;
* numbers: `gcd, lcm, floor, ceil, abs, min, max` (also over a list), `pow(x,n)` (int n, |n|≤64), `round(x,k)` (half up), `isqrt, icbrt, sqrt_dec, cbrt_dec` (root rounded half up to k places), `is_square, is_prime, factorize, divisors, digits, rev_digits, sign, numer, denom, sum, product, mean, median`;
* lists: `len, sorted, reverse, take, drop, range, count, index, setat, uniq, repeat, join, expand`;
* text and formatting: `str` (id string), `cap`, `roman`, `words` (Polish numerals), `pln`, `plw` (plural agreement), `fmt`, `hhmm`, `par` (parentheses around negatives), `poly(coeffs, vars)` (an algebraic sum with correct signs, e.g. `poly([3,-1,5],['x','y',''])` → `3x − y + 5`).

Names `true/false/True/False` are boolean literals; not available: `**`, `int()`, comprehensions, list `*`. A generator author must not put `}` inside `@{…}` (the interpolation regex ends at the first `}`) — build LaTeX with braces in a `var` and interpolate the var.

### 6.3 Text interpolation `@{expr|filter:arg}`
| Filter | Result |
|---|---|
| *(none)* / `dec` / `dec:k` | number with decimal comma (minimal digits, or fixed `k` places); inside `$…$` emits `{,}`; 5+ digit integers grouped with a NBSP |
| `int` | integer with NBSP grouping |
| `money` | `12,50 zł` (2 places, NBSP before `zł`) |
| `frac` | `\frac{n}{d}` |
| `pl:var` | Polish plural agreement using a 3-form list: `@{n|pl:item}` → `1 zeszyt`, `2 zeszyty`, `5 zeszytów`, `12 zeszytów`, `22 zeszyty`; non-integers use form 2 (`2,5 kg`-style) |

### 6.4 More generator features
* `vars[].require: true` — reject the draw immediately (cheap early filter), then redraw.
* `selfCheck[]` — invariants that must hold for every generated task (lint-only; e.g. `a*b == product`). They catch authoring mistakes without a second implementation.
* `minDistinct` (per generator or per level) — lint fails if 200 seeds give fewer distinct tasks, so a lesson never repeats itself.
* Per-level `vars` (difficulty knobs), `capsNote` (which regulation cap the level respects).
* **Options:** `correct` is always the first option; the app shuffles unless `input.fixedOrder`.
* **Answer types:** `int, decimal, rational (form lowest|any), mixed, quantity (unit may be an expression), text, choice, set, sequence, point, bool, time`. **Task kinds** include `number-input, decimal-input, fraction-input, mixed-number-input, quantity-input, time-input, point-input, multiple-choice, multi-select, order-items, find-the-mistake`.
* **Media** (`task.media[]`): figures, charts and tables — 28 renderer kinds, parameters in `docs/03-media.md`; `essential: true` means the task cannot be answered without it; every item has an `alt` text; `when` attaches an item conditionally; the renderer is `tools/render.py` / `cognio-render/`.
* Allowed LaTeX additionally: `\left`, `\right`.

### 6.5 What a generator author must do
Respect the regulation's **caps** (documented per level in `capsNote`; e.g. fractions with 1–2-digit denominators, ≤ 3 decimal places, factorisation of ≤ 2-digit numbers). `cognio.py lint` smoke-tests every level with 200 seeds; add property checks in the lint when a cap becomes testable.

## 7. LLM task-writing specs (`authoring/*.llm.json`, `llm-spec.schema.json`)

The spec is a complete, reusable brief for a model: `system`, `instructions` (with `@{count}`, `@{level}`), `perLevel` counts/constraints, few-shot `examples`, the `output` format, a **`verifier`**, a `taskTemplate` and `acceptance` rules.

**Principle: the model proposes, deterministic code disposes.**
* `output.format = "params+story"` (recommended): the model returns **numbers + wording** only. The `verifier` recomputes the answer, steps and sanity constraints from the numbers; `mustAppearInText` forces the story to actually contain them. The model's own arithmetic is never trusted.
* `"full-task"`: the model also proposes the answer; it is accepted only if the verifier reproduces it.
* Rejected outputs are discarded (not repaired). Accepted ones are written to a bank with `provenance = {source: bank-llm, specId, model, verifiedBy: solver}`; the linter rejects any `bank-llm` task with `verifiedBy: none`.
* `mode: author` — run on a PC (any strong model), review a sample (`acceptance.humanReview`), commit the bank into the pack. `mode: device` — reserved for on-device story variation of already-verified parameters; **disabled by default on the target cheap phone**.

Workflow: `author spec → run model → verify (cognio.py) → dedupe → sample review → bank.jsonl → lint → pack`. (The runner script that calls a model API is not written yet; the verifier `verify_llm_output` is.)

## 8. Versioning, compatibility, distribution

* **Format:** `formatVersion` `1.x` is additive (new optional fields, new kinds). A `2.x` pack is refused by a `1.x` app.
* **Course:** semver. Skill ids are **permanent**; learner progress is keyed by `(courseId, skillId, level)`. Renames go in `replaces[]`; removed skills keep their learner state, hidden. Changing a generator's randomness changes the tasks for the same seed — fine for generated tasks (not stored), but banks keep stable `id`s.
* **Integrity:** every file has sha256 in `course.json`; `cognio.py pack` writes them and builds `.cognio`; `lint` verifies them. Signature slot reserved.
* **File type:** extension `.cognio`, content = ZIP (deflate) with `course.json` at the root; MIME `application/vnd.cognio+zip` (the app registers an intent filter for it, so tapping a `.cognio` file in a file manager/messenger opens Cognio's import screen; the importer also accepts `application/zip` + `.cognio` name because many apps hand over generic types).
* **Install now:** parent opens a `.cognio` file (tap it, or use the file picker, or `adb push` to the app's folder). Works offline.
* **Network:** the app has the `INTERNET` permission, used only by the `:net` module for downloads the parent starts. Packs can still be side-loaded without it.
* **Server:** `cognio-server` (this repo, `server/`; deployed by `deployment/`) serves, under a base URL such as `https://ennor.ddns.net/cognio/`:
  * `GET index.json` → `{formatVersion, courses:[{id, version, latest, title, language, formatVersion, engine, size, sha256, url}], models}` (`url` and `models` are **relative to the index URL**);
  * `GET courses/<id>-<version>.cognio` → the pack (HTTP `Range` supported for resumable downloads);
  * `GET models/catalog.json` → the model catalog (schema `schemas/model-catalog.schema.json`).
  The app verifies size + sha256 (+ ed25519 signature once the key exists), installs side-by-side, and switches on parent confirmation. Publishing = build with `cognio.py pack`, then `foreman run push-data` in `server/`; the index updates on the next request.
* **Static source (GitHub):** `dist/` of this repository has exactly the server's layout (`index.json`, `courses/`, `models/`), kept current by `tools/make_index.py`, so `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/dist/` works as a base URL with no server at all. An app build's flavor decides which sources it offers (one fixed, a choice of several, or a free address).
* **Multiple courses** can coexist (the learner model is per course).

## 9. Tooling (reference implementation)

The sample pack is **generated** from Python sources in `content-src/` (`dsl.py` = authoring helpers, `build.py` = list of modules → `skills/`, `generators/`, `banks/`, `paths/` → `cognio.py pack`). Run `python3 -I content-src/build.py` and then `lint`. The pack files are the product; `content-src/` is just a convenient way to write 300+ skills consistently. Hand-written files (e.g. `authoring/*.llm.json`) are left untouched.

| Command | What it does |
|---|---|
| `python3 -I tools/cognio.py lint courses/pl-primary-math` | schema validation of every file, reference integrity (objectives, prerequisites, files), 200-seed smoke test per generator level, bank validation, LLM-spec example verification, hash check |
| `… gen <pack> <generator> <level> <seed>` | print one generated task |
| `… vectors <pack> tests/conformance/vectors.json` | conformance vectors for an engine port |
| `… scenes <pack> tests/conformance/scenes.json` | media → scene conformance cases for a renderer port |
| `… quest <pack> <id> [seed]` | print one generated quest |
| `… fit <pack>` | lower lesson sizes to what the sources can supply (run by the build) |
| `tools/render.py`, `tools/gallery.py` | reference renderer (scene + SVG), HTML contact sheet of all media |
| `… coverage <pack>` | official objectives with/without skills |
| `… pack <pack> dist/<id>-<version>.cognio` | hash + zip |
| `tools/parse_regulation.py`, `tools/build_curriculum.py` | rebuild `curriculum.json` and `docs/curriculum/stage-*.md` from the regulation PDF text |

## 10. What the sample course contains

`courses/pl-primary-math` v0.1.0 covers **all 176 objectives** of the regulation (`coverage`: I–III 43/43, IV–VI 86/86, VII–VIII 47/47) and the regulation's *doświadczenia edukacyjne* for IV–VI (4) and VII–VIII (4 + the shared interdisciplinary one).

| | I–III | IV–VI | VII–VIII | total |
|---|---|---|---|---|
| skills (incl. quests) | 71 | 183 | 84 | 338 |
| path units / lessons | 11 / 88 | 30 / 231 | 17 / 100 | 58 / 419 |

314 skills have a generator, 15 are static banks (101 tasks), 9 are quests, one has an LLM authoring spec. The app does not need a language model for any of this.

**Task supply.** Lint draws 200 seeds per generator level and requires ≥ 8 distinct tasks (most levels give 40–1000+); levels with a naturally small space (clock hours, multiplication facts, Roman numerals, symmetry of named shapes, …) get shorter lessons via `fit`, and the adaptive engine reuses them as spaced repetition rather than as fresh tasks.

Known gaps: further ports of the interpreter; `tutor.keyIdeas`/`commonErrors` are only filled where the error rules already carry feedback; no audio.
