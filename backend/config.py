import os
from pathlib import Path
from dotenv import load_dotenv

# Get the base directory (project root)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from project root
load_dotenv(BASE_DIR / ".env")


class Config:
    """Centralized configuration for the Wahl-Chatbot application."""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))
    
    # Server Configuration
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    
    # Directory Paths
    DATA_DIR = BASE_DIR / "data"
    FRONTEND_DIR = BASE_DIR / "frontend"
    
    # File Paths
    KNOWLEDGE_BASE_PATH = DATA_DIR / "knowledge_base.json"
    PARTIES_INFO_PATH = DATA_DIR / "parties_info.json"
    SYSTEM_PROMPT_PATH = DATA_DIR / "system_prompt.txt"
    FAQS_PATH = DATA_DIR / "faqs.json"
    
    # API Limits
    MAX_MESSAGE_LENGTH = 1000
    MAX_CHAT_HISTORY_LENGTH = 50
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        
        if not cls.DATA_DIR.exists():
            raise FileNotFoundError(f"Data directory not found: {cls.DATA_DIR}")
        
        if not cls.FRONTEND_DIR.exists():
            raise FileNotFoundError(f"Frontend directory not found: {cls.FRONTEND_DIR}")
