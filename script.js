"""
Sentence-BERT Model Loader
Encapsulates SentenceTransformer model initialization with caching to optimize performance.
"""

from sentence_transformers import SentenceTransformer
import os

# Module level cache for loaded SBERT models
_model_cache = {}

def load_sbert_model(model_name="all-MiniLM-L6-v2"):
    """
    Retrieves the cached model or instantiates a new SentenceTransformer.
    Optimizes performance under multi-request scenarios in Flask.
    """
    global _model_cache
    
    if model_name not in _model_cache:
        print(f"[ModelLoader] Model '{model_name}' not cached. Loading into memory...", flush=True)
        # Load the model (downloads if not present locally)
        _model_cache[model_name] = SentenceTransformer(model_name)
        print(f"[ModelLoader] Model '{model_name}' loaded successfully.", flush=True)
    else:
        print(f"[ModelLoader] Retrieving cached model instance for '{model_name}'.", flush=True)
        
    return _model_cache[model_name]
