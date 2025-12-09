from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base

if TYPE_CHECKING:
    from app.metas.persistence.meta_orm import MetaORM


class MovimentacaoMetaORM(Base):
    __tablename__ = "movimentacao_meta"

    id_movimentacao: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    fk_meta_id_meta: Mapped[int] = mapped_column(
        Integer, ForeignKey("meta.id_meta", ondelete="CASCADE"), nullable=False
    )

    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    acao: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint("acao IN ('adicionado', 'retirado')"),
        nullable=False,
    )
    data: Mapped[date] = mapped_column(Date, nullable=False)

    meta: Mapped["MetaORM"] = relationship("MetaORM", back_populates="movimentacoes")

    def __repr__(self) -> str:
        return f"<MovimentacaoMetaORM id={self.id_movimentacao} acao={self.acao} valor={self.valor}>"

