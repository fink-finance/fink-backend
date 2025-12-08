from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import CheckConstraint, Date, Numeric, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base

if TYPE_CHECKING:
    from app.identidade.persistence.pessoa_orm import PessoaORM
    from app.alertas.persistence.alerta_orm import AlertaORM


class MetaORM(Base):
    __tablename__ = "meta"

    id_meta: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    fk_pessoa_id_pessoa: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), ForeignKey("pessoa.id_pessoa", ondelete="CASCADE"), nullable=False
    )

    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    categoria: Mapped[str] = mapped_column(String(500), nullable=False)
    valor_alvo: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    valor_atual: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    criada_em: Mapped[date] = mapped_column(Date, nullable=False)
    termina_em: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint("status IN ('em_andamento', 'concluida', 'cancelada', 'atrasada')"),
        nullable=False,
    )

    pessoa: Mapped["PessoaORM"] = relationship("PessoaORM", back_populates="metas")
    alertas: Mapped[list["AlertaORM"]] = relationship("AlertaORM", back_populates="meta", passive_deletes=True)

    def __repr__(self) -> str:
        return f"<MetaORM id={self.id_meta} titulo={self.titulo}>"
