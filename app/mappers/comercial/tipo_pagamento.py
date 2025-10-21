from __future__ import annotations

from app.domain.models.comercial.tipo_pagamento import TipoPagamento
from app.persistence.db.comercial.tipo_pagamento_orm import TipoPagamentoORM


def orm_to_model(orm: TipoPagamentoORM) -> TipoPagamento:
    return TipoPagamento(
        id_pagamento=orm.id_pagamento,
        tipo_pagamento=orm.tipo_pagamento,
    )


def model_to_orm_new(model: TipoPagamento) -> TipoPagamentoORM:
    return TipoPagamentoORM(
        id_pagamento=model.id_pagamento,
        tipo_pagamento=model.tipo_pagamento,
    )


def update_orm_from_model(orm: TipoPagamentoORM, model: TipoPagamento) -> TipoPagamentoORM:
    orm.tipo_pagamento = model.tipo_pagamento
    return orm
