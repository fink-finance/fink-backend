"""Mapper para conversão entre Sessao (domain) e SessaoORM (persistence)."""

from __future__ import annotations

from app.identidade.domain.sessao import Sessao
from app.identidade.persistence.sessao_orm import SessaoORM


def orm_to_model(orm: SessaoORM) -> Sessao:
    return Sessao(
        id_sessao=orm.id_sessao,
        fk_pessoa_id_pessoa=orm.fk_pessoa_id_pessoa,
        token_hash=orm.token_hash,
        criada_em=orm.criada_em,
        expira_em=orm.expira_em,
    )


def model_to_orm_new(model: Sessao) -> SessaoORM:
    return SessaoORM(
        id_sessao=model.id_sessao,
        fk_pessoa_id_pessoa=model.fk_pessoa_id_pessoa,
        token_hash=model.token_hash,
        criada_em=model.criada_em,
        expira_em=model.expira_em,
    )


def update_orm_from_model(orm: SessaoORM, model: Sessao) -> SessaoORM:
    orm.fk_pessoa_id_pessoa = model.fk_pessoa_id_pessoa
    orm.token_hash = model.token_hash
    orm.criada_em = model.criada_em
    orm.expira_em = model.expira_em
    return orm
