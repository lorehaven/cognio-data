The content module `{{module_out}}` of the Cognio course `{{course}}` failed the acceptance gate. Fix **only that file** (keep skill ids, objectives and levels as they are; fix the generator/bank so the failure cannot occur — do not weaken constraints just to hide it, and do not lower `min_distinct` below 8).

Failures:
```
{{failures}}
```

Useful commands: `python3 -I tools/coursegen.py check-batch {{course}} {{module_name}}` (re-run the gate on this module) and `python3 -I tools/cognio.py gen <pack> <generator-id> <level> <seed>` on `{{scratch_pack}}` to print one generated task.
Task-format reminders are in `docs/02-course-format.md` §4–6 and `content-src/dsl.py`.
Re-run the gate until no FAIL remains (max {{rounds}} rounds), then reply with one line.

{{gates}}
