# Importe TODAS as classes ORM aqui (novos caminhos - refatorado para Package by Feature)
from app.identidade.persistence.pessoa_orm import PessoaORM  # noqa: F401
from app.identidade.persistence.sessao_orm import SessaoORM  # noqa: F401
from app.metas.persistence.meta_orm import MetaORM  # noqa: F401
from app.alertas.persistence.alerta_orm import AlertaORM  # noqa: F401
from app.comercial.persistence.plano_orm import PlanoORM  # noqa: F401
from app.comercial.persistence.assinatura_orm import AssinaturaORM  # noqa: F401
from app.comercial.persistence.solicitacao_pagamento_orm import SolicitacaoPagamentoORM  # noqa: F401
from app.comercial.persistence.tipo_pagamento_orm import TipoPagamentoORM  # noqa: F401
