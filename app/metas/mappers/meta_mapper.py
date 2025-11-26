"""Mapper para conversão entre Meta (domain) e MetaORM (persistence)."""

from __future__ import annotations

from app.metas.domain.meta import Meta
from app.metas.persistence.meta_orm import MetaORM


def orm_to_model(orm: MetaORM) -> Meta:
    """Converte MetaORM (persistence) para Meta (domain)."""
    return Meta(
        id_meta=orm.id_meta,
        fk_pessoa_id_pessoa=orm.fk_pessoa_id_pessoa,
        titulo=orm.titulo,
        categoria=orm.categoria,
        valor_alvo=orm.valor_alvo,
        valor_atual=orm.valor_atual,
        criada_em=orm.criada_em,
        termina_em=orm.termina_em,
        status=orm.status,
    )


def model_to_orm_new(model: Meta) -> MetaORM:
    """Cria nova instância de MetaORM a partir de Meta (domain)."""
    return MetaORM(
        id_meta=model.id_meta,
        fk_pessoa_id_pessoa=model.fk_pessoa_id_pessoa,
        titulo=model.titulo,
        categoria=model.categoria,
        valor_alvo=model.valor_alvo,
        valor_atual=model.valor_atual,
        criada_em=model.criada_em,
        termina_em=model.termina_em,
        status=model.status,
    )


def update_orm_from_model(orm: MetaORM, model: Meta) -> MetaORM:
    """Atualiza instância de MetaORM existente com dados de Meta (domain)."""
    orm.fk_pessoa_id_pessoa = model.fk_pessoa_id_pessoa
    orm.titulo = model.titulo
    orm.categoria = model.categoria
    orm.valor_alvo = model.valor_alvo
    orm.valor_atual = model.valor_atual
    orm.criada_em = model.criada_em
    orm.termina_em = model.termina_em
    orm.status = model.status
    return orm
