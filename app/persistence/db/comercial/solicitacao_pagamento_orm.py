from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.persistence.db.comercial.assinatura_orm import AssinaturaORM
    from app.persistence.db.comercial.tipo_pagamento_orm import TipoPagamentoORM

class SolicitacaoPagamentoORM(Base):
    __tablename__ = "solicitacao_pagamento"
    __table_args__ = (
        UniqueConstraint("fk_assinatura_id_assinatura", name="uq_solicitacao_por_assinatura"),
    )

    id_solicitacao: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    fk_tipo_pagamento_id_pagamento: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tipo_pagamento.id_pagamento", ondelete="RESTRICT"),
        nullable=False,
    )

    fk_assinatura_id_assinatura: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("assinatura.id_assinatura", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    data_hora: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    tipo_pagamento: Mapped["TipoPagamentoORM"] = relationship(
        "TipoPagamentoORM", back_populates="solicitacoes"
    )
    assinatura: Mapped["AssinaturaORM"] = relationship(
        "AssinaturaORM", back_populates="solicitacao_pagamento", uselist=False
    )

    def __repr__(self) -> str:
        return f"<SolicitacaoPagamentoORM id={self.id_solicitacao} assinatura={self.fk_assinatura_id_assinatura}>"
