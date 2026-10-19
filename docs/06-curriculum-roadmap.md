# 06 - Covering the whole school curriculum, and language courses (roadmap)

Status: planning document, written 18 Oct 2026. Nothing here is built yet except maths (stages I-III, IV-VI, VII-VIII). It follows the decisions in
[05-monetization.md](05-monetization.md): **school-curriculum courses are free and ad-free**; extra modes and premium courses are the paid part; the
curriculum has to be covered *first*.

## 1. Goal

* Cover **every subject of the official primary-school curriculum that can be practised on a phone** (not PE, not handicraft), as free courses, in the
  same quality as maths: exact alignment to the regulation, generated or reviewed tasks with explanations, mastery-based path, figures/maps/audio where needed.
* Add **language courses** (English first) built on a language-independent skeleton that the regulation itself provides (section 4).
* Keep the product **honest to the curriculum**: every skill points to a requirement of the regulation (as the maths pack does with `curriculum.json`).

## 2. What "the whole curriculum" is

**Source:** Rozporządzenie Ministra Edukacji z 11 III 2026 r., Dz.U. 2026 poz. 378 - the one regulation we already parsed for maths
(`tools/parse_regulation.py`, see [curriculum/README.md](curriculum/README.md)). It holds the core curriculum of **all** primary-school subjects, so
the same pipeline can read every subject. Secondary school (liceum, technikum) is a separate regulation and a later project.

**Reform timing:** the new core curriculum applies from **1 Sept 2026 in grades I and IV**; other grades stay on the previous one for 2026/27 and move
up year by year. Cognio's packs follow the 2026 regulation by *stage* (I-III, IV-VI, VII-VIII), not by school year, which makes the transition
harmless: a child in grade 5 uses the same IV-VI path as a child in grade 4. Keep the regulation reference in every pack so an update is traceable.

**Mastery learning:** the regulation asks for *mastery learning* in language and maths competencies (move on only when the simpler skill is secure) and defines
a "wstępny" (initial) and "oczekiwany" (expected) level at the end of grade VIII. This is exactly how Cognio's path and practice already work; say so in the store listing.

**Size of each subject** - approximate number of requirement lines counted in the regulation text (method: numbered "Uczeń:" items; maths calibrates it, the count
was within about 10% of our parsed 133 objectives for IV-VIII). Expected pack size uses the ratios of the maths pack: about **1.9 skills** and **2.4 lessons** per objective.

| Subject (stage) | Requirements (about) | Skills (est.) | Lessons (est.) | Automatic checking | Content needs |
|---|---|---|---|---|---|
| Matematyka I-III, IV-VIII | 176 (parsed) | 338 (done) | 419 (done) | **high** | done |
| Język polski IV-VIII | 210 | 400 | 500 | medium-high (spelling, grammar, vocabulary, reading comprehension; not essays) | typed-text input, passages, banks |
| Język obcy nowożytny (all languages) | 360 | 680 per language set, shared skeleton | 870 | **high** for vocabulary/grammar/listening; speaking needs speech recognition | audio, typed text, matching, decks |
| Historia IV-VIII | 240 | 450 | 570 | medium (dates, order, cause, source questions) | images, timelines, banks |
| Przyroda IV-VI | 120 | 230 | 290 | medium | images, banks |
| Biologia V-VIII | 110 | 210 | 270 | medium | images (labelling), banks |
| Geografia V-VIII | 80 | 150 | 190 | medium | **maps** (tap on map), charts, banks |
| Chemia VII-VIII | 60 | 115 | 145 | **high** (formulas, stoichiometry, balancing) | formula input, tables |
| Fizyka VII-VIII | 60 | 115 | 145 | **high** (units, formulas, graphs) | media already mostly there |
| Informatyka IV-VIII | 75 | 140 | 180 | medium (logic, algorithms, binary, spreadsheets) | puzzle input types |
| Edukacja obywatelska VIII | 70 | 130 | 160 | low-medium (scenarios, definitions) | banks |
| Edukacja wczesnoszkolna I-III, **other than maths** | several hundred lines (needs a real parse) | - | - | medium (language, nature, social education) | pictures, audio, large type |
| Muzyka, Plastyka | 60 + 70 | - | - | low (note reading, ear training, art history quizzes) | audio, images |
| Edukacja zdrowotna, EDB, Etyka | 130 + 40 + 110 | - | - | low (scenario multiple choice) | banks |
| Wychowanie fizyczne, Zajęcia praktyczno-techniczne | 140 + 50 | - | - | not suitable | skip (maybe short theory quizzes later) |
| Języki mniejszości, kaszubski, łaciński | - | - | - | - | later, on demand |

The eight "integrated educations" of grades I-III are: language (Polish, foreign, minority, Kashubian), maths, nature, social, art (visual arts and music),
technical and computing, physical education and ethics.

