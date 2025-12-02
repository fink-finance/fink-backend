from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

from app.shared.database import async_session_maker
from app.api.deps import get_current_user_id  # <- token do usuário logado

from ..services.alerta_service import AlertaService
from ..repositories.alerta_repository_impl import AlertaRepositoryImpl
from .schemas import AlertaCreate, AlertaResponse, AlertaUpdate

router = APIRouter(tags=["alertas"])


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_alerta_service(session: AsyncSession = Depends(get_db)) -> AlertaService:
    repo = AlertaRepositoryImpl(session)
    return AlertaService(repo)


@router.post("/", response_model=AlertaResponse, status_code=status.HTTP_201_CREATED)
async def create_alerta(
    alerta: AlertaCreate,
    service: AlertaService = Depends(get_alerta_service),
    user_id: int = Depends(get_current_user_id),
) -> AlertaResponse:
    """
    Cria um novo alerta para o usuário autenticado.

    O campo fk_pessoa_id_pessoa é preenchido automaticamente com o ID do usuário logado.
    """
    try:
        data = alerta.dict()
        # Garante que o alerta pertence ao usuário autenticado
        data["fk_pessoa_id_pessoa"] = user_id

        created = await service.criar(data)
        return AlertaResponse.from_orm(created)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[AlertaResponse])
async def list_alertas(
    service: AlertaService = Depends(get_alerta_service),
    user_id: int = Depends(get_current_user_id),
) -> List[AlertaResponse]:
    """
    Lista todos os alertas do usuário autenticado.
    """
    alertas = await service.listar_por_pessoa(user_id)
    return [AlertaResponse.from_orm(alerta) for alerta in alertas]


@router.get("/{id_alerta}", response_model=AlertaResponse)
async def get_alerta(
    id_alerta: int,
    service: AlertaService = Depends(get_alerta_service),
    user_id: int = Depends(get_current_user_id),
) -> AlertaResponse:
    """
    Busca um alerta pelo ID, apenas se ele pertencer ao usuário autenticado.
    """
    try:
        alerta = await service.buscar_por_id(id_alerta)

        if alerta.fk_pessoa_id_pessoa != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este alerta",
            )

        return AlertaResponse.from_orm(alerta)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alerta não encontrado")


@router.put("/{id_alerta}", response_model=AlertaResponse)
async def update_alerta(
    id_alerta: int,
    alerta_update: AlertaUpdate,
    service: AlertaService = Depends(get_alerta_service),
    user_id: int = Depends(get_current_user_id),
) -> AlertaResponse:
    """
    Atualiza um alerta existente, apenas se ele pertencer ao usuário autenticado.
    """
    try:
        # Verifica se o alerta pertence ao usuário antes de atualizar
        alerta_atual = await service.buscar_por_id(id_alerta)
        if alerta_atual.fk_pessoa_id_pessoa != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para atualizar este alerta",
            )

        updated = await service.atualizar(id_alerta, alerta_update.dict(exclude_unset=True))
        return AlertaResponse.from_orm(updated)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id_alerta}")
async def delete_alerta(
    id_alerta: int,
    service: AlertaService = Depends(get_alerta_service),
    user_id: int = Depends(get_current_user_id),
) -> Dict[str, str]:
    """
    Remove um alerta, apenas se ele pertencer ao usuário autenticado.
    """
    try:
        alerta = await service.buscar_por_id(id_alerta)
        if alerta.fk_pessoa_id_pessoa != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para remover este alerta",
            )

        await service.remover(id_alerta)
        return {"message": "Alerta removido com sucesso"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alerta não encontrado")
