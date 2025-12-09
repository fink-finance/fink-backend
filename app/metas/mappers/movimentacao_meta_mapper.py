"""Mapper para conversão entre MovimentacaoMeta (domain) e MovimentacaoMetaORM (persistence)."""

from __future__ import annotations

from app.metas.domain.movimentacao_meta import MovimentacaoMeta
from app.metas.persistence.movimentacao_meta_orm import MovimentacaoMetaORM


def orm_to_model(orm: MovimentacaoMetaORM) -> MovimentacaoMeta:
    """Converte MovimentacaoMetaORM (persistence) para MovimentacaoMeta (domain)."""
    return MovimentacaoMeta(
        id_movimentacao=orm.id_movimentacao,
        fk_meta_id_meta=orm.fk_meta_id_meta,
        valor=orm.valor,
        acao=orm.acao,
        data=orm.data,
    )


def model_to_orm_new(model: MovimentacaoMeta) -> MovimentacaoMetaORM:
    """Cria nova instância de MovimentacaoMetaORM a partir de MovimentacaoMeta (domain)."""
    return MovimentacaoMetaORM(
        id_movimentacao=model.id_movimentacao,
        fk_meta_id_meta=model.fk_meta_id_meta,
        valor=model.valor,
        acao=model.acao,
        data=model.data,
    )

