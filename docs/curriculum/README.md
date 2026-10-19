# Polish primary-school maths curriculum — official structure

## Source
**Rozporządzenie Ministra Edukacji z 11 III 2026 r.** w sprawie podstawy programowej wychowania przedszkolnego oraz kształcenia ogólnego dla szkoły podstawowej (**Dz.U. 2026 poz. 378**) — <https://dziennikustaw.gov.pl/DU/2026/378>. All requirement text in the stage files is taken **verbatim** from it by script (`tools/parse_regulation.py` → `tools/build_curriculum.py`); nothing is paraphrased or assigned to school years by us.

## Structure (as in the regulation)

| Stage | Grades | Subject in the regulation | Areas (działy) | Objectives |
|---|---|---|---|---|
| [**I–III**](stage-I-III.md) | 1–3 | Edukacja wczesnoszkolna → *Edukacja matematyczna* | Liczby · Miary · Figury · Dane · Myślenie matematyczne | 43 |
| [**IV–VI**](stage-IV-VI.md) | 4–6 | *Matematyka* | Liczby · Miary · Algebra · Figury · Dane · Myślenie matematyczne | 86 |
| [**VII–VIII**](stage-VII-VIII.md) | 7–8 | *Matematyka* | Liczby · Algebra · Figury · Dane i zdarzenia losowe · Myślenie matematyczne | 47 |

Each stage file contains: general aims (*cele kształcenia*, stages IV–VIII), the detailed requirements (*wymagania szczegółowe*) grouped by area, and the *doświadczenia edukacyjne* (practical experiences) for stages IV–VI and VII–VIII. Tags: 💰 *moduł ekonomiczno-finansowy*, 🎨 *moduł kultura*.

**The regulation does not assign requirements to individual school years.** Order and pacing inside a stage belong to the teacher/textbook. The app therefore works per stage and orders skills by prerequisites and learner state (see `../01-architecture.md §7`).

## Objective IDs
`<stage>.<area>.<item>[.<part>]`, e.g. `IV-VI.1.19` (stage IV–VI, Liczby, item 19), `IV-VI.1.28.a` (sub-point a), `I-III.1.p` (stage I–III, Liczby, point p). They are the keys that skills in course packs point to (`courses/pl-primary-math/curriculum.json`).

## Context
* The new podstawa is taught from **1 Sept 2026 in grades I and IV** (reform "Kompas Jutra"), then rolls up year by year; the child in 4th grade in 2026/27 is in the first cohort. The previous podstawa still applies to other grades in 2026/27.
* Commentary and teaching approach (IBE PIB 2026): <https://ibe.edu.pl/files/Reforma26/Komentarze_dydaktyczne/Matematyka_komentarz_do_podstawy.pdf>.
* Difficulty caps are part of the requirements (e.g. fractions with 1–2-digit denominators, ≤ 3 decimal places, factorisation of ≤ 2-digit numbers) — generators encode them per level.
* Calculators are meant only for tasks where computation is not the point; skills carry the `no-calculator` tag.
