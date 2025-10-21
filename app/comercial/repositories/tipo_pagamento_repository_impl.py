from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.comercial.persistence.tipo_pagamento_orm import TipoPagamentoORM
from app.comercial.repositories.tipo_pagamento_repository import TipoPagamentoRepository


class TipoPagamentoRepositoryImpl(TipoPagamentoRepository):
    """Implementação concreta do repositório de Tipo de Pagamento."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id_pagamento: int) -> TipoPagamentoORM | None:
        """Busca um tipo de pagamento pelo ID."""
        return await self.session.get(TipoPagamentoORM, id_pagamento)

    async def get_by_tipo(self, tipo_pagamento: str) -> TipoPagamentoORM | None:
        """Busca um tipo de pagamento pelo nome (ex: crédito, débito)."""
        result = await self.session.execute(
            select(TipoPagamentoORM).where(TipoPagamentoORM.tipo_pagamento == tipo_pagamento)
        )
        return result.scalar_one_or_none()

    async def list_all(self) -> list[TipoPagamentoORM]:
        """Lista todos os tipos de pagamento disponíveis."""
        result = await self.session.execute(select(TipoPagamentoORM))
        return result.scalars().all()

    async def add(self, tipo_pagamento: TipoPagamentoORM) -> TipoPagamentoORM:
        """Adiciona um novo tipo de pagamento."""
        self.session.add(tipo_pagamento)
        await self.session.flush()
        return tipo_pagamento

    async def delete(self, id_pagamento: int) -> None:
        """Remove um tipo de pagamento pelo ID."""
        await self.session.execute(delete(TipoPagamentoORM).where(TipoPagamentoORM.id_pagamento == id_pagamento))
