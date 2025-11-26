from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class MetaBase(BaseModel):
    """Schema base com campos comuns."""
    titulo: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Título da meta",
        examples=["Comprar apartamento"]
    )
    categoria: str = Field(
        ..., 
        min_length=1, 
        max_length=500,
        description="Categoria da meta financeira",
        examples=["Investimento", "Reserva de Emergência", "Viagem", "Educação"]
    )
    valor_alvo: Decimal = Field(
        ...,
        gt=0,
        description="Valor alvo a ser atingido (em reais)",
        examples=[100000.00]
    )
    termina_em: date = Field(
        ...,
        description="Data limite para atingir a meta",
        examples=["2026-12-31"]
    )


class MetaCreate(MetaBase):
    """Schema para criação de meta.
    
    ⚠️ Campos gerenciados automaticamente pelo backend (NÃO enviar):
    - id_meta: gerado pelo banco de dados
    - fk_pessoa_id_pessoa: extraído do token de autenticação
    - criada_em: data atual do sistema
    - valor_atual: inicializado como 0
    - status: inicializado como 'em_andamento'
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "titulo": "Viagem para Europa",
                "categoria": "Viagem",
                "valor_alvo": 15000.00,
                "termina_em": "2026-06-01"
            }
        }
    )


class MetaUpdate(BaseModel):
    """Schema para atualização parcial de meta.

    ⚠️ Campos que NÃO podem ser alterados:
    - id_meta (identificador único)
    - fk_pessoa_id_pessoa (proprietário da meta)
    - criada_em (data de criação)
    """

    titulo: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=100,
        description="Novo título da meta"
    )
    categoria: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=500,
        description="Nova categoria da meta"
    )
    valor_alvo: Optional[Decimal] = Field(
        None, 
        gt=0,
        description="Novo valor alvo"
    )
    valor_atual: Optional[Decimal] = Field(
        None, 
        ge=0,
        description="Valor atual já economizado"
    )
    termina_em: Optional[date] = Field(
        None,
        description="Nova data limite"
    )
    status: Optional[str] = Field(
        None, 
        pattern=r"^(em_andamento|concluida|cancelada|atrasada)$",
        description="Status da meta: em_andamento, concluida, cancelada ou atrasada"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "valor_atual": 5000.00,
                "status": "em_andamento"
            }
        }
    )


class MetaResponse(MetaBase):
    """Schema para respostas da API.
    
    Inclui todos os campos da meta, incluindo os gerenciados pelo backend.
    """
    id_meta: int = Field(
        ...,
        gt=0,
        description="ID único da meta"
    )
    fk_pessoa_id_pessoa: int = Field(
        ...,
        gt=0,
        description="ID do usuário proprietário da meta"
    )
    valor_atual: Decimal = Field(
        ...,
        ge=0,
        description="Valor já economizado"
    )
    criada_em: date = Field(
        ...,
        description="Data de criação da meta"
    )
    status: str = Field(
        ...,
        pattern=r"^(em_andamento|concluida|cancelada|atrasada)$",
        description="Status atual da meta"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id_meta": 1,
                "fk_pessoa_id_pessoa": 123,
                "titulo": "Viagem para Europa",
                "descricao": "Economizar para viagem de férias",
                "valor_alvo": 15000.00,
                "valor_atual": 5000.00,
                "criada_em": "2025-11-21",
                "termina_em": "2026-06-01",
                "status": "em_andamento"
            }
        }
    )
