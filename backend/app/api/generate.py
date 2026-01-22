"""API routes for content generation."""
from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.schemas import (
    GenerateRequest,
    GenerateResponse,
    QueryRequest,
    QueryResponse,
    ChatRequest,
    ChatResponse,
    GenerationType,
)
from app.services.vector_store import vector_store
from app.services.ai_service import ai_service

router = APIRouter(prefix="/generate", tags=["generate"])


def get_relevant_context(
    query: str,
    document_ids: List[str] = None,
    top_k: int = 5,
) -> tuple[str, List[dict]]:
    """Get relevant context from documents."""
    # Create embedding for query
    query_embedding = ai_service.create_embedding(query)

    # Search for relevant chunks
    matches = vector_store.query(
        query_embedding=query_embedding,
        top_k=top_k,
        document_ids=document_ids,
    )

    if not matches:
        return "", []

    # Combine contexts
    context_parts = []
    sources = []
    seen_docs = set()

    for match in matches:
        context_parts.append(match["content"])
        doc_id = match["metadata"].get("doc_id", "")
        if doc_id and doc_id not in seen_docs:
            seen_docs.add(doc_id)
            sources.append({
                "doc_id": doc_id,
                "filename": match["metadata"].get("filename", ""),
                "relevance": 1 - match["distance"],
            })

    context = "\n\n---\n\n".join(context_parts)
    return context, sources


@router.post("/content", response_model=GenerateResponse)
async def generate_content(request: GenerateRequest):
    """
    Generate content (reports, emails, summaries, etc.) based on documents.

    Types available:
    - report: Professional detailed report
    - email: Professional email
    - summary: Concise summary
    - analysis: Deep analysis
    - presentation: Presentation content
    - letter: Formal letter
    - memo: Internal memo
    - custom: Custom content
    """
    # Check if there are documents
    if vector_store.get_document_count() == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay documentos cargados. Por favor, suba documentos primero.",
        )

    # Get relevant context
    context, sources = get_relevant_context(
        request.prompt,
        request.document_ids,
        top_k=10,
    )

    if not context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró información relevante en los documentos.",
        )

    # Generate content
    try:
        result = ai_service.generate_content(
            prompt=request.prompt,
            context=context,
            generation_type=request.generation_type,
            language=request.language,
            tone=request.tone,
            length=request.length,
            additional_instructions=request.additional_instructions,
        )

        return GenerateResponse(
            content=result["content"],
            generation_type=request.generation_type.value,
            sources_used=[s["filename"] for s in sources],
            tokens_used=result["tokens_used"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando contenido: {str(e)}",
        )


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Query documents and get an AI-powered answer.
    """
    if vector_store.get_document_count() == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay documentos cargados. Por favor, suba documentos primero.",
        )

    # Get relevant context
    context, sources = get_relevant_context(
        request.query,
        request.document_ids,
        request.top_k,
    )

    if not context:
        return QueryResponse(
            answer="No encontré información relevante en los documentos para responder tu pregunta.",
            sources=[],
            query=request.query,
        )

    # Get answer
    try:
        answer = ai_service.answer_query(request.query, context)

        return QueryResponse(
            answer=answer,
            sources=sources,
            query=request.query,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando consulta: {str(e)}",
        )


@router.post("/chat", response_model=ChatResponse)
async def chat_with_documents(request: ChatRequest):
    """
    Have a conversation with your documents.
    """
    if request.use_documents and vector_store.get_document_count() == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay documentos cargados. Por favor, suba documentos primero.",
        )

    # Get the last user message for context retrieval
    last_user_message = ""
    for msg in reversed(request.messages):
        if msg.role == "user":
            last_user_message = msg.content
            break

    # Get relevant context
    context = ""
    sources = []
    if request.use_documents and last_user_message:
        context, sources = get_relevant_context(
            last_user_message,
            request.document_ids,
            top_k=5,
        )

    # Chat with context
    try:
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        result = ai_service.chat_with_context(messages, context if context else "No hay documentos cargados.")

        return ChatResponse(
            message=result["message"],
            sources=sources,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en el chat: {str(e)}",
        )


@router.get("/types")
async def get_generation_types():
    """Get available generation types with descriptions."""
    types = {
        "report": {
            "name": "Informe",
            "description": "Informe profesional y detallado con resumen ejecutivo, análisis y conclusiones",
            "icon": "📊",
        },
        "email": {
            "name": "Correo Electrónico",
            "description": "Correo profesional con asunto, cuerpo y cierre apropiado",
            "icon": "📧",
        },
        "summary": {
            "name": "Resumen",
            "description": "Resumen conciso con los puntos más importantes",
            "icon": "📝",
        },
        "analysis": {
            "name": "Análisis",
            "description": "Análisis profundo con patrones, tendencias y recomendaciones",
            "icon": "🔍",
        },
        "presentation": {
            "name": "Presentación",
            "description": "Contenido estructurado para diapositivas",
            "icon": "📑",
        },
        "letter": {
            "name": "Carta Formal",
            "description": "Carta formal con todos los elementos requeridos",
            "icon": "✉️",
        },
        "memo": {
            "name": "Memorando",
            "description": "Memorando interno con formato estándar",
            "icon": "📋",
        },
        "custom": {
            "name": "Personalizado",
            "description": "Contenido personalizado según tus instrucciones",
            "icon": "✨",
        },
    }
    return types


@router.post("/chart")
async def generate_chart(request: QueryRequest):
    """
    Generate chart/graph data based on documents.
    Returns structured data for frontend visualization.
    """
    if vector_store.get_document_count() == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay documentos cargados. Por favor, suba documentos primero.",
        )

    # Get relevant context
    context, sources = get_relevant_context(
        request.query,
        request.document_ids,
        top_k=10,
    )

    if not context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró información relevante en los documentos.",
        )

    # Generate chart data
    try:
        result = ai_service.generate_chart_data(request.query, context)

        if result["success"]:
            return {
                "success": True,
                "chart_data": result["data"],
                "sources": [s["filename"] for s in sources],
            }
        else:
            return {
                "success": False,
                "error": result["error"],
                "sources": [s["filename"] for s in sources],
            }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando gráfico: {str(e)}",
        )
