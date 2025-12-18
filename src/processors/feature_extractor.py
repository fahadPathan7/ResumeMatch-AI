"""
Feature Extraction Module
Extracts structured features from CV text
"""

import re
from typing import List, Dict, Optional
from .text_processor import TextProcessor


class FeatureExtractor:
    """Extracts features from CV text"""
    
    def __init__(self):
        self.text_processor = TextProcessor()
        
        # Common skill keywords (can be expanded)
        self.skill_patterns = [
            r'\b(python|java|javascript|typescript|react|angular|vue|node\.?js|sql|mongodb|postgresql|mysql)\b',
            r'\b(machine learning|deep learning|ai|artificial intelligence|nlp|natural language processing)\b',
            r'\b(aws|azure|gcp|cloud|docker|kubernetes|ci/cd|devops)\b',
            r'\b(agile|scrum|kanban|project management|leadership|team management)\b',
        ]
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from text
        
        Args:
            text: CV text content
            
        Returns:
            List of extracted skills
        """
        skills = set()
        text_lower = text.lower()
        
        # Extract using patterns
        for pattern in self.skill_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            skills.update([m.lower() for m in matches])
        
        # Look for skills sections
        sections = self.text_processor.identify_sections(text)
        if 'skills' in sections:
            skills_text = sections['skills'].lower()
            # Extract comma-separated or bullet-pointed skills
            skill_items = re.split(r'[,•\-\n]', skills_text)
            for item in skill_items:
                item = item.strip()
                if len(item) > 2 and len(item) < 50:  # Reasonable skill length
                    skills.add(item)
        
        return sorted(list(skills))
    
    def extract_experience_years(self, text: str) -> Optional[float]:
        """
        Extract years of experience from text
        
        Args:
            text: CV text content
            
        Returns:
            Years of experience or None
        """
        # Patterns for years of experience
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp)[:\s]+(\d+)\+?\s*(?:years?|yrs?)',
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1))
                except:
                    continue
        
        return None
    
    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """
        Extract education information
        
        Args:
            text: CV text content
            
        Returns:
            List of education entries with degree and field
        """
        education = []
        sections = self.text_processor.identify_sections(text)
        
        education_text = sections.get('education', '')
        if not education_text:
            return education
        
        # Look for degree patterns
        degree_patterns = [
            r'\b(bachelor|b\.?s\.?|b\.?a\.?|master|m\.?s\.?|m\.?a\.?|ph\.?d\.?|doctorate|mba)\b',
        ]
        
        lines = education_text.split('\n')
        for line in lines:
            line_lower = line.lower()
            for pattern in degree_patterns:
                if re.search(pattern, line_lower, re.IGNORECASE):
                    education.append({
                        'degree': line.strip(),
                        'field': self._extract_field(line)
                    })
                    break
        
        return education
    
    def _extract_field(self, text: str) -> str:
        """Extract field of study from education text"""
        # Common fields
        fields = ['computer science', 'engineering', 'business', 'mathematics', 
                  'physics', 'chemistry', 'biology', 'economics']
        text_lower = text.lower()
        for field in fields:
            if field in text_lower:
                return field.title()
        return ""
    
    def extract_job_titles(self, text: str) -> List[str]:
        """
        Extract job titles from experience section
        
        Args:
            text: CV text content
            
        Returns:
            List of job titles
        """
        titles = []
        sections = self.text_processor.identify_sections(text)
        
        experience_text = sections.get('experience', text)
        
        # Common job title patterns
        title_patterns = [
            r'\b(software engineer|developer|data scientist|analyst|manager|director|lead|senior|junior)\b',
        ]
        
        for pattern in title_patterns:
            matches = re.findall(pattern, experience_text, re.IGNORECASE)
            titles.extend([m.title() for m in matches])
        
        return list(set(titles))
    
    def extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        """
        Extract important keywords from text
        
        Args:
            text: CV text content
            min_length: Minimum keyword length
            
        Returns:
            List of keywords
        """
        # Clean and normalize
        text = self.text_processor.normalize_text(text, lowercase=True)
        
        # Extract words (excluding common stop words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                     'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        
        words = re.findall(r'\b\w+\b', text)
        keywords = [w for w in words if len(w) >= min_length and w not in stop_words]
        
        # Count frequency and return most common
        from collections import Counter
        keyword_counts = Counter(keywords)
        return [word for word, count in keyword_counts.most_common(50)]

