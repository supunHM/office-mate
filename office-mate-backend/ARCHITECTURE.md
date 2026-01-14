# Office Mate Backend - Architecture Summary

## 🎯 Project Overview

**AI-Powered Document Organizer with Smart To-Do List**

- Target: Sri Lankan offices
- Features: OCR, ML classification, bilingual support (English/Sinhala)
- Categories: Finance, HR, Procurement, Maintenance

---

## 🏗️ Technology Stack

| Component           | Technology                        |
| ------------------- | --------------------------------- |
| Framework           | FastAPI (Python)                  |
| Database            | SQLite + SQLAlchemy ORM           |
| Authentication      | JWT (OAuth2) + bcrypt             |
| OCR                 | Tesseract + Pillow                |
| ML/NLP              | scikit-learn (TF-IDF + LinearSVC) |
| Document Processing | PyPDF2, python-docx               |

---

## 📂 Complete File Structure

```
office-mate-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration (SECRET_KEY, DB, uploads)
│   ├── database.py                # SQLAlchemy setup
│   ├── models.py                  # 4 models: User, Document, Tag, Task
│   ├── schemas.py                 # Pydantic validation schemas
│   ├── utils.py                   # Helper functions
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py               # Register, login, profile (/auth)
│   │   ├── documents.py          # Upload, CRUD, tagging (/documents)
│   │   ├── tasks.py              # Task CRUD with filters (/tasks)
│   │   ├── tags.py               # Tag management (/tags)
│   │   └── stats.py              # Dashboard & statistics (/stats)
│   │
│   └── services/
│       ├── __init__.py
│       ├── auth.py               # JWT, password hashing, dependencies
│       ├── ocr.py                # PDF/Image/Word text extraction
│       ├── classifier.py         # ML category prediction
│       └── search.py             # Document search/filtering
│
├── models_store/
│   └── classifier.joblib         # Trained ML model
│
├── uploads/                      # User file storage
│   └── {user_id}/               # Per-user directories
│
├── init_db.py                    # DB initialization + seeding
├── train_classifier.py           # ML model training
├── requirements.txt              # Python dependencies
├── app.db                        # SQLite database (auto-created)
├── BACKEND_README.md             # Setup & deployment guide
└── API_ROUTES.md                 # Complete API documentation
```

---

## 🗄️ Database Schema

### User

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    is_active BOOLEAN DEFAULT 1,
    is_admin BOOLEAN DEFAULT 0,
    preferred_language VARCHAR DEFAULT 'en',
    created_at DATETIME
);
```

### Document

```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    filename VARCHAR NOT NULL,
    file_path VARCHAR NOT NULL,
    file_size INTEGER DEFAULT 0,
    file_type VARCHAR,
    category VARCHAR DEFAULT 'unknown',
    content TEXT,                  -- OCR extracted
    content_si TEXT,               -- Sinhala text
    ocr_confidence INTEGER,
    user_id INTEGER REFERENCES users(id),
    created_at DATETIME,
    updated_at DATETIME
);
```

### Tag

```sql
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    name_si VARCHAR,               -- Sinhala translation
    color VARCHAR DEFAULT '#3B82F6',
    created_at DATETIME
);

