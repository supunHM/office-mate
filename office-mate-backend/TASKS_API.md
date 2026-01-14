# Tasks API Documentation

## Overview
The Tasks API provides endpoints for managing tasks with support for linking to documents, filtering, and status tracking.

**Base URL**: `http://localhost:5001`

**Authentication**: All endpoints require Bearer token authentication (JWT from login).

---

## Endpoints

### 1. Create Task
**POST** `/api/tasks`

Create a new task with optional document linking.

**Headers**:
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Review contract",
  "description": "Review and sign the new vendor contract",
  "priority": "High",
  "due_date": "2026-01-20",
  "status": "Todo",
  "document_id": 1
}
```

**Fields**:
- `title` (required): Task title (string)
- `description` (optional): Task description (string)
- `priority` (optional): One of: `Low`, `Medium`, `High`, `Urgent` (default: `Low`)
- `status` (optional): One of: `Todo`, `InProgress`, `Done` (default: `Todo`)
- `due_date` (optional): Due date in `YYYY-MM-DD` format
- `document_id` (optional): Link to a document (integer)

**Response** (201 Created):
```json
{
  "id": 1,
  "title": "Review contract",
  "description": "Review and sign the new vendor contract",
  "priority": "High",
  "due_date": "2026-01-20",
  "status": "Todo",
  "document_id": 1,
  "created_at": "2026-01-14T08:00:00",
  "message": "Task created successfully"
}
```

**Error Responses**:
- `400 Bad Request`: Missing required fields or invalid data
- `401 Unauthorized`: Missing or invalid authentication token
- `404 Not Found`: Document not found or access denied

---

### 2. Get Upcoming Tasks
**GET** `/api/tasks/upcoming`

Get tasks due within the next 2 days (excludes completed tasks).

**Headers**:
```
Authorization: Bearer <your_jwt_token>
```

**Query Parameters**:
- `days` (optional): Number of days to look ahead (default: 2, max: 30)

**Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Review contract",
      "description": "Review and approve vendor contract",
      "priority": "High",
      "due_date": "2026-01-15",
      "status": "Todo",
      "document_id": 5,
      "created_at": "2026-01-14T10:30:00",
      "days_until_due": 1,
      "is_overdue": false,
      "document": {
        "id": 5,
        "original_name": "vendor_contract.pdf",
        "category": "Finance"
      }
    }
  ],
  "count": 1,
  "period_days": 2
}
```

**Usage Examples**:
```bash
# Get tasks due in next 2 days (default)
curl -H "Authorization: Bearer <token>" http://localhost:5001/api/tasks/upcoming

# Get tasks due in next 7 days
curl -H "Authorization: Bearer <token>" http://localhost:5001/api/tasks/upcoming?days=7
```

---

### 3. List Tasks
**GET** `/api/tasks`

Get all tasks for the authenticated user with optional filters.

**Headers**:
```
Authorization: Bearer <your_jwt_token>
```

**Query Parameters**:
- `status` (optional): Filter by status (`Todo`, `InProgress`, `Done`)
- `due_from` (optional): Tasks due from this date (`YYYY-MM-DD`)
- `due_to` (optional): Tasks due until this date (`YYYY-MM-DD`)
- `document_id` (optional): Filter by linked document ID
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 50, max: 100)

**Examples**:
```
GET /api/tasks
GET /api/tasks?status=Todo
GET /api/tasks?due_from=2026-01-14&due_to=2026-01-31
GET /api/tasks?document_id=1
GET /api/tasks?status=InProgress&page=1&per_page=20
```

**Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Review contract",
      "description": "Review and sign the new vendor contract",
      "priority": "High",
      "due_date": "2026-01-20",
      "status": "Todo",
      "document_id": 1,
      "created_at": "2026-01-14T08:00:00",
      "document": {
        "id": 1,
        "original_name": "contract.pdf",
        "category": "Finance"
      }
    },
    {
      "id": 2,
      "title": "Update documentation",
      "description": "",
      "priority": "Low",
      "due_date": null,
      "status": "Todo",
      "document_id": null,
      "created_at": "2026-01-14T09:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 2,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

**Error Responses**:
- `400 Bad Request`: Invalid query parameters
- `401 Unauthorized`: Missing or invalid authentication token

---

### 3. Get Single Task
**GET** `/api/tasks/<task_id>`

Get details of a specific task.

**Headers**:
```
Authorization: Bearer <your_jwt_token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Review contract",
  "description": "Review and sign the new vendor contract",
  "priority": "High",
  "due_date": "2026-01-20",
  "status": "Todo",
  "document_id": 1,
  "created_at": "2026-01-14T08:00:00",
  "document": {
    "id": 1,
    "original_name": "contract.pdf",
    "category": "Finance",
    "created_at": "2026-01-13T10:30:00"
  }
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid authentication token
- `404 Not Found`: Task not found

---

### 4. Update Task
**PATCH** `/api/tasks/<task_id>`

Update an existing task. All fields are optional.

**Headers**:
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

**Request Body** (all fields optional):
```json
{
  "status": "InProgress"
}
```

Or update multiple fields:
```json
{
  "title": "Review and finalize contract",
  "priority": "Urgent",
  "status": "InProgress",
  "due_date": "2026-01-18"
}
```

To unlink a document:
```json
{
  "document_id": null
}
```

**Fields**:
- `title`: New title (string)
- `description`: New description (string)
- `priority`: New priority (`Low`, `Medium`, `High`, `Urgent`)
- `status`: New status (`Todo`, `InProgress`, `Done`)
- `due_date`: New due date (`YYYY-MM-DD`) or `null` to remove
- `document_id`: Link to new document (integer) or `null` to unlink

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Review and finalize contract",
  "description": "Review and sign the new vendor contract",
  "priority": "Urgent",
  "due_date": "2026-01-18",
  "status": "InProgress",
  "document_id": 1,
  "created_at": "2026-01-14T08:00:00",
  "message": "Task updated successfully"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Missing or invalid authentication token
- `404 Not Found`: Task or document not found

---

### 5. Delete Task
**DELETE** `/api/tasks/<task_id>`

Delete a task permanently.

**Headers**:
```
Authorization: Bearer <your_jwt_token>
```

**Response** (200 OK):
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid authentication token
- `404 Not Found`: Task not found

---

## Common Workflows

### Create a task linked to a document
1. Upload document using `POST /api/documents` (get document ID)
2. Create task: `POST /api/tasks` with `document_id`

### Update task status
```bash
curl -X PATCH http://localhost:5001/api/tasks/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "Done"}'
```

### Get all high-priority tasks due this week
```bash
curl "http://localhost:5001/api/tasks?priority=High&due_from=2026-01-14&due_to=2026-01-20" \
  -H "Authorization: Bearer <token>"
```

### Get all tasks linked to a specific document
```bash
curl "http://localhost:5001/api/tasks?document_id=1" \
  -H "Authorization: Bearer <token>"
```

---

## Data Models

### Task Object
```typescript
{
  id: number;
  title: string;
  description: string;
  priority: "Low" | "Medium" | "High" | "Urgent";
  due_date: string | null;  // YYYY-MM-DD format
  status: "Todo" | "InProgress" | "Done";
  document_id: number | null;
  created_at: string;  // ISO 8601 format
  document?: {  // Included when task is linked to a document
    id: number;
    original_name: string;
    category: string;
    created_at?: string;
  }
}
```

---

## Postman Collection

### 1. Create Task
```
POST http://localhost:5001/api/tasks
Headers:
  Authorization: Bearer <token>
  Content-Type: application/json
Body (raw JSON):
{
  "title": "Review contract",
  "priority": "High",
  "due_date": "2026-01-20",
  "document_id": 1
}
```

### 2. List All Tasks
```
GET http://localhost:5001/api/tasks
Headers:
  Authorization: Bearer <token>
```

### 3. Update Task Status
```
PATCH http://localhost:5001/api/tasks/1
Headers:
  Authorization: Bearer <token>
  Content-Type: application/json
Body (raw JSON):
{
  "status": "Done"
}
```

### 4. Delete Task
```
DELETE http://localhost:5001/api/tasks/1
Headers:
  Authorization: Bearer <token>
```

---

## Performance Notes

The tasks table has the following indexes for optimal query performance:
- Composite index on `(user_id, status)` for filtering by status
- Composite index on `(user_id, due_date)` for date range queries
- Individual indexes on `document_id`, `created_at`, `status`, `due_date`

Tasks are ordered by:
1. Due date (ascending, nulls last)
2. Created date (descending)

This ensures overdue and upcoming tasks appear first.
