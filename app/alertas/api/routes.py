from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

from app.shared.database import async_session_maker
from app.api.deps import get_current_user_id

from ..services.alerta_service import AlertaService
from ..repositories.alerta_repository_impl import AlertaRepositoryImpl
from .schemas import AlertaResponse, AlertaUpdate

router = APIRouter(
    tags=["alertas"],
    responses={
        401: {"description": "Token de autenticação inválido ou ausente"},
        500: {"description": "Erro interno do servidor"}
    }
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_alerta_service(session: AsyncSession = Depends(get_db)) -> AlertaService:
    repo = AlertaRepositoryImpl(session)
    return AlertaService(repo)


@router.get(
    "/",
    response_model=List[AlertaResponse],
    summary="Listar alertas não lidos",
    description="Retorna todos os alertas não lidos do usuário autenticado",
    responses={
        200: {
            "description": "Lista de alertas não lidos retornada com sucesso",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id_alerta": 1,
                            "fk_pessoa_id_pessoa": "123e4567-e89b-12d3-a456-426614174000",
                            "data": "2025-01-16T10:30:00Z",
                            "conteudo": "Nova atividade relacionada à sua meta",
                            "lida": False
                        }
                    ]
                }
            }
        },
        400: {"description": "Erro na requisição"},
        401: {"description": "Token de autenticação inválido ou ausente"}
    }
)
async def list_alertas(
    service: AlertaService = Depends(get_alerta_service),
    user_id: UUID = Depends(get_current_user_id),
) -> List[AlertaResponse]:
    """
    Lista todos os alertas não lidos do usuário autenticado.
    
    **Comportamento:**
    - Retorna apenas alertas com `lida=False` pertencentes ao usuário autenticado
    - Automaticamente exclui alertas com mais de 1 mês antes de retornar os resultados
    - A limpeza de alertas antigos ajuda a evitar poluição do banco de dados
    
    **Autenticação:**
    - Requer token Bearer válido no header `Authorization`
    - O `user_id` é extraído automaticamente do token
    
    **Resposta:**
    - Lista vazia `[]` se não houver alertas não lidos
    - Lista de objetos `AlertaResponse` com os alertas encontrados
    """
    try:
        alertas = await service.listar_por_pessoa(user_id)
        return [AlertaResponse.model_validate(alerta.__dict__) for alerta in alertas]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch(
    "/{id_alerta}",
    response_model=AlertaResponse,
    summary="Marcar alerta como lido",
    description="Atualiza o status de um alerta para lido",
    responses={
        200: {
            "description": "Alerta marcado como lido com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id_alerta": 1,
                        "fk_pessoa_id_pessoa": "123e4567-e89b-12d3-a456-426614174000",
                        "data": "2025-01-16T10:30:00Z",
                        "conteudo": "Nova atividade relacionada à sua meta",
                        "lida": True
                    }
                }
            }
        },
        400: {"description": "Requisição inválida (ex: tentativa de marcar como não lido)"},
        401: {"description": "Token de autenticação inválido ou ausente"},
        403: {"description": "Alerta não pertence ao usuário autenticado"},
        404: {"description": "Alerta não encontrado"}
    }
)
async def marcar_alerta_como_lido(
    id_alerta: int,
    alerta_update: AlertaUpdate,
    service: AlertaService = Depends(get_alerta_service),
    user_id: UUID = Depends(get_current_user_id),
) -> AlertaResponse:
    """
    Marca um alerta como lido.
    
    **Comportamento:**
    - Atualiza o campo `lida` de `false` para `true`
    - Apenas alertas pertencentes ao usuário autenticado podem ser atualizados
    - O campo `lida` no body deve ser `true`, caso contrário retorna erro 400
    
    **Autenticação:**
    - Requer token Bearer válido no header `Authorization`
    - Valida que o alerta pertence ao usuário do token
    
    **Validações:**
    - `id_alerta` deve existir no banco de dados
    - Alerta deve pertencer ao usuário autenticado
    - Campo `lida` no body deve ser `true`
    
    **Erros:**
    - `400`: Se `lida` não for `true`
    - `403`: Se o alerta não pertencer ao usuário
    - `404`: Se o alerta não existir
    """
    try:
        if not alerta_update.lida:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este endpoint serve apenas para marcar alertas como lidos (lida=true)",
            )
        
        updated = await service.marcar_como_lida(id_alerta, user_id)
        return AlertaResponse.model_validate(updated.__dict__)
    except ValueError as e:
        if "permissão" in str(e).lower() or "não tem" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
