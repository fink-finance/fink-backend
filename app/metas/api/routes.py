from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user_id
from ..services.meta_service import MetaService
from ..repositories.meta_repository_impl import MetaRepositoryImpl
from ..repositories.movimentacao_meta_repository_impl import MovimentacaoMetaRepositoryImpl
from .meta_schema import MetaCreate, MetaUpdate, MetaResponse, AtualizarSaldoRequest, MovimentacaoMetaResponse

router = APIRouter(tags=["metas"])


async def get_meta_service(session: AsyncSession = Depends(get_db)) -> MetaService:
    repository = MetaRepositoryImpl(session)
    movimentacao_repository = MovimentacaoMetaRepositoryImpl(session)
    return MetaService(repository, movimentacao_repository)


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


@router.post("/{id_meta}/atualizar_saldo", response_model=MetaResponse, status_code=status.HTTP_200_OK)
async def atualizar_saldo_meta(
    id_meta: int,
    request: AtualizarSaldoRequest,
    service: MetaService = Depends(get_meta_service),
    user_id: UUID = Depends(get_current_user_id)
) -> MetaResponse:
    """Atualiza o saldo de uma meta financeira e registra a movimentação.
    
    Permite adicionar ou retirar valores do saldo atual da meta.
    O valor é sempre tratado como positivo, independente do sinal enviado.
    A movimentação é registrada no histórico da meta.
    
    **Regras:**
    - Meta deve pertencer ao usuário autenticado
    - Valor sempre positivo (módulo do valor enviado)
    - Não permite saldo negativo após retirada
    - Cria registro automático na tabela de movimentações
    """
    try:
        meta_atualizada = await service.atualizar_saldo(
            id_meta=id_meta,
            user_id=user_id,
            action=request.action,
            valor=request.valor,
            data_movimentacao=request.data,
        )
        return MetaResponse.model_validate(meta_atualizada.__dict__)
    except ValueError as e:
        if "não encontrada" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif "permissão" in str(e).lower() or "não tem" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/movimentacao/{id_meta}", response_model=List[MovimentacaoMetaResponse])
async def listar_movimentacoes_meta(
    id_meta: int,
    service: MetaService = Depends(get_meta_service),
    user_id: UUID = Depends(get_current_user_id)
) -> List[MovimentacaoMetaResponse]:
    """Lista todas as movimentações de uma meta financeira.
    
    Retorna o histórico completo de movimentações (adições e retiradas)
    da meta especificada, ordenado por data (mais recente primeiro).
    
    **Requisitos:**
    - Meta deve pertencer ao usuário autenticado
    """
    try:
        movimentacoes = await service.listar_movimentacoes(id_meta, user_id)
        return [
            MovimentacaoMetaResponse.model_validate(m.__dict__)
            for m in movimentacoes
        ]
    except ValueError as e:
        if "não encontrada" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif "permissão" in str(e).lower() or "não tem" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
