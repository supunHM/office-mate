"""
Application configuration settings
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-123456789")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# File Upload
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {
    "pdf": "application/pdf",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "tiff": "image/tiff",
    "bmp": "image/bmp",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

# ML Model
MODEL_PATH = BASE_DIR / "models_store" / "classifier.joblib"

# Categories
DOCUMENT_CATEGORIES = ["Finance", "HR", "Procurement", "Maintenance", "unknown"]

# Task Priorities
TASK_PRIORITIES = ["Low", "Medium", "High", "Urgent"]

# Task Statuses
TASK_STATUSES = ["Todo", "InProgress", "Done"]

# Languages
SUPPORTED_LANGUAGES = ["en", "si"]  # English, Sinhala

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
