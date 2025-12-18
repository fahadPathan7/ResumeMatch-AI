"""
Similarity Calculator Module
Calculates similarity between embeddings
"""

import numpy as np
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity
from .embedding_model import EmbeddingModel


class SimilarityCalculator:
    """Calculates similarity between texts using embeddings"""
    
    def __init__(self, embedding_model: EmbeddingModel):
        """
        Initialize similarity calculator
        
        Args:
            embedding_model: EmbeddingModel instance
        """
        self.embedding_model = embedding_model
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        if not text1 or not text2:
            return 0.0
        
        embedding1 = self.embedding_model.encode_single(text1)
        embedding2 = self.embedding_model.encode_single(text2)
        
        # Reshape for sklearn cosine_similarity
        embedding1 = embedding1.reshape(1, -1)
        embedding2 = embedding2.reshape(1, -1)
        
        similarity = cosine_similarity(embedding1, embedding2)[0][0]
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, float(similarity)))
    
    def calculate_section_similarities(self, cv_sections: Dict[str, str], 
                                       job_sections: Dict[str, str]) -> Dict[str, float]:
        """
        Calculate similarity for each section
        
        Args:
            cv_sections: Dictionary of CV sections
            job_sections: Dictionary of job description sections
            
        Returns:
            Dictionary of section similarities
        """
        similarities = {}
        
        # Calculate similarity for each section
        all_sections = set(cv_sections.keys()) | set(job_sections.keys())
        
        for section in all_sections:
            cv_text = cv_sections.get(section, "")
            job_text = job_sections.get(section, "")
            
            if cv_text and job_text:
                similarities[section] = self.calculate_similarity(cv_text, job_text)
            else:
                similarities[section] = 0.0
        
        return similarities
    
    def calculate_overall_similarity(self, cv_text: str, job_text: str) -> float:
        """
        Calculate overall similarity between CV and job description
        
        Args:
            cv_text: Full CV text
            job_text: Full job description text
            
        Returns:
            Overall similarity score
        """
        return self.calculate_similarity(cv_text, job_text)

