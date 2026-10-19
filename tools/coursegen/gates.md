## Acceptance gates (the minimum a course must meet — all are checked by code, none by opinion)

**G1 · source** (`coursegen.py source`)
- `curriculum.json`: `stages[] → areas[] → objectives[]`; each stage has ≥ 1 area, each area ≥ 1 objective.
- Stage ids are `I-III`, `IV-VI` or `VII-VIII` (format v1.0 restriction). Area ids `<stage>.<n>`; objective ids `<stage>.<area-no>.<item>[.<part>]`, `item` = number or letter. All ids unique.
- Every objective `text` (and part text) is **verbatim** from the source: after collapsing whitespace and line-break hyphenation it must occur in the source text. No paraphrase, no summary, no translation.

**G2 · plan** (`coursegen.py plan`)
- `plan.json` has `skills[]` and `units[]` (shape in the plan prompt). Skill and unit ids: slugs `[a-z0-9-]`, unique, ≤ 60 chars.
- **100 % objective coverage**: every objective item is trained by ≥ 1 skill (listing the item id, or any one of its part ids, counts — same rule as `cognio.py coverage`); no unknown objective ids.
- Every skill is in **exactly one unit**; every unit holds ≥ 2 skills, in learning order; prerequisites exist, are in the same stage, are acyclic and appear **earlier** in the path.
- Every skill has 1–3 levels and a `source` of `generator` or `bank`.

**G3 · author** (`coursegen.py author`) — per batch, then again for the whole pack
- Every file validates against `schemas/*.schema.json`.
- A **generator** skill: `cognio.py lint` draws 200 seeds per level; none may raise, leave `@{…}` unresolved, print a decimal point instead of a comma, double spaces, or lack `steps`; every level must yield **≥ 12 distinct tasks** (set `min_distinct` lower only when the task space is naturally small, never below 8).
- A **bank** skill: ≥ 10 tasks per level (a lesson is ≥ 4 tasks, and lessons draw 10 by default; `fit` lowers lessons to the supply), every task has `steps`, `provenance`, correct `answer`; choice tasks have exactly one correct option.
- Every skill that has a `learn` lesson has `tutor.intro` (≥ 1 sentence, in the course language, with a tiny worked example).
- Every task: `prompt` in the course language, ≥ 1 `steps`, an **exact** `answer`; at least one `errorRules` entry wherever a typical wrong procedure exists (computational skills); no error rule whose answer equals the correct one.
- Difficulty levels respect the caps of the curriculum text (put the cap in `capsNote`).

**G4 · path** (built from `plan.json`, checked by `cognio.py lint`)
- Every skill appears in some lesson; the first lesson of a stage is open; each unit = `learn` per skill (+ `review` every 3 skills when ≥ 4 skills) + final `checkpoint` (mix of ≥ 2 skills).
- Every lesson can be supplied **without repeating a task**: bank ≥ `tasks`; generator level ≥ max(8, 2 × `tasks`) distinct tasks (`cognio.py fit` lowers `tasks` automatically).

**G5 · validate** (`coursegen.py validate`)
- `cognio.py lint` → **0 errors**; `cognio.py coverage` → every objective covered.
- **Blind solve** (data validity): for a sample of tasks (default 3 per skill-level, different seeds) an independent model, *without* seeing the answer and with shuffled options, solves the task. Its answer must equal the stored `answer` for **every** sampled task (tasks it declares unsolvable without a picture are reported, not counted as failures). Any mismatch fails the gate: either the stored answer is wrong or the task is ambiguous — both are defects.
- `errorRules` sample: the buggy answers differ from the correct one and from each other.
- The pack builds (`pack`) and file hashes verify.
