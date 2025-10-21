"""Mapper para conversão entre Assinatura (domain) e AssinaturaORM (persistence)."""

from __future__ import annotations

from app.comercial.domain.assinatura import Assinatura
from app.comercial.persistence.assinatura_orm import AssinaturaORM


def orm_to_model(orm: AssinaturaORM) -> Assinatura:
    """Converte AssinaturaORM (persistence) para Assinatura (domain)."""
    return Assinatura(
        id_assinatura=orm.id_assinatura,
        fk_pessoa_id_pessoa=orm.fk_pessoa_id_pessoa,
        fk_plano_id_plano=orm.fk_plano_id_plano,
        comeca_em=orm.comeca_em,
        termina_em=orm.termina_em,
        status=orm.status,
    )


def model_to_orm_new(model: Assinatura) -> AssinaturaORM:
    """Cria nova instância de AssinaturaORM a partir de Assinatura (domain)."""
    return AssinaturaORM(
        id_assinatura=model.id_assinatura,
        fk_pessoa_id_pessoa=model.fk_pessoa_id_pessoa,
        fk_plano_id_plano=model.fk_plano_id_plano,
        comeca_em=model.comeca_em,
        termina_em=model.termina_em,
        status=model.status,
    )


def update_orm_from_model(orm: AssinaturaORM, model: Assinatura) -> AssinaturaORM:
    """Atualiza instância de AssinaturaORM existente com dados de Assinatura (domain)."""
    orm.fk_pessoa_id_pessoa = model.fk_pessoa_id_pessoa
    orm.fk_plano_id_plano = model.fk_plano_id_plano
    orm.comeca_em = model.comeca_em
    orm.termina_em = model.termina_em
    orm.status = model.status
    return orm


#
