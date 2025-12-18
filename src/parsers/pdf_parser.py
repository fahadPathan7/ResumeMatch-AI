"""
PDF Parser Module
Extracts text from PDF files using pdfplumber and PyPDF2 as fallback
"""

import io
from typing import Optional

# Optional imports with helpful error messages
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    pdfplumber = None

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    PyPDF2 = None


class PDFParser:
    """Parser for extracting text from PDF files"""
    
    def __init__(self):
        self.primary_parser = 'pdfplumber'
        self.fallback_parser = 'pypdf2'
    
    def extract_text(self, file_content: bytes, filename: Optional[str] = None) -> str:
        """
        Extract text from PDF file content
        
        Args:
            file_content: PDF file content as bytes
            filename: Optional filename for error messages
            
        Returns:
            Extracted text as string
            
        Raises:
            ValueError: If PDF cannot be parsed
        """
        # Try pdfplumber first (better for complex layouts)
        try:
            return self._extract_with_pdfplumber(file_content)
        except Exception as e:
            # Fallback to PyPDF2
            try:
                return self._extract_with_pypdf2(file_content)
            except Exception as fallback_error:
                error_msg = f"Failed to parse PDF file"
                if filename:
                    error_msg += f": {filename}"
                error_msg += f"\nPrimary parser error: {str(e)}\nFallback parser error: {str(fallback_error)}"
                raise ValueError(error_msg)
    
    def _extract_with_pdfplumber(self, file_content: bytes) -> str:
        """Extract text using pdfplumber"""
        if not PDFPLUMBER_AVAILABLE:
            raise ImportError("pdfplumber is not installed. Install it with: pip install pdfplumber")
        text_parts = []
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return '\n\n'.join(text_parts)
    
    def _extract_with_pypdf2(self, file_content: bytes) -> str:
        """Extract text using PyPDF2 as fallback"""
        if not PYPDF2_AVAILABLE:
            raise ImportError("PyPDF2 is not installed. Install it with: pip install PyPDF2")
        text_parts = []
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        
        return '\n\n'.join(text_parts)
    
    def is_valid_pdf(self, file_content: bytes) -> bool:
        """Check if file content is a valid PDF"""
        if PDFPLUMBER_AVAILABLE:
            try:
                with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                    return len(pdf.pages) > 0
            except:
                pass
        
        if PYPDF2_AVAILABLE:
            try:
                pdf_file = io.BytesIO(file_content)
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                return len(pdf_reader.pages) > 0
            except:
                pass
        
        return False

