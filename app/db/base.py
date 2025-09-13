"""SQLAlchemy Declarative Base for ORM models."""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):  # type: ignore[misc]
    """Base class for all ORM models."""

    pass
