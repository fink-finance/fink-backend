from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class PessoaBase(BaseModel):
    email: EmailStr
    nome: str
    data_nascimento: date
    telefone: str
    genero: str
    estado: str
    cidade: str
    rua: str
    numero: str
    cep: str


class PessoaCreate(PessoaBase):
    senha: str


class PessoaUpdate(BaseModel):
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    estado: Optional[str] = None
    cidade: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[str] = None
    cep: Optional[str] = None
    senha: Optional[str] = None


class PessoaResponse(PessoaBase):
    id_pessoa: int
    data_criacao: date
    admin: bool = False

    class Config:
        from_attributes = True
