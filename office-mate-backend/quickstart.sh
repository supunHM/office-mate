#!/bin/bash
# Quick Start Script for Office Mate Backend

echo "======================================"
echo "Office Mate Backend - Quick Start"
echo "======================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check Tesseract
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  Tesseract OCR not found."
    echo "   Please install it:"
    echo "   macOS: brew install tesseract tesseract-lang"
    echo "   Ubuntu: sudo apt-get install tesseract-ocr tesseract-ocr-sin"
    echo ""
    read -p "Continue without Tesseract? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Tesseract found: $(tesseract --version | head -1)"
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo ""
echo "🗄️  Initializing database..."
python init_db.py

# Success message
echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Then visit:"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Health Check: http://localhost:8000/"
echo ""
echo "Default admin credentials (if seeded):"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
