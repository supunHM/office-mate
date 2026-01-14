# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for OCR and image processing
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY flask_requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r flask_requirements.txt

# Download spaCy model (optional, comment out if not needed)
# RUN python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Create directory for SQLite database (if using SQLite)
RUN mkdir -p /app/data

# Expose port
EXPOSE 10000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Run with gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "flask_app:app"]
