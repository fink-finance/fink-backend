from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum
from uuid import UUID


class CategoriaMetaEnum(str, Enum):
    """Categorias permitidas para metas financeiras."""
    EMERGENCIA = "Emergência"
    INVESTIMENTO = "Investimento"
    VIAGEM = "Viagem"
    EDUCACAO = "Educação"
    DIVIDAS = "Dívidas"
    MORADIA = "Moradia"
    VEICULO = "Veículo"
    INTERCAMBIO = "Intercâmbio"
    SEGURANCA = "Segurança"
    SAUDE = "Saúde"
    OUTROS = "Outros"  # Categoria padrão
    
    @classmethod
    def get_default(cls) -> str:
        """Retorna a categoria padrão."""
        return cls.OUTROS.value
    
    @classmethod
    def is_valid(cls, categoria: str | None) -> bool:
        """Verifica se a categoria é válida."""
        if not categoria:
            return False
        return categoria in [c.value for c in cls]
    
    @classmethod
    def normalize(cls, categoria: str | None) -> str:
        """Normaliza a categoria: se inválida ou vazia, retorna padrão."""
        if not categoria or not categoria.strip():
            return cls.get_default()
        
        # Verifica se é uma categoria válida
        if cls.is_valid(categoria):
            return categoria
        
        # Categoria inválida: retorna padrão
        return cls.get_default()


@dataclass
class Meta:
    id_meta: int | None
    fk_pessoa_id_pessoa: UUID
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
        
        # Normaliza categoria: se vazia ou inválida, usa padrão
        if not self.categoria or not self.categoria.strip():
            object.__setattr__(self, 'categoria', CategoriaMetaEnum.get_default())
        elif not CategoriaMetaEnum.is_valid(self.categoria):
            object.__setattr__(self, 'categoria', CategoriaMetaEnum.get_default())
        if not self.fk_pessoa_id_pessoa:
            raise ValueError("ID da pessoa é obrigatório")
        if self.valor_alvo <= 0:
            raise ValueError("Valor alvo deve ser maior que zero")
        if self.valor_atual < 0:
            raise ValueError("Valor atual não pode ser negativo")
        if self.termina_em < self.criada_em:
            raise ValueError("Data de término não pode ser anterior à data de criação")

        status_permitidos = {"em_andamento", "concluida", "cancelada", "atrasada"}
        if not self.status or self.status.strip() not in status_permitidos:
            raise ValueError(f"Status deve ser um dos seguintes: {', '.join(status_permitidos)}")
