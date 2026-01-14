# 🚀 Flask Document Upload API - Complete Implementation

## Overview

Complete Flask backend implementation for **Office Mate** document management system with:

- ✅ File upload (PDF, Images, Word)
- ✅ OCR text extraction (PyPDF2 + Tesseract)
- ✅ NLP preprocessing (spaCy)
- ✅ ML classification (scikit-learn)
- ✅ Tag extraction
- ✅ SQLite database
- ✅ RESTful API

---

## 📁 Files Created

```
office-mate-backend/
├── flask_models.py              # SQLAlchemy models (User, Document, Tag, Task)
├── flask_documents_api.py       # Document upload API endpoint
├── flask_app.py                 # Main Flask application
├── flask_requirements.txt       # Python dependencies
├── train_flask_classifier.py    # ML model training script
├── test_flask_api.py           # API test suite
├── FLASK_INTEGRATION.md        # Models integration guide
└── FLASK_API_SETUP.md          # Complete setup guide
```

---

## ⚡ Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
pip install -r flask_requirements.txt
brew install tesseract  # macOS
python -m spacy download en_core_web_sm
```

### Step 2: Setup Database & ML Model

```bash
# Initialize database
python -c "from flask_app import app, db; app.app_context().push(); db.create_all()"

# Train classifier
python train_flask_classifier.py
```

### Step 3: Start Server

```bash
python flask_app.py
```

Server runs at: **http://localhost:5000**

---

## 🎯 API Endpoint

### POST /api/documents

Upload and process documents with OCR, NLP, and ML classification.

**Request:**

```bash
curl -X POST http://localhost:5000/api/documents \
  -F "file=@invoice.pdf" \
  -F "user_id=1"
```

**Response:**

```json
{
  "id": 1,
  "category": "Finance",
  "tags": ["invoice", "payment", "amount", "services", "rendered"],
  "summary": "Invoice for payment of services rendered. Amount due 5000. Please process payment by end of month.",
  "filename": "invoice.pdf",
  "created_at": "2026-01-14T10:30:00"
}
```

---

## 🔧 How It Works

### Processing Pipeline

```
File Upload (PDF/Image/Word)
    ↓
Text Extraction
├─ PDF: PyPDF2
├─ Image: Tesseract OCR
└─ Word: python-docx
    ↓
NLP Preprocessing (spaCy)
├─ Tokenization
├─ Lemmatization
└─ Stopword removal
    ↓
ML Classification (scikit-learn)
├─ TF-IDF vectorization
└─ LinearSVC prediction
    ↓
Tag Extraction (spaCy)
├─ Named entities
├─ Noun phrases
└─ Top 5 keywords
    ↓
Database Save (SQLite)
├─ Document record
└─ Tag associations
    ↓
JSON Response
```

---

## 📊 Database Models

### User

- `id`, `username`, `email`, `password_hash`
- Relationships: documents, tasks

### Document

- `id`, `file_path`, `original_name`, `text`, `category`, `user_id`
- Relationships: owner, tags (M:N), tasks

### Tag

- `id`, `name`
- Relationships: documents (M:N)

### Task

- `id`, `title`, `description`, `priority`, `due_date`, `status`
- `document_id` (optional), `user_id`
- Relationships: owner, document

---

## 🧪 Testing

### Quick Test

```bash
python test_flask_api.py
```

### Manual Test with curl

```bash
# Upload PDF
curl -X POST http://localhost:5000/api/documents \
  -F "file=@test.pdf"

# Get all documents
curl http://localhost:5000/api/documents?user_id=1

# Get specific document
curl http://localhost:5000/api/documents/1
```

### Python Test

```python
import requests

# Upload
files = {'file': open('invoice.pdf', 'rb')}
response = requests.post('http://localhost:5000/api/documents', files=files)
print(response.json())
```

---

## 🎨 Frontend Integration

### JavaScript Example

```javascript
// Upload document
const formData = new FormData();
formData.append("file", fileInput.files[0]);

