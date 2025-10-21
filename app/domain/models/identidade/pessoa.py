from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class Pessoa:
    id_pessoa: int | None
    email: str
    senha: str
    nome: str
    data_nascimento: date
    telefone: str
    genero: str
    estado: str
    cidade: str
    rua: str
    numero: str
    cep: str
    data_criacao: date
    admin: bool

    def __post_init__(self) -> None:
        for field_name, value in [
            ("email", self.email),
            ("senha", self.senha),
            ("nome", self.nome),
            ("telefone", self.telefone),
            ("genero", self.genero),
            ("estado", self.estado),
            ("cidade", self.cidade),
            ("rua", self.rua),
            ("numero", self.numero),
            ("cep", self.cep),
        ]:
            if value is None or (isinstance(value, str) and value.strip() == ""):
                raise ValueError(f"{field_name} é obrigatório")
