import logging

import uvicorn

from .app import create_app
from .config import Settings


def main() -> None:
    settings = Settings.from_env()
    logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    logging.getLogger("cognio").info("serving %s under '%s/'", settings.data_dir.resolve(), settings.base_path)
    uvicorn.run(create_app(settings), host=settings.host, port=settings.port, log_level=settings.log_level.lower())


if __name__ == "__main__":
    main()
