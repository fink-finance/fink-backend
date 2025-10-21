"""Imports de todos os ORM models para Alembic autogenerate.

IMPORTANTE: Este arquivo é importado pelo Alembic para detectar todos os modelos ORM.
Os imports cíclicos são esperados e não causam problemas em runtime porque:
1. SQLAlchemy usa strings para relationships
2. TYPE_CHECKING guards previnem imports em tempo de execução
3. Este arquivo só é usado pelo Alembic em tempo de migração
"""


def import_all_models() -> None:
    """Importa todos os modelos ORM.

    Esta função garante que todos os modelos estejam registrados no metadata
    do SQLAlchemy para o Alembic poder detectá-los durante autogenerate.
    """
    # fmt: off
    from app.alertas.persistence.alerta_orm import AlertaORM  # noqa: F401
    from app.comercial.persistence.assinatura_orm import AssinaturaORM  # noqa: F401
    from app.comercial.persistence.plano_orm import PlanoORM  # noqa: F401
    from app.comercial.persistence.solicitacao_pagamento_orm import (  # noqa: F401
        SolicitacaoPagamentoORM,
    )
    from app.comercial.persistence.tipo_pagamento_orm import TipoPagamentoORM  # noqa: F401
    from app.identidade.persistence.pessoa_orm import PessoaORM  # noqa: F401
    from app.identidade.persistence.sessao_orm import SessaoORM  # noqa: F401
    from app.metas.persistence.meta_orm import MetaORM  # noqa: F401
    # fmt: on


# Importar todos os modelos quando este módulo é carregado
import_all_models()
