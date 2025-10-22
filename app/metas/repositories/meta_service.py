from datetime import date
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

from app.metas.persistence.meta_orm import MetaORM
from app.metas.repositories.meta_repository import MetaRepository


class MetaService:
    """Camada de regras de negócio de Meta."""

    def __init__(self, repo: MetaRepository):
        self.repo = repo

    # -------------------------------------------------------------------------
    # CRUD principal
    # -------------------------------------------------------------------------

    async def listar_todas(self):
        """Lista todas as metas cadastradas (uso administrativo)."""
        return await self.repo.list_all()

    async def listar_por_pessoa(self, id_pessoa: int):
        """Lista todas as metas vinculadas a uma pessoa."""
        metas = await self.repo.list_by_pessoa(id_pessoa)
        return metas or []

    async def buscar_por_id(self, id_meta: int):
        """Busca uma meta específica pelo ID."""
        meta = await self.repo.get_by_id(id_meta)
        if not meta:
            raise ValueError("Meta não encontrada.")
        return meta

    async def criar(self, dados: dict):
        """
        Cria uma nova meta financeira.

        Regras de negócio:
        - 'fk_pessoa_id_pessoa' é obrigatório (meta precisa pertencer a alguém)
        - 'valor_alvo' deve ser positivo (> 0)
        - 'valor_atual' inicia em 0 ou valor informado >= 0
        - 'termina_em' deve ser uma data no futuro
        - 'status' padrão: 'em andamento'
        """
        obrigatorios = [
            "fk_pessoa_id_pessoa", "titulo", "descricao",
            "valor_alvo", "termina_em"
        ]
        for campo in obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        valor_alvo = Decimal(str(dados.get("valor_alvo", "0")))
        if valor_alvo <= 0:
            raise ValueError("O valor-alvo deve ser maior que zero.")

        valor_atual = Decimal(str(dados.get("valor_atual", "0")))
        if valor_atual < 0:
            raise ValueError("O valor atual não pode ser negativo.")

        data_termino = dados["termina_em"]
        if data_termino < date.today():
            raise ValueError("A data de término não pode ser anterior à data atual.")

        # Preenche campos padrão se não vierem do payload
        dados.setdefault("criada_em", date.today())
        dados.setdefault("status", "em andamento")

        nova_meta = MetaORM(**dados)

        try:
            return await self.repo.add(nova_meta)
        except IntegrityError as e:
            raise ValueError(f"Erro ao salvar meta: {e}")

    async def atualizar(self, id_meta: int, dados: dict):
        """
        Atualiza os campos de uma meta existente.
        Permite mudar título, descrição, valores, data de término e status.
        """
        meta = await self.repo.get_by_id(id_meta)
        if not meta:
            raise ValueError("Meta não encontrada.")

        for campo, valor in dados.items():
            if hasattr(meta, campo):
                setattr(meta, campo, valor)

        # Validações rápidas pós-update
        if meta.valor_alvo <= 0:
            raise ValueError("O valor-alvo deve ser maior que zero.")
        if meta.valor_atual < 0:
            raise ValueError("O valor atual não pode ser negativo.")
        if meta.termina_em < meta.criada_em:
            raise ValueError("A data de término não pode ser anterior à data de criação.")

        try:
            return await self.repo.update(meta)
        except IntegrityError as e:
            raise ValueError(f"Erro ao atualizar meta: {e}")

    async def remover(self, id_meta: int):
        """Remove uma meta existente."""
        meta = await self.repo.get_by_id(id_meta)
        if not meta:
            raise ValueError("Meta não encontrada.")
        await self.repo.delete(id_meta)

    # -------------------------------------------------------------------------
    # Regras de negócio adicionais
    # -------------------------------------------------------------------------

    async def atualizar_progresso(self, id_meta: int, novo_valor: float):
        """
        Incrementa ou redefine o progresso de uma meta.
        - Não permite reduzir valor_atual para negativo.
        - Se atingir ou ultrapassar valor_alvo, muda status para 'concluída'.
        """
        meta = await self.repo.get_by_id(id_meta)
        if not meta:
            raise ValueError("Meta não encontrada.")

        if novo_valor < 0:
            raise ValueError("O valor informado deve ser positivo.")

        meta.valor_atual += float(novo_valor)

        if meta.valor_atual >= meta.valor_alvo:
            meta.status = "concluída"

        return await self.repo.update(meta)
