"""Start the API only after Alembic upgrade head succeeds.

/health is served by uvicorn. This process does not listen until migrate()
returns, so a Compose healthcheck cannot pass on an unmigrated database.
"""

from __future__ import annotations

import os
import sys

from lait.adapters.persistence.database import migrate


def main() -> None:
    database_url = os.environ.get("LAIT_DATABASE_URL")
    if not database_url:
        print("LAIT_DATABASE_URL is required", file=sys.stderr)
        raise SystemExit(1)
    migrate(database_url)
    os.execvp(
        "uvicorn",
        [
            "uvicorn",
            "lait.adapters.http.app:create_app",
            "--factory",
            "--app-dir",
            "backend",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
        ],
    )


if __name__ == "__main__":
    main()
