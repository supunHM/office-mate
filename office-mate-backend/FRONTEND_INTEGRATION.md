# Frontend Integration Guide for Search API

## Overview
This guide shows how to integrate the search API with the existing React/TypeScript frontend.

## TypeScript Types

Create `src/types/search.ts`:

```typescript
export interface Document {
  id: number;
  original_name: string;
  category: 'Finance' | 'HR' | 'Procurement' | 'Maintenance';
  tags: string[];
  created_at: string;
  text_preview: string;
}

export interface PaginationInfo {
  page: number;
  per_page: number;
  total: number;
  pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface SearchResponse {
  documents: Document[];
  pagination: PaginationInfo;
}

export interface SearchFilters {
  q?: string;
  category?: string;
  start_date?: string;
  end_date?: string;
  page?: number;
  per_page?: number;
  user_id?: number;
}
```

## API Service

Update `src/services/api.ts`:

```typescript
import axios from 'axios';
import { SearchFilters, SearchResponse } from '../types/search';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const documentApi = {
  /**
   * Search and filter documents
   * @param filters Search parameters
   * @returns Promise with documents and pagination
   */
  async searchDocuments(filters: SearchFilters): Promise<SearchResponse> {
    try {
      // Remove undefined values
      const params = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v !== undefined && v !== '')
      );

      const response = await axios.get<SearchResponse>(`${API_BASE}/api/documents`, {
        params
      });

      return response.data;
    } catch (error) {
      console.error('Search error:', error);
      throw error;
    }
  },

  /**
   * Upload a new document
   * @param file File to upload
   * @returns Promise with document details
   */
  async uploadDocument(file: File): Promise<Document> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_BASE}/api/documents`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    return response.data;
  }
};
```

## React Hook

Create `src/hooks/useDocumentSearch.ts`:

```typescript
import { useState, useEffect, useCallback } from 'react';
import { documentApi } from '../services/api';
import { SearchFilters, SearchResponse } from '../types/search';

