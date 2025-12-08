from datetime import date, timedelta
from typing import Any, List
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.comercial.persistence.assinatura_orm import AssinaturaORM
from app.comercial.repositories.assinatura_repository import AssinaturaRepository


class AssinaturaService:
    """Camada de regras de negócio de Assinatura."""

    def __init__(self, repo: AssinaturaRepository):
        self.repo = repo

    # -------------------------------------------------------------------------
    # CRUD principal
    # -------------------------------------------------------------------------

    async def listar_todas(self) -> List[AssinaturaORM]:
        """Lista todas as assinaturas (uso administrativo)."""
        return await self.repo.list_all()

    async def listar_por_pessoa(self, id_pessoa: UUID) -> List[AssinaturaORM]:
        """Lista todas as assinaturas vinculadas a uma pessoa."""
        return await self.repo.list_by_pessoa(id_pessoa)

    async def listar_por_plano(self, id_plano: int) -> List[AssinaturaORM]:
        """Lista todas as assinaturas vinculadas a um plano."""
        return await self.repo.list_by_plano(id_plano)

    async def buscar_por_id(self, id_assinatura: int) -> AssinaturaORM:
        """Busca uma assinatura pelo ID."""
        assinatura = await self.repo.get_by_id(id_assinatura)
        if not assinatura:
            raise ValueError("Assinatura não encontrada.")
        return assinatura

    async def criar(self, dados: dict[str, Any]) -> AssinaturaORM:
        """
        Cria uma nova assinatura.

        Regras de negócio:
        - Deve ter `fk_pessoa_id_pessoa` e `fk_plano_id_plano` definidos.
        - `comeca_em` deve ser hoje ou no futuro.
        - `termina_em` deve ser posterior a `comeca_em`.
        - A pessoa não pode ter outra assinatura ativa para o mesmo plano.
        - `status` padrão: 'ativa'.
        """
        obrigatorios = [
            "fk_pessoa_id_pessoa",
            "fk_plano_id_plano",
            "comeca_em",
            "termina_em",
        ]
        for campo in obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        data_inicio = dados["comeca_em"]
        data_fim = dados["termina_em"]

        if data_inicio < date.today():
            raise ValueError("A data de início não pode ser no passado.")
        if data_fim <= data_inicio:
            raise ValueError("A data de término deve ser posterior à data de início.")

        # regra: uma pessoa não pode ter duas assinaturas ativas do mesmo plano
        assinaturas_existentes = await self.repo.list_by_pessoa(dados["fk_pessoa_id_pessoa"])
        for a in assinaturas_existentes:
            if (
                a.fk_plano_id_plano == dados["fk_plano_id_plano"]
                and a.status.lower() == "ativa"
                and a.termina_em >= date.today()
            ):
                raise ValueError("Essa pessoa já possui uma assinatura ativa para esse plano.")

        dados.setdefault("status", "ativa")

        nova_assinatura = AssinaturaORM(**dados)

        try:
            return await self.repo.add(nova_assinatura)
        except IntegrityError as e:
            raise ValueError(f"Erro ao criar assinatura: {e}")

    async def atualizar(self, id_assinatura: int, dados: dict[str, Any]) -> AssinaturaORM:
        """Atualiza uma assinatura existente."""
        assinatura = await self.repo.get_by_id(id_assinatura)
        if not assinatura:
            raise ValueError("Assinatura não encontrada.")

        for campo, valor in dados.items():
            if hasattr(assinatura, campo):
                setattr(assinatura, campo, valor)

        if assinatura.termina_em <= assinatura.comeca_em:
            raise ValueError("A data de término deve ser posterior à data de início.")

        try:
            return await self.repo.update(assinatura)
        except IntegrityError as e:
            raise ValueError(f"Erro ao atualizar assinatura: {e}")

    async def remover(self, id_assinatura: int) -> None:
        """Remove uma assinatura existente."""
        assinatura = await self.repo.get_by_id(id_assinatura)
        if not assinatura:
            raise ValueError("Assinatura não encontrada.")
        await self.repo.delete(id_assinatura)

    # -------------------------------------------------------------------------
    # Regras de negócio adicionais
    # -------------------------------------------------------------------------

    async def renovar(self, id_assinatura: int, meses: int = 1) -> AssinaturaORM:
        """
        Renova uma assinatura existente, estendendo o período.
        - Se a assinatura estiver ativa, adiciona meses ao término.
        - Se estiver expirada, reativa a partir de hoje.
        """
        assinatura = await self.repo.get_by_id(id_assinatura)
        if not assinatura:
            raise ValueError("Assinatura não encontrada.")

        if meses < 1:
            raise ValueError("O período de renovação deve ser de pelo menos 1 mês.")

        hoje = date.today()
        if assinatura.status.lower() != "ativa" or assinatura.termina_em < hoje:
            assinatura.comeca_em = hoje
            assinatura.termina_em = hoje + timedelta(days=30 * meses)
            assinatura.status = "ativa"
        else:
            assinatura.termina_em += timedelta(days=30 * meses)

        return await self.repo.update(assinatura)

    async def cancelar(self, id_assinatura: int) -> AssinaturaORM:
        """Cancela uma assinatura (define status='cancelada')."""
        assinatura = await self.repo.get_by_id(id_assinatura)
        if not assinatura:
            raise ValueError("Assinatura não encontrada.")
        assinatura.status = "cancelada"
        return await self.repo.update(assinatura)
