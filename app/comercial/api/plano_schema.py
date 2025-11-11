from pydantic import BaseModel, Field
from typing import Optional


class PlanoBase(BaseModel):
    titulo: str = Field(..., min_length=2, description="Título do plano")
    descricao: str
    preco: float = Field(..., gt=0, description="Preço mensal do plano")
    duracao_meses: int = Field(..., ge=1, description="Duração do plano em meses")
    status: str = Field(..., description="Status do plano (ativo/inativo)")


class PlanoCreate(PlanoBase):
    pass


class PlanoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = Field(None, gt=0)
    duracao_meses: Optional[int] = Field(None, ge=1)
    status: Optional[str] = None


class PlanoResponse(PlanoBase):
    id_plano: int

    class Config:
        from_attributes = True
