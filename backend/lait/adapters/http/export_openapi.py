"""Write the FastAPI OpenAPI 3.1 document consumed by the TypeScript client generator.

No provider credentials are read or written. The document is the public HTTP contract only.
"""

from __future__ import annotations

import json
from pathlib import Path

from lait.adapters.http.app import create_app

_REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OPENAPI_PATH = _REPO_ROOT / "frontend" / "openapi.json"


def export_openapi(destination: Path | None = None) -> Path:
    target = destination or DEFAULT_OPENAPI_PATH
    schema = create_app("sqlite:///:memory:").openapi()
    version = str(schema.get("openapi", ""))
    if not version.startswith("3.1"):
        raise RuntimeError(f"expected OpenAPI 3.1, got {version!r}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
    return target


def main() -> None:
    export_openapi()


if __name__ == "__main__":
    main()
