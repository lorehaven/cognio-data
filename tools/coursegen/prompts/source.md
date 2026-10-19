You are preparing the **curriculum source** of a new Cognio course (`{{course}}`, language `{{language}}`).

Read `{{source_txt}}` (plain text of the official curriculum / syllabus: {{source_note}}) and write **`{{curriculum_out}}`** — a JSON file in the same format as `courses/pl-primary-math/curriculum.json` (read it first, and `docs/curriculum/README.md`).

Rules:
- Keep the **official structure**: stage → area (dział) → objective (wymaganie szczegółowe), plus `goals` and `experiences` if the source has them (otherwise `[]`).
- `text` of every objective and part is copied **verbatim** from the source. Only whitespace and line-break hyphenation may be normalised. Never paraphrase, translate, merge or invent objectives. If the source has an item that is not an objective (a heading, a note), leave it out.
- Ids: stage `I-III` / `IV-VI` / `VII-VIII` (pick the stage the source assigns; if it uses other stages, ask in your final message and stop), area `<stage>.<no>`, objective `<stage>.<area-no>.<item>` (item number, or a letter when the source uses letters), part `<objective-id>.<letter>`.
- `flags`: `finance` / `culture` only if the source marks the objective so; otherwise `[]`.
- Top-level keys exactly as in the reference file (`formatVersion`, `kind`, `curriculumId` = `{{course}}-curriculum`, `legalBasis`, `note`, `stages`). `legalBasis`: {{source_note}}.
- Write the file with the Write tool. Do not create other files. If the source is long, work area by area and re-read the source for each area rather than relying on memory.

When finished, check yourself: `python3 -I tools/coursegen.py check-source {{course}}` must print `OK`; fix and re-run until it does.

{{gates}}
