# 🏗️ Office Mate Backend - Visual Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)                       │
│                      http://localhost:5173                           │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ HTTP/JSON + JWT
                                 │
┌────────────────────────────────┴────────────────────────────────────┐
│                    FASTAPI APPLICATION (Port 8000)                   │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                      MIDDLEWARE                               │  │
│  │  • CORS (Cross-Origin Resource Sharing)                      │  │
│  │  • Authentication (JWT Token Validation)                     │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                       ROUTERS (API Endpoints)                 │  │
│  │                                                               │  │
│  │  /auth          → Authentication (5 routes)                  │  │
│  │  /documents     → Document Management (7 routes)             │  │
│  │  /tasks         → Task Management (5 routes)                 │  │
│  │  /tags          → Tag Management (5 routes)                  │  │
│  │  /stats         → Statistics (3 routes)                      │  │
│  └───────────────────────────┬─────────────────────────────────┘  │
│                               │                                      │
│  ┌───────────────────────────┴─────────────────────────────────┐  │
│  │                       SERVICES (Business Logic)               │  │
│  │                                                               │  │
│  │  auth.py        → JWT, password hashing, user validation     │  │
│  │  ocr.py         → Text extraction (PDF/Image/Word)           │  │
│  │  classifier.py  → ML classification (TF-IDF + SVC)           │  │
│  │  search.py      → Document search & filtering                │  │
│  └───────────────────────────┬─────────────────────────────────┘  │
│                               │                                      │
│  ┌───────────────────────────┴─────────────────────────────────┐  │
│  │                    SCHEMAS (Pydantic Models)                  │  │
│  │                                                               │  │
│  │  UserCreate, UserRead, DocumentRead, TaskCreate, etc.        │  │
│  │  • Request validation                                         │  │
│  │  • Response serialization                                     │  │
│  └───────────────────────────┬─────────────────────────────────┘  │
│                               │                                      │
│  ┌───────────────────────────┴─────────────────────────────────┐  │
│  │                    DATABASE (SQLAlchemy ORM)                  │  │
│  │                                                               │  │
│  │  models.py → User, Document, Tag, Task                       │  │
│  │              + document_tags (junction table)                │  │
│  └───────────────────────────┬─────────────────────────────────┘  │
└───────────────────────────────┼─────────────────────────────────────┘
                                │
                   ┌────────────┴────────────┐
                   │                         │
          ┌────────▼────────┐       ┌───────▼────────┐
          │   SQLite DB     │       │  File Storage  │
          │   (app.db)      │       │  (uploads/)    │
          │                 │       │                │
          │ • users         │       │ • {user_id}/   │
          │ • documents     │       │   - file1.pdf  │
          │ • tasks         │       │   - file2.jpg  │
          │ • tags          │       │   - file3.docx │
          │ • document_tags │       │                │
          └─────────────────┘       └────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL DEPENDENCIES                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Tesseract OCR                                                       │
│  ├─ Extract text from images                                        │
│  ├─ Support English + Sinhala                                       │
│  └─ Used by: services/ocr.py                                        │
│                                                                       │
│  scikit-learn                                                        │
│  ├─ TF-IDF vectorization                                            │
│  ├─ LinearSVC classifier                                            │
│  └─ Used by: services/classifier.py                                 │
│                                                                       │
│  PyPDF2 + python-docx                                               │
│  ├─ Extract text from PDFs                                          │
│  ├─ Extract text from Word documents                                │
│  └─ Used by: services/ocr.py                                        │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                      DATA FLOW DIAGRAM                               │
└─────────────────────────────────────────────────────────────────────┘

1. DOCUMENT UPLOAD FLOW
   ┌────────┐    file     ┌──────────┐    OCR     ┌─────────┐
   │ Client │ ─────────> │ FastAPI  │ ─────────> │  OCR    │
   └────────┘             │ /documents│            │ Service │
                          └──────┬───┘            └────┬────┘
                                 │                     │
                                 │ extracted text      │
                                 │<────────────────────┘
                                 │
                                 │    classify    ┌──────────┐
                                 ├──────────────> │ ML Model │
                                 │                └────┬─────┘
                                 │                     │
                                 │ category            │
                                 │<────────────────────┘
                                 │
                                 │    save       ┌──────────┐
                                 ├─────────────> │ Database │
                                 │               └──────────┘
                                 │
                                 │    store      ┌──────────┐
                                 └─────────────> │  Disk    │
                                                 └──────────┘

