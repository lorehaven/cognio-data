# cognio-server

Serves Cognio **course packs** (`.cognio`) and the **tutor-model catalog** to the Cognio Android app. Read-only, no database,
no authentication (everything served is non-confidential course data). Python, [Starlette](https://www.starlette.io/) + uvicorn.

## Data directory

```
<DATA_DIR>/
  courses/pl-primary-math-0.1.0.cognio     one file per pack version (ZIP with course.json at the root)
  models/catalog.json                      optional; see ../models/catalog.json
```

New or replaced files appear in the index on the next request - no restart. Files that are not valid packs (not a ZIP,
no `course.json`, bad name) are ignored and logged. A pack's file name must match `[a-z0-9][a-z0-9._-]*.cognio`.

## API (all under `BASE_PATH`, e.g. `/cognio`)

| Request | Response |
|---|---|
| `GET /healthz` | `ok` (probes) |
| `GET /index.json` | `{formatVersion, courses:[{id, version, latest, title, language, formatVersion, engine, size, sha256, url}], models}`; sorted by id and semver; `ETag` + `If-None-Match` → 304. `url` and `models` are **relative to the index URL**, so the server needs no knowledge of its public address. |
| `GET /courses/<file>.cognio` | the pack, `application/vnd.cognio+zip`, `Range` (resumable), `ETag`/`Last-Modified` |
| `GET /models/catalog.json` | the model catalog (404 if absent) |

The app verifies `size` and `sha256` from the index after downloading (see `../docs/02-course-format.md §8`).

## Configuration (environment)

| Variable | Default | |
|---|---|---|
| `DATA_DIR` | `./data` | data directory |
| `BASE_PATH` | *(empty)* | serve under a prefix; the ingress passes the path through unchanged |
| `HOST` / `PORT` | `0.0.0.0` / `8080` | |
| `LOG_LEVEL` | `INFO` | |

## Develop

```sh
uv sync
uv run pytest -q                   # or: foreman run test
foreman run dev                    # serves ./data on :8080
mkdir -p data/courses && cp ../dist/*.cognio data/courses/ && curl localhost:8080/index.json
```

## Build, publish, deploy

`foreman.toml` mirrors kindle-sync: `foreman run release` = test + build + push the image + `riveter apply` of
`../deployment` + rollout. The image tag lives in `../deployment/overlays/cognio/deployment.yaml.j2`.
`foreman run push-data` rsyncs `../dist/*.cognio` and `../models/catalog.json` to the node
(`DATA_REMOTE`, default `ossiriand.arda:/mnt/dev/cognio/data`).
Publishing a new course version = `python3 -I ../tools/cognio.py pack ...` → `foreman run push-data`.

## Not (yet) here

Uploads over HTTP, authentication, pack signatures (the `signature` field of `course.json` is reserved), per-pack delta downloads.
