"""Mapper para conversão entre TipoPagamento (domain) e TipoPagamentoORM (persistence)."""

from __future__ import annotations

from app.comercial.domain.tipo_pagamento import TipoPagamento
from app.comercial.persistence.tipo_pagamento_orm import TipoPagamentoORM


def orm_to_model(orm: TipoPagamentoORM) -> TipoPagamento:
    """Converte TipoPagamentoORM (persistence) para TipoPagamento (domain)."""
    return TipoPagamento(
        id_pagamento=orm.id_pagamento,
        tipo_pagamento=orm.tipo_pagamento,
    )


def model_to_orm_new(model: TipoPagamento) -> TipoPagamentoORM:
    """Cria nova instância de TipoPagamentoORM a partir de TipoPagamento (domain)."""
    return TipoPagamentoORM(
        id_pagamento=model.id_pagamento,
        tipo_pagamento=model.tipo_pagamento,
    )


def update_orm_from_model(orm: TipoPagamentoORM, model: TipoPagamento) -> TipoPagamentoORM:
    """Atualiza instância de TipoPagamentoORM existente com dados de TipoPagamento (domain)."""
    orm.tipo_pagamento = model.tipo_pagamento
    return orm
