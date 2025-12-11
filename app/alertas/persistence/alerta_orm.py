from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base


class AlertaORM(Base):
    __tablename__ = "alerta"

    id_alerta: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    fk_pessoa_id_pessoa: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), ForeignKey("pessoa.id_pessoa", ondelete="CASCADE"), nullable=False
    )

    data: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    conteudo: Mapped[str] = mapped_column(String, nullable=False)
    lida: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    pessoa: Mapped["PessoaORM"] = relationship("PessoaORM", back_populates="alertas")

    def __repr__(self) -> str:
        return f"<AlertaORM id={self.id_alerta} conteudo={self.conteudo[:30]}... lida={self.lida}>"
