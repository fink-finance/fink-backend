"""Dependências compartilhadas da API."""
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database import async_session_maker
from app.identidade.services.sessao_service import SessaoService
from app.identidade.repositories.sessao_repository_impl import SessaoRepositoryImpl
from app.identidade.repositories.pessoa_repository_impl import PessoaRepositoryImpl


security = HTTPBearer(auto_error=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Fornece uma sessão de banco de dados assíncrona."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_sessao_service(session: AsyncSession = Depends(get_db)) -> SessaoService:
    """Fornece o serviço de sessão/autenticação."""
    return SessaoService(SessaoRepositoryImpl(session), PessoaRepositoryImpl(session))


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    sessao_service: SessaoService = Depends(get_sessao_service),
) -> int:
    """
    Valida o token Bearer e retorna o ID do usuário autenticado.
    
    Raises:
        HTTPException: 401 se o token for inválido ou ausente
    """
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token ausente ou inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        sessao = await sessao_service.validar(credentials.credentials)
        return sessao.fk_pessoa_id_pessoa
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