export function useDocumentSearch(initialFilters: SearchFilters = {}) {
  const [data, setData] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<SearchFilters>(initialFilters);

  const search = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await documentApi.searchDocuments(filters);
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  // Auto-search when filters change
  useEffect(() => {
    search();
  }, [search]);

  const updateFilters = useCallback((newFilters: Partial<SearchFilters>) => {
    setFilters(prev => ({ ...prev, ...newFilters, page: 1 })); // Reset to page 1
  }, []);

  const goToPage = useCallback((page: number) => {
    setFilters(prev => ({ ...prev, page }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters(initialFilters);
  }, [initialFilters]);

  return {
    documents: data?.documents || [],
    pagination: data?.pagination,
    loading,
    error,
    filters,
    updateFilters,
    goToPage,
    resetFilters,
    refetch: search
  };
}
```

## Search Component

Create `src/components/DocumentSearch.tsx`:

```typescript
import React from 'react';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Calendar } from './ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from './ui/popover';
import { useDocumentSearch } from '../hooks/useDocumentSearch';
import { format } from 'date-fns';

export function DocumentSearch() {
  const {
    documents,
    pagination,
    loading,
    error,
    filters,
    updateFilters,
    goToPage,
    resetFilters
  } = useDocumentSearch({ user_id: 1, per_page: 20 });

  return (
    <div className="space-y-6">
      {/* Search Filters */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Keyword Search */}
        <div className="md:col-span-2">
          <Input
            placeholder="Search documents..."
            value={filters.q || ''}
            onChange={(e) => updateFilters({ q: e.target.value })}
          />
        </div>

        {/* Category Filter */}
        <Select
          value={filters.category || 'all'}
          onValueChange={(value) => 
            updateFilters({ category: value === 'all' ? undefined : value })
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="All Categories" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Categories</SelectItem>
            <SelectItem value="Finance">Finance</SelectItem>
            <SelectItem value="HR">HR</SelectItem>
            <SelectItem value="Procurement">Procurement</SelectItem>
            <SelectItem value="Maintenance">Maintenance</SelectItem>
          </SelectContent>
        </Select>

        {/* Date Range */}
        <Popover>
          <PopoverTrigger asChild>
            <Button variant="outline">
              {filters.start_date 
                ? `From ${format(new Date(filters.start_date), 'PP')}`
                : 'Select Date Range'}
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-auto p-0" align="start">
            <Calendar
              mode="range"
              selected={{
                from: filters.start_date ? new Date(filters.start_date) : undefined,
                to: filters.end_date ? new Date(filters.end_date) : undefined,
              }}
              onSelect={(range) => {
                updateFilters({
                  start_date: range?.from ? format(range.from, 'yyyy-MM-dd') : undefined,
                  end_date: range?.to ? format(range.to, 'yyyy-MM-dd') : undefined,
                });
              }}
            />
          </PopoverContent>
        </Popover>

        {/* Reset Button */}
        <Button variant="outline" onClick={resetFilters}>
          Reset Filters
        </Button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded">
          {error}
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto" />
        </div>
      )}

      {/* Results Count */}
      {pagination && (
        <div className="text-sm text-gray-600">
          Found {pagination.total} document{pagination.total !== 1 ? 's' : ''}
        </div>
      )}

      {/* Document List */}
      {!loading && documents.length > 0 && (
        <div className="space-y-4">
          {documents.map((doc) => (
            <div
              key={doc.id}
              className="border rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="font-semibold text-lg">{doc.original_name}</h3>
                  <p className="text-sm text-gray-600 mt-1">{doc.text_preview}</p>
                  
                  <div className="flex items-center gap-4 mt-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {doc.category}
                    </span>
                    
                    <div className="flex gap-2">
                      {doc.tags.map((tag) => (
                        <span
                          key={tag}
                          className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
                
                <div className="text-sm text-gray-500">
                  {format(new Date(doc.created_at), 'MMM d, yyyy')}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && documents.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          No documents found. Try adjusting your filters.
        </div>
      )}

      {/* Pagination */}
      {pagination && pagination.pages > 1 && (
        <div className="flex items-center justify-center gap-2">
          <Button
            variant="outline"
            disabled={!pagination.has_prev}
            onClick={() => goToPage(filters.page! - 1)}
          >
            Previous
          </Button>
          
          <span className="text-sm">
            Page {pagination.page} of {pagination.pages}
          </span>
          
          <Button
            variant="outline"
            disabled={!pagination.has_next}
            onClick={() => goToPage(filters.page! + 1)}
          >
            Next
          </Button>
        </div>
      )}
    </div>
  );
}
```

## Add to Documents Page

Update `src/pages/Documents.tsx`:

```typescript
import React from 'react';
import { DocumentSearch } from '../components/DocumentSearch';
import { Button } from '../components/ui/button';
import { Upload } from 'lucide-react';

export function Documents() {
  return (
    <div className="container mx-auto py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold">Documents</h1>
        
        <Button>
          <Upload className="mr-2 h-4 w-4" />
          Upload Document
        </Button>
      </div>

      <DocumentSearch />
    </div>
  );
}
```

## Environment Configuration

Update `.env`:

```env
VITE_API_URL=http://localhost:5000
```

For production:

```env
VITE_API_URL=https://api.yourapp.com
```

## Advanced Features

### 1. Debounced Search

```typescript
import { useDebounce } from '../hooks/useDebounce';

export function DocumentSearch() {
  const [searchQuery, setSearchQuery] = useState('');
  const debouncedQuery = useDebounce(searchQuery, 500); // 500ms delay

  const { documents, loading } = useDocumentSearch({
    q: debouncedQuery,
    user_id: 1
  });

  return (
    <Input
      placeholder="Search..."
      value={searchQuery}
      onChange={(e) => setSearchQuery(e.target.value)}
    />
  );
}
```

### 2. Search Suggestions

```typescript
export function SearchWithSuggestions() {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);

  useEffect(() => {
    if (query.length > 2) {
      // Fetch suggestions based on existing tags
      documentApi.searchDocuments({ q: query, per_page: 5 })
        .then(data => {
          const tags = data.documents.flatMap(d => d.tags);
          setSuggestions([...new Set(tags)].slice(0, 5));
        });
    }
  }, [query]);

  return (
    <div className="relative">
      <Input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      
      {suggestions.length > 0 && (
        <div className="absolute z-10 w-full bg-white shadow-lg rounded mt-1">
          {suggestions.map((tag) => (
            <div
              key={tag}
              className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
              onClick={() => setQuery(tag)}
            >
              {tag}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

### 3. URL State Management

```typescript
import { useSearchParams } from 'react-router-dom';

export function DocumentSearch() {
  const [searchParams, setSearchParams] = useSearchParams();

  const filters = {
    q: searchParams.get('q') || '',
    category: searchParams.get('category') || '',
    page: parseInt(searchParams.get('page') || '1')
  };

  const updateFilters = (newFilters: Partial<SearchFilters>) => {
    const params = new URLSearchParams(searchParams);
    
    Object.entries(newFilters).forEach(([key, value]) => {
      if (value) {
        params.set(key, String(value));
      } else {
        params.delete(key);
      }
    });

    setSearchParams(params);
  };

  // Use filters from URL
  const { documents } = useDocumentSearch(filters);

  // Now the search state is in the URL!
  // Users can bookmark searches, share links, etc.
}
```

### 4. Export Results

```typescript
export function ExportButton({ filters }: { filters: SearchFilters }) {
  const handleExport = async () => {
    // Get all results (no pagination)
    const allResults = await documentApi.searchDocuments({
      ...filters,
      per_page: 1000 // Get all
    });

    // Convert to CSV
    const csv = [
      ['Name', 'Category', 'Tags', 'Date'],
      ...allResults.documents.map(doc => [
        doc.original_name,
        doc.category,
        doc.tags.join(', '),
        doc.created_at
      ])
    ].map(row => row.join(',')).join('\n');

    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'documents.csv';
    a.click();
  };

  return (
    <Button onClick={handleExport}>
      Export Results
    </Button>
  );
}
```

## Testing

Create `src/components/DocumentSearch.test.tsx`:

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { DocumentSearch } from './DocumentSearch';
import { documentApi } from '../services/api';

jest.mock('../services/api');

describe('DocumentSearch', () => {
  it('renders search input', () => {
    render(<DocumentSearch />);
    expect(screen.getByPlaceholderText('Search documents...')).toBeInTheDocument();
  });

  it('fetches documents on mount', async () => {
    const mockData = {
      documents: [
        { id: 1, original_name: 'test.pdf', category: 'Finance', tags: [], created_at: '2024-01-01', text_preview: 'test' }
      ],
      pagination: { page: 1, per_page: 20, total: 1, pages: 1, has_next: false, has_prev: false }
    };

    (documentApi.searchDocuments as jest.Mock).mockResolvedValue(mockData);

    render(<DocumentSearch />);

    await waitFor(() => {
      expect(screen.getByText('test.pdf')).toBeInTheDocument();
    });
  });

  it('updates search query', async () => {
    render(<DocumentSearch />);
    
    const input = screen.getByPlaceholderText('Search documents...');
    fireEvent.change(input, { target: { value: 'invoice' } });

    await waitFor(() => {
      expect(documentApi.searchDocuments).toHaveBeenCalledWith(
        expect.objectContaining({ q: 'invoice' })
      );
    });
  });
});
```

## Complete Example

Here's a complete working example page:

```typescript
import React, { useState } from 'react';
import { DocumentSearch } from '../components/DocumentSearch';
import { Button } from '../components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../components/ui/dialog';
import { useDocumentUpload } from '../hooks/useDocumentUpload';

export function DocumentsPage() {
  const [uploadOpen, setUploadOpen] = useState(false);
  const { upload, uploading } = useDocumentUpload();

  const handleUpload = async (file: File) => {
    try {
      await upload(file);
      setUploadOpen(false);
      // Trigger search refetch
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Documents</h1>
        <Button onClick={() => setUploadOpen(true)}>
          Upload Document
        </Button>
      </div>

      <DocumentSearch />

      <Dialog open={uploadOpen} onOpenChange={setUploadOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Upload Document</DialogTitle>
          </DialogHeader>
          {/* Upload form here */}
        </DialogContent>
      </Dialog>
    </div>
  );
}
```

## CORS Configuration

Ensure Flask backend has CORS enabled in `flask_app.py`:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])  # Vite default port
```

## Next Steps

1. **Install dependencies:**
   ```bash
   npm install axios date-fns
   ```

2. **Create the types file**
3. **Update the API service**
4. **Create the custom hook**
5. **Build the search component**
6. **Test the integration**

## Troubleshooting

### Issue: CORS errors
**Solution:** Verify Flask CORS configuration includes your frontend URL

### Issue: Slow searches
**Solution:** Implement debounced search (see Advanced Features #1)

### Issue: Pagination not working
**Solution:** Check that `page` parameter is being sent correctly

### Issue: Date filters not working
**Solution:** Verify date format is YYYY-MM-DD

## Performance Tips

1. Use debounced search for keyword queries
2. Cache search results client-side
3. Implement infinite scroll instead of pagination
4. Lazy load document previews
5. Use React Query or SWR for automatic caching
