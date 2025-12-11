"""Mapper para conversão entre Alerta (domain) e AlertaORM (persistence)."""

from __future__ import annotations

from app.alertas.domain.alerta import Alerta
from app.alertas.persistence.alerta_orm import AlertaORM


def orm_to_model(orm: AlertaORM) -> Alerta:
    """Converte AlertaORM (persistence) para Alerta (domain)."""
    return Alerta(
        id_alerta=orm.id_alerta,
        fk_pessoa_id_pessoa=orm.fk_pessoa_id_pessoa,
        data=orm.data,
        conteudo=orm.conteudo,
        lida=orm.lida,
    )


def model_to_orm_new(model: Alerta) -> AlertaORM:
    """Cria nova instância de AlertaORM a partir de Alerta (domain)."""
    return AlertaORM(
        id_alerta=model.id_alerta,
        fk_pessoa_id_pessoa=model.fk_pessoa_id_pessoa,
        data=model.data,
        conteudo=model.conteudo,
        lida=model.lida,
    )


def update_orm_from_model(orm: AlertaORM, model: Alerta) -> AlertaORM:
    """Atualiza instância de AlertaORM existente com dados de Alerta (domain)."""
    orm.fk_pessoa_id_pessoa = model.fk_pessoa_id_pessoa
    orm.data = model.data
    orm.conteudo = model.conteudo
    orm.lida = model.lida
    return orm
