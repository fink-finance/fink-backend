from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SolicitacaoPagamento:
    id_solicitacao: int | None
    fk_tipo_pagamento_id_pagamento: int
    fk_assinatura_id_assinatura: int
    data_hora: datetime | None

    def __post_init__(self):
        if not self.fk_tipo_pagamento_id_pagamento:
            raise ValueError("Solicitação precisa ter um tipo de pagamento")
        if not self.fk_assinatura_id_assinatura:
            raise ValueError("Solicitação precisa estar vinculada a uma assinatura")
