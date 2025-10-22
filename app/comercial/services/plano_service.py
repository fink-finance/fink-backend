from sqlalchemy.exc import IntegrityError
from app.comercial.persistence.plano_orm import PlanoORM
from app.comercial.repositories.plano_repository import PlanoRepository


class PlanoService:
    """Camada de regras de negócio de Plano."""

    def __init__(self, repo: PlanoRepository):
        self.repo = repo

    # -------------------------------------------------------------------------
    # CRUD principal
    # -------------------------------------------------------------------------

    async def listar_todos(self):
        """Lista todos os planos cadastrados."""
        return await self.repo.list_all()

    async def buscar_por_id(self, id_plano: int):
        """Busca um plano específico pelo ID."""
        plano = await self.repo.get_by_id(id_plano)
        if not plano:
            raise ValueError("Plano não encontrado.")
        return plano

    async def buscar_por_titulo(self, titulo: str):
        """Busca um plano específico pelo título."""
        plano = await self.repo.get_by_titulo(titulo)
        if not plano:
            raise ValueError("Nenhum plano encontrado com esse título.")
        return plano

    async def criar(self, dados: dict):
        """
        Cria um novo plano de assinatura.

        Regras de negócio:
        - 'titulo', 'descricao', 'preco', 'duracao_meses' e 'status' são obrigatórios.
        - 'preco' deve ser positivo (> 0).
        - 'duracao_meses' deve ser no mínimo 1.
        - 'titulo' deve ser único.
        """
        obrigatorios = ["titulo", "descricao", "preco", "duracao_meses", "status"]
        for campo in obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        preco = float(dados["preco"])
        if preco <= 0:
            raise ValueError("O preço do plano deve ser maior que zero.")

        duracao = int(dados["duracao_meses"])
        if duracao < 1:
            raise ValueError("A duração mínima de um plano é de 1 mês.")

        existente = await self.repo.get_by_titulo(dados["titulo"])
        if existente:
            raise ValueError("Já existe um plano com esse título.")

        novo_plano = PlanoORM(**dados)

        try:
            return await self.repo.add(novo_plano)
        except IntegrityError as e:
            raise ValueError(f"Erro ao salvar plano: {e}")

    async def atualizar(self, id_plano: int, dados: dict):
        """Atualiza os dados de um plano existente."""
        plano = await self.repo.get_by_id(id_plano)
        if not plano:
            raise ValueError("Plano não encontrado.")

        for campo, valor in dados.items():
            if hasattr(plano, campo):
                setattr(plano, campo, valor)

        if plano.preco <= 0:
            raise ValueError("O preço do plano deve ser maior que zero.")
        if plano.duracao_meses < 1:
            raise ValueError("A duração mínima de um plano é de 1 mês.")

        try:
            return await self.repo.update(plano)
        except IntegrityError as e:
            raise ValueError(f"Erro ao atualizar plano: {e}")

    async def remover(self, id_plano: int):
        """Remove um plano existente."""
        plano = await self.repo.get_by_id(id_plano)
        if not plano:
            raise ValueError("Plano não encontrado.")
        await self.repo.delete(id_plano)

    # -------------------------------------------------------------------------
    # Regras adicionais (opcionais)
    # -------------------------------------------------------------------------

    async def ativar(self, id_plano: int):
        """Ativa um plano (define status='ativo')."""
        plano = await self.repo.get_by_id(id_plano)
        if not plano:
            raise ValueError("Plano não encontrado.")
        plano.status = "ativo"
        return await self.repo.update(plano)

    async def desativar(self, id_plano: int):
        """Desativa um plano (define status='inativo')."""
        plano = await self.repo.get_by_id(id_plano)
        if not plano:
            raise ValueError("Plano não encontrado.")
        plano.status = "inativo"
        return await self.repo.update(plano)
