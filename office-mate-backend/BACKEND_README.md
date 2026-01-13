# Office Mate Backend

AI-Powered Document Organizer with Smart To-Do List for Office Administration

## Stack
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT with OAuth2
- **OCR**: Tesseract + Pillow
- **ML**: scikit-learn for document classification

## Project Structure

```
office-mate-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection and session
│   ├── models.py               # SQLAlchemy models (User, Document, Tag, Task)
│   ├── schemas.py              # Pydantic schemas for validation
│   │
│   ├── routers/                # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication endpoints (register, login, me)
│   │   ├── documents.py       # Document CRUD and upload
│   │   ├── tasks.py           # Task management
│   │   └── tags.py            # Tag management
│   │
│   └── services/              # Business logic services
│       ├── __init__.py
│       ├── auth.py            # JWT, password hashing, user authentication
│       ├── ocr.py             # OCR text extraction (PDF, images)
│       ├── classifier.py      # ML document classification
│       └── search.py          # Document search and filtering
│
├── models_store/              # ML model storage
│   └── classifier.joblib      # Trained classifier model
│
├── uploads/                   # User uploaded files (auto-created)
│   └── {user_id}/            # Per-user directories
│
├── init_db.py                 # Database initialization script
├── train_classifier.py        # ML model training script
├── requirements.txt           # Python dependencies
├── app.db                     # SQLite database (auto-created)
└── README.md                  # This file
```

## Database Models

### 1. **User**
- Authentication and user management
- Fields: id, email, username, hashed_password, full_name, is_active, is_admin, preferred_language
- Relationships: documents, tasks

### 2. **Document**
- Uploaded files with OCR content
- Fields: id, filename, file_path, file_size, file_type, category, content, content_si, ocr_confidence, user_id
- Categories: Finance, HR, Procurement, Maintenance
- Relationships: owner (User), tags (many-to-many), tasks

### 3. **Tag**
- Categorization labels for documents
- Fields: id, name, name_si (Sinhala), color
- Relationships: documents (many-to-many)

### 4. **Task**
- To-do items with optional document linking
- Fields: id, title, title_si, description, description_si, document_id, user_id, priority, due_date, status, completed_at
- Priorities: Low, Medium, High, Urgent
- Statuses: Todo, InProgress, Done
- Relationships: owner (User), document

## API Routes

### Authentication (`/auth`)
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login (returns JWT token)
- `GET /auth/me` - Get current user info
- `PUT /auth/me` - Update current user
- `POST /auth/logout` - Logout

### Documents (`/documents`)
- `POST /documents/` - Upload document (OCR + classification)
- `GET /documents/` - List documents with search/filter
- `GET /documents/{id}` - Get document details
- `PUT /documents/{id}` - Update document metadata
- `DELETE /documents/{id}` - Delete document
- `POST /documents/{id}/tags/{tag_id}` - Add tag to document
- `DELETE /documents/{id}/tags/{tag_id}` - Remove tag from document

### Tasks (`/tasks`)
- `POST /tasks/` - Create task
- `GET /tasks/` - List tasks with filters (status, priority, overdue, upcoming, document_id)
- `GET /tasks/{id}` - Get task details
- `PATCH /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

### Tags (`/tags`)
- `POST /tags/` - Create tag
- `GET /tags/` - List all tags
- `GET /tags/{id}` - Get tag details
- `PUT /tags/{id}` - Update tag
- `DELETE /tags/{id}` - Delete tag

## Setup Instructions

### 1. Install Dependencies
```bash
cd office-mate-backend
pip install -r requirements.txt
```

### 2. Install Tesseract OCR
**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

### 3. Initialize Database
```bash
python init_db.py
```
This creates tables and optionally seeds default tags and an admin user.

### 4. Train ML Classifier (Optional)
```bash
python train_classifier.py
```
Train the document classifier with sample data.

### 5. Run the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Variables

Create a `.env` file (optional):
```env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-secret-key-change-in-production
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Features

### ✅ Implemented
- User authentication with JWT
- Document upload with OCR (PDF, images)
- ML-based document classification (Finance, HR, Procurement, Maintenance)
- Tag management with Sinhala support
- Smart task management with document linking
- Priority levels and due dates
- Advanced search and filtering
- User-specific data isolation

### 🚧 To Be Enhanced
- Advanced OCR confidence scoring
- Multi-language NLP (Sinhala/English)
- Better ML model training with more data
- Document preview/download
- Email notifications for tasks
- Document versioning
- Audit logs

## API Documentation

Once the server is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

### Test Authentication
```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -F "username=test" \
  -F "password=test123"
```

### Test Document Upload
```bash
# Upload a document (requires auth token)
curl -X POST http://localhost:8000/documents/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf"
```

## Security Notes

1. Change `SECRET_KEY` in production
2. Use HTTPS in production
3. Implement rate limiting
4. Add input validation
5. Regular security audits

## License

Private - Office Mate System
