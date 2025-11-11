from pydantic import BaseModel
from typing import Optional


class AlertaBase(BaseModel):
    parametro: str
    acao: str
    valor: float
    fk_pessoa_id_pessoa: int
    fk_meta_id_meta: Optional[int] = None


class AlertaCreate(AlertaBase):
    pass


class AlertaUpdate(BaseModel):
    parametro: Optional[str] = None
    acao: Optional[str] = None
    valor: Optional[float] = None
    fk_pessoa_id_pessoa: Optional[int] = None
    fk_meta_id_meta: Optional[int] = None


class AlertaResponse(AlertaBase):
    id_alerta: int

    class Config:
        from_attributes = True
