from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.alertas.persistence.alerta_orm import AlertaORM
from app.alertas.repositories.alerta_repository import AlertaRepository


class AlertaRepositoryImpl(AlertaRepository):
    """Implementação concreta do repositório de Alerta."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id_alerta: int) -> AlertaORM | None:
        """Busca um alerta pelo ID."""
        return await self.session.get(AlertaORM, id_alerta)

    async def list_by_pessoa(self, id_pessoa: int) -> list[AlertaORM]:
        """Lista todos os alertas de uma pessoa específica."""
        result = await self.session.execute(select(AlertaORM).where(AlertaORM.fk_pessoa_id_pessoa == id_pessoa))
        return list(result.scalars())

    async def list_by_meta(self, id_meta: int) -> list[AlertaORM]:
        """Lista todos os alertas relacionados a uma meta."""
        result = await self.session.execute(select(AlertaORM).where(AlertaORM.fk_meta_id_meta == id_meta))
        return list(result.scalars())

    async def list_all(self) -> list[AlertaORM]:
        """Lista todos os alertas cadastrados."""
        result = await self.session.execute(select(AlertaORM))
        return list(result.scalars())

    async def add(self, alerta: AlertaORM) -> AlertaORM:
        """Adiciona um novo alerta."""
        self.session.add(alerta)
        await self.session.flush()
        return alerta

    async def update(self, alerta: AlertaORM) -> AlertaORM:
        """Atualiza um alerta existente."""
        merged = await self.session.merge(alerta)
        await self.session.flush()
        return merged

    async def delete(self, id_alerta: int) -> None:
        """Remove um alerta pelo ID."""
        await self.session.execute(delete(AlertaORM).where(AlertaORM.id_alerta == id_alerta))
        await self.session.flush()
