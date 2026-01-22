"""DocuMind AI - Main FastAPI Application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.documents import router as documents_router
from app.api.generate import router as generate_router
from app.models.schemas import HealthCheck
from app.services.vector_store import vector_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print(f"🚀 Starting {settings.app_name}...")
    print(f"📂 Upload directory: {settings.upload_directory}")
    print(f"🗄️ ChromaDB directory: {settings.chroma_persist_directory}")
    yield
    # Shutdown
    print(f"👋 Shutting down {settings.app_name}...")


app = FastAPI(
    title=settings.app_name,
    description="""
## DocuMind AI - Repositorio Inteligente de Documentos

Una aplicación web que permite:
- 📤 **Subir documentos** (PDF, DOCX, TXT, MD, XLSX, PPTX)
- 🔍 **Consultar información** usando lenguaje natural
- 📊 **Generar informes** basados en tus documentos
- ✉️ **Crear correos** profesionales
- 📝 **Obtener resúmenes** automáticos
- 💬 **Chatear** con tus documentos

### Tipos de contenido que puedes generar:
- Informes profesionales
- Correos electrónicos
- Resúmenes ejecutivos
- Análisis detallados
- Contenido para presentaciones
- Cartas formales
- Memorandos internos
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents_router, prefix="/api")
app.include_router(generate_router, prefix="/api")


@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "description": "Repositorio inteligente de documentos con IA",
        "docs_url": "/docs",
        "endpoints": {
            "documents": "/api/documents",
            "generate": "/api/generate",
            "health": "/health",
        },
    }


@app.get("/health", response_model=HealthCheck, tags=["health"])
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        documents_count=vector_store.get_document_count(),
    )


@app.get("/api/stats", tags=["stats"])
async def get_stats():
    """Get application statistics."""
    docs = vector_store.get_all_documents()
    total_chunks = sum(doc.get("chunk_count", 0) for doc in docs)
    total_size = sum(doc.get("file_size", 0) for doc in docs)

    return {
        "total_documents": len(docs),
        "total_chunks": total_chunks,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / 1024 / 1024, 2),
    }
