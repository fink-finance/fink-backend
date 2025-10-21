"""ORM models do módulo Metas."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.metas.persistence.meta_orm import MetaORM

__all__ = ["MetaORM"]
