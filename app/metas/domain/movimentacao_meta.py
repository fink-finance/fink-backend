from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum


class AcaoMovimentacao(str, Enum):
    """Ações permitidas para movimentação de meta."""
    ADICIONADO = "adicionado"
    RETIRADO = "retirado"
    
    @classmethod
    def is_valid(cls, acao: str | None) -> bool:
        """Verifica se a ação é válida."""
        if not acao:
            return False
        return acao in [a.value for a in cls]


@dataclass
class MovimentacaoMeta:
    """Modelo de domínio para movimentação de meta financeira."""
    id_movimentacao: int | None
    fk_meta_id_meta: int
    valor: Decimal
    acao: str
    data: date

    def __post_init__(self) -> None:
        if not self.fk_meta_id_meta:
            raise ValueError("ID da meta é obrigatório")
        if self.valor <= 0:
            raise ValueError("Valor deve ser maior que zero")
        if not AcaoMovimentacao.is_valid(self.acao):
            raise ValueError(f"Ação deve ser uma das seguintes: {', '.join([a.value for a in AcaoMovimentacao])}")

