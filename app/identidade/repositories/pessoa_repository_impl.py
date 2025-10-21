from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.identidade.persistence.pessoa_orm import PessoaORM
from app.identidade.repositories.pessoa_repository import PessoaRepository


class PessoaRepositoryImpl(PessoaRepository):
    """Implementação concreta do repositório de Pessoa usando SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id_pessoa: int) -> PessoaORM | None:
        """Busca uma pessoa pelo ID."""
        return await self.session.get(PessoaORM, id_pessoa)

    async def get_by_email(self, email: str) -> PessoaORM | None:
        """Busca uma pessoa pelo email."""
        result = await self.session.execute(
            select(PessoaORM).where(PessoaORM.email == email)
        )
        return result.scalar_one_or_none()

    async def list_all(self) -> list[PessoaORM]:
        """Lista todas as pessoas cadastradas."""
        result = await self.session.execute(select(PessoaORM))
        return result.scalars().all()

    async def add(self, pessoa: PessoaORM) -> PessoaORM:
        """Adiciona uma nova pessoa no banco."""
        self.session.add(pessoa)
        await self.session.flush()  # gera o ID no objeto
        return pessoa

    async def delete(self, id_pessoa: int) -> None:
        """Remove uma pessoa pelo ID."""
        await self.session.execute(
            delete(PessoaORM).where(PessoaORM.id_pessoa == id_pessoa)
        )
