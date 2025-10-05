from __future__ import annotations
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class TipoPagamentoORM(Base):
    __tablename__ = "tipo_pagamento"

    id_pagamento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo_pagamento: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<TipoPagamentoORM id={self.id_pagamento} tipo={self.tipo_pagamento}>"
