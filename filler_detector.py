import os

class Config:
    """
    Configuration settings for Voice Based Concept Understanding Analyser application.
    """
    # Flask application settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'voice_concept_analyser_secret_key_2026')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Upload folder configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit audio uploads to 16 MB
    
    # Supported audio formats
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}
    
    # ML/DL Model configuration
    WHISPER_MODEL = 'base'  # Options: 'tiny', 'base', 'small', 'medium', 'large'
    SBERT_MODEL = 'all-MiniLM-L6-v2'  # Lightweight and highly accurate for sentence embeddings
    
    # Feature extraction settings
    TOP_DB_SILENCE_THRESHOLD = 25  # dB below reference to be considered silent in Librosa
