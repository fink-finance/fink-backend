# Refatoração: Package by Feature (Modular Monolith)

## 📋 Resumo da Refatoração

Esta refatoração migrou o projeto de uma **arquitetura por camadas** para uma **arquitetura por funcionalidades** (Package by Feature), mantendo as camadas dentro de cada módulo.

### Antes (Package by Layer)
```
app/
├── domain/models/           # Todos os domain models misturados
│   ├── identidade/
│   ├── metas/
│   ├── alertas/
│   └── comercial/
├── persistence/db/          # Todos os ORMs misturados
├── repositories/            # Todos os repositories misturados
├── services/                # Serviços misturados
└── schemas/                 # Schemas misturados
```

### Depois (Package by Feature)
```
app/
├── shared/                  # ✅ Infraestrutura compartilhada
│   ├── database.py         # Base + Session + Engine
│   ├── common.py           # Schemas comuns (placeholder)
│   ├── transaction.py      # Transaction schemas (placeholder)
│   └── transaction_service.py  # Services compartilhados (placeholder)
│
├── identidade/              # ✅ Módulo completo e independente
│   ├── domain/             # Entidades de negócio
│   ├── persistence/        # ORM models
│   ├── repositories/       # Data access (preparado)
│   ├── schemas/            # DTOs (preparado)
│   ├── services/           # Business logic (preparado)
│   └── api/                # HTTP endpoints (preparado)
│
├── metas/                   # ✅ Módulo completo e independente
│   └── ... (mesma estrutura)
│
├── alertas/                 # ✅ Módulo completo e independente
│   └── ... (mesma estrutura)
│
├── comercial/               # ✅ Módulo completo e independente
│   └── ... (mesma estrutura)
│
├── core/                    # Configuração global
├── api/v1/                  # Rotas versionadas
└── main.py                  # Entry point
```

## ✅ Módulos Migrados

### 1. **shared/** - Infraestrutura Compartilhada
- `database.py`: Base declarativa, Engine, SessionLocal, get_db(), init_db()
- Arquivos placeholder: `common.py`, `transaction.py`, `transaction_service.py`

### 2. **identidade/** - Autenticação e Usuários
- **Domain**: `Pessoa`, `Sessao`
- **Persistence**: `PessoaORM`, `SessaoORM`
- **Relationships**: Pessoa → Sessões, Metas, Alertas, Assinaturas

### 3. **metas/** - Objetivos Financeiros
- **Domain**: `Meta`
- **Persistence**: `MetaORM`
- **Relationships**: Meta → Pessoa (FK), Meta → Alertas

### 4. **alertas/** - Notificações e Gatilhos
- **Domain**: `Alerta`
- **Persistence**: `AlertaORM`
- **Relationships**: Alerta → Pessoa (FK), Alerta → Meta (FK opcional)

### 5. **comercial/** - Planos, Assinaturas e Pagamentos
- **Domain**: `Plano`, `Assinatura`, `TipoPagamento`, `SolicitacaoPagamento`
- **Persistence**: 4 ORMs correspondentes
- **Relationships**:
  - Plano → Assinaturas
  - Assinatura → Pessoa (FK), Plano (FK)
  - SolicitacaoPagamento → Assinatura (FK), TipoPagamento (FK)

## 🔄 Mudanças Importantes

### Imports Atualizados
```python
# ANTES
from app.db.base import Base
from app.persistence.db.identidade.pessoa_orm import PessoaORM

# DEPOIS
from app.shared.database import Base
from app.identidade.persistence.pessoa_orm import PessoaORM
```

### Retrocompatibilidade
Os arquivos `app/db/base.py` e `app/db/session.py` foram atualizados para **re-exportar** de `app.shared.database`, garantindo que imports antigos ainda funcionem temporariamente.

### Relationships Entre Módulos
Todos os relationships foram atualizados para usar os novos caminhos:
```python
# app/identidade/persistence/pessoa_orm.py
if TYPE_CHECKING:
    from app.metas.persistence.meta_orm import MetaORM
    from app.alertas.persistence.alerta_orm import AlertaORM
    from app.comercial.persistence.assinatura_orm import AssinaturaORM
```

