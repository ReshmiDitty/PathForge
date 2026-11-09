import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

class Config:
    """Application configuration loaded securely from environment variables."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback_dev_secret_key_never_in_production")
    
    # Database
    db_path = BASE_DIR / "pathforge.db"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{db_path}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # External API Integrations (Anthropic & Razorpay)
    # Strictly read from environment variables - never hardcoded
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "").strip()
    RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "").strip()
    
    # Helper flags to check if external integrations are actively configured
    @property
    def has_anthropic_key(self) -> bool:
        return bool(self.ANTHROPIC_API_KEY)
        
    @property
    def has_razorpay_keys(self) -> bool:
        return bool(self.RAZORPAY_KEY_ID and self.RAZORPAY_KEY_SECRET)

config = Config()

