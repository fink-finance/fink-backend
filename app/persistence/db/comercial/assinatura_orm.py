from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import date
from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.persistence.db.identidade.pessoa_orm import PessoaORM
    from app.persistence.db.comercial.plano_orm import PlanoORM

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

    def __repr__(self) -> str:
        return f"<AssinaturaORM id={self.id_assinatura} pessoa={self.fk_pessoa_id_pessoa} plano={self.fk_plano_id_plano}>"
