from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Alerta:
    id_alerta: int | None
    fk_pessoa_id_pessoa: UUID
    data: datetime
    conteudo: str
    lida: bool

    def __post_init__(self) -> None:
        if not self.conteudo.strip():
            raise ValueError("conteudo é obrigatório")
