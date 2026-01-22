"""API routes for document management."""
import os
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, status
import aiofiles

from app.core.config import settings
from app.models.schemas import Document, DocumentList
from app.services.document_processor import document_processor
from app.services.vector_store import vector_store
from app.services.ai_service import ai_service

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=Document)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document and process it for AI queries.

    Supports: PDF, DOCX, TXT, MD, XLSX, PPTX
    """
    # Validate file extension
    if not document_processor.is_supported(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no soportado. Formatos permitidos: {', '.join(settings.allowed_extensions_list)}",
        )

    # Validate file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > settings.max_upload_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Archivo muy grande. Máximo permitido: {settings.max_upload_size // 1024 // 1024}MB",
        )

    # Generate unique ID and save file
    doc_id = str(uuid.uuid4())
    file_extension = document_processor.get_file_extension(file.filename)
    saved_filename = f"{doc_id}{file_extension}"
    file_path = os.path.join(settings.upload_directory, saved_filename)

    try:
        # Save file
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        # Extract text
        text_content = document_processor.extract_text(file_path)
        if not text_content.strip():
            os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo extraer texto del documento. El archivo puede estar vacío o corrupto.",
            )

        # Create chunks
        chunks = document_processor.chunk_text(text_content)

        # Create embeddings
        embeddings = ai_service.create_embeddings(chunks)

        # Store in vector database
        metadata = {
            "filename": file.filename,
            "file_type": file_extension[1:],
            "file_size": file_size,
            "saved_path": file_path,
        }
        chunk_count = vector_store.add_document(doc_id, chunks, embeddings, metadata)

        return Document(
            id=doc_id,
            filename=file.filename,
            file_type=file_extension[1:],
            file_size=file_size,
            upload_date=datetime.utcnow(),
            chunk_count=chunk_count,
        )

    except HTTPException:
        raise
    except Exception as e:
        # Clean up on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando documento: {str(e)}",
        )


@router.get("/", response_model=DocumentList)
async def list_documents():
    """Get list of all uploaded documents."""
    docs = vector_store.get_all_documents()
    documents = [
        Document(
            id=doc["id"],
            filename=doc.get("filename", "Unknown"),
            file_type=doc.get("file_type", ""),
            file_size=doc.get("file_size", 0),
            upload_date=datetime.fromisoformat(doc.get("upload_date", datetime.utcnow().isoformat())),
            chunk_count=doc.get("chunk_count", 0),
        )
        for doc in docs
    ]
    return DocumentList(documents=documents, total=len(documents))


@router.get("/{doc_id}", response_model=Document)
async def get_document(doc_id: str):
    """Get a specific document by ID."""
    doc = vector_store.get_document(doc_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado",
        )

    return Document(
        id=doc_id,
        filename=doc.get("filename", "Unknown"),
        file_type=doc.get("file_type", ""),
        file_size=doc.get("file_size", 0),
        upload_date=datetime.fromisoformat(doc.get("upload_date", datetime.utcnow().isoformat())),
        chunk_count=doc.get("chunk_count", 0),
    )


@router.delete("/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document."""
    doc = vector_store.get_document(doc_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado",
        )

    # Delete file from disk
    saved_path = doc.get("saved_path")
    if saved_path and os.path.exists(saved_path):
        os.remove(saved_path)

    # Delete from vector store
    vector_store.delete_document(doc_id)

    return {"message": "Documento eliminado correctamente", "id": doc_id}


@router.post("/upload-multiple", response_model=List[Document])
async def upload_multiple_documents(files: List[UploadFile] = File(...)):
    """Upload multiple documents at once."""
    results = []
    errors = []

    for file in files:
        try:
            # Reuse single upload logic
            doc = await upload_document(file)
            results.append(doc)
        except HTTPException as e:
            errors.append({"filename": file.filename, "error": e.detail})
        except Exception as e:
            errors.append({"filename": file.filename, "error": str(e)})

    if errors and not results:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "No se pudo subir ningún documento", "errors": errors},
        )

    return results
