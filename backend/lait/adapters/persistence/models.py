"""SQLite tables owned by the persistence adapter."""

from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class LessonRow(Base):
    __tablename__ = "lessons"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
