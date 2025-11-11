from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.comercial.persistence.tipo_pagamento_orm import TipoPagamentoORM
from app.comercial.repositories.tipo_pagamento_repository import TipoPagamentoRepository


class TipoPagamentoRepositoryImpl(TipoPagamentoRepository):
    """Implementação concreta do repositório de Tipo de Pagamento."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id_pagamento: int) -> TipoPagamentoORM | None:
        return await self.session.get(TipoPagamentoORM, id_pagamento)

    async def get_by_tipo(self, tipo_pagamento: str) -> TipoPagamentoORM | None:
        result = await self.session.execute(
            select(TipoPagamentoORM).where(TipoPagamentoORM.tipo_pagamento == tipo_pagamento)
        )
        return result.scalar_one_or_none()

    async def list_all(self) -> list[TipoPagamentoORM]:
        result = await self.session.execute(select(TipoPagamentoORM))
        return list(result.scalars().all())

    async def add(self, tipo_pagamento: TipoPagamentoORM) -> TipoPagamentoORM:
        try:
            self.session.add(tipo_pagamento)
            await self.session.flush()
            await self.session.commit()
            await self.session.refresh(tipo_pagamento)
            return tipo_pagamento
        except Exception as e:
            await self.session.rollback()
            raise ValueError(f"Erro ao criar tipo_pagamento: {str(e)}")

    async def delete(self, id_pagamento: int) -> None:
        try:
            await self.session.execute(delete(TipoPagamentoORM).where(TipoPagamentoORM.id_pagamento == id_pagamento))
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise ValueError(f"Erro ao deletar tipo_pagamento: {str(e)}")

    async def update(self, tipo_pagamento: TipoPagamentoORM) -> TipoPagamentoORM:
        try:
            merged = await self.session.merge(tipo_pagamento)
            await self.session.commit()
            return merged
        except Exception as e:
            await self.session.rollback()
            raise ValueError(f"Erro ao atualizar tipo_pagamento: {str(e)}")
