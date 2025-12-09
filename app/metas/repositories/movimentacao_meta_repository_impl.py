from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.metas.persistence.movimentacao_meta_orm import MovimentacaoMetaORM
from app.metas.repositories.movimentacao_meta_repository import MovimentacaoMetaRepository


class MovimentacaoMetaRepositoryImpl(MovimentacaoMetaRepository):
    """Implementação concreta do repositório de MovimentacaoMeta."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id_movimentacao: int) -> MovimentacaoMetaORM | None:
        """Busca uma movimentação pelo ID."""
        return await self.session.get(MovimentacaoMetaORM, id_movimentacao)

    async def list_by_meta_id(self, id_meta: int) -> list[MovimentacaoMetaORM]:
        """Lista todas as movimentações de uma meta."""
        result = await self.session.execute(
            select(MovimentacaoMetaORM)
            .where(MovimentacaoMetaORM.fk_meta_id_meta == id_meta)
            .order_by(MovimentacaoMetaORM.data.desc(), MovimentacaoMetaORM.id_movimentacao.desc())
        )
        return list(result.scalars())

    async def add(self, movimentacao: MovimentacaoMetaORM) -> MovimentacaoMetaORM:
        """Adiciona uma nova movimentação."""
        self.session.add(movimentacao)
        await self.session.flush()
        await self.session.commit()
        return movimentacao

