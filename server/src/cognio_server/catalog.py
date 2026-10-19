"""Scans <data>/courses/*.cognio and builds the index the Cognio app downloads from.

A .cognio file is a ZIP with course.json at its root (docs/02-course-format.md). Only course.json is read;
the file's sha256 is cached per (name, mtime, size), so a rescan after a new upload hashes just that file.
"""
import hashlib
import json
import logging
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger("cognio.catalog")

PACK_NAME = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}\.cognio$")
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


@dataclass(frozen=True)
class Pack:
    name: str
    id: str
    version: str
    format_version: str
    language: str
    title: dict
    engine: dict
    size: int
    sha256: str


def _semver_key(v: str) -> tuple:
    m = SEMVER.match(v)
    return tuple(int(x) for x in m.groups()) if m else (-1, -1, -1)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_manifest(path: Path) -> dict:
    with zipfile.ZipFile(path) as z:
        manifest = json.loads(z.read("course.json"))
    for key in ("id", "version", "formatVersion", "language", "title"):
        if key not in manifest:
            raise ValueError(f"course.json has no '{key}'")
    if not SEMVER.match(str(manifest["version"])):
        raise ValueError(f"version '{manifest['version']}' is not x.y.z")
    return manifest


class Catalog:
    def __init__(self, data_dir: Path):
        self.courses_dir = data_dir / "courses"
        self.models_catalog = data_dir / "models" / "catalog.json"
        self._cache: dict[tuple, Pack | None] = {}  # (name, mtime_ns, size) -> Pack, or None if the file is invalid

    def pack_path(self, name: str) -> Path | None:
        """Path of a served pack, or None. Only names that pass the filter and are indexed are served."""
        if not PACK_NAME.match(name):
            return None
        p = self.courses_dir / name
        return p if p.is_file() and any(x.name == name for x in self.packs()) else None

    def packs(self) -> list[Pack]:
        found, live = [], set()
        if self.courses_dir.is_dir():
            for p in sorted(self.courses_dir.iterdir()):
                if not (p.is_file() and PACK_NAME.match(p.name)):
                    continue
                st = p.stat()
                key = (p.name, st.st_mtime_ns, st.st_size)
                live.add(key)
                if key not in self._cache:
                    self._cache[key] = self._load(p, st.st_size)
                if self._cache[key]:
                    found.append(self._cache[key])
        for key in set(self._cache) - live:
            del self._cache[key]
        return found

    @staticmethod
    def _load(path: Path, size: int) -> Pack | None:
        try:
            m = _read_manifest(path)
            return Pack(path.name, m["id"], m["version"], m["formatVersion"], m["language"], m["title"],
                        m.get("engine", {}), size, _sha256(path))
        except (OSError, KeyError, ValueError, zipfile.BadZipFile) as e:
            log.warning("ignoring %s: %s", path.name, e)
            return None

    def index(self) -> dict:
        packs = sorted(self.packs(), key=lambda p: (p.id, _semver_key(p.version)))
        newest: dict[str, str] = {}
        for p in packs:
            newest[p.id] = p.version  # sorted ascending, so the last one wins
        return {
            "formatVersion": "1.0",
            "courses": [
                {"id": p.id, "version": p.version, "latest": newest[p.id] == p.version, "title": p.title,
                 "language": p.language, "formatVersion": p.format_version, "engine": p.engine,
                 "size": p.size, "sha256": p.sha256, "url": f"courses/{p.name}"}
                for p in packs
            ],
            "models": "models/catalog.json" if self.models_catalog.is_file() else None,
        }
