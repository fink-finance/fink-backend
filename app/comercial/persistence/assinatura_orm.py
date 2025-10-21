from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base


class AssinaturaORM(Base):
    __tablename__ = "assinatura"

    id_assinatura: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    fk_pessoa_id_pessoa: Mapped[int] = mapped_column(
        Integer, ForeignKey("pessoa.id_pessoa", ondelete="CASCADE"), nullable=False
    )
    fk_plano_id_plano: Mapped[int] = mapped_column(
        Integer, ForeignKey("plano.id_plano", ondelete="CASCADE"), nullable=False
    )

    comeca_em: Mapped[date] = mapped_column(Date, nullable=False)
    termina_em: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    pessoa: Mapped["PessoaORM"] = relationship("PessoaORM", back_populates="assinaturas")
    plano: Mapped["PlanoORM"] = relationship("PlanoORM", back_populates="assinaturas")
    solicitacao_pagamento: Mapped["SolicitacaoPagamentoORM | None"] = relationship(
        "SolicitacaoPagamentoORM", back_populates="assinatura", uselist=False
    )

    def __repr__(self) -> str:
        return (
            f"<AssinaturaORM id={self.id_assinatura} pessoa={self.fk_pessoa_id_pessoa} plano={self.fk_plano_id_plano}>"
        )