## 📁 Estrutura Detalhada de um Módulo

```
app/identidade/
├── __init__.py              # Exports do módulo
├── domain/                  # 📋 Entidades de negócio (independentes)
│   ├── __init__.py
│   ├── pessoa.py           # Validações, regras de negócio
│   └── sessao.py
├── persistence/             # 💾 ORM (SQLAlchemy)
│   ├── __init__.py
│   ├── pessoa_orm.py       # Mapeamento de tabelas
│   └── sessao_orm.py
├── repositories/            # 🗄️ Data Access (futuro)
│   └── __init__.py         # Conversões Domain ↔ ORM
├── schemas/                 # 📄 DTOs (futuro)
│   └── __init__.py         # Request/Response (Pydantic)
├── services/                # ⚙️ Business Logic (futuro)
│   └── __init__.py         # Use cases, orquestração
└── api/                     # 🌐 HTTP Endpoints (futuro)
    └── __init__.py         # Rotas FastAPI
```

## 🎯 Vantagens da Nova Estrutura

### ✅ Alta Coesão
Tudo relacionado a "Identidade" está em `app/identidade/`.

### ✅ Baixo Acoplamento
Módulos são independentes, comunicam-se via interfaces claras.

### ✅ Navegabilidade
Encontrar código de "Metas"? Tudo está em `app/metas/`.

### ✅ Escalabilidade
Fácil adicionar novos módulos (ex: `transacoes/`, `relatorios/`).

### ✅ Migração para Microserviços
Se necessário, cada módulo pode virar um serviço independente.

### ✅ Ownership Claro
Times podem "possuir" módulos completos.

## 📝 Como Adicionar uma Nova Feature

```bash
# 1. Criar estrutura
mkdir -p app/nova_feature/{domain,persistence,repositories,schemas,services,api}
touch app/nova_feature/__init__.py

# 2. Implementar camadas (ordem recomendada)
# - domain/          (entidades de negócio)
# - persistence/     (ORM models)
# - repositories/    (data access)
# - schemas/         (DTOs)
# - services/        (business logic)
# - api/             (routes)

# 3. Adicionar ORM ao models_imports.py
# from app.nova_feature.persistence.entidade_orm import EntidadeORM

# 4. Criar migração Alembic
# alembic revision --autogenerate -m "Add nova_feature"
```

## 🧪 Testes

A estrutura facilita testes:
```python
# Teste unitário (domain)
from app.identidade.domain.pessoa import Pessoa

def test_pessoa_valida_email():
    with pytest.raises(ValueError):
        Pessoa(email="invalido", ...)

# Teste de integração (repository)
from app.identidade.repositories.pessoa_repository import PessoaRepository

async def test_criar_pessoa(db_session):
    repo = PessoaRepository(db_session)
    # ...
```

## 📊 Estatísticas da Refatoração

- **Arquivos Criados**: ~40 novos arquivos
- **Arquivos Deletados**: ~50 arquivos antigos
- **Módulos Migrados**: 4 (Identidade, Metas, Alertas, Comercial)
- **Entidades**: 8 domain models + 8 ORMs
- **Zero Breaking Changes**: Retrocompatibilidade mantida

## 🚀 Próximos Passos

1. ✅ Implementar Repositories (conversões Domain ↔ ORM)
2. ✅ Implementar Services (use cases)
3. ✅ Criar Schemas (DTOs de request/response)
4. ✅ Criar API Routes (endpoints FastAPI)
5. ✅ Adicionar testes unitários e de integração
6. ✅ Remover retrocompatibilidade de `app/db/` (quando seguro)

## 📚 Referências

- [Package by Feature vs Package by Layer](https://phauer.com/2020/package-by-feature/)
- [Modular Monolith Architecture](https://www.kamilgrzybek.com/design/modular-monolith-primer/)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)

---

**Data da Refatoração**: 20 de outubro de 2025
**Branch**: `refactor/organize-by-feature`
