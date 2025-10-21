from __future__ import annotations

from app.domain.models.identidade.pessoa import Pessoa
from app.persistence.db.identidade.pessoa_orm import PessoaORM


def orm_to_model(orm: PessoaORM) -> Pessoa:
    return Pessoa(
        id_pessoa=orm.id_pessoa,
        email=orm.email,
        senha=orm.senha,
        nome=orm.nome,
        data_nascimento=orm.data_nascimento,
        telefone=orm.telefone,
        genero=orm.genero,
        estado=orm.estado,
        cidade=orm.cidade,
        rua=orm.rua,
        numero=orm.numero,
        cep=orm.cep,
        data_criacao=orm.data_criacao,
        admin=orm.admin,
    )


def model_to_orm_new(model: Pessoa) -> PessoaORM:
    return PessoaORM(
        id_pessoa=model.id_pessoa,
        email=model.email,
        senha=model.senha,
        nome=model.nome,
        data_nascimento=model.data_nascimento,
        telefone=model.telefone,
        genero=model.genero,
        estado=model.estado,
        cidade=model.cidade,
        rua=model.rua,
        numero=model.numero,
        cep=model.cep,
        data_criacao=model.data_criacao,
        admin=model.admin,
    )


def update_orm_from_model(orm: PessoaORM, model: Pessoa) -> PessoaORM:
    orm.email = model.email
    orm.senha = model.senha
    orm.nome = model.nome
    orm.data_nascimento = model.data_nascimento
    orm.telefone = model.telefone
    orm.genero = model.genero
    orm.estado = model.estado
    orm.cidade = model.cidade
    orm.rua = model.rua
    orm.numero = model.numero
    orm.cep = model.cep
    orm.admin = model.admin
    return orm
