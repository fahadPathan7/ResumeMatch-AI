"""
Text Processing Module
Cleans and normalizes text content
"""

import re
from typing import List, Dict


class TextProcessor:
    """Processes and cleans text content"""
    
    def __init__(self):
        self.section_keywords = {
            'experience': ['experience', 'work experience', 'employment', 'employment history', 'career', 'professional experience'],
            'education': ['education', 'academic', 'qualifications', 'degrees', 'university', 'college'],
            'skills': ['skills', 'technical skills', 'competencies', 'expertise', 'proficiencies'],
            'certifications': ['certifications', 'certificates', 'certified', 'credentials'],
            'summary': ['summary', 'profile', 'objective', 'about', 'overview']
        }
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text content
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', ' ', text)
        
        # Normalize line breaks
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def identify_sections(self, text: str) -> Dict[str, str]:
        """
        Identify and extract CV sections
        
        Args:
            text: CV text content
            
        Returns:
            Dictionary with section names as keys and content as values
        """
        sections = {}
        lines = text.split('\n')
        current_section = 'other'
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            line_clean = re.sub(r'[^\w\s]', '', line_lower)
            
            # Check if line is a section header
            section_found = False
            for section_name, keywords in self.section_keywords.items():
                for keyword in keywords:
                    if keyword in line_clean and len(line_clean) < 50:  # Likely a header
                        # Save previous section
                        if current_section != 'other' and current_content:
                            sections[current_section] = '\n'.join(current_content)
                        # Start new section
                        current_section = section_name
                        current_content = []
                        section_found = True
                        break
                if section_found:
                    break
            
            if not section_found and line.strip():
                current_content.append(line)
        
        # Save last section
        if current_section != 'other' and current_content:
            sections[current_section] = '\n'.join(current_content)
        
        # If no sections found, return full text as 'other'
        if not sections:
            sections['other'] = text
        
        return sections
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        
        Args:
            text: Text content
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def normalize_text(self, text: str, lowercase: bool = False) -> str:
        """
        Normalize text for processing
        
        Args:
            text: Text content
            lowercase: Whether to convert to lowercase
            
        Returns:
            Normalized text
        """
        text = self.clean_text(text)
        if lowercase:
            text = text.lower()
        return text

