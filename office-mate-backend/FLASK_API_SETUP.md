# Flask Document Upload API - Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd office-mate-backend

# Install Python packages
pip install -r flask_requirements.txt

# Install Tesseract OCR
# macOS:
brew install tesseract

# Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### 2. Initialize Database

```python
python -c "from flask_app import app, db; app.app_context().push(); db.create_all()"
```

Or run this script:
```python
from flask_app import app
from flask_models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create tables
    db.create_all()
    
    # Create test user
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash=generate_password_hash('password123'),
        full_name='Test User'
    )
    db.session.add(user)
    db.session.commit()
    print("Database initialized!")
```

### 3. Train ML Classifier (Optional)

Create `train_simple_classifier.py`:
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import joblib
import os

# Sample training data
train_texts = [
    "Invoice for payment of services rendered Amount due 5000",
    "Employee leave application from John for vacation",
    "Purchase order for office supplies and equipment",
    "Maintenance request for broken air conditioning system",
    "Financial report quarterly budget expenses revenue",
    "HR policy document employee handbook benefits",
    "Vendor quotation for procurement of computers",
    "Repair work order facility maintenance schedule",
]

labels = [
    'Finance', 'HR', 'Procurement', 'Maintenance',
    'Finance', 'HR', 'Procurement', 'Maintenance'
]

# Train classifier
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(train_texts)

classifier = LinearSVC()
classifier.fit(X, labels)

# Save model
os.makedirs('models_store', exist_ok=True)
joblib.dump({
    'vectorizer': vectorizer,
    'model': classifier
}, 'models_store/classifier.joblib')

print("Classifier trained and saved!")
```

Run: `python train_simple_classifier.py`

### 4. Start Flask Server

```bash
python flask_app.py
```

Server will run on: `http://localhost:5000`

---

## 📝 API Documentation

### POST /api/documents

Upload and process a document with OCR, NLP, and ML classification.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Fields:
  - `file`: Document file (PDF, Image, Word)
  - `user_id`: User ID (optional, defaults to 1)

**Response:**
```json
{
  "id": 1,
  "category": "Finance",
  "tags": ["invoice", "payment", "amount", "services"],
  "summary": "Invoice for payment of services rendered. Amount due 5000. Please process payment by end of month.",
  "filename": "invoice.pdf",
  "created_at": "2026-01-14T10:30:00"
}
```

**Status Codes:**
- `201`: Document created successfully
- `400`: Bad request (no file, invalid type, text extraction failed)
- `500`: Server error

---

## 🧪 Testing the API

### Using curl

```bash
# Upload a PDF
curl -X POST http://localhost:5000/api/documents \
  -F "file=@invoice.pdf" \
  -F "user_id=1"

# Upload an image
curl -X POST http://localhost:5000/api/documents \
  -F "file=@receipt.jpg" \
  -F "user_id=1"

# Get all documents
curl http://localhost:5000/api/documents?user_id=1

# Get specific document
curl http://localhost:5000/api/documents/1
```

### Using Python

```python
import requests

# Upload document
url = 'http://localhost:5000/api/documents'
files = {'file': open('invoice.pdf', 'rb')}
data = {'user_id': 1}

response = requests.post(url, files=files, data=data)
print(response.json())

# Get documents
response = requests.get(url, params={'user_id': 1})
print(response.json())
```

### Using JavaScript (Frontend)

```javascript
// Upload document
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('user_id', 1);

fetch('http://localhost:5000/api/documents', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => {
    console.log('Document uploaded:', data);
    console.log('Category:', data.category);
    console.log('Tags:', data.tags);
  });

// Get documents
fetch('http://localhost:5000/api/documents?user_id=1')
  .then(response => response.json())
  .then(documents => {
    console.log('Documents:', documents);
  });
```

### Using Postman

1. Create new POST request to `http://localhost:5000/api/documents`
2. Go to "Body" tab
3. Select "form-data"
4. Add field:
   - Key: `file` (change type to "File")
   - Value: Select your PDF/image file
5. Add field:
   - Key: `user_id`
   - Value: `1`
6. Click "Send"

---

## 🔧 How It Works

### Processing Pipeline

