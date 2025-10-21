from __future__ import annotations

from app.comercial.domain.solicitacao_pagamento import SolicitacaoPagamento
from app.comercial.persistence.solicitacao_pagamento_orm import SolicitacaoPagamentoORM


def orm_to_model(orm: SolicitacaoPagamentoORM) -> SolicitacaoPagamento:
    return SolicitacaoPagamento(
        id_solicitacao=orm.id_solicitacao,
        fk_tipo_pagamento_id_pagamento=orm.fk_tipo_pagamento_id_pagamento,
        fk_assinatura_id_assinatura=orm.fk_assinatura_id_assinatura,
        data_hora=orm.data_hora,
    )


def model_to_orm_new(model: SolicitacaoPagamento) -> SolicitacaoPagamentoORM:
    return SolicitacaoPagamentoORM(
        id_solicitacao=model.id_solicitacao,
        fk_tipo_pagamento_id_pagamento=model.fk_tipo_pagamento_id_pagamento,
        fk_assinatura_id_assinatura=model.fk_assinatura_id_assinatura,
        data_hora=model.data_hora,
    )


def update_orm_from_model(orm: SolicitacaoPagamentoORM, model: SolicitacaoPagamento) -> SolicitacaoPagamentoORM:
    orm.fk_tipo_pagamento_id_pagamento = model.fk_tipo_pagamento_id_pagamento
    orm.fk_assinatura_id_assinatura = model.fk_assinatura_id_assinatura
    orm.data_hora = model.data_hora
    return orm