**Where the real effort is:** the numbers above are only the *counts*. The maths pack needed generators with error rules, figures and quests; most other
subjects are **banks** of reviewed questions plus media, so the cost shifts from generator logic to **content volume, accuracy review and image/audio licensing**.

## 3. What the engine can do today, and what each subject needs

Today the checker supports: integers, decimals, quantities with units, fractions, mixed numbers, points, times, single and multiple choice, and ordering.
Media: 28 figure kinds, charts, tables. Tasks come from generators (with error rules), banks (JSONL) and quests (stories with steps).

| Gap | Needed by | Sketch |
|---|---|---|
| **Typed text answer** with a normalisation policy (case, spaces, diacritics ignored or required, list of accepted variants, "almost" for a missing diacritic) | Polish spelling, vocabulary, English/German translation | new `text` answer type; `equivalent[]` for variants |
| **Matching pairs** (two columns) | vocabulary, history (event-date), chemistry (symbol-name), biology | new `match` input |
| **Cloze / gap fill** (several gaps in a sentence, choose or type) | grammar, languages, Polish | extend `choice`/`text` with several slots |
| **Audio** (play a sound or speak a text, then answer) | languages, music, early grades read-aloud | use Android TTS (the otter already speaks Polish) for target languages, or recorded audio assets with a licence; `audio` media kind |
| **Images** (photos, drawings) with credits | biology, geography, history, early grades, art | pack `assets/` folder, size budget, licence + attribution in the pack (Wikimedia Commons CC0/CC BY; **no scans of textbooks**) |
| **Maps** and tap-on-map input | geography, history | simplified vector maps (public-domain Natural Earth style data), regions as hit areas, new `map-point` input |
| **Timeline / order with dates** | history | existing `order` input plus date items; a `timeline` media kind |
| **Vocabulary decks with spaced repetition** | all languages, also terms in science | new `deck` source type: items with their own memory state; a daily "review" session like *Powtórka dnia* |
| **Passages** (a text and several questions) | Polish reading, English reading, history sources | already possible as a *quest* (story + steps); give it a nicer layout |
| **Formula / equation input** (chemistry equations, balancing) | chemistry, physics | structured input; sub/superscripts already render |
| **Speech recognition** (say the word) | language speaking practice | Android `SpeechRecognizer`; **privacy**: prefer on-device recognition; otherwise this is a Plus feature with a clear parent consent |
| **Puzzle inputs** (grid, blocks, drag) | informatics | later |

All of these are additions to the pack format (docs/02) and the checker; each needs conformance vectors like the maths ones so the Python reference and the engine
engine stay identical.

## 4. Language courses

**The regulation makes language courses cheap to structure.** The requirements for *język obcy nowożytny* are **common to all modern languages**
(seven general aims: language means, understanding spoken and written text, producing text, interaction, mediation, learning strategies, cultural openness) and are
written for **four proficiency levels: A1, A1+, A2, B1**. The expected end-of-grade-VIII level is **A2 for the first language and A1 for the second**.

So the design is a **language-independent skill tree** (taken from the regulation, parsed like maths) plus **language packs** that fill it with vocabulary,
grammar and texts:

```
course "język obcy" (skeleton: requirements A1 .. B1, task kinds, path rules)
  + language pack: en  (first language, to A2, optional B1 as premium)
  + language pack: de  (second language, to A1)  -> later es, fr, ru, it
```

**Suggested order of languages:** English first (it is the first language for almost every pupil, the biggest audience, the best TTS and content availability);
German second (the most common second language in Polish schools), then Spanish and French on demand. Polish-for-Ukrainian-speaking children
(*Polish as a second language* with a Ukrainian interface) is a separate, socially valuable course and a good grant candidate - but it needs Ukrainian UI strings.

**Task kinds per level (all automatically checkable except speaking):**
vocabulary by topic (picture/word/translation, typed or chosen), listening (hear a word or sentence, choose the picture or the meaning), reading (short text
with questions), grammar in context (gap fill, choose the form, reorder words into a sentence - the `order` input already exists), everyday dialogues
(choose the reply), spelling of words, and later short writing checks (compare against accepted answers only - never free-text grading).

**Vocabulary source:** the regulation lists the **topics** (me and my family, home, school, food, shopping, travel, culture, sport, health, nature, social life...).
Build the word lists ourselves from those topics (generated with an LLM, reviewed, graded by CEFR level) rather than copying commercial or copyleft word lists,
so licensing stays simple. Each item: word, part of speech, example sentence, translation, picture (optional), audio (TTS), level, topic.

**Speaking:** not in the free core at first. Premium "speak" mode with on-device speech recognition when it is good enough, or recording-and-compare without sending audio anywhere.

**Effort (rough):** one language pack at A1-A2 is about **600-700 skills and 800+ lessons** if every requirement gets full coverage, but most of it is banks/decks
generated from word lists, so the human work is **review**, not authoring: figure on a few hundred reviewed items per week for one reviewer.

## 5. Order of work

The order balances audience, how well the engine fits, and effort. Each step ends in a releasable pack.

