from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.shared.database import Base

if TYPE_CHECKING:
    from app.comercial.persistence.assinatura_orm import AssinaturaORM


class PlanoORM(Base):
    __tablename__ = "plano"

    id_plano: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    descricao: Mapped[str] = mapped_column(String, nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    duracao_meses: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    # 1 Plano -> N Assinaturas
    assinaturas: Mapped[list["AssinaturaORM"]] = relationship(
        "AssinaturaORM", back_populates="plano", cascade="all, delete-orphan", passive_deletes=True
    )

    def __repr__(self) -> str:
        return f"<PlanoORM id={self.id_plano} titulo={self.titulo} preco={self.preco}>"
