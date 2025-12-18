"""
Embedding Model Module
Handles text embedding generation using Sentence-BERT
"""

from sentence_transformers import SentenceTransformer
from typing import List, Optional
import numpy as np


class EmbeddingModel:
    """Manages embedding model for text similarity"""
    
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        """
        Initialize embedding model
        
        Args:
            model_name: Name of the Sentence-BERT model to use
        """
        self.model_name = model_name
        self.model: Optional[SentenceTransformer] = None
        self._load_model()
    
    def _load_model(self):
        """Load the Sentence-BERT model"""
        try:
            self.model = SentenceTransformer(self.model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load embedding model '{self.model_name}': {str(e)}")
    
    def encode(self, texts: List[str], normalize: bool = True) -> np.ndarray:
        """
        Generate embeddings for a list of texts
        
        Args:
            texts: List of text strings
            normalize: Whether to normalize embeddings
            
        Returns:
            Numpy array of embeddings
        """
        if not self.model:
            raise RuntimeError("Model not loaded")
        
        if not texts:
            return np.array([])
        
        # Filter out empty texts
        non_empty_texts = [text if text else " " for text in texts]
        
        embeddings = self.model.encode(
            non_empty_texts,
            convert_to_numpy=True,
            normalize_embeddings=normalize,
            show_progress_bar=False
        )
        
        return embeddings
    
    def encode_single(self, text: str, normalize: bool = True) -> np.ndarray:
        """
        Generate embedding for a single text
        
        Args:
            text: Text string
            normalize: Whether to normalize embedding
            
        Returns:
            Numpy array of embedding
        """
        return self.encode([text], normalize=normalize)[0]
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        return {
            'model_name': self.model_name,
            'loaded': self.model is not None,
            'max_seq_length': self.model.max_seq_length if self.model else None
        }