```
1. File Upload
   ↓
2. Text Extraction
   - PDF → PyPDF2
   - Image/Scanned PDF → Tesseract OCR
   - Word → python-docx
   ↓
3. NLP Preprocessing (spaCy)
   - Tokenization
   - Lemmatization
   - Stopword removal
   ↓
4. Text Classification (scikit-learn)
   - TF-IDF vectorization
   - LinearSVC prediction
   - Categories: Finance, HR, Procurement, Maintenance
   ↓
5. Tag Extraction (spaCy)
   - Named Entity Recognition
   - Noun phrase extraction
   - Top 5 keywords
   ↓
6. Summary Generation
   - First 3 sentences
   ↓
7. Database Storage (SQLite)
   - Save Document record
   - Create/link Tags
   ↓
8. JSON Response
```

### Fallback Mechanisms

If ML model not found:
- Uses keyword-based classification

If spaCy not found:
- Uses simple word frequency for tags
- Basic text preprocessing

If OCR fails on PDF:
- Tries image OCR (for scanned PDFs)

---

## 📁 File Structure

```
office-mate-backend/
├── flask_app.py                   # Main Flask application
├── flask_models.py                # SQLAlchemy models
├── flask_documents_api.py         # Document upload API
├── flask_requirements.txt         # Dependencies
├── train_simple_classifier.py     # ML model training
├── models_store/
│   └── classifier.joblib         # Trained ML model
├── uploads/
│   └── 1/                        # User-specific folders
│       ├── 20260114_invoice.pdf
│       └── 20260114_receipt.jpg
└── office_mate.db                # SQLite database
```

---

## 🎯 Supported File Types

- **PDF**: `.pdf`
- **Images**: `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`
- **Word**: `.docx`

Max file size: 10 MB

---

## 🔐 Security Notes

**Important**: The current implementation uses `user_id` from form data for testing.

For production:
1. Implement proper authentication (Flask-Login or JWT)
2. Extract `user_id` from session/token
3. Validate user permissions
4. Add rate limiting
5. Scan uploaded files for malware

Example with Flask-Login:
```python
from flask_login import login_required, current_user

@documents_bp.route('/api/documents', methods=['POST'])
@login_required
def upload_document():
    user_id = current_user.id  # Get from authenticated user
    # ... rest of code
```

---

## 🐛 Troubleshooting

### 1. "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

### 2. "Tesseract not found"
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr
```

### 3. "No text extracted from PDF"
- PDF might be scanned/image-based
- API will automatically try OCR
- Ensure Tesseract is installed

### 4. "Import error: No module named 'docx'"
```bash
pip install python-docx
```

### 5. Database errors
```bash
# Reset database
rm office_mate.db
python -c "from flask_app import app, db; app.app_context().push(); db.create_all()"
```

---

## 🚀 Integration with Existing Frontend

The API is designed to work with your existing React frontend at `http://localhost:5173`.

### Frontend Integration Steps:

1. **Update API base URL** in your frontend:
```javascript
const API_BASE = 'http://localhost:5000';
```

2. **Create upload function**:
```javascript
async function uploadDocument(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE}/api/documents`, {
    method: 'POST',
    body: formData,
    // Add auth headers if needed
  });
  
  return response.json();
}
```

3. **Display results**:
```javascript
const result = await uploadDocument(selectedFile);
console.log('Category:', result.category);
console.log('Tags:', result.tags);
console.log('Summary:', result.summary);
```

---

## 📊 Example Response

```json
{
  "id": 1,
  "category": "Finance",
  "tags": [
    "invoice",
    "payment",
    "ABC Company",
    "services",
    "amount"
  ],
  "summary": "Invoice for payment of services rendered. Amount due: $5,000. Payment terms: Net 30 days.",
  "filename": "invoice_2024.pdf",
  "created_at": "2026-01-14T10:30:45.123456"
}
```

---

## ✅ Testing Checklist

- [ ] Install all dependencies
- [ ] Install Tesseract OCR
- [ ] Download spaCy model
- [ ] Initialize database
- [ ] Train ML classifier
- [ ] Start Flask server
- [ ] Upload PDF document
- [ ] Upload image document
- [ ] Check category prediction
- [ ] Verify tags extraction
- [ ] Test with scanned PDF
- [ ] Test error handling
- [ ] Test from frontend

---

**API is ready for integration!** 🎉
