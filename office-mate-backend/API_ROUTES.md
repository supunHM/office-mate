# Office Mate API - Complete Route Reference

## Base URL
`http://localhost:8000`

---

## 🔐 Authentication Routes (`/auth`)

### 1. Register User
**POST** `/auth/register`
```json
Request Body:
{
  "username": "string",
  "email": "user@example.com",
  "password": "string",
  "full_name": "string (optional)",
  "preferred_language": "en" // or "si"
}

Response: UserRead (201 Created)
```

### 2. Login
**POST** `/auth/login`
```
Form Data:
- username: string
- password: string

Response:
{
  "access_token": "string",
  "token_type": "bearer"
}
```

### 3. Get Current User
**GET** `/auth/me`
- **Auth Required**: Bearer Token
```json
Response: UserRead
{
  "id": 1,
  "email": "user@example.com",
  "username": "string",
  "full_name": "string",
  "is_active": true,
  "is_admin": false,
  "preferred_language": "en",
  "created_at": "2026-01-14T..."
}
```

### 4. Update Current User
**PUT** `/auth/me`
- **Auth Required**: Bearer Token
```json
Request Body:
{
  "email": "newemail@example.com (optional)",
  "full_name": "string (optional)",
  "preferred_language": "en (optional)",
  "password": "newpassword (optional)"
}

Response: UserRead
```

### 5. Logout
**POST** `/auth/logout`
- **Auth Required**: Bearer Token
- Client-side token removal

---

## 📄 Document Routes (`/documents`)

### 1. Upload Document
**POST** `/documents/`
- **Auth Required**: Bearer Token
- **Content-Type**: multipart/form-data
```
Form Data:
- file: File (PDF, Word, Image)

Response: DocumentRead (201 Created)
- Performs OCR extraction
- Auto-classifies into categories
- Stores file securely
```

### 2. List Documents
**GET** `/documents/`
- **Auth Required**: Bearer Token
- **Query Parameters**:
  - `query` (optional): Search term
  - `category` (optional): Finance, HR, Procurement, Maintenance
  - `date_from` (optional): YYYY-MM-DD
  - `date_to` (optional): YYYY-MM-DD

```json
Response: List[DocumentListRead]
[
  {
    "id": 1,
    "filename": "invoice.pdf",
    "category": "Finance",
    "file_size": 12345,
    "file_type": "application/pdf",
    "user_id": 1,
    "created_at": "2026-01-14T...",
    "tags": [...]
  }
]
```

### 3. Get Document Details
**GET** `/documents/{document_id}`
- **Auth Required**: Bearer Token
```json
Response: DocumentRead (includes full content)
```

### 4. Update Document
**PUT** `/documents/{document_id}`
- **Auth Required**: Bearer Token
```json
Request Body:
{
  "filename": "string (optional)",
  "category": "string (optional)"
}

Response: DocumentRead
```

### 5. Delete Document
**DELETE** `/documents/{document_id}`
- **Auth Required**: Bearer Token
- Deletes file from storage

### 6. Add Tag to Document
**POST** `/documents/{document_id}/tags/{tag_id}`
- **Auth Required**: Bearer Token

### 7. Remove Tag from Document
**DELETE** `/documents/{document_id}/tags/{tag_id}`
- **Auth Required**: Bearer Token

---

## ✅ Task Routes (`/tasks`)

### 1. Create Task
**POST** `/tasks/`
- **Auth Required**: Bearer Token
```json
Request Body:
{
  "title": "string",
  "title_si": "string (optional)",
  "description": "string (optional)",
  "description_si": "string (optional)",
  "document_id": 1, // optional - link to document
  "priority": "Low", // Low, Medium, High, Urgent
  "due_date": "2026-01-20", // YYYY-MM-DD
  "status": "Todo" // Todo, InProgress, Done
}

Response: TaskRead (201 Created)
```

### 2. List Tasks
**GET** `/tasks/`
- **Auth Required**: Bearer Token
- **Query Parameters**:
  - `status` (optional): Todo, InProgress, Done
  - `priority` (optional): Low, Medium, High, Urgent
  - `overdue` (optional): true/false
  - `upcoming_days` (optional): integer (e.g., 7 for next 7 days)
  - `document_id` (optional): Filter by linked document

