from __future__ import annotations

from pydantic import BaseModel
from typing import Optional


class TipoPagamentoBase(BaseModel):
    tipo_pagamento: str


class TipoPagamentoCreate(TipoPagamentoBase):
    pass


class TipoPagamentoUpdate(BaseModel):
    tipo_pagamento: Optional[str] = None


class TipoPagamentoResponse(TipoPagamentoBase):
    id_pagamento: int

    class Config:
        from_attributes = True
