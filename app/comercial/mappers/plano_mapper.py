"""Mapper para conversão entre Plano (domain) e PlanoORM (persistence)."""

from __future__ import annotations

from app.comercial.domain.plano import Plano
from app.comercial.persistence.plano_orm import PlanoORM


def orm_to_model(orm: PlanoORM) -> Plano:
    """Converte PlanoORM (persistence) para Plano (domain)."""
    return Plano(
        id_plano=orm.id_plano,
        titulo=orm.titulo,
        descricao=orm.descricao,
        preco=orm.preco,
        duracao_meses=orm.duracao_meses,
        status=orm.status,
    )


def model_to_orm_new(model: Plano) -> PlanoORM:
    """Cria nova instância de PlanoORM a partir de Plano (domain)."""
    return PlanoORM(
        id_plano=model.id_plano,
        titulo=model.titulo,
        descricao=model.descricao,
        preco=model.preco,
        duracao_meses=model.duracao_meses,
        status=model.status,
    )


def update_orm_from_model(orm: PlanoORM, model: Plano) -> PlanoORM:
    """Atualiza instância de PlanoORM existente com dados de Plano (domain)."""
    orm.titulo = model.titulo
    orm.descricao = model.descricao
    orm.preco = model.preco
    orm.duracao_meses = model.duracao_meses
    orm.status = model.status
    return orm
