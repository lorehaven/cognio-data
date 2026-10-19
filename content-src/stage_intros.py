"""Applies the lesson introductions (tutor.intro) written in stage_intros_1/2 to skills that do not define their own."""
from dsl import SKILLS
from stage_intros_1 import INTROS_1
from stage_intros_2 import INTROS_2

for sid, text in {**INTROS_1, **INTROS_2}.items():
    tutor = SKILLS[sid].setdefault('tutor', {})
    tutor.setdefault('intro', {'pl': text})
