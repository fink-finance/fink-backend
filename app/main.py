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
    """Manage application startup and shutdown tasks.

    Initializes database objects on startup (except in production)
    and yields control back to FastAPI; no explicit shutdown logic yet.
    """
    await init_db(create_all=(settings.environment != "production"))
    yield


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
