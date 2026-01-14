# Search API Quick Reference

## Endpoint

```
GET /api/documents
```

## Quick Examples

### 1. Basic Search

```bash
# Get all documents
curl "http://localhost:5000/api/documents?user_id=1"

# Search keyword
curl "http://localhost:5000/api/documents?user_id=1&q=invoice"
```

### 2. Filter by Category

```bash
curl "http://localhost:5000/api/documents?user_id=1&category=Finance"
```

### 3. Filter by Date

```bash
# Single date boundary
curl "http://localhost:5000/api/documents?user_id=1&start_date=2024-01-01"

# Date range
curl "http://localhost:5000/api/documents?user_id=1&start_date=2024-01-01&end_date=2024-12-31"
```

### 4. Pagination

```bash
# Page 1, 10 items
curl "http://localhost:5000/api/documents?user_id=1&page=1&per_page=10"

# Page 2
curl "http://localhost:5000/api/documents?user_id=1&page=2&per_page=10"
```

### 5. Combined Filters

```bash
curl "http://localhost:5000/api/documents?user_id=1&q=budget&category=Finance&start_date=2024-01-01&end_date=2024-12-31&page=1&per_page=20"
```

## Parameters Cheat Sheet

| Param        | Type   | Example      | Description              |
| ------------ | ------ | ------------ | ------------------------ |
| `q`          | string | `invoice`    | Keyword search           |
| `category`   | string | `Finance`    | Filter by category       |
| `start_date` | date   | `2024-01-01` | From date (YYYY-MM-DD)   |
| `end_date`   | date   | `2024-12-31` | To date (YYYY-MM-DD)     |
| `page`       | int    | `1`          | Page number              |
| `per_page`   | int    | `20`         | Items per page (max 100) |
| `user_id`    | int    | `1`          | User ID                  |

## Response Structure

```json
{
  "documents": [
    {
      "id": 123,
      "original_name": "file.pdf",
      "category": "Finance",
      "tags": ["tag1", "tag2"],
      "created_at": "2024-01-15T10:30:00",
      "text_preview": "First 200 chars..."
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 45,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

## Categories

- `Finance` - Invoices, budgets, financial reports
- `HR` - Employee records, leave requests
- `Procurement` - Purchase orders, contracts
- `Maintenance` - Equipment logs, repairs

## Testing

```bash
python test_search_api.py
```

## Full Documentation

See [SEARCH_API_GUIDE.md](SEARCH_API_GUIDE.md) for complete details.
