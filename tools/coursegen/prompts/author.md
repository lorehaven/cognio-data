You are writing the **content** of the Cognio course `{{course}}` (language `{{language}}`) for one batch of skills.

Read first (do not skip): `docs/02-course-format.md` (esp. §4–6: task, typed answers, DSL, interpolation), `content-src/dsl.py` (the authoring helpers you must use), and these existing modules as style references: `content-src/stage_iv_vi_fractions.py`, `content-src/stage_iv_vi_percent_money.py`. For media (figures/charts/tables) see `docs/03-media.md`. Read `{{curriculum_out}}` only for the objectives listed below.

Write **one file**: `{{module_out}}` — a Python module that starts with `from dsl import *` and defines exactly the skills of this batch, using `skill(...)` (generators) or `bank_skill(...)` (banks). Do not touch `Unit`/paths: the path is built from the plan. Do not write any other file.

Batch skills (from the plan; ids, titles, levels, objectives and prerequisites must be used as given):
```json
{{batch}}
```
Objective texts (verbatim from the official curriculum):
```json
{{objectives}}
```

Quality bar — a child aged 8–14 will see these tasks, and a parent will trust the answers:
- Everything the child reads is in `{{language}}`, simple and friendly. Math markup per §5 of the format doc (decimal comma `{,}` inside `$…$`).
- **Answers are computed by expressions from the random variables, never typed in.** Use `constraints` so the draw is always a valid, unambiguous, non-degenerate task, and `selfCheck` for an invariant that independently confirms the answer (e.g. `a*b == product`). Use `require` vars for cheap rejection.
- Every level respects the curriculum's caps (say which in `lvl(..., caps='…')`). Levels must differ in difficulty, not only in magnitude.
- Add `errors=[…]` with the answers produced by the 1–3 most typical wrong procedures (with a short, kind feedback in the course language) wherever such procedures exist. Write `steps` as a real worked solution (idea → computation → conclusion), usable as hints.
- Each skill: `intro=` (short explanation + tiny worked example, in the course language) and `area=` (the area id from the plan). Use `min_distinct=` only when the task space is truly small.
- Vary the task: several phrasings/contexts per skill where it makes sense (a `choice` var selecting among templates), not one sentence with other numbers.
- For `bank_skill`: ≥ 10 tasks per level, each with a full `steps` list; correct answers verified by you step by step.

Gate loop — do this until it prints no FAIL lines (max {{rounds}} rounds):
`python3 -I tools/coursegen.py check-batch {{course}} {{module_name}}`
It builds only your module into a scratch pack and runs the real linter (200 seeds per level). Fix the module, never the linter. Then reply with one line: the number of skills written.

{{gates}}
