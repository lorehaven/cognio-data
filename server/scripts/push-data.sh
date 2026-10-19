#!/usr/bin/env bash
# Copies the built course packs and the model catalog to the node's data directory (DATA_REMOTE=host:/dir).
set -e
cd "$(dirname "$0")/.."
remote="${DATA_REMOTE:-ossiriand.arda:/mnt/dev/cognio/data}"
host="${remote%%:*}"; dir="${remote#*:}"
ssh "$host" "mkdir -p '$dir/courses' '$dir/models'"
rsync -av --chmod=D755,F644 ../dist/courses/*.cognio "$remote/courses/"
rsync -av --chmod=D755,F644 ../dist/models/catalog.json "$remote/models/"
