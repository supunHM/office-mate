# 🚀 Development Workflow Guide

## Quick Reference for Developers

---

## 📋 Daily Development Workflow

### 1. Start Development Server

```bash
cd office-mate-backend
source venv/bin/activate  # Activate virtual environment
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Check API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Test Endpoints

Use the interactive Swagger UI or curl commands from API_ROUTES.md

---

## 🔧 Common Development Tasks

### Adding a New Model Field

1. **Update Model** ([app/models.py](app/models.py))

```python
class Document(Base):
    # ... existing fields
    new_field = Column(String, nullable=True)  # Add new field
```

2. **Update Schema** ([app/schemas.py](app/schemas.py))

```python
class DocumentBase(BaseModel):
    # ... existing fields
    new_field: Optional[str] = None  # Add to schema
```

3. **Recreate Database** (Development only)

```bash
rm app.db  # Delete old database
python init_db.py  # Create new one
```

### Adding a New API Endpoint

1. **Add Route** ([app/routers/your_router.py](app/routers/))

```python
@router.get("/new-endpoint")
def new_endpoint(db: Session = Depends(get_db)):
    # Your logic here
    return {"message": "success"}
```

2. **Test in Swagger**

- Go to http://localhost:8000/docs
- Find your new endpoint
- Click "Try it out"

### Adding a New Service Function

1. **Create Function** ([app/services/your_service.py](app/services/))

```python
def process_data(data: str) -> dict:
    """Process data and return result"""
    # Your logic here
    return {"result": "processed"}
```

2. **Use in Router**

```python
from app.services.your_service import process_data

@router.post("/process")
def process(data: str):
    result = process_data(data)
    return result
```

---

## 🗄️ Database Management

### View Database Contents

```bash
# Install sqlite3 if not available
brew install sqlite3  # macOS
sudo apt install sqlite3  # Ubuntu

# Open database
sqlite3 app.db

# List tables
.tables

# Query users
SELECT * FROM users;

# Query documents
SELECT id, filename, category, user_id FROM documents;

# Exit
.exit
```

### Reset Database

```bash
# Delete database
rm app.db

# Recreate with seeds
python init_db.py
```

### Database Migrations (Production)

For production, use Alembic:

```bash
pip install alembic
alembic init migrations
# Configure alembic.ini with your database URL
alembic revision --autogenerate -m "Add new field"
alembic upgrade head
```

---

## 🧪 Testing

### Manual API Testing

#### 1. Register User

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123"
  }'
```

#### 2. Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -F "username=testuser" \
  -F "password=test123"
```

Save the `access_token` from response.

#### 3. Upload Document

```bash
curl -X POST http://localhost:8000/documents/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@test.pdf"
```

#### 4. Create Task

```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review document",
    "priority": "High",
    "due_date": "2026-01-20"
  }'
```

### Python Testing Script

Create `test_api.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "username": "test",
    "email": "test@test.com",
    "password": "test123"
})
print("Register:", response.json())

# Login
response = requests.post(f"{BASE_URL}/auth/login", data={
    "username": "test",
    "password": "test123"
})
token = response.json()["access_token"]
print("Token:", token)

# Get user info
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
print("User:", response.json())
```

Run: `python test_api.py`

---

## 🐛 Debugging

### Enable Debug Logging

Add to [app/main.py](app/main.py):

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs

Server logs appear in terminal where you ran `uvicorn`.

### Common Issues

#### 1. Import Errors

```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**: Install dependencies

```bash
pip install -r requirements.txt
```

#### 2. Database Locked

```
sqlite3.OperationalError: database is locked
```

**Solution**: Stop all server instances

```bash
pkill -f uvicorn
```

#### 3. Port Already in Use

```
ERROR: [Errno 48] Address already in use
```

**Solution**: Use different port or kill process

```bash
lsof -ti:8000 | xargs kill -9
uvicorn app.main:app --reload --port 8001
```

#### 4. Tesseract Not Found

```
pytesseract.pytesseract.TesseractNotFoundError
```

**Solution**: Install Tesseract

```bash
brew install tesseract tesseract-lang  # macOS
```

---

## 📦 Dependency Management

### Add New Dependency

```bash
pip install new-package
pip freeze > requirements.txt
```

### Update All Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Check Outdated Packages

```bash
pip list --outdated
```

---

## 🔐 Environment Configuration

### Development (.env)

```env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=dev-secret-key
CORS_ORIGINS=http://localhost:5173
```

### Production (.env.production)

```env
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=super-secure-random-key-here
CORS_ORIGINS=https://yourdomain.com
```

### Load Environment

```python
from dotenv import load_dotenv
load_dotenv('.env.production')
```

---

## 🚀 Deployment

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-sin \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t office-mate-backend .
docker run -p 8000:8000 office-mate-backend
```

### Production Server (gunicorn)

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:8000/
```

### Check All Endpoints

```bash
curl http://localhost:8000/docs
```

### Database Size

```bash
ls -lh app.db
```

### Upload Directory Size

```bash
du -sh uploads/
```

---

## 🔄 Git Workflow

### Initial Commit

```bash
git init
git add .
git commit -m "Initial backend implementation"
```

### Daily Work

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# ... edit files ...

# Commit changes
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature
```

### .gitignore Important Items

- `app.db` (database)
- `.env` (secrets)
- `uploads/` (user files)
- `__pycache__/` (Python cache)
- `venv/` (virtual environment)

---

## 📝 Code Style

### Follow PEP 8

```bash
pip install black flake8
black app/  # Format code
flake8 app/  # Check style
```

### Type Hints

Always use type hints:

```python
def process_document(doc_id: int, db: Session) -> Document:
    return db.query(Document).filter(Document.id == doc_id).first()
```

### Docstrings

```python
def upload_document(file: UploadFile) -> Document:
    """
    Upload and process a document.

    Args:
        file: The uploaded file

    Returns:
        Document: The created document object
    """
    pass
```

---

## 🎯 Best Practices

1. **Always use dependencies** for database sessions
2. **Filter by user_id** for user-specific queries
3. **Validate input** with Pydantic schemas
4. **Handle errors** with appropriate HTTP status codes
5. **Document APIs** with docstrings
6. **Use transactions** for multiple database operations
7. **Log important events** for debugging
8. **Test endpoints** after changes

---

## 📚 Useful Commands Cheatsheet

```bash
# Start server
uvicorn app.main:app --reload

# Install dependencies
pip install -r requirements.txt

# Reset database
rm app.db && python init_db.py

# Format code
black app/

# Check types
mypy app/

# View database
sqlite3 app.db

# Check running processes
ps aux | grep uvicorn

# Kill server
pkill -f uvicorn

# Check API health
curl http://localhost:8000/

# View logs (if redirected to file)
tail -f server.log
```

---

## 🆘 Getting Help

1. **API Documentation**: http://localhost:8000/docs
2. **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
3. **API Routes**: See [API_ROUTES.md](API_ROUTES.md)
4. **Setup**: See [BACKEND_README.md](BACKEND_README.md)

---

**Happy Coding! 🚀**
