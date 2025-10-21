from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.comercial.persistence.solicitacao_pagamento_orm import SolicitacaoPagamentoORM
from app.comercial.repositories.solicitacao_pagamento_repository import SolicitacaoPagamentoRepository


class SolicitacaoPagamentoRepositoryImpl(SolicitacaoPagamentoRepository):
    """Implementação concreta do repositório de Solicitação de Pagamento."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id_solicitacao: int) -> SolicitacaoPagamentoORM | None:
        """Busca uma solicitação pelo ID."""
        return await self.session.get(SolicitacaoPagamentoORM, id_solicitacao)

    async def list_by_assinatura(self, id_assinatura: int) -> list[SolicitacaoPagamentoORM]:
        """Lista solicitações relacionadas a uma assinatura."""
        result = await self.session.execute(
            select(SolicitacaoPagamentoORM).where(
                SolicitacaoPagamentoORM.fk_assinatura_id_assinatura == id_assinatura
            )
        )
        return result.scalars().all()

    async def list_all(self) -> list[SolicitacaoPagamentoORM]:
        """Lista todas as solicitações de pagamento."""
        result = await self.session.execute(select(SolicitacaoPagamentoORM))
        return result.scalars().all()

    async def add(self, solicitacao: SolicitacaoPagamentoORM) -> SolicitacaoPagamentoORM:
        """Adiciona uma nova solicitação."""
        self.session.add(solicitacao)
        await self.session.flush()
        return solicitacao

    async def update(self, solicitacao: SolicitacaoPagamentoORM) -> SolicitacaoPagamentoORM:
        """Atualiza uma solicitação existente."""
        await self.session.merge(solicitacao)
        await self.session.flush()
        return solicitacao

    async def delete(self, id_solicitacao: int) -> None:
        """Remove uma solicitação de pagamento pelo ID."""
        await self.session.execute(
            delete(SolicitacaoPagamentoORM).where(
                SolicitacaoPagamentoORM.id_solicitacao == id_solicitacao
            )
        )
