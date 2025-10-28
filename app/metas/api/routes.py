from typing import List, AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database import async_session_maker
from ..services.meta_service import MetaService
from ..repositories.meta_repository_impl import MetaRepositoryImpl
from .meta_schema import MetaCreate, MetaUpdate, MetaResponse

router = APIRouter(tags=["metas"])


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_meta_service(session: AsyncSession = Depends(get_db)) -> MetaService:
    repository = MetaRepositoryImpl(session)
    return MetaService(repository)


@router.post("/", response_model=MetaResponse, status_code=status.HTTP_201_CREATED)
async def create_meta(meta: MetaCreate, service: MetaService = Depends(get_meta_service)) -> MetaResponse:
    """Cria uma nova meta financeira"""
    try:
        created = await service.criar(meta.model_dump())
        return MetaResponse.model_validate(created.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[MetaResponse])
async def list_metas(
    service: MetaService = Depends(get_meta_service),
) -> List[MetaResponse]:
    """Lista todas as metas (administrativo)"""
    try:
        metas = await service.listar_todas()
        return [MetaResponse.model_validate(m.__dict__) for m in metas]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/pessoa/{id_pessoa}", response_model=List[MetaResponse])
async def list_metas_by_pessoa(id_pessoa: int, service: MetaService = Depends(get_meta_service)) -> List[MetaResponse]:
    """Lista todas as metas de uma pessoa específica"""
    try:
        metas = await service.listar_por_pessoa(id_pessoa)
        return [MetaResponse.model_validate(m.__dict__) for m in metas]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{id_meta}", response_model=MetaResponse)
async def get_meta(id_meta: int, service: MetaService = Depends(get_meta_service)) -> MetaResponse:
    """Busca uma meta por ID"""
    try:
        meta = await service.buscar_por_id(id_meta)
        return MetaResponse.model_validate(meta.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{id_meta}", response_model=MetaResponse)
async def update_meta(id_meta: int, meta: MetaUpdate, service: MetaService = Depends(get_meta_service)) -> MetaResponse:
    """Atualiza parcialmente uma meta existente"""
    try:
        updated = await service.atualizar(id_meta, meta.model_dump(exclude_unset=True))
        return MetaResponse.model_validate(updated.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id_meta}")
async def delete_meta(id_meta: int, service: MetaService = Depends(get_meta_service)):
    """Remove uma meta"""
    try:
        await service.remover(id_meta)
        return {"message": "Meta removida com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