const response = await fetch("http://localhost:5000/api/documents", {
  method: "POST",
  body: formData,
});

const result = await response.json();
console.log("Category:", result.category);
console.log("Tags:", result.tags);
console.log("Summary:", result.summary);
```

### React Example

```jsx
const handleUpload = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://localhost:5000/api/documents", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  setCategory(data.category);
  setTags(data.tags);
  setSummary(data.summary);
};
```

---

## 📋 Features Implemented

### ✅ File Processing

- PDF text extraction (PyPDF2)
- Image OCR (Tesseract)
- Word document extraction (python-docx)
- Fallback to OCR for scanned PDFs

### ✅ NLP & ML

- Text preprocessing with spaCy
- Document classification (4 categories)
- Named entity recognition
- Keyword extraction
- Summary generation

### ✅ Database

- SQLAlchemy models
- Many-to-many tag relationships
- User-specific data isolation
- SQLite storage

### ✅ API

- RESTful endpoints
- File upload handling
- JSON responses
- Error handling
- CORS enabled

---

## 🔐 Security Notes

**Current Implementation:**

- Uses `user_id` from form data (for testing)
- No authentication middleware

**Production Recommendations:**

1. Add authentication (Flask-Login or JWT)
2. Validate user permissions
3. Add rate limiting
4. Implement file scanning
5. Use environment variables for secrets

---

## 📦 Dependencies

### Core

- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-CORS 4.0.0

### Document Processing

- PyPDF2 3.0.1
- Pillow 10.2.0
- pytesseract 0.3.10
- python-docx 1.1.0

### NLP & ML

- spaCy 3.7.2
- scikit-learn 1.4.0
- joblib 1.3.2

---

## 🐛 Troubleshooting

### "spaCy model not found"

```bash
python -m spacy download en_core_web_sm
```

### "Tesseract not found"

```bash
brew install tesseract  # macOS
sudo apt install tesseract-ocr  # Ubuntu
```

### "No text extracted"

- Ensure Tesseract is installed
- Check if PDF is scanned (API auto-tries OCR)

### "Module not found"

```bash
pip install -r flask_requirements.txt
```

---

## 📚 Documentation

1. **Models**: See [flask_models.py](flask_models.py)
2. **API**: See [flask_documents_api.py](flask_documents_api.py)
3. **Setup**: See [FLASK_API_SETUP.md](FLASK_API_SETUP.md)
4. **Integration**: See [FLASK_INTEGRATION.md](FLASK_INTEGRATION.md)

---

## 🎯 Categories Supported

- **Finance**: Invoices, receipts, budgets, financial reports
- **HR**: Leave applications, employee records, payroll
- **Procurement**: Purchase orders, vendor quotations, contracts
- **Maintenance**: Repair requests, service reports, inspections

---

## ✅ Testing Checklist

- [x] SQLAlchemy models defined
- [x] Text extraction (PDF, Image, Word)
- [x] spaCy NLP preprocessing
- [x] ML classification
- [x] Tag extraction
- [x] Database operations
- [x] API endpoint
- [x] Error handling
- [x] CORS configuration
- [x] Documentation

---

## 🚀 Next Steps

1. **Test the API** with your documents
2. **Integrate with frontend** (React at localhost:5173)
3. **Add authentication** for production
4. **Train with more data** for better accuracy
5. **Deploy** to production server

---

## 📞 API Endpoints Summary

| Method | Endpoint             | Description               |
| ------ | -------------------- | ------------------------- |
| GET    | `/`                  | Health check              |
| POST   | `/api/documents`     | Upload & process document |
| GET    | `/api/documents`     | List all documents        |
| GET    | `/api/documents/:id` | Get specific document     |

---

## 🎉 You're Ready!

The Flask backend is **fully implemented** and ready to integrate with your existing UI.

**No UI changes were made** - only backend logic as requested! ✅

Start the server and test with:

```bash
python flask_app.py
python test_flask_api.py
```

---

**Happy Coding! 🚀**
