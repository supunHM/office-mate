# Document Search API - Complete Guide

## Overview
The GET `/api/documents` endpoint provides powerful search, filtering, and pagination capabilities for documents in the Office Mate system.

## Endpoint
```
GET /api/documents
```

## Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `q` | string | No | - | Keyword search in document text and tags (case-insensitive) |
| `category` | string | No | - | Filter by category: `Finance`, `HR`, `Procurement`, or `Maintenance` |
| `start_date` | string | No | - | Filter documents created on or after this date (format: YYYY-MM-DD) |
| `end_date` | string | No | - | Filter documents created on or before this date (format: YYYY-MM-DD) |
| `page` | integer | No | 1 | Page number for pagination |
| `per_page` | integer | No | 20 | Items per page (max: 100) |
| `user_id` | integer | No | 1 | User ID (will be replaced with actual authentication) |

## Response Format

### Success Response (200 OK)
```json
{
  "documents": [
    {
      "id": 123,
      "original_name": "invoice_2024.pdf",
      "category": "Finance",
      "tags": ["invoice", "payment", "2024"],
      "created_at": "2024-01-15T10:30:00",
      "text_preview": "Invoice for services rendered in January 2024..."
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

### Error Response (400 Bad Request)
```json
{
  "error": "Invalid start_date format. Use YYYY-MM-DD"
}
```

### Error Response (500 Internal Server Error)
```json
{
  "error": "Error message details"
}
```

## Features

### 1. Keyword Search (`q` parameter)
- Searches in document **text content** (case-insensitive)
- Searches in document **tags** (case-insensitive)
- Uses SQL `ILIKE` for partial matching
- Results with matching tags are prioritized over text-only matches

**Example:**
```bash
curl "http://localhost:5000/api/documents?q=invoice"
```

### 2. Category Filtering
Filter documents by their ML-predicted category:
- `Finance` - Invoices, budgets, financial reports
- `HR` - Employee records, leave requests, payroll
- `Procurement` - Purchase orders, supplier contracts
- `Maintenance` - Equipment logs, repair requests

**Example:**
```bash
curl "http://localhost:5000/api/documents?category=Finance"
```

### 3. Date Range Filtering
Filter by document creation date:
- `start_date` - Include documents created on or after this date
- `end_date` - Include documents created on or before this date
- Format: `YYYY-MM-DD` (ISO 8601)

**Example:**
```bash
curl "http://localhost:5000/api/documents?start_date=2024-01-01&end_date=2024-12-31"
```

### 4. Pagination
Control response size and navigate through large result sets:
- `page` - Current page number (1-indexed)
- `per_page` - Items per page (max 100)
- Response includes pagination metadata

**Example:**
```bash
curl "http://localhost:5000/api/documents?page=2&per_page=10"
```

### 5. Combined Filters
All filters can be combined for precise searches:

**Example:**
```bash
curl "http://localhost:5000/api/documents?q=budget&category=Finance&start_date=2024-01-01&page=1&per_page=20"
```

## Ordering Logic

### With Search Query (`q` parameter):
1. **Relevance**: Documents with matching tags are ranked higher
2. **Recency**: Within each relevance tier, newest documents appear first

### Without Search Query:
- **Recency only**: Documents ordered by `created_at` (newest first)

## Database Indexes

The following indexes are automatically created for optimal performance:

1. **Single Column Indexes:**
   - `category` - Fast category filtering
   - `created_at` - Fast date sorting and filtering
   - `user_id` - Fast user-specific queries

2. **Composite Indexes:**
   - `idx_user_created` on (`user_id`, `created_at`) - Optimizes user + date queries
   - `idx_user_category` on (`user_id`, `category`) - Optimizes user + category queries

3. **Association Table Indexes:**
   - `document_id` in `document_tags` - Fast tag lookups
   - `tag_id` in `document_tags` - Fast reverse tag lookups

## Usage Examples

### 1. Get All Documents (First Page)
```bash
curl "http://localhost:5000/api/documents?user_id=1"
```

### 2. Search for "invoice" in Any Document
```bash
curl "http://localhost:5000/api/documents?user_id=1&q=invoice"
```

### 3. Get All Finance Documents
```bash
curl "http://localhost:5000/api/documents?user_id=1&category=Finance"
```

### 4. Get Documents from January 2024
```bash
curl "http://localhost:5000/api/documents?user_id=1&start_date=2024-01-01&end_date=2024-01-31"
```

### 5. Search "budget" in Finance Category, 2024 Only
```bash
curl "http://localhost:5000/api/documents?user_id=1&q=budget&category=Finance&start_date=2024-01-01&end_date=2024-12-31"
```

### 6. Paginate Through Results (5 per page)
```bash
# Page 1
curl "http://localhost:5000/api/documents?user_id=1&per_page=5&page=1"

