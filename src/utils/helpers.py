"""
Helper Utilities
"""

from typing import Optional, Tuple
from ..parsers.pdf_parser import PDFParser
from ..parsers.docx_parser import DOCXParser
from ..parsers.text_parser import TextParser


def get_file_type(filename: str) -> str:
    """
    Determine file type from filename
    
    Args:
        filename: File name
        
    Returns:
        File type: 'pdf', 'docx', 'txt', or 'unknown'
    """
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.pdf'):
        return 'pdf'
    elif filename_lower.endswith('.docx') or filename_lower.endswith('.doc'):
        return 'docx'
    elif filename_lower.endswith('.txt'):
        return 'txt'
    else:
        return 'unknown'


def parse_document(file_content: bytes, filename: str) -> Tuple[str, str]:
    """
    Parse document based on file type
    
    Args:
        file_content: File content as bytes
        filename: File name
        
    Returns:
        Tuple of (extracted_text, file_type)
        
    Raises:
        ValueError: If file type is unsupported or parsing fails
    """
    file_type = get_file_type(filename)
    
    if file_type == 'pdf':
        parser = PDFParser()
        text = parser.extract_text(file_content, filename)
    elif file_type == 'docx':
        parser = DOCXParser()
        text = parser.extract_text(file_content, filename)
    elif file_type == 'txt':
        parser = TextParser()
        text = parser.extract_text(file_content, filename)
    else:
        raise ValueError(f"Unsupported file type: {file_type}. Supported types: PDF, DOCX, TXT")
    
    return text, file_type

