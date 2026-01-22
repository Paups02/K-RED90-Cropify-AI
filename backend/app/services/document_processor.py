"""Document processing service for extracting text from various file formats."""
import os
from typing import List, Tuple
from pathlib import Path
import PyPDF2
from docx import Document as DocxDocument
from openpyxl import load_workbook
from pptx import Presentation
import markdown
from bs4 import BeautifulSoup


class DocumentProcessor:
    """Handles extraction of text content from various document formats."""

    SUPPORTED_EXTENSIONS = {
        ".pdf": "pdf",
        ".docx": "docx",
        ".doc": "docx",
        ".txt": "text",
        ".md": "markdown",
        ".xlsx": "excel",
        ".xls": "excel",
        ".pptx": "powerpoint",
        ".ppt": "powerpoint",
    }

    def __init__(self):
        """Initialize document processor."""
        pass

    def extract_text(self, file_path: str) -> str:
        """
        Extract text from a document file.

        Args:
            file_path: Path to the document file

        Returns:
            Extracted text content

        Raises:
            ValueError: If file type is not supported
        """
        path = Path(file_path)
        extension = path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {extension}")

        file_type = self.SUPPORTED_EXTENSIONS[extension]

        extractors = {
            "pdf": self._extract_from_pdf,
            "docx": self._extract_from_docx,
            "text": self._extract_from_text,
            "markdown": self._extract_from_markdown,
            "excel": self._extract_from_excel,
            "powerpoint": self._extract_from_powerpoint,
        }

        return extractors[file_type](file_path)

    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text_parts = []
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n\n".join(text_parts)

    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from Word document."""
        doc = DocxDocument(file_path)
        text_parts = []

        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)

        # Also extract from tables
        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_text:
                    text_parts.append(" | ".join(row_text))

        return "\n\n".join(text_parts)

    def _extract_from_text(self, file_path: str) -> str:
        """Extract text from plain text file."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            return file.read()

    def _extract_from_markdown(self, file_path: str) -> str:
        """Extract text from Markdown file."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            md_content = file.read()

        # Convert to HTML and extract plain text
        html = markdown.markdown(md_content)
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="\n\n")

    def _extract_from_excel(self, file_path: str) -> str:
        """Extract text from Excel file."""
        workbook = load_workbook(file_path, data_only=True)
        text_parts = []

        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
            text_parts.append(f"=== Hoja: {sheet_name} ===")

            for row in sheet.iter_rows(values_only=True):
                row_values = [str(cell) if cell is not None else "" for cell in row]
                if any(row_values):
                    text_parts.append(" | ".join(row_values))

        return "\n".join(text_parts)

    def _extract_from_powerpoint(self, file_path: str) -> str:
        """Extract text from PowerPoint file."""
        prs = Presentation(file_path)
        text_parts = []

        for slide_num, slide in enumerate(prs.slides, 1):
            slide_text = [f"=== Diapositiva {slide_num} ==="]

            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_text.append(shape.text)

            if len(slide_text) > 1:
                text_parts.append("\n".join(slide_text))

        return "\n\n".join(text_parts)

    def chunk_text(
        self, text: str, chunk_size: int = 1000, overlap: int = 200
    ) -> List[str]:
        """
        Split text into overlapping chunks for embedding.

        Args:
            text: Text to split
            chunk_size: Maximum size of each chunk
            overlap: Number of characters to overlap between chunks

        Returns:
            List of text chunks
        """
        if not text or len(text) <= chunk_size:
            return [text] if text else []

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size

            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence end within last 200 chars
                for i in range(min(200, end - start)):
                    if text[end - i - 1] in ".!?\n":
                        end = end - i
                        break

            chunks.append(text[start:end].strip())
            start = end - overlap

        return [c for c in chunks if c]

    def get_file_extension(self, filename: str) -> str:
        """Get file extension from filename."""
        return Path(filename).suffix.lower()

    def is_supported(self, filename: str) -> bool:
        """Check if file type is supported."""
        extension = self.get_file_extension(filename)
        return extension in self.SUPPORTED_EXTENSIONS


# Singleton instance
document_processor = DocumentProcessor()
