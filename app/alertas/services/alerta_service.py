from datetime import datetime, timedelta
from typing import Any, List
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

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
        """
        Lista todos os alertas não lidos de uma pessoa.
        Antes de retornar, deleta alertas com mais de 1 mês do mesmo usuário.
        """
        # Deleta alertas antigos (>1 mês)
        um_mes_atras = datetime.now() - timedelta(days=30)
        await self.repo.delete_old_alertas(id_pessoa, um_mes_atras)
        
        # Retorna apenas alertas não lidos
        return await self.repo.list_by_pessoa(id_pessoa)

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
        - Campos obrigatórios: fk_pessoa_id_pessoa, conteudo
        - 'conteudo' não pode ser vazio
        """
        obrigatorios = ["fk_pessoa_id_pessoa", "conteudo"]
        for campo in obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        conteudo = dados.get("conteudo", "").strip()
        if not conteudo:
            raise ValueError("O campo 'conteudo' não pode ser vazio.")

        # Preenche campos padrão se não fornecidos
        dados.setdefault("data", datetime.now())
        dados.setdefault("lida", False)
        dados.setdefault("id_alerta", None)

        novo_alerta = AlertaORM(**dados)

        try:
            return await self.repo.add(novo_alerta)
        except IntegrityError as e:
            raise ValueError(f"Erro ao salvar alerta: {e}")

    async def marcar_como_lida(self, id_alerta: int, user_id: UUID) -> AlertaORM:
        """
        Marca um alerta como lido.
        Valida que o alerta pertence ao usuário antes de atualizar.
        """
        alerta = await self.buscar_por_id(id_alerta)
        
        if alerta.fk_pessoa_id_pessoa != user_id:
            raise ValueError("Você não tem permissão para atualizar este alerta.")
        
        alerta.lida = True
        
        try:
            return await self.repo.update(alerta)
        except IntegrityError as e:
            raise ValueError(f"Erro ao atualizar alerta: {e}")

    async def criar_alerta_automatico(
        self, conteudo: str, user_id: UUID, session: AsyncSession, data: datetime = datetime.now()
    ) -> AlertaORM:
        """
        Cria um alerta automaticamente.
        Usado internamente quando eventos ocorrem (criação de meta, movimentação, etc).
        
        Args:
            conteudo: Mensagem do alerta
            user_id: ID do usuário que receberá o alerta
            session: Sessão do banco de dados (para usar na mesma transação)
        
        Returns:
            AlertaORM criado
        """
        if not conteudo.strip():
            raise ValueError("Conteudo não pode ser vazio.")
        
        novo_alerta = AlertaORM(
            id_alerta=None,
            fk_pessoa_id_pessoa=user_id,
            data=data,
            conteudo=conteudo,
            lida=False,
        )
        
        try:
            # Adiciona à sessão e faz commit
            session.add(novo_alerta)
            await session.flush()
            await session.commit()
            await session.refresh(novo_alerta)
            return novo_alerta
        except IntegrityError as e:
            await session.rollback()
            raise ValueError(f"Erro ao criar alerta automático: {e}")
