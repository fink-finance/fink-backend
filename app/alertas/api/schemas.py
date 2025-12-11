from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID


class AlertaBase(BaseModel):
    """Schema base para alerta."""
    fk_pessoa_id_pessoa: UUID = Field(..., description="ID da pessoa proprietária do alerta")
    data: datetime = Field(..., description="Data e hora de criação do alerta (com timezone)")
    conteudo: str = Field(..., description="Conteúdo/mensagem do alerta", examples=["Nova atividade relacionada à sua meta"])
    lida: bool = Field(default=False, description="Indica se o alerta foi lido pelo usuário")


class AlertaResponse(AlertaBase):
    """Schema de resposta para alerta."""
    id_alerta: int = Field(..., description="ID único do alerta", examples=[1])
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id_alerta": 1,
                "fk_pessoa_id_pessoa": "123e4567-e89b-12d3-a456-426614174000",
                "data": "2025-01-16T10:30:00Z",
                "conteudo": "Nova atividade relacionada à sua meta",
                "lida": False
            }
        }
    )


class AlertaUpdate(BaseModel):
    """Schema para atualização de alerta."""
    lida: bool = Field(..., description="Status de leitura do alerta. Deve ser `true` para marcar como lido.", examples=[True])
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "lida": True
            }
        }
    )
