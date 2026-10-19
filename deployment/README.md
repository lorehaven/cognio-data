# deployment (cognio-server on the home cluster)

riveter overlays for Cognio, in the style of `homecloud` and `kindle-deployment`. One overlay today:

| Overlay | Package | What |
|---|---|---|
| [`overlays/cognio`](overlays/cognio/README.md) | `cognio` | `cognio-server` - serves course packs and the model catalog at `https://ennor.ddns.net/cognio/` |

```sh
riveter --env cognio render --scope all     # write manifests/ (gitignored)
riveter --env cognio apply  --scope all     # apply to the cluster
riveter --env cognio pack --no-pin          # build a .rivet package
```

To publish through homecloud's pipeline instead, add `cognio` to homecloud's `.conveyor.toml` (check + publish jobs) and move the
overlay under `homecloud/overlays/`; nothing in the overlay is specific to this repository.
