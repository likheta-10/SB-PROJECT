"""
Semantic Similarity Module
Computes semantic similarity between the student explanation and reference concept
using Sentence-BERT embeddings and Cosine Similarity.
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sys
import os

def compute_similarity(student_explanation, reference_concept, model_name='all-MiniLM-L6-v2'):
    """
    Computes semantic similarity using Sentence-BERT and Cosine Similarity.
    
    Parameters:
        student_explanation (str): The transcribed student text.
        reference_concept (str): The reference standard concept answer.
        model_name (str): Sentence-BERT model identifier.
        
    Returns:
        float: Cosine similarity score between 0.0 and 1.0.
    """
    if not student_explanation.strip() or not reference_concept.strip():
        print("[SemanticSimilarity] One or both of the inputs are empty. Returning 0.0 similarity.")
        return 0.0
        
    print(f"[SemanticSimilarity] Initializing SentenceTransformer model: '{model_name}'...", flush=True)
    try:
        # Load the sentence BERT model
        model = SentenceTransformer(model_name)
        
        print("[SemanticSimilarity] Encoding texts into vector embeddings...", flush=True)
        # Generate embeddings for both sentences
        embeddings = model.encode([student_explanation, reference_concept])
        
        # Reshape for sklearn cosine_similarity (expects 2D array)
        emb_student = embeddings[0].reshape(1, -1)
        emb_reference = embeddings[1].reshape(1, -1)
        
        # Compute Cosine Similarity
        similarity_matrix = cosine_similarity(emb_student, emb_reference)
        similarity_score = float(similarity_matrix[0][0])
        
        # Bound score between 0.0 and 1.0 (deal with tiny floating-point fluctuations or negative correlation)
        similarity_score = max(0.0, min(1.0, similarity_score))
        
        print(f"[SemanticSimilarity] Computed cosine similarity: {similarity_score:.4f} ({similarity_score * 100:.2f}%)", flush=True)
        return similarity_score
        
    except Exception as e:
        print(f"[SemanticSimilarity] Error during similarity calculation: {str(e)}", file=sys.stderr, flush=True)
        raise e
