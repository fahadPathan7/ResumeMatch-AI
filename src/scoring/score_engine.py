"""
Scoring Engine Module
Calculates weighted matching scores
"""

from typing import Dict, Optional
from ..models.similarity_calculator import SimilarityCalculator
from ..processors.feature_extractor import FeatureExtractor


class ScoreEngine:
    """Calculates weighted matching scores"""
    
    def __init__(self, similarity_calculator: SimilarityCalculator):
        """
        Initialize scoring engine
        
        Args:
            similarity_calculator: SimilarityCalculator instance
        """
        self.similarity_calculator = similarity_calculator
        self.feature_extractor = FeatureExtractor()
        
        # Default scoring weights
        self.weights = {
            'overall_similarity': 0.4,
            'skills_match': 0.3,
            'experience_match': 0.2,
            'education_match': 0.1
        }
    
    def calculate_match_score(self, cv_text: str, job_text: str, 
                              cv_sections: Optional[Dict[str, str]] = None,
                              job_sections: Optional[Dict[str, str]] = None) -> Dict:
        """
        Calculate comprehensive match score
        
        Args:
            cv_text: Full CV text
            job_text: Full job description text
            cv_sections: CV sections dictionary
            job_sections: Job description sections dictionary
            
        Returns:
            Dictionary with scores and breakdown
        """
        # Calculate overall similarity
        overall_similarity = self.similarity_calculator.calculate_overall_similarity(
            cv_text, job_text
        )
        
        # Calculate section-wise similarities
        if cv_sections and job_sections:
            section_similarities = self.similarity_calculator.calculate_section_similarities(
                cv_sections, job_sections
            )
        else:
            section_similarities = {}
        
        # Extract features
        cv_skills = set(self.feature_extractor.extract_skills(cv_text))
        job_skills = set(self.feature_extractor.extract_skills(job_text))
        
        # Calculate skills match
        if job_skills:
            matched_skills = cv_skills & job_skills
            skills_match = len(matched_skills) / len(job_skills)
        else:
            skills_match = 0.0
        
        # Calculate experience match
        cv_exp = self.feature_extractor.extract_experience_years(cv_text)
        job_exp = self.feature_extractor.extract_experience_years(job_text)
        
        if job_exp and cv_exp:
            if cv_exp >= job_exp:
                experience_match = 1.0
            else:
                experience_match = max(0.0, cv_exp / job_exp)
        else:
            # Use section similarity if available
            experience_match = section_similarities.get('experience', 0.0)
        
        # Calculate education match
        cv_education = self.feature_extractor.extract_education(cv_text)
        job_education = self.feature_extractor.extract_education(job_text)
        
        if job_education:
            # Simple check if CV has similar education
            education_match = 1.0 if cv_education else 0.5
        else:
            education_match = section_similarities.get('education', 0.0)
        
        # Calculate weighted final score
        final_score = (
            overall_similarity * self.weights['overall_similarity'] +
            skills_match * self.weights['skills_match'] +
            experience_match * self.weights['experience_match'] +
            education_match * self.weights['education_match']
        )
        
        # Convert to percentage
        final_score = final_score * 100
        
        return {
            'final_score': round(final_score, 2),
            'overall_similarity': round(overall_similarity * 100, 2),
            'skills_match': round(skills_match * 100, 2),
            'experience_match': round(experience_match * 100, 2),
            'education_match': round(education_match * 100, 2),
            'section_similarities': {k: round(v * 100, 2) for k, v in section_similarities.items()},
            'matched_skills': list(matched_skills) if job_skills else [],
            'missing_skills': list(job_skills - cv_skills) if job_skills else [],
            'cv_skills_count': len(cv_skills),
            'job_skills_count': len(job_skills),
            'matched_skills_count': len(matched_skills) if job_skills else 0
        }
    
    def get_score_interpretation(self, score: float) -> str:
        """
        Get interpretation of score
        
        Args:
            score: Match score (0-100)
            
        Returns:
            Interpretation string
        """
        if score >= 90:
            return "Excellent Match"
        elif score >= 75:
            return "Good Match"
        elif score >= 60:
            return "Moderate Match"
        elif score >= 40:
            return "Weak Match"
        else:
            return "Poor Match"
    
    def set_weights(self, weights: Dict[str, float]):
        """
        Set custom scoring weights
        
        Args:
            weights: Dictionary of weights (should sum to 1.0)
        """
        total = sum(weights.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total}")
        self.weights = weights

