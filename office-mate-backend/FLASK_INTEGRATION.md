# Flask Models Integration Guide

## Quick Setup

### 1. Install Dependencies

```bash
pip install flask flask-sqlalchemy
```

### 2. Configure Flask App

```python
from flask import Flask
from flask_models import db, init_db, User, Document, Tag, Task

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///office_mate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize database
init_db(app)
```

### 3. Create Tables

```python
# Run once to create all tables
from flask_models import db
with app.app_context():
    db.create_all()
```

## Usage Examples

### Create a User

```python
from werkzeug.security import generate_password_hash
from flask_models import db, User

user = User(
    username='john',
    email='john@example.com',
    password_hash=generate_password_hash('password123'),
    full_name='John Doe'
)
db.session.add(user)
db.session.commit()
```

### Create a Document

```python
from flask_models import db, Document

doc = Document(
    file_path='/uploads/invoice.pdf',
    original_name='invoice.pdf',
    text='Extracted text from OCR...',
    category='Finance',
    user_id=user.id
)
db.session.add(doc)
db.session.commit()
```

### Add Tags to Document

```python
from flask_models import db, Tag

# Create tags
tag1 = Tag(name='Invoice')
tag2 = Tag(name='2024')

# Add to document
doc.tags.append(tag1)
doc.tags.append(tag2)
db.session.commit()
```

### Create a Task

```python
from datetime import date
from flask_models import db, Task

task = Task(
    title='Review invoice',
    description='Check amounts and approve',
    priority='High',
    due_date=date(2026, 1, 20),
    status='Todo',
    document_id=doc.id,
    user_id=user.id
)
db.session.add(task)
db.session.commit()
```

### Query Examples

#### Get user's documents

```python
user_docs = Document.query.filter_by(user_id=user.id).all()
```

#### Search documents by category

```python
finance_docs = Document.query.filter_by(category='Finance').all()
```

#### Get documents with specific tag

```python
tag = Tag.query.filter_by(name='Invoice').first()
tagged_docs = tag.documents  # Access via backref
```

#### Get user's tasks with filters

```python
# Get pending high priority tasks
tasks = Task.query.filter_by(
    user_id=user.id,
    status='Todo',
    priority='High'
).all()

# Get overdue tasks
from datetime import date
overdue = Task.query.filter(
    Task.user_id == user.id,
    Task.status != 'Done',
    Task.due_date < date.today()
).all()
```

#### Get task with linked document

```python
task = Task.query.get(1)
if task.document:
    print(f"Task linked to: {task.document.original_name}")
```

## Model Relationships

```
User (1) ──────> (N) Document
  │                    │
  │                    │ (M)
  │                    │
  │                   (N)
  │                   Tag
  │
  └──────> (N) Task
              │
              └──> (1) Document [optional]
```

## Field Descriptions

### User

- `id`: Primary key
- `username`: Unique username (indexed)
- `email`: Unique email (indexed)
- `password_hash`: Hashed password
- `full_name`: Full name (optional)
- `created_at`: Account creation timestamp

### Document

- `id`: Primary key
- `file_path`: Path to stored file
- `original_name`: Original filename
- `text`: OCR extracted text
- `category`: Document category (Finance, HR, etc.)
- `created_at`: Upload timestamp (indexed)
- `user_id`: Foreign key to User
- `tags`: Many-to-many with Tag
- `tasks`: One-to-many with Task

### Tag

- `id`: Primary key
- `name`: Unique tag name (indexed)
- `documents`: Many-to-many with Document (via backref)

### Task

- `id`: Primary key
- `title`: Task title
- `description`: Task description
- `priority`: Low, Medium, High, Urgent
- `due_date`: Due date
- `status`: Todo, InProgress, Done
- `created_at`: Creation timestamp
- `document_id`: Optional link to Document
- `user_id`: Foreign key to User

## Complete Flask App Example

```python
from flask import Flask, jsonify, request
from flask_models import db, init_db, User, Document, Tag, Task
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///office_mate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'change-me-in-production'

init_db(app)

@app.route('/documents', methods=['GET'])
def get_documents():
    docs = Document.query.all()
    return jsonify([{
        'id': d.id,
        'original_name': d.original_name,
        'category': d.category,
        'tags': [t.name for t in d.tags]
    } for d in docs])

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'priority': t.priority,
        'status': t.status
    } for t in tasks])

if __name__ == '__main__':
    app.run(debug=True)
```

## Migration from FastAPI

If you have existing FastAPI models, the data structure is the same. You just need to:

1. Export data from FastAPI SQLite database
2. Import into Flask SQLite database
3. Or simply point Flask to the same database file

The SQLAlchemy table structure is compatible!
