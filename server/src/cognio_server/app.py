import hashlib
import json
import logging

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, PlainTextResponse, Response
from starlette.routing import Mount, Route

from .catalog import Catalog
from .config import Settings

log = logging.getLogger("cognio")

PACK_MEDIA_TYPE = "application/vnd.cognio+zip"


def create_app(settings: Settings) -> Starlette:
    catalog = Catalog(settings.data_dir)

    async def healthz(request: Request) -> Response:
        return PlainTextResponse("ok")

    async def index(request: Request) -> Response:
        body = json.dumps(catalog.index(), ensure_ascii=False, sort_keys=True).encode()
        etag = '"' + hashlib.sha256(body).hexdigest()[:32] + '"'
        headers = {"ETag": etag, "Cache-Control": "no-cache"}
        if request.headers.get("if-none-match") == etag:
            return Response(status_code=304, headers=headers)
        return Response(body, media_type="application/json", headers=headers)

    async def course(request: Request) -> Response:
        path = catalog.pack_path(request.path_params["name"])
        if path is None:
            return PlainTextResponse("not found", status_code=404)
        # FileResponse brings Range (resumable downloads), ETag/Last-Modified and conditional requests.
        return FileResponse(path, media_type=PACK_MEDIA_TYPE, filename=path.name,
                            headers={"Cache-Control": "public, max-age=300"})

    async def models(request: Request) -> Response:
        if not catalog.models_catalog.is_file():
            return PlainTextResponse("not found", status_code=404)
        return FileResponse(catalog.models_catalog, media_type="application/json",
                            headers={"Cache-Control": "no-cache"})

    routes = [
        Route("/healthz", healthz),
        Route("/index.json", index),
        Route("/courses/{name}", course),
        Route("/models/catalog.json", models),
    ]
    if settings.base_path:
        routes = [Mount(settings.base_path, routes=routes)]
    return Starlette(routes=routes)
