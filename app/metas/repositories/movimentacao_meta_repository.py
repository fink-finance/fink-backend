from __future__ import annotations

from typing import Protocol
from collections.abc import Iterable

from app.metas.persistence.movimentacao_meta_orm import MovimentacaoMetaORM


class MovimentacaoMetaRepository(Protocol):
    """Contrato que define o comportamento esperado do repositório de MovimentacaoMeta."""

    async def get_by_id(self, id_movimentacao: int) -> MovimentacaoMetaORM | None: ...
    async def list_by_meta_id(self, id_meta: int) -> Iterable[MovimentacaoMetaORM]: ...
    async def add(self, movimentacao: MovimentacaoMetaORM) -> MovimentacaoMetaORM: ...

