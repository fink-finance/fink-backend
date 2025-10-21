"""Mapper para conversão entre Alerta (domain) e AlertaORM (persistence)."""

from __future__ import annotations

from app.alertas.domain.alerta import Alerta
from app.alertas.persistence.alerta_orm import AlertaORM

def orm_to_model(orm: AlertaORM) -> Alerta:
    return Alerta(
        id_alerta=orm.id_alerta,
        fk_pessoa_id_pessoa=orm.fk_pessoa_id_pessoa,
        parametro=orm.parametro,
        acao=orm.acao,
        valor=orm.valor,
        fk_meta_id_meta=orm.fk_meta_id_meta,
    )


def model_to_orm_new(model: Alerta) -> AlertaORM:
    return AlertaORM(
        id_alerta=model.id_alerta,
        fk_pessoa_id_pessoa=model.fk_pessoa_id_pessoa,
        parametro=model.parametro,
        acao=model.acao,
        valor=model.valor,
        fk_meta_id_meta=model.fk_meta_id_meta,
    )


def update_orm_from_model(orm: AlertaORM, model: Alerta) -> AlertaORM:
    orm.fk_pessoa_id_pessoa = model.fk_pessoa_id_pessoa
    orm.parametro = model.parametro
    orm.acao = model.acao
    orm.valor = model.valor
    orm.fk_meta_id_meta = model.fk_meta_id_meta
    return orm
