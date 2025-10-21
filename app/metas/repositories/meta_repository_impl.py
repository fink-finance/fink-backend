from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.metas.persistence.meta_orm import MetaORM
from app.metas.repositories.meta_repository import MetaRepository


class MetaRepositoryImpl(MetaRepository):
    """Implementação concreta do repositório de Meta."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id_meta: int) -> MetaORM | None:
        """Busca uma meta pelo ID."""
        return await self.session.get(MetaORM, id_meta)

    async def list_by_pessoa(self, id_pessoa: int) -> list[MetaORM]:
        """Lista todas as metas de uma pessoa."""
        result = await self.session.execute(
            select(MetaORM).where(MetaORM.fk_pessoa_id_pessoa == id_pessoa)
        )
        return result.scalars().all()

    async def list_all(self) -> list[MetaORM]:
        """Lista todas as metas cadastradas."""
        result = await self.session.execute(select(MetaORM))
        return result.scalars().all()

    async def add(self, meta: MetaORM) -> MetaORM:
        """Adiciona uma nova meta."""
        self.session.add(meta)
        await self.session.flush()
        return meta

    async def update(self, meta: MetaORM) -> MetaORM:
        """Atualiza uma meta existente."""
        await self.session.merge(meta)
        await self.session.flush()
        return meta

    async def delete(self, id_meta: int) -> None:
        """Remove uma meta pelo ID."""
        await self.session.execute(
            delete(MetaORM).where(MetaORM.id_meta == id_meta)
        )
