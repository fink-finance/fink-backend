from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user_id
from ..services.meta_service import MetaService
from ..repositories.meta_repository_impl import MetaRepositoryImpl
from .meta_schema import MetaCreate, MetaUpdate, MetaResponse

router = APIRouter(tags=["metas"])


async def get_meta_service(session: AsyncSession = Depends(get_db)) -> MetaService:
    repository = MetaRepositoryImpl(session)
    return MetaService(repository)


@router.post("/", response_model=MetaResponse, status_code=status.HTTP_201_CREATED)
async def create_meta(
    meta: MetaCreate,
    service: MetaService = Depends(get_meta_service),
    user_id: UUID = Depends(get_current_user_id)
) -> MetaResponse:
    """Cria uma nova meta financeira para o usuário autenticado.
    
    O campo fk_pessoa_id_pessoa é automaticamente preenchido com o ID do usuário logado.
    """
    try:
        # Adiciona o ID do usuário autenticado aos dados
        data = meta.model_dump()
        data["fk_pessoa_id_pessoa"] = user_id
        
        created = await service.criar(data)
        return MetaResponse.model_validate(created.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[MetaResponse])
async def list_metas(
    service: MetaService = Depends(get_meta_service),
    user_id: UUID = Depends(get_current_user_id)
) -> List[MetaResponse]:
    """Lista todas as metas do usuário autenticado."""
    try:
        metas = await service.listar_por_pessoa(user_id)
        return [MetaResponse.model_validate(m.__dict__) for m in metas]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{id_meta}", response_model=MetaResponse)
async def get_meta(
    id_meta: int,
    service: MetaService = Depends(get_meta_service),
    user_id: UUID = Depends(get_current_user_id)
) -> MetaResponse:
    """Busca uma meta específica do usuário autenticado."""
    try:
        meta = await service.buscar_por_id(id_meta)
        
        # Verifica se a meta pertence ao usuário autenticado
        if meta.fk_pessoa_id_pessoa != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar esta meta"
            )
        
        return MetaResponse.model_validate(meta.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{id_meta}", response_model=MetaResponse)
async def update_meta(
    id_meta: int,
    meta: MetaUpdate,
    service: MetaService = Depends(get_meta_service),
    user_id: UUID = Depends(get_current_user_id)
) -> MetaResponse:
    """Atualiza parcialmente uma meta do usuário autenticado."""
    try:
        # Verifica se a meta pertence ao usuário antes de atualizar
        meta_atual = await service.buscar_por_id(id_meta)
        if meta_atual.fk_pessoa_id_pessoa != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para atualizar esta meta"
            )
        
        updated = await service.atualizar(id_meta, meta.model_dump(exclude_unset=True))
        return MetaResponse.model_validate(updated.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id_meta}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meta(
    id_meta: int,
    service: MetaService = Depends(get_meta_service),
    user_id: UUID = Depends(get_current_user_id)
):
    """Remove uma meta do usuário autenticado."""
    try:
        # Verifica se a meta pertence ao usuário antes de remover
        meta = await service.buscar_por_id(id_meta)
        if meta.fk_pessoa_id_pessoa != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para remover esta meta"
            )
        
        await service.remover(id_meta)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
