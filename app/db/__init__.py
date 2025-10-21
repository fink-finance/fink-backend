"""Module __init__."""

# opcional: expor os modelos para autoload de migrações
from . import models_imports as models  # noqa: F401
from .base import Base

__all__ = ["Base", "models"]