2. AUTHENTICATION FLOW
   ┌────────┐  username/pwd  ┌──────────┐   verify   ┌──────────┐
   │ Client │ ─────────────> │  /auth   │ ────────> │  Auth    │
   └────────┘                 │  /login  │            │ Service  │
       ▲                      └────┬─────┘            └────┬─────┘
       │                           │                       │
       │ JWT token                 │                       │ check pwd
       │<──────────────────────────┤                       │
       │                           │                       ▼
       │                           │                  ┌──────────┐
       │                           │                  │ Database │
       │                           │                  └──────────┘
       │
       │ subsequent requests with Bearer token
       │
       ▼
   All protected endpoints


3. TASK MANAGEMENT FLOW
   ┌────────┐  create task  ┌──────────┐   validate  ┌──────────┐
   │ Client │ ────────────> │  /tasks  │ ──────────> │ Database │
   └────────┘                └────┬─────┘             └──────────┘
       ▲                          │
       │                          │ link to document (optional)
       │ task with status         │
       │<─────────────────────────┘
       │
       │ PATCH /tasks/{id}
       │ (update status to "Done")
       │
       └────────────────────────> auto-set completed_at


┌─────────────────────────────────────────────────────────────────────┐
│                    DATABASE RELATIONSHIPS                            │
└─────────────────────────────────────────────────────────────────────┘

         ┌────────────┐
         │    User    │
         │            │
         │ • id       │
         │ • username │
         │ • email    │
         └──────┬─────┘
                │
                │ owns (1:N)
       ┌────────┴────────┐
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│  Document   │   │    Task     │
│             │   │             │
│ • id        │   │ • id        │
│ • filename  │   │ • title     │
│ • content   │   │ • priority  │
│ • category  │   │ • status    │
│ • user_id   │   │ • user_id   │
└──────┬──────┘   └──────┬──────┘
       │                 │
       │ links (N:1)     │
       │<────────────────┘
       │
       │ tagged with (M:N)
       │
       │  ┌───────────────┐
       └──┤ document_tags │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────┐
          │    Tag    │
          │           │
          │ • id      │
          │ • name    │
          │ • color   │
          └───────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                                   │
└─────────────────────────────────────────────────────────────────────┘

Layer 1: CORS
  ├─ Allow only specific origins (React frontend)
  └─ Configured in main.py

Layer 2: Authentication
  ├─ JWT tokens with expiration (7 days)
  ├─ OAuth2 password bearer scheme
  └─ Secure password hashing (bcrypt)

Layer 3: Authorization
  ├─ User-specific data filtering (user_id in queries)
  ├─ Token validation on every request
  └─ Admin role checks where needed

Layer 4: Input Validation
  ├─ Pydantic schemas for all requests
  ├─ File type validation
  └─ File size limits (10 MB)

Layer 5: Data Protection
  ├─ Per-user upload directories
  ├─ Sanitized filenames
  └─ SQL injection protection (SQLAlchemy ORM)


┌─────────────────────────────────────────────────────────────────────┐
│                    ML CLASSIFICATION PIPELINE                        │
└─────────────────────────────────────────────────────────────────────┘

Training Phase (train_classifier.py):
  ┌────────────────┐
  │ Sample Docs    │
  │ (labeled data) │
  └───────┬────────┘
          │
          ▼
  ┌────────────────┐
  │  TF-IDF        │
  │  Vectorizer    │
  └───────┬────────┘
          │
          ▼
  ┌────────────────┐
  │  LinearSVC     │
  │  Training      │
  └───────┬────────┘
          │
          ▼
  ┌────────────────┐
  │ Save Model     │
  │ (.joblib)      │
  └────────────────┘

Prediction Phase (on document upload):
  ┌────────────────┐
  │ OCR Text       │
  └───────┬────────┘
          │
          ▼
  ┌────────────────┐
  │ Load Model     │
  └───────┬────────┘
          │
          ▼
  ┌────────────────┐
  │ Vectorize Text │
  └───────┬────────┘
          │
          ▼
  ┌────────────────┐
  │ Predict        │
  │ Category       │
  └───────┬────────┘
          │
          ▼
  Finance / HR / Procurement / Maintenance


┌─────────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────┘

Development:
  ├─ SQLite database (app.db)
  ├─ Local file storage (uploads/)
  └─ uvicorn --reload

Production (Recommended):
  ├─ PostgreSQL database
  ├─ Cloud storage (S3/Azure Blob)
  ├─ Docker containerization
  ├─ Nginx reverse proxy
  ├─ SSL/TLS certificates
  └─ gunicorn + uvicorn workers
```

**Key Metrics:**

- 25 API endpoints
- 4 database models
- 4 service modules
- 5 router modules
- JWT authentication
- ML-powered classification
- Bilingual support (EN/SI)
