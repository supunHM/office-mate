"""
Utility functions and helpers
"""
import os
from typing import Optional
from datetime import datetime, date


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def is_allowed_file_type(filename: str, allowed_extensions: set) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal attacks"""
    # Remove path components
    filename = os.path.basename(filename)
    # Remove dangerous characters
    dangerous_chars = ['/', '\\', '..', '\0', '\n', '\r']
    for char in dangerous_chars:
        filename = filename.replace(char, '')
    return filename


def calculate_days_until(target_date: Optional[date]) -> Optional[int]:
    """Calculate days until target date"""
    if not target_date:
        return None
    today = date.today()
    delta = target_date - today
    return delta.days


def is_overdue(target_date: Optional[date], status: str) -> bool:
    """Check if task is overdue"""
    if not target_date or status == "Done":
        return False
    return target_date < date.today()


def get_priority_weight(priority: str) -> int:
    """Get numeric weight for priority sorting"""
    priority_map = {
        "Urgent": 4,
        "High": 3,
        "Medium": 2,
        "Low": 1,
    }
    return priority_map.get(priority, 0)


def detect_language(text: str) -> str:
    """Detect if text is primarily Sinhala or English (simple heuristic)"""
    if not text:
        return "en"
    
    # Count Sinhala Unicode characters (0D80-0DFF)
    sinhala_chars = sum(1 for char in text if '\u0D80' <= char <= '\u0DFF')
    total_chars = len(text.strip())
    
    if total_chars == 0:
        return "en"
    
    # If more than 30% Sinhala characters, consider it Sinhala
    if sinhala_chars / total_chars > 0.3:
        return "si"
    return "en"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length with suffix"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
