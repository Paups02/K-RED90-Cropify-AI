"""Application configuration settings."""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App settings
    app_name: str = "DocuMind AI"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # OpenAI
    openai_api_key: str = ""

    # Upload settings
    max_upload_size: int = 52428800  # 50MB
    allowed_extensions: str = "pdf,docx,txt,md,xlsx,pptx"
    upload_directory: str = "./uploads"

    # ChromaDB
    chroma_persist_directory: str = "./chroma_db"

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    @property
    def allowed_extensions_list(self) -> List[str]:
        """Return allowed extensions as a list."""
        return [ext.strip().lower() for ext in self.allowed_extensions.split(",")]

    @property
    def cors_origins_list(self) -> List[str]:
        """Return CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.upload_directory, exist_ok=True)
os.makedirs(settings.chroma_persist_directory, exist_ok=True)
