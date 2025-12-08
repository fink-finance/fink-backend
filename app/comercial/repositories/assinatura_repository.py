"""Interface do repositório de Assinatura."""

from collections.abc import Iterable
from typing import Protocol
from uuid import UUID

from app.comercial.persistence.assinatura_orm import AssinaturaORM


class AssinaturaRepository(Protocol):
    """Contrato para operações relacionadas às assinaturas."""

    async def get_by_id(self, id_assinatura: int) -> AssinaturaORM | None:
        """Busca assinatura por ID."""
        ...

    async def list_by_pessoa(self, id_pessoa: UUID) -> Iterable[AssinaturaORM]:
        """Lista assinaturas por pessoa."""
        ...

    async def list_by_plano(self, id_plano: int) -> Iterable[AssinaturaORM]:
        """Lista assinaturas por plano."""
        ...

    async def list_all(self) -> Iterable[AssinaturaORM]:
        """Lista todas as assinaturas."""
        ...

    async def add(self, assinatura: AssinaturaORM) -> AssinaturaORM:
        """Adiciona nova assinatura."""
        ...

    async def update(self, assinatura: AssinaturaORM) -> AssinaturaORM:
        """Atualiza assinatura existente."""
        ...

    async def delete(self, id_assinatura: int) -> None:
        """Deleta assinatura por ID."""
        ...
