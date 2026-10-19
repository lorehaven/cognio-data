import hashlib
import json
import zipfile

import pytest
from starlette.testclient import TestClient

from cognio_server.app import create_app
from cognio_server.config import Settings


def make_pack(path, id="demo", version="1.0.0", **extra):
    manifest = {"formatVersion": "1.0", "id": id, "version": version, "language": "pl",
                "title": {"pl": "Demo"}, "engine": {"min": "1.0.0"}, **extra}
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("course.json", json.dumps(manifest))
        z.writestr("padding.txt", "x" * 5000)


@pytest.fixture
def data(tmp_path):
    (tmp_path / "courses").mkdir()
    (tmp_path / "models").mkdir()
    return tmp_path


def client(data, base_path=""):
    return TestClient(create_app(Settings(data, base_path, "127.0.0.1", 8080, "INFO")))


def test_healthz(data):
    assert client(data).get("/healthz").text == "ok"


def test_index_lists_packs_and_marks_latest(data):
    make_pack(data / "courses" / "demo-1.0.0.cognio", version="1.0.0")
    make_pack(data / "courses" / "demo-1.10.0.cognio", version="1.10.0")
    make_pack(data / "courses" / "demo-1.2.0.cognio", version="1.2.0")
    body = client(data).get("/index.json").json()
    assert [c["version"] for c in body["courses"]] == ["1.0.0", "1.2.0", "1.10.0"]  # semver order, not text order
    assert [c["latest"] for c in body["courses"]] == [False, False, True]
    first = body["courses"][0]
    raw = (data / "courses" / "demo-1.0.0.cognio").read_bytes()
    assert first["sha256"] == hashlib.sha256(raw).hexdigest() and first["size"] == len(raw)
    assert first["url"] == "courses/demo-1.0.0.cognio" and body["models"] is None


def test_invalid_files_are_ignored(data):
    (data / "courses" / "broken.cognio").write_bytes(b"not a zip")
    (data / "courses" / "notes.txt").write_text("hi")
    (data / "courses" / "Bad Name.cognio").write_bytes(b"x")
    with zipfile.ZipFile(data / "courses" / "nomanifest.cognio", "w") as z:
        z.writestr("other.json", "{}")
    assert client(data).get("/index.json").json()["courses"] == []


def test_index_sees_new_upload_without_restart(data):
    c = client(data)
    assert c.get("/index.json").json()["courses"] == []
    make_pack(data / "courses" / "demo-1.0.0.cognio")
    assert len(c.get("/index.json").json()["courses"]) == 1


def test_index_etag(data):
    make_pack(data / "courses" / "demo-1.0.0.cognio")
    c = client(data)
    etag = c.get("/index.json").headers["etag"]
    assert c.get("/index.json", headers={"If-None-Match": etag}).status_code == 304


def test_download_and_range(data):
    make_pack(data / "courses" / "demo-1.0.0.cognio")
    raw = (data / "courses" / "demo-1.0.0.cognio").read_bytes()
    c = client(data)
    r = c.get("/courses/demo-1.0.0.cognio")
    assert r.status_code == 200 and r.content == raw
    assert r.headers["content-type"] == "application/vnd.cognio+zip"
    part = c.get("/courses/demo-1.0.0.cognio", headers={"Range": "bytes=100-199"})
    assert part.status_code == 206 and part.content == raw[100:200]


@pytest.mark.parametrize("name", ["missing.cognio", "..%2F..%2Fetc%2Fpasswd", "%2e%2e/x.cognio", "broken.cognio", "a.txt"])
def test_other_names_are_404(data, name):
    (data / "courses" / "broken.cognio").write_bytes(b"not a zip")
    assert client(data).get(f"/courses/{name}").status_code == 404


def test_models_catalog(data):
    c = client(data)
    assert c.get("/models/catalog.json").status_code == 404
    (data / "models" / "catalog.json").write_text('{"models": []}')
    assert c.get("/models/catalog.json").json() == {"models": []}
    assert c.get("/index.json").json()["models"] == "models/catalog.json"


def test_base_path(data):
    make_pack(data / "courses" / "demo-1.0.0.cognio")
    c = client(data, "/cognio")
    assert c.get("/cognio/healthz").status_code == 200
    assert c.get("/cognio/courses/demo-1.0.0.cognio").status_code == 200
    assert c.get("/healthz").status_code == 404
