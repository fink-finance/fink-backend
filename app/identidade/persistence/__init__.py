"""ORM models do módulo Identidade."""

from app.identidade.persistence.pessoa_orm import PessoaORM
from app.identidade.persistence.sessao_orm import SessaoORM

__all__ = ["PessoaORM", "SessaoORM"]
