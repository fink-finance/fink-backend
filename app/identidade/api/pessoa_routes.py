from typing import List, AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.database import async_session_maker
from ..services.pessoa_service import PessoaService
from ..repositories.pessoa_repository_impl import PessoaRepositoryImpl
from .pessoa_schema import PessoaCreate, PessoaResponse, PessoaUpdate

router = APIRouter(tags=["pessoas"])


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_pessoa_service(session: AsyncSession = Depends(get_db)) -> PessoaService:
    repository = PessoaRepositoryImpl(session)
    return PessoaService(repository)


@router.post("/", response_model=PessoaResponse, status_code=status.HTTP_201_CREATED)
async def create_pessoa(pessoa: PessoaCreate, service: PessoaService = Depends(get_pessoa_service)) -> PessoaResponse:
    """Cria uma nova pessoa"""
    try:
        pessoa_dict = pessoa.model_dump()
        created = await service.criar(pessoa_dict)
        return PessoaResponse.model_validate(created.__dict__)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[PessoaResponse])
async def list_pessoas(
    service: PessoaService = Depends(get_pessoa_service),
) -> List[PessoaResponse]:
    """Lista todas as pessoas"""
    try:
        pessoas = await service.listar()
        return [PessoaResponse.model_validate(p.__dict__) for p in pessoas]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{id_pessoa}", response_model=PessoaResponse)
async def get_pessoa(id_pessoa: int, service: PessoaService = Depends(get_pessoa_service)) -> PessoaResponse:
    """Busca uma pessoa por ID"""
    try:
        pessoa = await service.buscar_por_id(id_pessoa)
        return PessoaResponse.model_validate(pessoa.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/by-email/{email}", response_model=PessoaResponse)
async def get_pessoa_by_email(email: str, service: PessoaService = Depends(get_pessoa_service)) -> PessoaResponse:
    """Busca uma pessoa por email"""
    try:
        pessoa = await service.buscar_por_email(email)
        return PessoaResponse.model_validate(pessoa.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{id_pessoa}", response_model=PessoaResponse)
async def update_pessoa(
    id_pessoa: int,
    pessoa: PessoaUpdate,
    service: PessoaService = Depends(get_pessoa_service),
) -> PessoaResponse:
    """Atualiza parcialmente uma pessoa existente"""
    try:
        updated = await service.atualizar(id_pessoa, pessoa.model_dump(exclude_unset=True))
        return PessoaResponse.model_validate(updated.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id_pessoa}")
async def delete_pessoa(id_pessoa: int, service: PessoaService = Depends(get_pessoa_service)):
    """Remove uma pessoa"""
    try:
        await service.remover(id_pessoa)
        return {"message": "Pessoa removida com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
