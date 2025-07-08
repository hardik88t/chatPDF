"""
Configuration management for ChatPDF clone
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDhu_53or7bktMHSOeO39zY40NNebvDKmA')
    
    # Token limits for cost optimization
    MAX_TOKENS_PER_REQUEST = 800
    MAX_CONTEXT_LENGTH = 4000
    
    # PDF Processing settings
    CHUNK_SIZE = 1000  # Characters per chunk
    CHUNK_OVERLAP = 200  # Overlap between chunks
    
    # Model settings
    MODEL_NAME = 'gemini-pro'
    TEMPERATURE = 0.1  # Low temperature for factual responses
    
    # File paths
    PDF_DIRECTORY = './pdfs'
    
    @classmethod
    def validate(cls):
        """Validate configuration settings"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        return True
