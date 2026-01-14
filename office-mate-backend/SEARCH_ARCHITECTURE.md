# Search API Architecture

## Request Flow Diagram

```
Client Request
     |
     v
┌─────────────────────────────────────────────┐
│  GET /api/documents?q=invoice&category=...  │
└─────────────────────────────────────────────┘
     |
     v
┌─────────────────────────────────────────────┐
│         Parameter Extraction                │
│  - q (keyword)                              │
│  - category (Finance/HR/Proc/Maint)        │
│  - start_date, end_date                     │
│  - page, per_page                           │
│  - user_id                                  │
└─────────────────────────────────────────────┘
     |
     v
┌─────────────────────────────────────────────┐
│         Query Building (SQLAlchemy)         │
│                                             │
│  1. Base: filter_by(user_id)               │
│  2. Keyword: text ILIKE OR tags ILIKE      │
│  3. Category: filter(category == val)      │
│  4. Dates: filter(created_at >= start)     │
│  5. Order: relevance + recency             │
└─────────────────────────────────────────────┘
     |
     v
┌─────────────────────────────────────────────┐
│         Database Execution                  │
│                                             │
│  Using indexes:                             │
│  - idx_user_created                         │
│  - idx_user_category                        │
│  - ix_documents_user_id                     │
│  - document_tags association                │
└─────────────────────────────────────────────┘
     |
     v
┌─────────────────────────────────────────────┐
│            Pagination                       │
│  - Calculate total results                  │
│  - Extract page slice                       │
│  - Generate metadata                        │
└─────────────────────────────────────────────┘
     |
     v
┌─────────────────────────────────────────────┐
│         Response Formatting                 │
│  - Convert to JSON                          │
│  - Add text preview (200 chars)            │
│  - Include pagination metadata              │
└─────────────────────────────────────────────┘
     |
     v
JSON Response to Client
```

## Database Query Flow

```
┌──────────────────────────────────────────────────────────┐
│                     documents Table                      │
│  Columns: id, file_path, original_name, text,          │
│           category, created_at, user_id                 │
│  Indexes: user_id, category, created_at,               │
│           (user_id, created_at), (user_id, category)   │
└──────────────────────────────────────────────────────────┘
                    |                    |
                    |                    |
         ┌──────────┘                    └──────────┐
         v                                          v
┌──────────────────────┐              ┌──────────────────────┐
│  document_tags       │              │     tags Table       │
│  (Association)       │              │  Columns: id, name   │
│  Columns:            │              │  Index: name         │
│  - document_id (idx) │              └──────────────────────┘
│  - tag_id (idx)      │
└──────────────────────┘

Query Execution:
1. Filter by user_id (uses ix_documents_user_id)
2. If keyword: JOIN tags via document_tags, search text + tag.name
3. If category: filter (uses idx_user_category)
4. If dates: filter (uses idx_user_created)
5. Order by: relevance (tag match) + created_at DESC
6. Paginate: LIMIT/OFFSET
```

## Search Algorithm

```
Input: q="invoice", category="Finance", start_date="2024-01-01"

Step 1: Start with user filter
  SELECT * FROM documents WHERE user_id = 1

Step 2: Add keyword search (OR condition)
  ... AND (text ILIKE '%invoice%' OR
           id IN (SELECT document_id FROM document_tags
                  JOIN tags ON tags.id = tag_id
                  WHERE name ILIKE '%invoice%'))

Step 3: Add category filter
  ... AND category = 'Finance'

Step 4: Add date filter
  ... AND created_at >= '2024-01-01'

Step 5: Relevance ordering
  ORDER BY
    CASE WHEN tag_name ILIKE '%invoice%' THEN 0 ELSE 1 END,
    created_at DESC

Step 6: Paginate
  LIMIT 20 OFFSET 0

Result: Documents matching all criteria, tag matches first, newest first
```

## Indexing Strategy

```
Single Column Indexes (for simple filters):
┌─────────────┬──────────────────────────────────┐
│ Index Name  │ Purpose                          │
├─────────────┼──────────────────────────────────┤
│ user_id     │ Filter by user                   │
│ category    │ Filter by category               │
│ created_at  │ Order by date, date range filter │
└─────────────┴──────────────────────────────────┘

Composite Indexes (for combined filters):
┌────────────────────┬──────────────────────────────┐
│ Index Name         │ Purpose                      │
├────────────────────┼──────────────────────────────┤
│ idx_user_created   │ User + date range queries    │
│ idx_user_category  │ User + category queries      │
└────────────────────┴──────────────────────────────┘

Association Table Indexes:
┌─────────────┬──────────────────────────────────┐
│ Index Name  │ Purpose                          │
├─────────────┼──────────────────────────────────┤
│ document_id │ Find tags for document           │
│ tag_id      │ Find documents for tag           │
└─────────────┴──────────────────────────────────┘
```

## Relevance Scoring

