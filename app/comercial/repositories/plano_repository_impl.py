from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.comercial.persistence.plano_orm import PlanoORM
from app.comercial.repositories.plano_repository import PlanoRepository


class PlanoRepositoryImpl(PlanoRepository):
    """Implementação concreta do repositório de Plano."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id_plano: int) -> PlanoORM | None:
        """Busca um plano pelo ID."""
        return await self.session.get(PlanoORM, id_plano)

    async def get_by_titulo(self, titulo: str) -> PlanoORM | None:
        """Busca um plano pelo título."""
        result = await self.session.execute(select(PlanoORM).where(PlanoORM.titulo == titulo))
        return result.scalar_one_or_none()

    async def list_all(self) -> list[PlanoORM]:
        """Lista todos os planos disponíveis."""
        result = await self.session.execute(select(PlanoORM))
        return result.scalars().all()

    async def add(self, plano: PlanoORM) -> PlanoORM:
        """Adiciona um novo plano ao banco."""
        self.session.add(plano)
        await self.session.flush()
        return plano

    async def update(self, plano: PlanoORM) -> PlanoORM:
        """Atualiza um plano existente."""
        await self.session.merge(plano)
        await self.session.flush()
        return plano

    async def delete(self, id_plano: int) -> None:
        """Remove um plano pelo ID."""
        await self.session.execute(delete(PlanoORM).where(PlanoORM.id_plano == id_plano))
