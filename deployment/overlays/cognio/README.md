# cognio overlay - cognio-server

Package `cognio`, namespace `cognio`; run `riveter` from `deployment/`. Source of the image: `../server`.
Same age key as the other overlays (`~/.config/riveter/age.key`), though this overlay has **no secrets**.

| Workload | What | State |
|---|---|---|
| `cognio-server` | read-only file server for `.cognio` packs and the model catalog | `/mnt/dev/cognio/data` on the node (`courses/`, `models/`), mounted read-only at `/data` - **back up** |

Public at `https://ennor.ddns.net/cognio/` (ingress, Let's Encrypt, path passed through unchanged; the app owns the
`/cognio` prefix via `COGNIO_BASE_PATH`). Index: `https://ennor.ddns.net/cognio/index.json`.

## First deploy

1. **Image** (private registry, logged in on the host): `cd ../server && foreman run publish`
   (= `docker build` + `docker push ennor.ddns.net/utilities/cognio-server:0.1.0`). A new version means a new tag in
   `deployment.yaml.j2` (and `pyproject.toml`).
2. **Data** to the node: `cd ../server && foreman run push-data`. The pod runs as uid 10001 and the directory is
   mounted read-only, so the files must be world-readable (the task sets `D755,F644`).
3. `riveter --env cognio apply --scope all` (first time: namespace, service account and ingress are immutable).
4. Check: `curl https://ennor.ddns.net/cognio/index.json`.

## Day to day

* **New course version:** build the pack, `foreman run push-data` - nothing to restart.
* **Config:** `values.yaml` (`COGNIO_BASE_PATH`, `COGNIO_LOG_LEVEL`); commit, then `riveter --env cognio apply`.
  If `COGNIO_BASE_PATH` changes, change the ingress path in `ingress.yaml.j2` with it.
* **New server release:** `foreman run release` in `../server`.
