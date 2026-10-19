You are designing the **study path** of the Cognio course `{{course}}` (language `{{language}}`).

Inputs (read them): `{{curriculum_out}}` (the official objectives), `docs/02-course-format.md` (course format; §1–3 matter most), and as a worked example the existing course: `courses/pl-primary-math/curriculum.json`, `courses/pl-primary-math/paths/IV-VI.json` and a few of its `skills/IV-VI/*.json`.

Write **`{{plan_out}}`** (JSON, the only file you create):

```json
{
  "skills": [
    { "id": "slug", "stage": "IV-VI", "area": "IV-VI.1",
      "title": "learner-facing title in {{language}}",
      "objectives": ["IV-VI.1.16"],
      "prerequisites": ["slug-of-earlier-skill"],
      "levels": [ {"label": "Małe liczby", "caps": "which limit of the curriculum this level respects"} ],
      "source": "generator",
      "tasks": "one or two sentences: what ONE task looks like, what varies between tasks, what wrong procedures children typically apply" } ],
  "units": [
    { "id": "slug", "stage": "IV-VI", "area": "IV-VI.1", "title": "…", "description": "one sentence", "icon": "numbers",
      "skills": ["skill ids in learning order"] } ]
}
```

Design rules:
- **Coverage:** every objective id in the curriculum is trained by ≥ 1 skill. Use the *item* id; list part ids only when the skill trains one part. One objective may have several skills (different problem types); one skill may serve several objectives.
- **Granularity:** one skill = one class of problems the child can drill (≈ 1.9 skills per objective in the reference course). Not "fractions" (too big) and not one single fixed question (too small).
- **Order:** the curriculum fixes no order. Order units and skills pedagogically: simple → complex, prerequisites first. `prerequisites` only for real dependencies, same stage, earlier in the path.
- **Units:** 3–10 skills each, themed, one `area` each; icons are simple words (numbers, fractions, shapes, clock, money, chart, …). Every skill sits in exactly one unit.
- **Levels:** 1–3 per skill, each stricter or larger than the last, never beyond the caps stated in the curriculum text.
- **Source:** `generator` when the answer can be computed from random parameters (the default, strongly preferred); `bank` only when tasks cannot be parameterised (reasoning puzzles, find-the-mistake, text-based knowledge). Banks cost much more to write: keep them ≤ 20 % of skills.
- Skill ids carry a short course prefix so they never clash with other courses (e.g. `{{prefix}}-…`).

When finished run `python3 -I tools/coursegen.py check-plan {{course}}` — it must print `OK`; fix and re-run until it does.

{{gates}}