# Page 2
curl "http://localhost:5000/api/documents?user_id=1&per_page=5&page=2"
```

### 7. Search in Tags
```bash
curl "http://localhost:5000/api/documents?user_id=1&q=payment"
```
This finds documents with "payment" in tags or text content.

## Python Usage Example

```python
import requests

BASE_URL = 'http://localhost:5000'

# Search with multiple filters
params = {
    'user_id': 1,
    'q': 'invoice',
    'category': 'Finance',
    'start_date': '2024-01-01',
    'end_date': '2024-12-31',
    'page': 1,
    'per_page': 20
}

response = requests.get(f'{BASE_URL}/api/documents', params=params)

if response.status_code == 200:
    data = response.json()
    
    # Access documents
    for doc in data['documents']:
        print(f"{doc['original_name']} - {doc['category']}")
        print(f"Tags: {', '.join(doc['tags'])}")
        print(f"Preview: {doc['text_preview']}\n")
    
    # Access pagination info
    pagination = data['pagination']
    print(f"Page {pagination['page']} of {pagination['pages']}")
    print(f"Total: {pagination['total']} documents")
```

## JavaScript/TypeScript Usage Example

```typescript
interface SearchParams {
  user_id?: number;
  q?: string;
  category?: string;
  start_date?: string;
  end_date?: string;
  page?: number;
  per_page?: number;
}

interface Document {
  id: number;
  original_name: string;
  category: string;
  tags: string[];
  created_at: string;
  text_preview: string;
}

interface SearchResponse {
  documents: Document[];
  pagination: {
    page: number;
    per_page: number;
    total: number;
    pages: number;
    has_next: boolean;
    has_prev: boolean;
  };
}

async function searchDocuments(params: SearchParams): Promise<SearchResponse> {
  const queryString = new URLSearchParams(
    Object.entries(params)
      .filter(([_, v]) => v !== undefined)
      .map(([k, v]) => [k, String(v)])
  ).toString();
  
  const response = await fetch(`http://localhost:5000/api/documents?${queryString}`);
  
  if (!response.ok) {
    throw new Error(`Search failed: ${response.statusText}`);
  }
  
  return response.json();
}

// Usage
searchDocuments({
  user_id: 1,
  q: 'invoice',
  category: 'Finance',
  page: 1,
  per_page: 20
}).then(data => {
  console.log(`Found ${data.pagination.total} documents`);
  data.documents.forEach(doc => {
    console.log(`${doc.original_name} - ${doc.category}`);
  });
});
```

## Performance Considerations

### Query Optimization
1. **Use specific filters**: Combining filters (category + date range) is faster than broad searches
2. **Limit page size**: Smaller `per_page` values return faster
3. **Avoid very broad searches**: Specific keywords return faster than single characters

### Index Usage
The endpoint automatically uses indexes for:
- `user_id` filtering (always applied)
- `category` filtering (when provided)
- `created_at` ordering and filtering (when provided)
- Tag searches via `document_tags` table

### Best Practices
1. **Always specify user_id**: Even though it defaults to 1, explicit is better
2. **Use pagination**: Don't request all results at once
3. **Cache results**: Consider client-side caching for repeated queries
4. **Progressive loading**: Load initial results quickly, then fetch more as needed

## Testing

Run the test suite:
```bash
python test_search_api.py
```

This tests:
- Basic pagination
- Keyword search
- Category filtering
- Date range filtering
- Combined filters
- Tag search
- Error handling
- Edge cases

## Future Enhancements

Potential improvements (not yet implemented):
1. **Full-Text Search**: Use SQLite FTS5 for better text search performance
2. **Fuzzy Matching**: Handle typos and similar words
3. **Search Highlighting**: Return highlighted search terms in results
4. **Faceted Search**: Return category counts, tag suggestions
5. **Search History**: Track user search patterns
6. **Advanced Relevance**: TF-IDF or BM25 scoring for better relevance ranking
7. **Multi-language Support**: Full Sinhala text search
8. **Aggregations**: Count by category, date histograms
9. **Sorting Options**: Allow custom sort fields (name, category, etc.)
10. **Saved Searches**: Let users save common search queries

## Troubleshooting

### No Results Found
- Check if documents exist for the user_id
- Verify search keyword spelling
- Try broader date ranges
- Remove filters one by one to isolate the issue

### Slow Queries
- Check if indexes are created: Run `PRAGMA index_list('documents');` in SQLite
- Reduce page size
- Be more specific with filters

### Invalid Date Format Error
- Use YYYY-MM-DD format exactly
- Example: `2024-01-15` not `15/01/2024`

### Pagination Shows No Results
- Verify the page number is within range (check `pagination.pages`)
- First page is `1`, not `0`

## Related Endpoints

- `POST /api/documents` - Upload new documents
- `GET /api/documents/<id>` - Get single document details
- `PUT /api/documents/<id>` - Update document (future)
- `DELETE /api/documents/<id>` - Delete document (future)
