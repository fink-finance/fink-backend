from typing import Any, List
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.alertas.persistence.alerta_orm import AlertaORM
from app.alertas.repositories.alerta_repository import AlertaRepository


class AlertaService:
    """Camada de regras de negócio de Alerta."""

    def __init__(self, repo: AlertaRepository):
        self.repo = repo

    # -------------------------------------------------------------------------
    # CRUD principal
    # -------------------------------------------------------------------------

    async def listar_todos(self) -> List[AlertaORM]:
        """Lista todos os alertas cadastrados (uso administrativo)."""
        return await self.repo.list_all()

    async def listar_por_pessoa(self, id_pessoa: UUID) -> List[AlertaORM]:
        """Lista todos os alertas vinculados a uma pessoa."""
        return await self.repo.list_by_pessoa(id_pessoa)

    async def listar_por_meta(self, id_meta: int) -> List[AlertaORM]:
        """Lista todos os alertas vinculados a uma meta."""
        return await self.repo.list_by_meta(id_meta)

    async def buscar_por_id(self, id_alerta: int) -> AlertaORM:
        """Busca um alerta pelo ID."""
        alerta = await self.repo.get_by_id(id_alerta)
        if not alerta:
            raise ValueError("Alerta não encontrado.")
        return alerta

    async def criar(self, dados: dict[str, Any]) -> AlertaORM:
        """
        Cria um novo alerta.

        Regras de negócio:
        - Campos obrigatórios: fk_pessoa_id_pessoa, parametro, acao, valor
        - 'valor' deve ser positivo (> 0)
        - 'parametro' deve estar entre os parâmetros conhecidos
        - 'acao' deve ser um tipo conhecido ('maior que', 'menor que', etc.)
        """
        obrigatorios = ["fk_pessoa_id_pessoa", "parametro", "acao", "valor"]
        for campo in obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        valor = float(dados["valor"])
        if valor <= 0:
            raise ValueError("O valor do alerta deve ser maior que zero.")

        parametro = dados["parametro"].strip().lower()
        acao = dados["acao"].strip().lower()

        parametros_validos = {"saldo", "meta", "gasto", "rendimento"}
        acoes_validas = {"maior que", "menor que", "igual a"}

        if parametro not in parametros_validos:
            raise ValueError(f"Parâmetro inválido: {parametro}. Esperado um de {parametros_validos}.")
        if acao not in acoes_validas:
            raise ValueError(f"Ação inválida: {acao}. Esperado uma de {acoes_validas}.")

        novo_alerta = AlertaORM(**dados)

        try:
            return await self.repo.add(novo_alerta)
        except IntegrityError as e:
            raise ValueError(f"Erro ao salvar alerta: {e}")

    async def atualizar(self, id_alerta: int, dados: dict[str, Any]) -> AlertaORM:
        """Atualiza um alerta existente."""
        alerta = await self.repo.get_by_id(id_alerta)
        if not alerta:
            raise ValueError("Alerta não encontrado.")

        for campo, valor in dados.items():
            if hasattr(alerta, campo):
                setattr(alerta, campo, valor)

        if alerta.valor <= 0:
            raise ValueError("O valor do alerta deve ser maior que zero.")

        try:
            return await self.repo.update(alerta)
        except IntegrityError as e:
            raise ValueError(f"Erro ao atualizar alerta: {e}")

    async def remover(self, id_alerta: int) -> None:
        """Remove um alerta existente."""
        alerta = await self.repo.get_by_id(id_alerta)
        if not alerta:
            raise ValueError("Alerta não encontrado.")
        await self.repo.delete(id_alerta)

    # -------------------------------------------------------------------------
    # Regras de negócio adicionais (opcional)
    # -------------------------------------------------------------------------

    async def avaliar_alerta(self, parametro: str, valor_referencia: float, id_pessoa: UUID) -> List[AlertaORM]:
        """
        Avalia todos os alertas de uma pessoa para um determinado parâmetro,
        retornando os que foram 'disparados' (condição verdadeira).

        Exemplo:
        - parametro='saldo', valor_referencia=1000 → retorna alertas cujo
          valor (limite) foi ultrapassado conforme a ação definida.
        """
        alertas = await self.repo.list_by_pessoa(id_pessoa)
        disparados = []

        for alerta in alertas:
            if alerta.parametro.lower() != parametro.lower():
                continue

            condicao = False
            if alerta.acao.lower() == "maior que":
                condicao = valor_referencia > alerta.valor
            elif alerta.acao.lower() == "menor que":
                condicao = valor_referencia < alerta.valor
            elif alerta.acao.lower() == "igual a":
                condicao = valor_referencia == alerta.valor

            if condicao:
                disparados.append(alerta)

        return disparados
