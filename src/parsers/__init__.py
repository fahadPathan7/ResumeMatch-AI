"""
Document Parsers Module
"""

from .pdf_parser import PDFParser
from .docx_parser import DOCXParser
from .text_parser import TextParser

__all__ = ['PDFParser', 'DOCXParser', 'TextParser']