```
Priority 1: TAG MATCHES (Score: 0)
┌──────────────────────────────────────────┐
│  Documents with matching tags            │
│  - invoice.pdf (tags: invoice, payment)  │
│  - bill_2024.pdf (tags: invoice, bill)   │
└──────────────────────────────────────────┘
            |
            v
   Order by created_at DESC
            |
            v
   [invoice.pdf (2024-03-15)]
   [bill_2024.pdf (2024-02-10)]

Priority 2: TEXT MATCHES (Score: 1)
┌──────────────────────────────────────────┐
│  Documents with matching text only       │
│  - report.pdf (text contains "invoice")  │
│  - memo.doc (text contains "invoice")    │
└──────────────────────────────────────────┘
            |
            v
   Order by created_at DESC
            |
            v
   [report.pdf (2024-02-05)]
   [memo.doc (2024-01-20)]

Final Result Order:
1. invoice.pdf (tag match, newest)
2. bill_2024.pdf (tag match)
3. report.pdf (text match)
4. memo.doc (text match, oldest)
```

## Performance Characteristics

```
Query Type              | Complexity | Index Used         | Est. Time
------------------------|------------|--------------------|-----------
List all (user)         | O(log n)   | user_id           | <50ms
Filter by category      | O(log n)   | user_category     | <50ms
Filter by date range    | O(log n)   | user_created      | <50ms
Keyword in text         | O(n)       | None (full scan)  | <200ms
Keyword in tags         | O(log n)   | document_tags     | <100ms
Combined filters        | O(log n)   | Multiple          | <150ms
Pagination              | O(1)       | N/A               | ~0ms

Notes:
- Text search is O(n) because SQLite ILIKE requires full scan
- For large datasets (>100K docs), consider FTS5
- Tag search is fast due to association table indexes
- Combined filters use most selective index first
```

## Example Query Plans

```sql
-- Query 1: User + Category
EXPLAIN QUERY PLAN
SELECT * FROM documents
WHERE user_id=1 AND category='Finance';

-- Plan:
SEARCH documents USING INDEX idx_user_category (user_id=? AND category=?)

-- Query 2: User + Date Range
EXPLAIN QUERY PLAN
SELECT * FROM documents
WHERE user_id=1
  AND created_at >= '2024-01-01'
ORDER BY created_at DESC;

-- Plan:
SEARCH documents USING INDEX idx_user_created (user_id=? AND created_at>?)

-- Query 3: Tag Search
EXPLAIN QUERY PLAN
SELECT * FROM documents d
JOIN document_tags dt ON d.id = dt.document_id
JOIN tags t ON t.id = dt.tag_id
WHERE t.name ILIKE '%invoice%';

-- Plan:
SCAN tags t USING INDEX ix_tags_name
SEARCH document_tags dt USING INDEX (tag_id=?)
SEARCH documents d USING PRIMARY KEY
```

## Pagination Logic

```
Total Documents: 45
Per Page: 20
Current Page: 2

Calculation:
- Total Pages = ceil(45 / 20) = 3
- Offset = (2 - 1) * 20 = 20
- Limit = 20
- Has Next = (2 < 3) = true
- Has Prev = (2 > 1) = true

SQL:
SELECT * FROM documents
WHERE ...
ORDER BY ...
LIMIT 20 OFFSET 20;

Returns: Documents 21-40 (page 2 of 3)
```

## Error Handling Flow

```
Request → Validate Parameters → Valid?
                                   |
                        ┌──────────┴──────────┐
                        NO                   YES
                        |                     |
                        v                     v
                Return 400             Execute Query
                (Bad Request)                |
                                            v
                                     Success?
                                       |
                            ┌──────────┴──────────┐
                            NO                   YES
                            |                     |
                            v                     v
                     Return 500           Format Response
                  (Internal Error)              |
                                               v
                                        Return 200 OK
```

## Client Integration Pattern

```javascript
// React Component
function DocumentSearch() {
  const [filters, setFilters] = useState({
    q: "",
    category: "",
    page: 1,
  });

  const { data, loading } = useDocumentSearch(filters);

  return (
    <div>
      <SearchBar onChange={(q) => setFilters({ ...filters, q })} />
      <CategoryFilter
        onChange={(cat) => setFilters({ ...filters, category: cat })}
      />
      <DocumentList documents={data?.documents} />
      <Pagination
        page={data?.pagination.page}
        total={data?.pagination.pages}
        onChange={(page) => setFilters({ ...filters, page })}
      />
    </div>
  );
}

// Custom Hook
function useDocumentSearch(filters) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(filters);
    setLoading(true);

    fetch(`/api/documents?${params}`)
      .then((res) => res.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, [filters]);

  return { data, loading };
}
```

## Caching Strategy (Future)

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ GET /api/documents?q=invoice
       v
┌─────────────┐
│   Cache?    │ ← Check if result cached
└──────┬──────┘
       │ MISS
       v
┌─────────────┐
│   Database  │ ← Execute query
└──────┬──────┘
       │
       v
┌─────────────┐
│ Store Cache │ ← Cache for 5 mins
└──────┬──────┘
       │
       v
   Return Result

Cache Key Format:
  search:{user_id}:{q}:{category}:{dates}:{page}

Cache Invalidation:
  - On document upload
  - On document update
  - After 5 minutes (TTL)
```
