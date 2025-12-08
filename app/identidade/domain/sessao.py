"""Domain model for Sessao."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass
class Sessao:
    """Representa uma sessão de autenticação de um usuário."""

    id_sessao: int | None
    fk_pessoa_id_pessoa: UUID
    token_hash: str
    criada_em: date
    expira_em: date

    def __post_init__(self) -> None:
        if not self.token_hash or not self.token_hash.strip():
            raise ValueError("token_hash é obrigatório")
        if not self.fk_pessoa_id_pessoa:
            raise ValueError("fk_pessoa_id_pessoa é obrigatório")
