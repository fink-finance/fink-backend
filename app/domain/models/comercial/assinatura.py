from __future__ import annotations
from dataclasses import dataclass
from datetime import date

@dataclass
class Assinatura:
    id_assinatura: int | None
    fk_pessoa_id_pessoa: int
    fk_plano_id_plano: int
    comeca_em: date
    termina_em: date
    status: str

    def __post_init__(self) -> None:
        if self.termina_em < self.comeca_em:
            raise ValueError("termina_em deve ser >= comeca_em")
        if not self.status.strip():
            raise ValueError("status é obrigatório")
