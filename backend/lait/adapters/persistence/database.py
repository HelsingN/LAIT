"""Engine, WAL pragmas, migrations, and repository construction."""

from __future__ import annotations

from pathlib import Path

from alembic.config import Config
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import sessionmaker

from alembic import command
from lait.adapters.persistence.repositories import RepositoryBundle
from lait.application.ports import LessonRepository

_BACKEND_ROOT = Path(__file__).resolve().parents[3]
_ALEMBIC_INI = _BACKEND_ROOT / "alembic.ini"


def make_engine(database_url: str) -> Engine:
    _ensure_sqlite_directory(database_url)
    connect_args: dict[str, object] = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    engine = create_engine(database_url, connect_args=connect_args)
    if database_url.startswith("sqlite"):
        event.listen(engine, "connect", _set_sqlite_pragmas)
    return engine


def migrate(database_url: str) -> None:
    _ensure_sqlite_directory(database_url)
    config = Config(str(_ALEMBIC_INI))
    config.set_main_option("script_location", str(_BACKEND_ROOT / "alembic"))
    config.set_main_option("prepend_sys_path", str(_BACKEND_ROOT))
    config.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(config, "head")


def open_repository(database_url: str) -> LessonRepository:
    engine = make_engine(database_url)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    return RepositoryBundle(factory)


def _ensure_sqlite_directory(database_url: str) -> None:
    url = make_url(database_url)
    if not url.drivername.startswith("sqlite"):
        return
    database = url.database
    if not database or database == ":memory:":
        return
    Path(database).parent.mkdir(parents=True, exist_ok=True)


def _set_sqlite_pragmas(dbapi_connection, _connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()
