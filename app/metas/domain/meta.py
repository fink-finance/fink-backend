from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class Meta:
    id_meta: int | None
    fk_pessoa_id_pessoa: int
    titulo: str
    descricao: str
    valor_alvo: float
    valor_atual: float
    criada_em: date
    termina_em: date
    status: str

    def __post_init__(self) -> None:
        if not self.titulo.strip():
            raise ValueError("Título é obrigatório")
        if not self.descricao.strip():
            raise ValueError("Descrição é obrigatória")
        if self.valor_alvo < 0:
            raise ValueError("valor_alvo deve ser >= 0")
        if self.valor_atual < 0:
            raise ValueError("valor_atual deve ser >= 0")
        if self.termina_em < self.criada_em:
            raise ValueError("termina_em deve ser >= criada_em")
        if not self.status.strip():
            raise ValueError("Status é obrigatório")
