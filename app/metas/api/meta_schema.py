from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class MetaBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=100)
    descricao: str = Field(..., min_length=1, max_length=500)
    valor_alvo: Decimal = Field(gt=0)
    termina_em: date
    fk_pessoa_id_pessoa: int = Field(gt=0)


class MetaCreate(MetaBase):
    """Schema para criação de meta."""

    valor_atual: Decimal = Decimal("0")
    status: str = "em_andamento"


class MetaUpdate(BaseModel):
    """Schema para atualização parcial de meta.

    Não permite alterar: fk_pessoa_id_pessoa e criada_em
    """

    titulo: Optional[str] = Field(None, min_length=1, max_length=100)
    descricao: Optional[str] = Field(None, min_length=1, max_length=500)
    valor_alvo: Optional[Decimal] = Field(None, gt=0)
    valor_atual: Optional[Decimal] = Field(None, ge=0)
    termina_em: Optional[date] = None
    status: Optional[str] = Field(None, pattern=r"^(em_andamento|concluida|cancelada|atrasada)$")


class MetaResponse(MetaBase):
    """Schema para respostas da API."""

    id_meta: int = Field(gt=0)
    valor_atual: Decimal = Field(ge=0)
    criada_em: date
    status: str = Field(pattern=r"^(em_andamento|concluida|cancelada|atrasada)$")

    class Config:
        from_attributes = True
