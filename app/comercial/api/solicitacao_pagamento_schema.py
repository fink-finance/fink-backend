from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class SolicitacaoPagamentoBase(BaseModel):
    fk_tipo_pagamento_id_pagamento: int = Field(..., description="ID do tipo de pagamento escolhido")
    fk_assinatura_id_assinatura: int = Field(..., description="ID da assinatura vinculada")
    data_hora: Optional[datetime] = Field(None, description="Data e hora da solicitação de pagamento")


class SolicitacaoPagamentoCreate(SolicitacaoPagamentoBase):
    # data_hora é opcional porque será preenchida automaticamente no service
    pass


class SolicitacaoPagamentoUpdate(BaseModel):
    fk_tipo_pagamento_id_pagamento: Optional[int] = None
    fk_assinatura_id_assinatura: Optional[int] = None
    data_hora: Optional[datetime] = None


class SolicitacaoPagamentoResponse(SolicitacaoPagamentoBase):
    id_solicitacao: int

    class Config:
        from_attributes = True
