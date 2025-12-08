from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.identidade.persistence.sessao_orm import SessaoORM
from app.identidade.repositories.sessao_repository import SessaoRepository


class SessaoRepositoryImpl(SessaoRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, sessao: SessaoORM) -> SessaoORM:
        try:
            self.session.add(sessao)
            await self.session.flush()
            await self.session.commit()
            await self.session.refresh(sessao)
            return sessao
        except Exception as e:
            await self.session.rollback()
            raise ValueError(f"Erro ao criar sessão: {str(e)}")

    async def get_by_id(self, id_sessao: int) -> SessaoORM | None:
        res = await self.session.execute(select(SessaoORM).where(SessaoORM.id_sessao == id_sessao))
        return res.scalar_one_or_none()

    async def get_by_token_hash(self, token_hash: str) -> SessaoORM | None:
        res = await self.session.execute(select(SessaoORM).where(SessaoORM.token_hash == token_hash))
        return res.scalar_one_or_none()

    async def list_by_pessoa(self, id_pessoa: UUID) -> list[SessaoORM]:
        res = await self.session.execute(
            select(SessaoORM).where(SessaoORM.fk_pessoa_id_pessoa == id_pessoa).order_by(SessaoORM.criada_em.desc())
        )
        return list(res.scalars().all())

    async def delete_by_id(self, id_sessao: int) -> None:
        await self.session.execute(delete(SessaoORM).where(SessaoORM.id_sessao == id_sessao))
        await self.session.commit()

    async def delete_by_token_hash(self, token_hash: str) -> None:
        await self.session.execute(delete(SessaoORM).where(SessaoORM.token_hash == token_hash))
        await self.session.commit()

    async def delete_all_for_pessoa(self, id_pessoa: UUID) -> int:
        res = await self.session.execute(delete(SessaoORM).where(SessaoORM.fk_pessoa_id_pessoa == id_pessoa))
        await self.session.commit()
        return res.rowcount or 0

    async def purge_expired(self) -> int:
        today = date.today()
        res = await self.session.execute(delete(SessaoORM).where(SessaoORM.expira_em < today))
        await self.session.commit()
        return res.rowcount or 0
