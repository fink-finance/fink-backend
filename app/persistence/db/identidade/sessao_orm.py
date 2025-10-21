from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.persistence.db.identidade.pessoa_orm import PessoaORM


class SessaoORM(Base):
    __tablename__ = "sessao"

    id_sessao: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    fk_pessoa_id_pessoa: Mapped[int] = mapped_column(
        Integer, ForeignKey("pessoa.id_pessoa", ondelete="CASCADE"), nullable=False
    )

    token_hash: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    criada_em: Mapped[date] = mapped_column(Date, nullable=False)
    expira_em: Mapped[date] = mapped_column(Date, nullable=False)

    pessoa: Mapped[PessoaORM] = relationship("PessoaORM", back_populates="sessoes")

    def __repr__(self) -> str:
        return f"<SessaoORM id={self.id_sessao} token={self.token_hash[:10]}...>"
