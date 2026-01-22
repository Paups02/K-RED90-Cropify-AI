"""Pydantic schemas for request/response models."""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class GenerationType(str, Enum):
    """Types of content that can be generated."""
    REPORT = "report"
    EMAIL = "email"
    SUMMARY = "summary"
    ANALYSIS = "analysis"
    PRESENTATION = "presentation"
    LETTER = "letter"
    MEMO = "memo"
    CUSTOM = "custom"


class DocumentBase(BaseModel):
    """Base document schema."""
    filename: str
    file_type: str
    file_size: int


class DocumentCreate(DocumentBase):
    """Schema for creating a document."""
    pass


class Document(DocumentBase):
    """Schema for a stored document."""
    id: str
    upload_date: datetime
    chunk_count: int = 0

    class Config:
        from_attributes = True


class DocumentList(BaseModel):
    """Schema for list of documents."""
    documents: List[Document]
    total: int


class QueryRequest(BaseModel):
    """Schema for querying documents."""
    query: str = Field(..., min_length=1, max_length=2000)
    document_ids: Optional[List[str]] = None
    top_k: int = Field(default=5, ge=1, le=20)


class QueryResponse(BaseModel):
    """Schema for query response."""
    answer: str
    sources: List[dict]
    query: str


class GenerateRequest(BaseModel):
    """Schema for content generation request."""
    prompt: str = Field(..., min_length=1, max_length=5000)
    generation_type: GenerationType = GenerationType.CUSTOM
    document_ids: Optional[List[str]] = None
    language: str = "es"  # Default Spanish
    tone: str = "professional"  # professional, casual, formal, friendly
    length: str = "medium"  # short, medium, long
    additional_instructions: Optional[str] = None


class GenerateResponse(BaseModel):
    """Schema for content generation response."""
    content: str
    generation_type: str
    sources_used: List[str]
    tokens_used: int


class ChatMessage(BaseModel):
    """Schema for chat message."""
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str


class ChatRequest(BaseModel):
    """Schema for chat request."""
    messages: List[ChatMessage]
    document_ids: Optional[List[str]] = None
    use_documents: bool = True


class ChatResponse(BaseModel):
    """Schema for chat response."""
    message: str
    sources: List[dict]


class HealthCheck(BaseModel):
    """Schema for health check response."""
    status: str
    version: str
    documents_count: int
