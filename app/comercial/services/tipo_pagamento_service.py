from __future__ import annotations

from typing import Any, Sequence

from app.comercial.domain.tipo_pagamento import TipoPagamento
from app.comercial.persistence.tipo_pagamento_orm import TipoPagamentoORM
from app.comercial.repositories.tipo_pagamento_repository import TipoPagamentoRepository
from app.comercial.mappers.tipo_pagamento_mapper import orm_to_model, model_to_orm_new


class TipoPagamentoService:
    """Regras de negócio para Tipo de Pagamento."""

    def __init__(self, repo: TipoPagamentoRepository) -> None:
        self.repo = repo

    async def criar(self, data: dict[str, Any]) -> TipoPagamento:
        try:
            data.pop("id_pagamento", None)
            tp = TipoPagamento(id_pagamento=None, **data)

            existente = await self.repo.get_by_tipo(tp.tipo_pagamento)
            if existente:
                raise ValueError("Tipo de pagamento já cadastrado")

            created_orm = await self.repo.add(model_to_orm_new(tp))
            return orm_to_model(created_orm)
        except Exception as e:
            raise ValueError(f"Erro ao criar tipo de pagamento: {str(e)}")

    async def listar(self) -> list[TipoPagamento]:
        itens = await self.repo.list_all()
        return [orm_to_model(i) for i in itens] if itens else []

    async def buscar_por_id(self, id_pagamento: int) -> TipoPagamento:
        orm = await self.repo.get_by_id(id_pagamento)
        if not orm:
            raise ValueError("Tipo de pagamento não encontrado")
        return orm_to_model(orm)

    async def buscar_por_tipo(self, tipo: str) -> TipoPagamento:
        orm = await self.repo.get_by_tipo(tipo)
        if not orm:
            raise ValueError("Tipo de pagamento não encontrado")
        return orm_to_model(orm)

    async def atualizar(self, id_pagamento: int, data: dict[str, Any]) -> TipoPagamento:
        try:
            atual = await self.repo.get_by_id(id_pagamento)
            if not atual:
                raise ValueError("Tipo de pagamento não encontrado")

            if "id_pagamento" in data:
                raise ValueError("Não é permitido modificar o id_pagamento")

            if "tipo_pagamento" in data and data["tipo_pagamento"]:
                # garantir unicidade
                ja = await self.repo.get_by_tipo(data["tipo_pagamento"])
                if ja and ja.id_pagamento != id_pagamento:
                    raise ValueError("Já existe outro registro com este tipo_pagamento")
                atual.tipo_pagamento = data["tipo_pagamento"]

            updated = await self.repo.update(atual)
            return orm_to_model(updated)
        except Exception as e:
            raise ValueError(f"Erro ao atualizar tipo de pagamento: {str(e)}")

    async def remover(self, id_pagamento: int) -> None:
        existe = await self.repo.get_by_id(id_pagamento)
        if not existe:
            raise ValueError("Tipo de pagamento não encontrado")
        await self.repo.delete(id_pagamento)

    # utilitários (mesmo padrão dos outros serviços)
    @staticmethod
    def to_dict(p: TipoPagamentoORM) -> dict[str, Any]:
        return {"id_pagamento": p.id_pagamento, "tipo_pagamento": p.tipo_pagamento}

    @classmethod
    def list_to_dict(cls, itens: Sequence[TipoPagamentoORM]) -> list[dict[str, Any]]:
        return [cls.to_dict(i) for i in itens]
