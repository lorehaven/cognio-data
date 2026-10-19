# cognio-data

Everything about the **content** of Cognio, a game for learning school subjects: the course format and its schemas, the course sources and
generators, the tools that build and validate course packs (`.cognio`), the conformance tests every app engine must pass, and the
file server that serves the packs. The app itself lives in a separate (private) repository, `cognio-app`.

## The repository is a pack source

`dist/` is the published tree and is committed:

```
dist/index.json                     what is available: id, version, title, language, size, sha256, url (relative)
dist/courses/<id>-<version>.cognio  one ZIP per pack version
dist/models/catalog.json            optional tutor-model catalog
```

The app can download straight from GitHub, no server needed: its source address is

    https://raw.githubusercontent.com/<owner>/cognio-data/<branch>/dist/

(the app verifies every download against the `sha256` of the index). The same tree is what `server/` serves, so a
self-hosted mirror and the GitHub address are interchangeable. Which sources an app build offers (one fixed, a choice of
several, or a free address) is a flavor setting of the app: `server.sources` / `server.downloads` in its `flavor.json`.

## Layout

| Path | Content |
|---|---|
| `docs/` | **format and pipeline**: [02-course-format](docs/02-course-format.md) (the pack format, DSL, checker, distribution), [03-media](docs/03-media.md) (figures, charts, tables), [06-curriculum-roadmap](docs/06-curriculum-roadmap.md), [07-course-generation](docs/07-course-generation.md) (generating a course with Claude), [curriculum/](docs/curriculum/README.md) (official requirements) |
| `schemas/` | JSON Schemas of the pack format and of the model catalog |
| `courses/pl-primary-math/` | the Polish maths course (generated from `content-src/`) |
| `content-src/` | Python sources that generate it: `python3 -I content-src/build.py` (writes the pack **and** `dist/index.json`) |
| `tools/cognio.py` | reference interpreter + `lint` / `gen` / `sample` / `quest` / `vectors` / `scenes` / `coverage` / `fit` / `pack` |
| `tools/coursegen.py` | the staged Claude-prompted course generator (`tools/coursegen/`) |
| `tools/make_index.py` | rebuilds `dist/index.json` from `dist/courses/` (`--check` for CI) |
| `tools/render.py`, `tools/gallery.py` | reference media renderer (scene + SVG) and an HTML contact sheet |
| `tests/conformance/` | `vectors.json`, `scenes.json`: expected outputs every engine port must reproduce bit for bit |
| `models/catalog.json` | optional tutor models the app can download |
| `server/` | Python file server for the packs (Starlette, Dockerfile, `foreman.toml`, tests) |
| `deployment/` | riveter overlay deploying it to the home cluster (`https://ennor.ddns.net/cognio/`) |

## Everyday commands

    python3 -I tools/cognio.py lint courses/pl-primary-math     # validate a course source
    python3 -I content-src/build.py                             # regenerate course + pack + dist/index.json
    python3 -I tools/make_index.py --check                      # is the committed index current?
    python3 -I tools/coursegen.py --help                        # generate a new course

After changing a course: build, commit `courses/`, `dist/`, and push. Apps that point at the GitHub source see the new version
on their next course check. A pack version is immutable once published: bump `version` for a change (see docs/02 §8).

## What the app repository needs from here

* the packs bundled into a build (`dist/courses/*.cognio`), chosen by the flavor,
* `tests/conformance/*.json` and `tools/cognio.py` for the engine conformance tests (`COGNIO_DATA=<path to this repo>`).
