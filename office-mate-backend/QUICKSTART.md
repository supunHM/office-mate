# Quick Start Guide - Document Search API

## 🚀 Get Started in 5 Minutes

### 1. Verify Implementation
```bash
cd office-mate-backend

# Check files exist
ls -la flask_documents_api.py  # ✓ Search endpoint
ls -la flask_models.py          # ✓ Models with indexes
ls -la test_search_api.py       # ✓ Test suite
```

### 2. Start the Backend
```bash
# Ensure dependencies are installed
pip install -r flask_requirements.txt

# Start Flask server
python flask_app.py
```

Server runs at: `http://localhost:5000`

### 3. Test the Search API
```bash
# In a new terminal
python test_search_api.py
```

### 4. Try Manual Queries

**Get all documents:**
```bash
curl "http://localhost:5000/api/documents?user_id=1"
```

**Search for keyword:**
```bash
curl "http://localhost:5000/api/documents?user_id=1&q=invoice"
```

**Filter by category:**
```bash
curl "http://localhost:5000/api/documents?user_id=1&category=Finance"
```

**Date range:**
```bash
curl "http://localhost:5000/api/documents?user_id=1&start_date=2024-01-01&end_date=2024-12-31"
```

**Combined filters:**
```bash
curl "http://localhost:5000/api/documents?user_id=1&q=budget&category=Finance&start_date=2024-01-01&page=1&per_page=20"
```

## 📋 API Quick Reference

### Endpoint
```
GET http://localhost:5000/api/documents
```

### Parameters
| Param | Example | Description |
|-------|---------|-------------|
| `q` | `invoice` | Keyword search |
| `category` | `Finance` | Filter by category |
| `start_date` | `2024-01-01` | From date |
| `end_date` | `2024-12-31` | To date |
| `page` | `1` | Page number |
| `per_page` | `20` | Items per page |
| `user_id` | `1` | User ID |

### Response
```json
{
  "documents": [
    {
      "id": 123,
      "original_name": "invoice.pdf",
      "category": "Finance",
      "tags": ["invoice", "payment"],
      "created_at": "2024-01-15T10:30:00",
      "text_preview": "Invoice for..."
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

## 🔧 Database Setup

### If Database Exists
```bash
# Update indexes
python migrate_search_indexes.py
```

### If New Database
```bash
# Create with indexes
python -c "from flask_app import app, db; app.app_context().push(); db.create_all()"
```

## 💻 Frontend Integration

### 1. Install Dependencies
```bash
cd ../office-mate
npm install axios date-fns
```

### 2. Add API Service
Create `src/services/api.ts` (see FRONTEND_INTEGRATION.md)

### 3. Add Search Hook
Create `src/hooks/useDocumentSearch.ts` (see FRONTEND_INTEGRATION.md)

### 4. Add Search Component
Create `src/components/DocumentSearch.tsx` (see FRONTEND_INTEGRATION.md)

### 5. Update Documents Page
```typescript
// src/pages/Documents.tsx
import { DocumentSearch } from '../components/DocumentSearch';

export function Documents() {
  return (
    <div>
      <h1>Documents</h1>
      <DocumentSearch />
    </div>
  );
}
```

## 📚 Documentation

| File | Purpose |
|------|---------|
| [SEARCH_API_GUIDE.md](SEARCH_API_GUIDE.md) | Complete API documentation |
| [SEARCH_API_QUICK_REF.md](SEARCH_API_QUICK_REF.md) | Quick reference |
| [SEARCH_IMPLEMENTATION.md](SEARCH_IMPLEMENTATION.md) | Implementation summary |
| [SEARCH_ARCHITECTURE.md](SEARCH_ARCHITECTURE.md) | Architecture diagrams |
| [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md) | Frontend integration guide |

## ✅ Feature Checklist

- [x] Keyword search in text
- [x] Keyword search in tags
- [x] Category filtering (Finance, HR, Procurement, Maintenance)
- [x] Date range filtering (start_date, end_date)
- [x] Pagination (page, per_page)
- [x] Relevance ordering (tag matches first)
- [x] Recency ordering (newest first)
- [x] Database indexes for performance
- [x] Error handling
- [x] Text preview in response
- [x] Test suite
- [x] Complete documentation

## 🎯 Common Use Cases

### 1. Find All Finance Documents
```bash
curl "http://localhost:5000/api/documents?user_id=1&category=Finance"
```

### 2. Search for Specific Invoice
```bash
curl "http://localhost:5000/api/documents?user_id=1&q=INV-2024-001"
```

### 3. Documents from Last Month
```bash
curl "http://localhost:5000/api/documents?user_id=1&start_date=2024-01-01&end_date=2024-01-31"
```

### 4. Paginate Through All Documents
```bash
# Page 1
curl "http://localhost:5000/api/documents?user_id=1&page=1&per_page=10"

# Page 2
curl "http://localhost:5000/api/documents?user_id=1&page=2&per_page=10"
```

### 5. Search Tags
```bash
curl "http://localhost:5000/api/documents?user_id=1&q=urgent"
```

## 🔍 Debugging

### Check Server Status
```bash
curl http://localhost:5000/health
```

### Verify Database
```bash
python migrate_search_indexes.py
```

### Run Tests
```bash
python test_search_api.py
```

### View Logs
Check Flask console output for errors

## 🚨 Troubleshooting

### "Connection refused"
→ Start Flask server: `python flask_app.py`

### "No documents found"
→ Upload test documents via POST /api/documents

### "Invalid date format"
→ Use YYYY-MM-DD format (e.g., 2024-01-15)

### Slow queries
→ Run `python migrate_search_indexes.py` to create indexes

## 📊 Performance

| Query Type | Expected Time |
|------------|--------------|
| Basic listing | <50ms |
| Category filter | <50ms |
| Date range | <100ms |
| Keyword search | <200ms |
| Combined filters | <150ms |

## 🎓 Next Steps

1. ✅ Test the API manually
2. ✅ Run automated tests
3. ✅ Integrate with frontend
4. ✅ Upload test documents
5. ✅ Test real searches

## 📖 Learn More

- **API Guide:** [SEARCH_API_GUIDE.md](SEARCH_API_GUIDE.md)
- **Frontend:** [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md)
- **Architecture:** [SEARCH_ARCHITECTURE.md](SEARCH_ARCHITECTURE.md)

## 💡 Tips

1. **Debounce searches** in frontend for better UX
2. **Cache results** to reduce API calls
3. **Use specific filters** for faster queries
4. **Monitor performance** with query times
5. **Index regularly** with SQLite ANALYZE

## 🎉 Success!

Your document search API is ready to use!

```bash
# Start backend
python flask_app.py

# Test it
curl "http://localhost:5000/api/documents?user_id=1&q=invoice"

# Enjoy! 🚀
```
