from typing import List, AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database import async_session_maker
from app.comercial.repositories.assinatura_repository_impl import AssinaturaRepositoryImpl
from app.comercial.services.assinatura_service import AssinaturaService
from .assinatura_schema import (
    AssinaturaCreate,
    AssinaturaResponse,
    AssinaturaUpdate,
)

router = APIRouter(tags=["assinaturas"])


# -------------------------------------------------------------------------
# Dependências
# -------------------------------------------------------------------------
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_assinatura_service(
    session: AsyncSession = Depends(get_db),
) -> AssinaturaService:
    repo = AssinaturaRepositoryImpl(session)
    return AssinaturaService(repo)


# -------------------------------------------------------------------------
# Endpoints CRUD
# -------------------------------------------------------------------------

@router.post(
    "/",
    response_model=AssinaturaResponse,
    status_code=status.HTTP_201_CREATED,
)
async def criar_assinatura(
    assinatura: AssinaturaCreate,
    service: AssinaturaService = Depends(get_assinatura_service),
) -> AssinaturaResponse:
    """Cria uma nova assinatura."""
    try:
        dados = assinatura.model_dump()
        criada = await service.criar(dados)
        return AssinaturaResponse.model_validate(criada.__dict__)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=List[AssinaturaResponse])
async def listar_assinaturas(
    service: AssinaturaService = Depends(get_assinatura_service),
) -> List[AssinaturaResponse]:
    """Lista todas as assinaturas (uso administrativo)."""
    try:
        assinaturas = await service.listar_todas()
        return [AssinaturaResponse.model_validate(a.__dict__) for a in assinaturas]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/{id_assinatura}",
    response_model=AssinaturaResponse,
)
async def buscar_assinatura(
    id_assinatura: int,
    service: AssinaturaService = Depends(get_assinatura_service),
) -> AssinaturaResponse:
    """Busca uma assinatura por ID."""
    try:
        assinatura = await service.buscar_por_id(id_assinatura)
        return AssinaturaResponse.model_validate(assinatura.__dict__)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.patch(
    "/{id_assinatura}",
    response_model=AssinaturaResponse,
)
async def atualizar_assinatura(
    id_assinatura: int,
    assinatura: AssinaturaUpdate,
    service: AssinaturaService = Depends(get_assinatura_service),
) -> AssinaturaResponse:
    """Atualiza parcialmente uma assinatura existente."""
    try:
        dados = assinatura.model_dump(exclude_unset=True)
        atualizada = await service.atualizar(id_assinatura, dados)
        return AssinaturaResponse.model_validate(atualizada.__dict__)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete("/{id_assinatura}")
async def remover_assinatura(
    id_assinatura: int,
    service: AssinaturaService = Depends(get_assinatura_service),
):
    """Remove uma assinatura."""
    try:
        await service.remover(id_assinatura)
        return {"message": "Assinatura removida com sucesso"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# -------------------------------------------------------------------------
# Regras adicionais: renovar / cancelar
# -------------------------------------------------------------------------

@router.post(
    "/{id_assinatura}/renovar",
    response_model=AssinaturaResponse,
)
async def renovar_assinatura(
    id_assinatura: int,
    meses: int = 1,
    service: AssinaturaService = Depends(get_assinatura_service),
) -> AssinaturaResponse:
    """Renova uma assinatura existente."""
    try:
        renovada = await service.renovar(id_assinatura, meses)
        return AssinaturaResponse.model_validate(renovada.__dict__)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.put(
    "/{id_assinatura}/cancelar",
    response_model=AssinaturaResponse,
)
async def cancelar_assinatura(
    id_assinatura: int,
    service: AssinaturaService = Depends(get_assinatura_service),
) -> AssinaturaResponse:
    """Cancela uma assinatura (status='cancelada')."""
    try:
        cancelada = await service.cancelar(id_assinatura)
        return AssinaturaResponse.model_validate(cancelada.__dict__)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
