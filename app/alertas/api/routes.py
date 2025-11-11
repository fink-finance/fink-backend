from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.alerta_service import AlertaService
from ..repositories.alerta_repository_impl import AlertaRepositoryImpl
from .schemas import AlertaCreate, AlertaResponse, AlertaUpdate
from collections.abc import AsyncGenerator
from app.shared.database import async_session_maker

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
async def create_alerta(alerta: AlertaCreate, service: AlertaService = Depends(get_alerta_service)) -> AlertaResponse:
    try:
        created = await service.criar(alerta.dict())
        return AlertaResponse.from_orm(created)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[AlertaResponse])
async def list_alertas(service: AlertaService = Depends(get_alerta_service)) -> List[AlertaResponse]:
    alertas = await service.listar_todos()
    return [AlertaResponse.from_orm(alerta) for alerta in alertas]


@router.get("/{id_alerta}", response_model=AlertaResponse)
async def get_alerta(id_alerta: int, service: AlertaService = Depends(get_alerta_service)) -> AlertaResponse:
    try:
        alerta = await service.buscar_por_id(id_alerta)
        return AlertaResponse.from_orm(alerta)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alerta não encontrado")


@router.put("/{id_alerta}", response_model=AlertaResponse)
async def update_alerta(
    id_alerta: int, alerta_update: AlertaUpdate, service: AlertaService = Depends(get_alerta_service)
) -> AlertaResponse:
    try:
        updated = await service.atualizar(id_alerta, alerta_update.dict(exclude_unset=True))
        return AlertaResponse.from_orm(updated)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id_alerta}")
async def delete_alerta(id_alerta: int, service: AlertaService = Depends(get_alerta_service)) -> Dict[str, str]:
    try:
        await service.remover(id_alerta)
        return {"message": "Alerta removido com sucesso"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alerta não encontrado")
