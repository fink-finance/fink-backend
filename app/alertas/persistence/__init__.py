"""ORM models do módulo Alertas."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.alertas.persistence.alerta_orm import AlertaORM

__all__ = ["AlertaORM"]
