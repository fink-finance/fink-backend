from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.identidade.persistence.pessoa_orm import PessoaORM
from app.identidade.repositories.pessoa_repository import PessoaRepository


class PessoaRepositoryImpl(PessoaRepository):
    """Implementação concreta do repositório de Pessoa usando SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, pessoa: PessoaORM) -> PessoaORM:
        try:
            self.session.add(pessoa)
            await self.session.flush()  # Flush to get the ID
            await self.session.commit()  # Commit the transaction
            await self.session.refresh(pessoa)  # Refresh to get all fields
            return pessoa
        except Exception as e:
            await self.session.rollback()
            raise ValueError(f"Erro ao criar pessoa: {str(e)}")

    async def list_all(self) -> list[PessoaORM]:
        stmt = select(PessoaORM)
        result = await self.session.execute(stmt)
        await self.session.commit()  # Add commit here
        return list(result.scalars().all())

    async def get_by_id(self, id_pessoa: int) -> PessoaORM | None:
        stmt = select(PessoaORM).where(PessoaORM.id_pessoa == id_pessoa)
        result = await self.session.execute(stmt)
        pessoa = result.scalar_one_or_none()
        return pessoa

    async def get_by_email(self, email: str) -> PessoaORM | None:
        stmt = select(PessoaORM).where(PessoaORM.email == email)
        result = await self.session.execute(stmt)
        pessoa = result.scalar_one_or_none()
        return pessoa

    async def update(self, pessoa: PessoaORM) -> PessoaORM:
        await self.session.merge(pessoa)
        await self.session.commit()  # Add commit here
        return pessoa

    async def delete(self, id_pessoa: int) -> None:
        stmt = delete(PessoaORM).where(PessoaORM.id_pessoa == id_pessoa)
        await self.session.execute(stmt)
        await self.session.commit()  # Add commit here
