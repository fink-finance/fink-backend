from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class AssinaturaBase(BaseModel):
    fk_pessoa_id_pessoa: int = Field(..., description="ID da pessoa dona da assinatura")
    fk_plano_id_plano: int = Field(..., description="ID do plano assinado")
    comeca_em: date = Field(..., description="Data de início da assinatura")
    termina_em: date = Field(..., description="Data de término da assinatura")
    status: str = Field(..., description="Status da assinatura (ativa, cancelada, expirada, etc.)")


class AssinaturaCreate(AssinaturaBase):
    # se quiser deixar status opcional e defaultar para 'ativa' no service:
    status: Optional[str] = Field(default=None, description="Status inicial da assinatura")


class AssinaturaUpdate(BaseModel):
    fk_plano_id_plano: Optional[int] = None
    comeca_em: Optional[date] = None
    termina_em: Optional[date] = None
    status: Optional[str] = None


class AssinaturaResponse(AssinaturaBase):
    id_assinatura: int

    class Config:
        from_attributes = True
