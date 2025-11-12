"""FastAPI application entrypoint: sets up lifespan, CORS, and API v1 routes."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import api_router
from app.core.settings import settings
from app.shared.database import init_db

from app.providers.pluggy_client import PluggyClient
from app.api.pluggy_routes import router as pluggy_router

from app.alertas.api.routes import router as alertas_router
from app.identidade.api.pessoa_routes import router as pessoas_router
from app.metas.api.routes import router as metas_router
from app.comercial.api.plano_routes import router as planos_router
from app.identidade.api.sessao_routes import router as sessoes_router
from app.comercial.api.assinatura_routes import router as assinaturas_router
from app.comercial.api.tipo_pagamento_routes import router as tipos_pagamento_router
from app.comercial.api.solicitacao_pagamento_routes import (
    router as solicitacoes_pagamento_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # DB
    await init_db(create_all=(settings.environment != "production"))

    # Sanity check das variáveis de ambiente da Pluggy
    print(f"[PLUGGY] base_url = {settings.pluggy_base_url}")
    print(f"[PLUGGY] client_id set? {bool(settings.pluggy_client_id)}")
    print(f"[PLUGGY] client_secret set? {bool(settings.pluggy_client_secret)}")

    # Inicializa o client
    app.state.pluggy_client = PluggyClient(
        base_url=settings.pluggy_base_url,
        client_id=settings.pluggy_client_id,
        client_secret=settings.pluggy_client_secret,
    )

    # Validação rápida (opcional, mas ajuda a pegar erro cedo)
    try:
        _ = await app.state.pluggy_client.auth_token()
        print("[PLUGGY] auth_token OK")
    except Exception as e:
        # Não derruba a app, mas deixa claro o motivo se /connect-token falhar depois
        print(f"[PLUGGY] auth_token FAILED: {e}")

    try:
        yield
    finally:
        client = getattr(app.state, "pluggy_client", None)
        if client:
            await client.close()



app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(pessoas_router, prefix="/api/v1/pessoas")
app.include_router(alertas_router, prefix="/api/v1/alertas")
app.include_router(metas_router, prefix="/api/v1/metas")
app.include_router(planos_router, prefix="/api/v1/planos")
app.include_router(sessoes_router, prefix="/api/v1/sessoes")
app.include_router(assinaturas_router, prefix="/api/v1/assinaturas")
app.include_router(tipos_pagamento_router, prefix="/api/v1/tipos-pagamento")
app.include_router(solicitacoes_pagamento_router, prefix="/api/v1/solicitacoes-pagamento")
app.include_router(pluggy_router)



@app.get("/")
async def root() -> dict[str, Any]:
    """Return basic app metadata for quick inspection."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.get("/health")
async def health_check() -> dict[str, Any]:
    """Liveness probe endpoint used by containers and load balancers."""
    return {"status": "healthy", "service": settings.app_name}