```json
Response: List[TaskRead]
```

### 3. Get Task Details
**GET** `/tasks/{task_id}`
- **Auth Required**: Bearer Token

### 4. Update Task
**PATCH** `/tasks/{task_id}`
- **Auth Required**: Bearer Token
```json
Request Body (all optional):
{
  "title": "string",
  "description": "string",
  "priority": "High",
  "due_date": "2026-01-25",
  "status": "InProgress"
}

Response: TaskRead
- Auto-sets completed_at when status becomes "Done"
```

### 5. Delete Task
**DELETE** `/tasks/{task_id}`
- **Auth Required**: Bearer Token

---

## 🏷️ Tag Routes (`/tags`)

### 1. Create Tag
**POST** `/tags/`
- **Auth Required**: Bearer Token
```json
Request Body:
{
  "name": "string",
  "name_si": "string (optional)",
  "color": "#3B82F6 (optional)"
}

Response: TagRead (201 Created)
```

### 2. List All Tags
**GET** `/tags/`
- **Auth Required**: Bearer Token

### 3. Get Tag Details
**GET** `/tags/{tag_id}`
- **Auth Required**: Bearer Token

### 4. Update Tag
**PUT** `/tags/{tag_id}`
- **Auth Required**: Bearer Token

### 5. Delete Tag
**DELETE** `/tags/{tag_id}`
- **Auth Required**: Bearer Token

---

## 📊 Statistics Routes (`/stats`)

### 1. Dashboard Statistics
**GET** `/stats/dashboard`
- **Auth Required**: Bearer Token
```json
Response:
{
  "documents": {
    "total": 42,
    "recent": 5, // Last 7 days
    "by_category": [
      {"category": "Finance", "count": 15},
      {"category": "HR", "count": 10}
    ]
  },
  "tasks": {
    "total": 28,
    "completed": 15,
    "pending": 13,
    "overdue": 3,
    "upcoming": 8, // Next 7 days
    "by_priority": [
      {"priority": "High", "count": 5}
    ]
  }
}
```

### 2. Document Statistics
**GET** `/stats/documents`
- **Auth Required**: Bearer Token
```json
Response:
{
  "total_size_bytes": 12345678,
  "average_confidence": 85.5,
  "by_file_type": [
    {"type": "application/pdf", "count": 20}
  ]
}
```

### 3. Task Statistics
**GET** `/stats/tasks`
- **Auth Required**: Bearer Token
```json
Response:
{
  "total": 28,
  "completed": 15,
  "completion_rate": 53.57,
  "by_status": [
    {"status": "Todo", "count": 8},
    {"status": "InProgress", "count": 5},
    {"status": "Done", "count": 15}
  ],
  "average_completion_days": 3.5
}
```

---

## 🔒 Authentication

All routes except `/auth/register` and `/auth/login` require authentication.

### How to Authenticate:
1. Register or login to get an access token
2. Include token in request headers:
   ```
   Authorization: Bearer YOUR_ACCESS_TOKEN
   ```

### Example (curl):
```bash
curl -X GET http://localhost:8000/documents/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 📁 Document Categories

Predefined categories:
- **Finance**: Financial documents, invoices, receipts
- **HR**: Human resources, employee records
- **Procurement**: Purchase orders, vendor contracts
- **Maintenance**: Maintenance requests, work orders
- **unknown**: Unclassified documents

---

## ⚙️ Task Configuration

### Priorities:
- Low
- Medium
- High
- Urgent

### Statuses:
- Todo
- InProgress
- Done

---

## 🌐 Supported Languages

- **English** (`en`)
- **Sinhala** (`si`)

OCR supports both languages for document text extraction.

---

## 📝 Response Status Codes

- **200**: OK
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **413**: Payload Too Large
- **422**: Validation Error
- **500**: Internal Server Error

---

## 🔍 Interactive API Documentation

Visit these URLs when the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
