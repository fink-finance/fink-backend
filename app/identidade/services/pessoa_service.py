from typing import Sequence
from sqlalchemy.exc import IntegrityError
from app.identidade.persistence.pessoa_orm import PessoaORM
from app.identidade.repositories.pessoa_repository import PessoaRepository

class PessoaService:
    """Camada de regras de negócio de Pessoa."""

    def __init__(self, repo: PessoaRepository):
        self.repo = repo

    # -------------------------------------------------------------------------
    # CRUD principal
    # -------------------------------------------------------------------------

    async def listar(self) -> Sequence[PessoaORM]:
        """Lista todas as pessoas cadastradas."""
        return await self.repo.list_all()

    async def buscar_por_id(self, id_pessoa: int) -> PessoaORM:
        pessoa = await self.repo.get_by_id(id_pessoa)
        if not pessoa:
            raise ValueError("Pessoa não encontrada.")
        return pessoa

    async def buscar_por_email(self, email: str) -> PessoaORM:
        pessoa = await self.repo.get_by_email(email)
        if not pessoa:
            raise ValueError("Nenhum cadastro encontrado para esse e-mail.")
        return pessoa

    async def criar(self, dados: dict) -> PessoaORM:
        """
        Cria uma nova pessoa no sistema.
        Regras:
        - Campos obrigatórios devem estar preenchidos.
        - E-mail deve ser único.
        """
        obrigatorios = [
            "email", "senha", "nome", "data_nascimento", "telefone",
            "genero", "estado", "cidade", "rua", "numero", "cep"
        ]
        for campo in obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        existente = await self.repo.get_by_email(dados["email"])
        if existente:
            raise ValueError("Já existe uma pessoa cadastrada com esse e-mail.")

        pessoa = PessoaORM(**dados)

        try:
            return await self.repo.add(pessoa)
        except IntegrityError as e:
            raise ValueError(f"Erro ao salvar pessoa: {e}")

    async def remover(self, id_pessoa: int) -> None:
        pessoa = await self.repo.get_by_id(id_pessoa)
        if not pessoa:
            raise ValueError("Pessoa não encontrada.")
        await self.repo.delete(id_pessoa)

    # -------------------------------------------------------------------------
    # Conversões auxiliares (ORM -> dict)
    # -------------------------------------------------------------------------

    @staticmethod
    def to_dict(p: PessoaORM) -> dict:
        return {
            "id_pessoa": p.id_pessoa,
            "email": p.email,
            "nome": p.nome,
            "data_nascimento": p.data_nascimento,
            "telefone": p.telefone,
            "genero": p.genero,
            "estado": p.estado,
            "cidade": p.cidade,
            "rua": p.rua,
            "numero": p.numero,
            "cep": p.cep,
            "data_criacao": p.data_criacao,
            "admin": p.admin,
        }

    @classmethod
    def list_to_dict(cls, pessoas: Sequence[PessoaORM]) -> list[dict]:
        return [cls.to_dict(p) for p in pessoas]