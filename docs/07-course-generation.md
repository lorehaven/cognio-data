# 07 - Generating a course with Claude

The sample course (`courses/pl-primary-math`) was produced by prompting Claude stage by stage and keeping only what passed code checks. `tools/coursegen.py` turns that routine into a script. **The model proposes, deterministic code disposes** (same principle as docs/02 §7): each stage ends in a gate that is plain code, and the next stage does not start until the gate passes.

```
 source ──G1──▶ plan ──G2──▶ author ──G3──▶ build ──G4──▶ blind solve ──G5──▶ pack
 curriculum     skills +     one python      path from     lint, fit,      independent       .cognio
 (verbatim)     units        module / batch  the plan      coverage        examiner
```

## 1. Quick start

```fish
# one workspace per course; the course id becomes courses/<id>/ and course-work/<id>/
python3 -I tools/coursegen.py new pl-primary-science --language pl --title "Przyroda – szkoła podstawowa" --prefix sc

# G1  fetch + format the official curriculum (url, pdf, html, txt/md; several allowed)
python3 -I tools/coursegen.py source pl-primary-science https://dziennikustaw.gov.pl/D2026000037801.pdf --note "Dz.U. 2026 poz. 378, Przyroda"
python3 -I tools/coursegen.py plan     pl-primary-science     # G2  skills, units, order
python3 -I tools/coursegen.py author   pl-primary-science     # G3  generators/banks, in batches, with repair rounds
python3 -I tools/coursegen.py validate pl-primary-science     # G4+G5  build, lint, coverage, blind solve, pack
# or: coursegen.py all <id> <source>...
```

* `--dry-run` writes the prompts to `course-work/<id>/logs/` and stops: paste them into an interactive Claude Code session if you prefer to drive a stage by hand, then run the gate alone (`check-source`, `check-plan`, `check-batch <module>`, `build`, `gates`).
* The script calls `claude -p` (Claude Code, headless, `acceptEdits`, tools limited to Read/Write/Edit/Glob/Grep and `python3 -I tools/*`). `--model`, `COGNIO_CLAUDE`, `COGNIO_CLAUDE_ARGS` change how. The blind-solve examiner runs with **no tools** at all.
* Every call is logged (`logs/<time>-<stage>.prompt.md` / `.out.md`). Stages are re-runnable: `author` skips modules that exist (`--redo` rewrites), `validate` always rebuilds.
* Cost scales with the curriculum: the maths course is ~340 skills, i.e. ~45 author batches. Start with `--batch-size 4` on one stage to see quality before running everything.

## 2. Files

| Path | Content | Tracked? |
|---|---|---|
| `course-work/<id>/course.cfg.json` | language, title, id prefix, source note | yes |
| `course-work/<id>/source.txt` | cleaned text of the source(s) — the reference for the verbatim check | yes |
| `course-work/<id>/plan.json` | skills + units (G2) | yes |
| `course-work/<id>/src/bNN_<stage>.py` | authored content modules (`from dsl import *`, same as `content-src/`) | yes |
| `course-work/<id>/{input,logs,tmp}/`, `review.json` | downloads, prompts/replies, scratch packs, blind-solve mismatches | no |
| `courses/<id>/` | the generated pack (curriculum.json, course.json, skills, generators, banks, paths) | yes |
| `dist/<id>-<version>.cognio` | packed course | yes |
| `tools/coursegen/prompts/*.md`, `tools/coursegen/gates.md` | the prompts and the gate list (the gate list is pasted into every prompt) | yes |

## 3. The stages and their minimal requirements

The authoritative text is `tools/coursegen/gates.md` — the model sees exactly that. Summary:

| Gate | Input → output | Minimum to pass |
|---|---|---|
| **G1 source** | URL/PDF/HTML/text → `courses/<id>/curriculum.json` | stages ∈ {I-III, IV-VI, VII-VIII}; every stage has areas, every area objectives; ids follow `<stage>.<area>.<item>[.<part>]` and are unique; **every objective text occurs verbatim in the source** (whitespace and line-break hyphenation ignored) |
| **G2 plan** | curriculum → `plan.json` | 100 % of objectives covered; unique slug ids; every skill in exactly one unit; units ≥ 2 skills; prerequisites exist, same stage, earlier in the path, acyclic; 1–3 levels; source `generator` or `bank` |
| **G3 author** (per batch) | plan batch → python module → scratch pack | schema-valid; 200 seeds per generator level without error, unresolved template, decimal point, double space; **≥ 12 distinct tasks per level** (≥ 8 if lowered explicitly); banks ≥ 10 tasks/level, one correct option per choice task; every task has `steps` and an exact `answer`; `tutor.intro` on every skill; error rules never equal the correct answer |
| **G4 build** | all modules + plan → `courses/<id>/` | path built from the plan (learn per skill, review every 3 skills when ≥ 4, checkpoint); `cognio.py fit`, `cognio.py lint` = **0 errors** (supply per lesson without repeats, every skill reachable, hashes), coverage of every objective |
| **G5 validate** | sample of tasks → examiner | **blind solve:** per skill level `--sample` (default 3) tasks, different seeds; an independent model (no tools, no answers, options shuffled) must reproduce every stored answer. Mismatch ⇒ repair round (`review-repair.md`), up to `--repair-rounds`; still failing ⇒ the gate fails and `review.json` lists the tasks. "Cannot solve without the picture" answers are counted separately, not as failures |

Form is checked by G1–G4 (schemas, references, structure, supply); data validity by G1 (verbatim), G3 (`selfCheck`, constraints, no degenerate draws) and G5 (independent solution). What the gates **cannot** prove: pedagogy, tone, age fit, and tasks whose truth depends on a figure (the examiner sees the figure parameters and `alt`, not the picture). Keep a human review of `cognio.py sample <pack> all 2` and `tools/gallery.py` before publishing, and give the pack a version bump.

## 4. Known limits (format v1.0)

* **Stage ids and objective ids are restricted by the schemas** (`I-III`, `IV-VI`, `VII-VIII`; numeric area). A course for another country or subject structure needs those enums relaxed in `schemas/` first (docs/06 lists the other engine gaps: typed text, matching, audio, maps). Until then, generated skills can only use the existing task kinds (numeric, fraction, choice, multi-select, order, find-the-mistake, quantity, time, point) and the 28 media kinds.
* Authoring modules import `content-src/dsl.py` (its output directory is switched by `COGNIO_PACK`, which `coursegen.py` sets). The maths course keeps using `content-src/build.py` unchanged.
* The blind-solve examiner is a model: a systematic misconception shared with the author is not caught. Run `author` with one model and `validate --model <other>` with another (the model flag applies to the examiner and to repair calls).
* `source` expects the text to be extractable (PDF with a text layer). Scanned PDFs need OCR first. Very long sources work because the prompt tells Claude to re-read the file area by area, but check the G1 report: a dropped objective is only noticed if you compare counts with the source.