| Step | What | Why now | Engine work |
|---|---|---|---|
| 0 | **Harden maths**: review a sample of all 338 skills with a teacher, fix wording, publish the quality report | the base everything else is compared with | none |
| 1 | **Engine v2 basics**: `text` answer, `match`, cloze, image assets, audio via TTS, vocabulary `deck` with spaced repetition | unlocks languages and most other subjects | checker, pack format, conformance vectors, UI |
| 2 | **English A1 -> A2** (first language skeleton + English pack) | biggest audience, best fit | step 1 |
| 3 | **Język polski IV-VIII** (spelling, parts of speech, syntax basics, vocabulary, reading passages) | second pillar of the school day | `text` answer with a diacritics policy |
| 4 | **Early grades beyond maths** (edukacja polonistyczna, przyrodnicza, społeczna of I-III) with read-aloud and big pictures | completes the youngest path | images, audio |
| 5 | **Przyroda IV-VI, then Biologia, Geografia** | one science line with shared images and maps | maps, images, labelling |
| 6 | **Fizyka and Chemia VII-VIII** | generator-friendly like maths | formula input |
| 7 | **Historia and Edukacja obywatelska** | timelines and source questions | timeline media |
| 8 | **Informatyka IV-VIII** | logic, algorithms, binary, spreadsheets | puzzle inputs |
| 9 | **Second language (German)** to A1, then others on demand | uses the skeleton from step 2 | none beyond step 2 |
| 10 | Music, art, health, EDB, ethics as short quiz courses | completeness | none |

Secondary school (liceum/technikum, from 2027 per the ministry schedule) is a follow-up once primary is complete.

## 6. Content pipeline and quality

1. **Parse** each subject from the regulation text into `curriculum.json` and a readable `docs/curriculum/<subject>.md` (generalise `parse_regulation.py`; the maths
   parser already handles "Uczeń:" areas and numbered/lettered items; the line ranges are edition-specific and must be re-checked).
2. **Plan skills** per requirement (prerequisites, levels, error rules for typical mistakes); lint checks coverage: every requirement has at least one skill.
3. **Author**: generators for computable content (physics, chemistry, informatics); banks and decks written with the LLM task-writing spec (`llm-spec.schema.json`),
   always with `provenance` fields. The human reviewer approves each bank before it ships.
4. **Test**: lint, conformance vectors, `cognio.py sample` for human reading, the existing "9,060 tasks solved through the checker" style test for each new input type.
5. **Teach-back**: ask two or three teachers or parents to play a unit and mark errors; add a *report a problem* link in settings that opens a prefilled e-mail.
6. **Versioning**: packs carry the regulation reference and a content version; the app already updates packs by hash.

**Copyright and licences:** the regulation text is public. Do not copy textbook or exam-sheet text (publishers, CKE). Reading lists: use public-domain works (author dead
more than 70 years) for excerpts; write original summaries. Images: only CC0/CC BY (keep a credits file in the pack); audio: Android TTS or own recordings.

## 7. Free and paid, applied to this plan

* **Free:** every subject above that belongs to the school curriculum, including English to A2 (the school target) and a second language to A1.
* **Plus (extras, parent-bought):** exam simulator, challenge modes, speaking practice, adaptive tutor, family features, and premium courses **beyond** the curriculum:
  English B1 and above, extra languages, logic and coding, contest maths, financial literacy, Polish for Ukrainian-speaking children.

## 8. Risks

| Risk | Reduction |
|---|---|
| Content volume is huge for one person | Order by audience; decks/banks from reviewed LLM drafts; ship subject by subject; recruit 2-3 teachers as reviewers |
| Errors in education content hurt trust | Review gate, tests, report-a-problem link, fast fixes, version notes |
| Curriculum changes under the reform | Packs are per stage and reference the regulation; re-run the parser on amendments |
| Image/audio licensing | Allow-list of licences, credits file, no scans, own TTS |
| TTS missing for a language on the phone | Detect and say so (as for Polish); recorded audio for the core vocabulary later |
| App size growth (images, audio) | Packs downloaded on demand (the server already exists); only bundle the first course |
| Speech recognition and children's privacy | On-device only or optional Plus mode with explicit parental consent; no audio stored |

## 9. Next steps (suggested, about the next month)

1. Generalise the regulation parser to **all subjects** and generate `docs/curriculum/<subject>.md`; get the real counts (replace the estimates in section 2).
2. Write the **engine v2 spec** (section 3 table) in docs/02 and add conformance vectors; implement `text`, `match`, cloze, `image`, `audio` (TTS), `deck`.
3. Build the **English A1 pilot** (about 12 topic units, 200-300 items) to prove the language skeleton end to end, and test it with one or two children.
4. In parallel, start the **maths review** with a teacher (step 0).
5. Decide how many hours per week you can give, and whether to recruit reviewers; the plan above fits roughly one to two subjects per quarter for one person.
