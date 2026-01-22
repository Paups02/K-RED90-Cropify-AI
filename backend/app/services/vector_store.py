"""Vector store service using ChromaDB for document embeddings."""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Optional, Any
import hashlib
from datetime import datetime
import json
import os

from app.core.config import settings


class VectorStore:
    """Manages document embeddings using ChromaDB."""

    def __init__(self):
        """Initialize ChromaDB client and collection."""
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"description": "Document embeddings for DocuMind AI"},
        )
        self._documents_metadata: Dict[str, dict] = {}
        self._load_metadata()

    def _load_metadata(self):
        """Load document metadata from file."""
        metadata_file = os.path.join(
            settings.chroma_persist_directory, "documents_metadata.json"
        )
        if os.path.exists(metadata_file):
            with open(metadata_file, "r") as f:
                self._documents_metadata = json.load(f)

    def _save_metadata(self):
        """Save document metadata to file."""
        metadata_file = os.path.join(
            settings.chroma_persist_directory, "documents_metadata.json"
        )
        os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
        with open(metadata_file, "w") as f:
            json.dump(self._documents_metadata, f)

    def add_document(
        self,
        doc_id: str,
        chunks: List[str],
        embeddings: List[List[float]],
        metadata: dict,
    ) -> int:
        """
        Add document chunks to the vector store.

        Args:
            doc_id: Unique document identifier
            chunks: List of text chunks
            embeddings: List of embedding vectors
            metadata: Document metadata

        Returns:
            Number of chunks added
        """
        if not chunks or not embeddings:
            return 0

        # Create unique IDs for each chunk
        chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]

        # Add metadata to each chunk
        chunk_metadatas = [
            {
                "doc_id": doc_id,
                "chunk_index": i,
                "filename": metadata.get("filename", ""),
                "file_type": metadata.get("file_type", ""),
            }
            for i in range(len(chunks))
        ]

        # Add to collection
        self.collection.add(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=chunk_metadatas,
        )

        # Store document metadata
        self._documents_metadata[doc_id] = {
            **metadata,
            "chunk_count": len(chunks),
            "upload_date": datetime.utcnow().isoformat(),
        }
        self._save_metadata()

        return len(chunks)

    def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        document_ids: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Query similar documents.

        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            document_ids: Optional list of document IDs to filter

        Returns:
            List of matching chunks with metadata
        """
        where_filter = None
        if document_ids:
            where_filter = {"doc_id": {"$in": document_ids}}

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        matches = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                matches.append(
                    {
                        "content": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else 0,
                    }
                )

        return matches

    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document and its chunks from the store.

        Args:
            doc_id: Document ID to delete

        Returns:
            True if deleted successfully
        """
        try:
            # Get all chunk IDs for this document
            results = self.collection.get(where={"doc_id": doc_id})
            if results and results["ids"]:
                self.collection.delete(ids=results["ids"])

            # Remove metadata
            if doc_id in self._documents_metadata:
                del self._documents_metadata[doc_id]
                self._save_metadata()

            return True
        except Exception:
            return False

    def get_document(self, doc_id: str) -> Optional[dict]:
        """Get document metadata."""
        return self._documents_metadata.get(doc_id)

    def get_all_documents(self) -> List[dict]:
        """Get all documents metadata."""
        return [
            {"id": doc_id, **metadata}
            for doc_id, metadata in self._documents_metadata.items()
        ]

    def get_document_count(self) -> int:
        """Get total number of documents."""
        return len(self._documents_metadata)

    def get_document_chunks(self, doc_id: str) -> List[str]:
        """Get all chunks for a document."""
        results = self.collection.get(
            where={"doc_id": doc_id}, include=["documents"]
        )
        return results["documents"] if results else []


# Singleton instance
vector_store = VectorStore()
