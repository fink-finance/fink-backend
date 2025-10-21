from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.comercial.persistence.assinatura_orm import AssinaturaORM
from app.comercial.repositories.assinatura_repository import AssinaturaRepository


class AssinaturaRepositoryImpl(AssinaturaRepository):
    """Implementação concreta do repositório de Assinatura."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id_assinatura: int) -> AssinaturaORM | None:
        """Busca uma assinatura pelo ID."""
        return await self.session.get(AssinaturaORM, id_assinatura)

    async def list_by_pessoa(self, id_pessoa: int) -> list[AssinaturaORM]:
        """Lista todas as assinaturas de uma pessoa."""
        result = await self.session.execute(
            select(AssinaturaORM).where(AssinaturaORM.fk_pessoa_id_pessoa == id_pessoa)
        )
        return result.scalars().all()

    async def list_by_plano(self, id_plano: int) -> list[AssinaturaORM]:
        """Lista todas as assinaturas de um plano específico."""
        result = await self.session.execute(
            select(AssinaturaORM).where(AssinaturaORM.fk_plano_id_plano == id_plano)
        )
        return result.scalars().all()

    async def list_all(self) -> list[AssinaturaORM]:
        """Lista todas as assinaturas cadastradas."""
        result = await self.session.execute(select(AssinaturaORM))
        return result.scalars().all()

    async def add(self, assinatura: AssinaturaORM) -> AssinaturaORM:
        """Cria uma nova assinatura."""
        self.session.add(assinatura)
        await self.session.flush()
        return assinatura

    async def update(self, assinatura: AssinaturaORM) -> AssinaturaORM:
        """Atualiza uma assinatura existente."""
        await self.session.merge(assinatura)
        await self.session.flush()
        return assinatura

    async def delete(self, id_assinatura: int) -> None:
        """Remove uma assinatura pelo ID."""
        await self.session.execute(
            delete(AssinaturaORM).where(AssinaturaORM.id_assinatura == id_assinatura)
        )
