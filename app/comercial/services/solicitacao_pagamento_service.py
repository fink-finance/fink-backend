from datetime import datetime
from typing import Any, List
from sqlalchemy.exc import IntegrityError

from app.comercial.persistence.solicitacao_pagamento_orm import SolicitacaoPagamentoORM
from app.comercial.repositories.solicitacao_pagamento_repository import (
    SolicitacaoPagamentoRepository,
)


class SolicitacaoPagamentoService:
    """Camada de regras de negócio de Solicitação de Pagamento."""

    def __init__(self, repo: SolicitacaoPagamentoRepository):
        self.repo = repo

    # -------------------------------------------------------------------------
    # CRUD principal
    # -------------------------------------------------------------------------

    async def listar_todas(self) -> List[SolicitacaoPagamentoORM]:
        """Lista todas as solicitações de pagamento (uso administrativo)."""
        return await self.repo.list_all()

    async def listar_por_assinatura(self, id_assinatura: int) -> List[SolicitacaoPagamentoORM]:
        """Lista solicitações vinculadas a uma assinatura específica."""
        return await self.repo.list_by_assinatura(id_assinatura)

    async def buscar_por_id(self, id_solicitacao: int) -> SolicitacaoPagamentoORM:
        """Busca uma solicitação pelo ID."""
        solicitacao = await self.repo.get_by_id(id_solicitacao)
        if not solicitacao:
            raise ValueError("Solicitação de pagamento não encontrada.")
        return solicitacao

    async def criar(self, dados: dict[str, Any]) -> SolicitacaoPagamentoORM:
        """
        Cria uma nova solicitação de pagamento.

        Regras de negócio:
        - 'fk_tipo_pagamento_id_pagamento' e 'fk_assinatura_id_assinatura' são obrigatórios.
        - Cada assinatura só pode ter uma solicitação (UniqueConstraint).
        - 'data_hora' é preenchida automaticamente com a data/hora atual.
        """
        obrigatorios = ["fk_tipo_pagamento_id_pagamento", "fk_assinatura_id_assinatura"]
        for campo in obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        # Verifica se já existe uma solicitação para essa assinatura
        existentes = await self.repo.list_by_assinatura(dados["fk_assinatura_id_assinatura"])
        if existentes:
            raise ValueError("Já existe uma solicitação de pagamento para essa assinatura.")

        # Define data/hora atual
        dados["data_hora"] = datetime.utcnow()

        nova_solicitacao = SolicitacaoPagamentoORM(**dados)

        try:
            return await self.repo.add(nova_solicitacao)
        except IntegrityError as e:
            raise ValueError(f"Erro ao salvar solicitação: {e}")


    async def remover(self, id_solicitacao: int) -> None:
        """Remove uma solicitação existente."""
        solicitacao = await self.repo.get_by_id(id_solicitacao)
        if not solicitacao:
            raise ValueError("Solicitação não encontrada.")
        await self.repo.delete(id_solicitacao)