from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Meta:
    id_meta: int | None
    fk_pessoa_id_pessoa: int
    titulo: str
    categoria: str
    valor_alvo: Decimal
    valor_atual: Decimal
    criada_em: date
    termina_em: date
    status: str

    def __post_init__(self) -> None:
        if not self.titulo or not self.titulo.strip():
            raise ValueError("Título é obrigatório")
        if not self.categoria or not self.categoria.strip():
            raise ValueError("Categoria é obrigatória")
        if not self.fk_pessoa_id_pessoa or self.fk_pessoa_id_pessoa <= 0:
            raise ValueError("ID da pessoa é obrigatório e deve ser maior que zero")
        if self.valor_alvo <= 0:
            raise ValueError("Valor alvo deve ser maior que zero")
        if self.valor_atual < 0:
            raise ValueError("Valor atual não pode ser negativo")
        if self.termina_em < self.criada_em:
            raise ValueError("Data de término não pode ser anterior à data de criação")

        status_permitidos = {"em_andamento", "concluida", "cancelada", "atrasada"}
        if not self.status or self.status.strip() not in status_permitidos:
            raise ValueError(f"Status deve ser um dos seguintes: {', '.join(status_permitidos)}")
