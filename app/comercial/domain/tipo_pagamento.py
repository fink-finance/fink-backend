from __future__ import annotations
from dataclasses import dataclass

@dataclass
class TipoPagamento:
    id_pagamento: int | None
    tipo_pagamento: str

    def __post_init__(self) -> None:
        if not self.tipo_pagamento or self.tipo_pagamento.strip() == "":
            raise ValueError("O tipo de pagamento é obrigatório")
