"""ORM models do módulo Identidade."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.identidade.persistence.pessoa_orm import PessoaORM
    from app.identidade.persistence.sessao_orm import SessaoORM

__all__ = ["PessoaORM", "SessaoORM"]
