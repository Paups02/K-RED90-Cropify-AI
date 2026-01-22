"""API module initialization."""
from .documents import router as documents_router
from .generate import router as generate_router

__all__ = ["documents_router", "generate_router"]
