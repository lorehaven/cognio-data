import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    base_path: str  # "" or "/prefix": the app serves everything under it, the ingress does not rewrite
    host: str
    port: int
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        base = os.environ.get("BASE_PATH", "").strip().rstrip("/")
        if base and not base.startswith("/"):
            base = "/" + base
        return cls(
            data_dir=Path(os.environ.get("DATA_DIR", "./data")),
            base_path=base,
            host=os.environ.get("HOST", "0.0.0.0"),
            port=int(os.environ.get("PORT", "8080")),
            log_level=os.environ.get("LOG_LEVEL", "INFO").upper(),
        )
