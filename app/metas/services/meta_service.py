from datetime import date
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.metas.domain.meta import Meta, CategoriaMetaEnum
from app.metas.domain.movimentacao_meta import MovimentacaoMeta, AcaoMovimentacao
from app.metas.repositories.meta_repository import MetaRepository
from app.metas.repositories.movimentacao_meta_repository import MovimentacaoMetaRepository
from app.metas.mappers.meta_mapper import orm_to_model, model_to_orm_new
from app.metas.mappers.movimentacao_meta_mapper import model_to_orm_new as movimentacao_model_to_orm


class MetaService:
    """Camada de regras de negócio de Meta."""

    def __init__(self, repo: MetaRepository, movimentacao_repo: MovimentacaoMetaRepository | None = None):
        self.repo = repo
        self.movimentacao_repo = movimentacao_repo

    # -------------------------------------------------------------------------
    # CRUD principal
    # -------------------------------------------------------------------------

    async def listar_todas(self) -> list[Meta]:
        """Lista todas as metas cadastradas (uso administrativo)."""
        metas_orm = await self.repo.list_all()
        return [orm_to_model(meta) for meta in metas_orm]

    async def listar_por_pessoa(self, id_pessoa: UUID) -> list[Meta]:
        """Lista todas as metas vinculadas a uma pessoa."""
        metas_orm = await self.repo.list_by_pessoa(id_pessoa)
        return [orm_to_model(meta) for meta in metas_orm] if metas_orm else []

    async def buscar_por_id(self, id_meta: int) -> Meta:
        """Busca uma meta específica pelo ID."""
        meta_orm = await self.repo.get_by_id(id_meta)
        if not meta_orm:
            raise ValueError("Meta não encontrada.")
        return orm_to_model(meta_orm)

    async def criar(self, dados: dict[str, Any]) -> Meta:
        """
        Cria uma nova meta financeira.

        Regras de negócio:
        - 'fk_pessoa_id_pessoa' é obrigatório (meta precisa pertencer a alguém)
        - 'valor_alvo' deve ser positivo (> 0)
        - 'valor_atual' inicia em 0 automaticamente
        - 'termina_em' deve ser uma data no futuro
        - 'status' padrão: 'em_andamento'
        """
        obrigatorios = [
            "fk_pessoa_id_pessoa",
            "titulo",
            "valor_alvo",
            "termina_em",
        ]
        for campo in obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")
        
        # ⚠️ COMPATIBILIDADE TEMPORÁRIA: aceita "descricao" como alias de "categoria"
        # TODO: Remover após frontend ser atualizado
        if "descricao" in dados and "categoria" not in dados:
            dados["categoria"] = dados.pop("descricao")
        
        # Remove descricao se vier junto (prioriza categoria)
        dados.pop("descricao", None)
        
        # Normaliza categoria: se vazia/nula/inválida, usa padrão "Outros"
        categoria = dados.get("categoria")
        dados["categoria"] = CategoriaMetaEnum.normalize(categoria)

        valor_alvo = Decimal(str(dados.get("valor_alvo", "0")))
        if valor_alvo <= 0:
            raise ValueError("O valor-alvo deve ser maior que zero.")

        data_termino = dados["termina_em"]
        if data_termino < date.today():
            raise ValueError("A data de término não pode ser anterior à data atual.")

        # Preenche campos padrão/automáticos
        dados.setdefault("criada_em", date.today())
        dados.setdefault("status", "em_andamento")
        dados.setdefault("valor_atual", Decimal("0"))  # Sempre inicia em 0
        dados.setdefault("id_meta", None)  # Necessário para o modelo de domínio

        # Cria primeiro o modelo de domínio para validações
        meta = Meta(**dados)
        # Converte para ORM
        nova_meta = model_to_orm_new(meta)

        try:
            meta_criada = await self.repo.add(nova_meta)
            return orm_to_model(meta_criada)
        except IntegrityError as e:
            raise ValueError(f"Erro de integridade ao salvar meta: {e}")
        except Exception as e:
            raise ValueError(f"Erro inesperado ao criar meta: {e}")

    async def atualizar(self, id_meta: int, dados: dict[str, Any]) -> Meta:
        """
        Atualiza os campos de uma meta existente.
        Permite mudar título, categoria, valores, data de término e status.
        """
        meta_orm = await self.repo.get_by_id(id_meta)
        if not meta_orm:
            raise ValueError("Meta não encontrada.")

        # ⚠️ COMPATIBILIDADE TEMPORÁRIA: aceita "descricao" como alias de "categoria"
        if "descricao" in dados and "categoria" not in dados:
            dados["categoria"] = dados.pop("descricao")
        
        # Remove descricao se vier junto (prioriza categoria)
        dados.pop("descricao", None)
        
        # Normaliza categoria se fornecida
        if "categoria" in dados:
            dados["categoria"] = CategoriaMetaEnum.normalize(dados["categoria"])

        # Convertemos para modelo de domínio para atualizações
        meta = orm_to_model(meta_orm)

        # Atualiza apenas os campos fornecidos
        for campo, valor in dados.items():
            if hasattr(meta, campo):
                setattr(meta, campo, valor)

        # As validações são feitas automaticamente pelo modelo de domínio
        # devido ao __post_init__

        try:
            # Converte de volta para ORM e atualiza
            meta_atualizada = await self.repo.update(model_to_orm_new(meta))
            return orm_to_model(meta_atualizada)
        except IntegrityError as e:
            raise ValueError(f"Erro ao atualizar meta: {e}")

    async def remover(self, id_meta: int) -> None:
        """Remove uma meta existente."""
        meta = await self.repo.get_by_id(id_meta)
        if not meta:
            raise ValueError("Meta não encontrada.")
        await self.repo.delete(id_meta)

    # -------------------------------------------------------------------------
    # Regras de negócio adicionais
    # -------------------------------------------------------------------------

    async def atualizar_progresso(self, id_meta: int, novo_valor: Decimal) -> Meta:
        """
        Incrementa ou redefine o progresso de uma meta.
        - Não permite reduzir valor_atual para negativo.
        - Se atingir ou ultrapassar valor_alvo, muda status para 'concluída'.
        """
        meta_orm = await self.repo.get_by_id(id_meta)
        if not meta_orm:
            raise ValueError("Meta não encontrada.")

        # Convertemos para modelo de domínio
        meta = orm_to_model(meta_orm)

        if novo_valor < 0:
            raise ValueError("O valor informado deve ser positivo.")

        meta.valor_atual += Decimal(str(novo_valor))

        if meta.valor_atual >= meta.valor_alvo:
            meta.status = "concluida"

        # Atualiza no banco e retorna modelo atualizado
        meta_atualizada = await self.repo.update(model_to_orm_new(meta))
        return orm_to_model(meta_atualizada)

    async def atualizar_saldo(
        self,
        id_meta: int,
        user_id: UUID,
        action: str,
        valor: Decimal,
        data_movimentacao: date,
    ) -> Meta:
        """
        Atualiza o saldo de uma meta financeira e registra a movimentação.
        
        Regras de negócio:
        - Meta deve existir e pertencer ao usuário autenticado
        - Valor é sempre tratado como positivo (abs)
        - Action determina se soma ou subtrai do valor_atual
        - Não permite valor_atual ficar negativo após retirada
        - Cria registro na tabela de movimentações
        
        Args:
            id_meta: ID da meta a ser atualizada
            user_id: ID do usuário autenticado (para validação de propriedade)
            action: "adicionado" ou "retirado"
            valor: Valor da movimentação (será normalizado para positivo)
            data_movimentacao: Data da movimentação
            
        Returns:
            Meta atualizada
            
        Raises:
            ValueError: Se meta não existir, não pertencer ao usuário, ou operação inválida
        """
        if not self.movimentacao_repo:
            raise ValueError("Repositório de movimentação não configurado.")
        
        # Busca a meta
        meta_orm = await self.repo.get_by_id(id_meta)
        if not meta_orm:
            raise ValueError("Meta não encontrada.")
        
        # Valida propriedade
        meta = orm_to_model(meta_orm)
        if meta.fk_pessoa_id_pessoa != user_id:
            raise ValueError("Você não tem permissão para atualizar esta meta.")
        
        # Valida action
        if not AcaoMovimentacao.is_valid(action):
            raise ValueError(f"Ação inválida. Deve ser 'adicionado' ou 'retirado'.")
        
        # Normaliza valor (sempre positivo)
        valor_normalizado = abs(valor)
        if valor_normalizado <= 0:
            raise ValueError("Valor deve ser maior que zero.")
        
        # Calcula novo valor_atual
        if action == AcaoMovimentacao.ADICIONADO.value:
            novo_valor_atual = meta.valor_atual + valor_normalizado
        elif action == AcaoMovimentacao.RETIRADO.value:
            novo_valor_atual = meta.valor_atual - valor_normalizado
            # Valida que não fique negativo
            if novo_valor_atual < 0:
                raise ValueError(
                    f"Não é possível retirar {valor_normalizado}. "
                    f"Saldo atual: {meta.valor_atual}. "
                    f"Saldo mínimo permitido: 0."
                )
        else:
            raise ValueError(f"Ação inválida: {action}")
        
        # Atualiza valor_atual da meta
        meta.valor_atual = novo_valor_atual
        
        # Atualiza status se necessário
        if meta.valor_atual >= meta.valor_alvo and meta.status == "em_andamento":
            meta.status = "concluida"
        
        # Atualiza meta no banco
        try:
            meta_atualizada_orm = await self.repo.update(model_to_orm_new(meta))
            
            # Cria registro de movimentação
            movimentacao = MovimentacaoMeta(
                id_movimentacao=None,
                fk_meta_id_meta=id_meta,
                valor=valor_normalizado,
                acao=action,
                data=data_movimentacao,
            )
            movimentacao_orm = movimentacao_model_to_orm(movimentacao)
            await self.movimentacao_repo.add(movimentacao_orm)
            
            return orm_to_model(meta_atualizada_orm)
        except IntegrityError as e:
            raise ValueError(f"Erro ao atualizar saldo da meta: {e}")

    async def listar_movimentacoes(self, id_meta: int, user_id: UUID) -> list[MovimentacaoMeta]:
        """
        Lista todas as movimentações de uma meta.
        
        Args:
            id_meta: ID da meta
            user_id: ID do usuário autenticado (para validação de propriedade)
            
        Returns:
            Lista de movimentações da meta
            
        Raises:
            ValueError: Se meta não existir ou não pertencer ao usuário
        """
        if not self.movimentacao_repo:
            raise ValueError("Repositório de movimentação não configurado.")
        
        # Valida que a meta existe e pertence ao usuário
        meta = await self.buscar_por_id(id_meta)
        if meta.fk_pessoa_id_pessoa != user_id:
            raise ValueError("Você não tem permissão para acessar as movimentações desta meta.")
        
        # Busca movimentações
        movimentacoes_orm = await self.movimentacao_repo.list_by_meta_id(id_meta)
        from app.metas.mappers.movimentacao_meta_mapper import orm_to_model as movimentacao_orm_to_model
        return [movimentacao_orm_to_model(m) for m in movimentacoes_orm]
