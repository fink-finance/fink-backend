from __future__ import annotations
from pydantic import BaseModel, EmailStr
from datetime import date


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class SessaoCriadaResponse(BaseModel):
    """Resposta do login: retorna o token em claro uma única vez."""

    id_sessao: int
    fk_pessoa_id_pessoa: int
    token: str
    criada_em: date
    expira_em: date

    class Config:
        from_attributes = True


class SessaoResponse(BaseModel):
    id_sessao: int
    fk_pessoa_id_pessoa: int
    criada_em: date
    expira_em: date

    class Config:
        from_attributes = True
