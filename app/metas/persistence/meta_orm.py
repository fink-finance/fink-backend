from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base

if TYPE_CHECKING:
    from app.alertas.persistence.alerta_orm import AlertaORM
    from app.identidade.persistence.pessoa_orm import PessoaORM


class MetaORM(Base):
    __tablename__ = "meta"

    id_meta: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    fk_pessoa_id_pessoa: Mapped[int] = mapped_column(
        Integer, ForeignKey("pessoa.id_pessoa", ondelete="CASCADE"), nullable=False
    )

    titulo: Mapped[str] = mapped_column(String, nullable=False)
    descricao: Mapped[str] = mapped_column(String, nullable=False)
    valor_alvo: Mapped[float] = mapped_column(Float, nullable=False)
    valor_atual: Mapped[float] = mapped_column(Float, nullable=False)
    criada_em: Mapped[date] = mapped_column(Date, nullable=False)
    termina_em: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    pessoa: Mapped[PessoaORM] = relationship("PessoaORM", back_populates="metas")
    alertas: Mapped[list[AlertaORM]] = relationship("AlertaORM", back_populates="meta", passive_deletes=True)

    def __repr__(self) -> str:
        return f"<MetaORM id={self.id_meta} titulo={self.titulo}>"
