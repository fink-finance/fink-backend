from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.shared.database import Base

if TYPE_CHECKING:
    from app.comercial.persistence.solicitacao_pagamento_orm import SolicitacaoPagamentoORM

class TipoPagamentoORM(Base):
    __tablename__ = "tipo_pagamento"

    id_pagamento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo_pagamento: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    # 1 TipoPagamento -> N SolicitacoesPagamento
    solicitacoes: Mapped[list["SolicitacaoPagamentoORM"]] = relationship(
        "SolicitacaoPagamentoORM", back_populates="tipo_pagamento"
    )

    def __repr__(self) -> str:
        return f"<TipoPagamentoORM id={self.id_pagamento} tipo={self.tipo_pagamento}>"
