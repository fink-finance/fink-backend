from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Plano:
    id_plano: int | None

    titulo: str
    descricao: str
    preco: float
    duracao_meses: int
    status: str

    def __post_init__(self) -> None:
        if not self.titulo or self.titulo.strip() == "":
            raise ValueError("O título do plano é obrigatório")
        if self.preco <= 0:
            raise ValueError("O preço deve ser maior que zero")
        if self.duracao_meses <= 0:
            raise ValueError("A duração deve ser maior que zero")
        if not self.status:
            raise ValueError("O status do plano é obrigatório")