-- Many-to-many relationship
CREATE TABLE document_tags (
    document_id INTEGER REFERENCES documents(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (document_id, tag_id)
);
```

### Task

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    title_si VARCHAR,
    description TEXT,
    description_si TEXT,
    document_id INTEGER REFERENCES documents(id),
    user_id INTEGER REFERENCES users(id),
    priority VARCHAR DEFAULT 'Low',
    due_date DATE,
    status VARCHAR DEFAULT 'Todo',
    completed_at DATETIME,
    created_at DATETIME,
    updated_at DATETIME
);
```

---

## 🔌 API Endpoints Summary

### Authentication (5 routes)

- POST `/auth/register` - User registration
- POST `/auth/login` - JWT token generation
- GET `/auth/me` - Current user info
- PUT `/auth/me` - Update profile
- POST `/auth/logout` - Logout

### Documents (7 routes)

- POST `/documents/` - Upload + OCR + classify
- GET `/documents/` - List with search/filter
- GET `/documents/{id}` - Get details
- PUT `/documents/{id}` - Update metadata
- DELETE `/documents/{id}` - Delete
- POST `/documents/{id}/tags/{tag_id}` - Add tag
- DELETE `/documents/{id}/tags/{tag_id}` - Remove tag

### Tasks (5 routes)

- POST `/tasks/` - Create task
- GET `/tasks/` - List with filters
- GET `/tasks/{id}` - Get details
- PATCH `/tasks/{id}` - Update
- DELETE `/tasks/{id}` - Delete

### Tags (5 routes)

- POST `/tags/` - Create tag
- GET `/tags/` - List all
- GET `/tags/{id}` - Get details
- PUT `/tags/{id}` - Update
- DELETE `/tags/{id}` - Delete

### Statistics (3 routes)

- GET `/stats/dashboard` - Overview stats
- GET `/stats/documents` - Document analytics
- GET `/stats/tasks` - Task analytics

**Total: 25 API endpoints**

---

## 🔐 Security Features

1. **Password Security**: bcrypt hashing
2. **JWT Authentication**: Secure token-based auth (7-day expiry)
3. **User Isolation**: All queries filtered by user_id
4. **File Security**: Per-user upload directories
5. **CORS**: Configurable origins
6. **Input Validation**: Pydantic schemas

---

## 🤖 AI/ML Features

### OCR Pipeline

1. **File Upload** → FastAPI UploadFile
2. **Format Detection** → PDF/Image/Word
3. **Text Extraction** → Tesseract (eng+sin)
4. **Content Storage** → Database

### Document Classification

1. **Training**: TF-IDF vectorization + LinearSVC
2. **Prediction**: Categorize into 4 classes
3. **Model Storage**: joblib serialization
4. **Auto-classification**: On document upload

### Supported Formats

- **PDF**: PyPDF2 text extraction
- **Images**: PNG, JPG, TIFF, BMP (Tesseract)
- **Word**: DOCX (python-docx)

---

## 🌐 Bilingual Support

### Sinhala + English

- User `preferred_language` field
- Task `title_si`, `description_si` fields
- Tag `name_si` field
- Document `content_si` field
- OCR language detection (eng+sin)

---

## 📊 Business Logic Highlights

### Task Management

- Auto-set `completed_at` when status → "Done"
- Overdue detection (due_date < today && status != Done)
- Upcoming filter (next N days)
- Priority-based sorting

### Document Search

- Full-text search (filename, content)
- Category filtering
- Date range filtering
- Tag-based organization

### Statistics

- Document count by category
- Task completion rates
- Overdue task tracking
- Recent activity (7 days)

---

## 🚀 Deployment Checklist

### Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install Tesseract
brew install tesseract tesseract-lang  # macOS
sudo apt install tesseract-ocr tesseract-ocr-sin  # Ubuntu

# 3. Initialize database
python init_db.py

# 4. Run server
uvicorn app.main:app --reload --port 8000
```

### Production

1. Change `SECRET_KEY` in `.env`
2. Use PostgreSQL instead of SQLite
3. Configure CORS_ORIGINS
4. Enable HTTPS
5. Add rate limiting
6. Set up file backup/CDN
7. Monitor logs and errors

---

## 🔧 Configuration

### Environment Variables

```env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:5173
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
```

### File Upload Limits

- Max size: 10 MB
- Allowed: PDF, Word, PNG, JPG, TIFF, BMP

---

## 📈 Future Enhancements

1. **Advanced NLP**: Sinhala entity extraction
2. **Email Integration**: Task deadline reminders
3. **Document Versioning**: Track changes
4. **Audit Logs**: User activity tracking
5. **Advanced Search**: Elasticsearch integration
6. **Mobile API**: Optimized endpoints
7. **Batch Upload**: Multiple file processing
8. **OCR Confidence**: Better accuracy scoring

---

## 🧪 Testing

### Manual Testing

```bash
# Register user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -F "username=test" \
  -F "password=test123"

# Upload document
curl -X POST http://localhost:8000/documents/ \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@invoice.pdf"
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📚 Related Documentation

- [BACKEND_README.md](BACKEND_README.md) - Setup guide
- [API_ROUTES.md](API_ROUTES.md) - Complete API reference
- FastAPI docs: https://fastapi.tiangolo.com

---

## 👥 Default Credentials (After Seeding)

**Admin User:**

- Username: `admin`
- Password: `admin123`
- Email: `admin@officemate.lk`

⚠️ **Change this in production!**

---

**Last Updated**: January 14, 2026
**Version**: 1.0.0
