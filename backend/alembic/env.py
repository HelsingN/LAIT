"""Alembic migration environment."""

from __future__ import annotations

from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine.url import make_url

from alembic import context
from lait.adapters.persistence.models import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _ensure_sqlite_directory(database_url: str | None) -> None:
    if not database_url:
        return
    parsed = make_url(database_url)
    if not parsed.drivername.startswith("sqlite"):
        return
    database = parsed.database
    if not database or database == ":memory:":
        return
    Path(database).parent.mkdir(parents=True, exist_ok=True)


def run_migrations_online() -> None:
    section = config.get_section(config.config_ini_section, {})
    _ensure_sqlite_directory(section.get("sqlalchemy.url"))
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
