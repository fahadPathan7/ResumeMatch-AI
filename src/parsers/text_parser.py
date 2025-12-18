"""
Text Parser Module
Handles plain text input
"""

from typing import Optional, Union


class TextParser:
    """Parser for plain text content"""
    
    def extract_text(self, content: Union[str, bytes], filename: Optional[str] = None) -> str:
        """
        Extract text from plain text content
        
        Args:
            content: Text content as string or bytes
            filename: Optional filename for error messages
            
        Returns:
            Text as string
        """
        if isinstance(content, bytes):
            try:
                # Try UTF-8 first
                return content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    # Fallback to latin-1
                    return content.decode('latin-1')
                except UnicodeDecodeError:
                    error_msg = f"Failed to decode text file"
                    if filename:
                        error_msg += f": {filename}"
                    raise ValueError(error_msg)
        return str(content)
    
    def is_valid_text(self, content: Union[str, bytes]) -> bool:
        """Check if content is valid text"""
        try:
            if isinstance(content, bytes):
                content.decode('utf-8')
            return True
        except:
            return False

