from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass
class Alerta:
    id_alerta: int | None
    fk_pessoa_id_pessoa: UUID
    parametro: str
    acao: str
    valor: float

    fk_meta_id_meta: int | None

    def __post_init__(self) -> None:
        if not self.parametro.strip():
            raise ValueError("parametro é obrigatório")
        if not self.acao.strip():
            raise ValueError("acao é obrigatória")
        if self.valor is None:
            raise ValueError("valor é obrigatório")
