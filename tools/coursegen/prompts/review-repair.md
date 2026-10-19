An independent examiner solved sampled tasks of the Cognio course `{{course}}` **without seeing the stored answers**, and disagreed with the pack on the tasks below. For each: decide who is right by solving it yourself step by step. If the stored answer is wrong, or the task is ambiguous / has several correct answers / depends on a missing figure, fix the generator or bank in `{{module_out}}` (the module that defines skill `{{skill}}`) so that **no seed** can produce such a task. If the examiner is wrong, change nothing for that task, but make the prompt clearer if the wording invited the mistake.

Mismatches:
```json
{{mismatches}}
```

Afterwards run `python3 -I tools/coursegen.py check-batch {{course}} {{module_name}}` until it shows no FAIL. Reply with one line.

{{gates}}
