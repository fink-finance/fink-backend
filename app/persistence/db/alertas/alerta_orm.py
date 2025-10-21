from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.persistence.db.identidade.pessoa_orm import PessoaORM
    from app.persistence.db.metas.meta_orm import MetaORM


class AlertaORM(Base):
    __tablename__ = "alerta"

    id_alerta: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    fk_pessoa_id_pessoa: Mapped[int] = mapped_column(
        Integer, ForeignKey("pessoa.id_pessoa", ondelete="CASCADE"), nullable=False
    )

    parametro: Mapped[str] = mapped_column(String, nullable=False)
    acao: Mapped[str] = mapped_column(String, nullable=False)
    valor: Mapped[float] = mapped_column(Float, nullable=False)

    fk_meta_id_meta: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("meta.id_meta", ondelete="SET NULL"), nullable=True
    )

    pessoa: Mapped["PessoaORM"] = relationship("PessoaORM", back_populates="alertas")
    meta: Mapped["MetaORM | None"] = relationship("MetaORM", back_populates="alertas")

    def __repr__(self) -> str:
        return f"<AlertaORM id={self.id_alerta} parametro={self.parametro} acao={self.acao} valor={self.valor}>"
