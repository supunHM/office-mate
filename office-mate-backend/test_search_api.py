"""
Test script for GET /api/documents search endpoint
Demonstrates various search and filter combinations
"""
import requests
import json

BASE_URL = 'http://localhost:5001'

def test_search_endpoint():
    """Test various search scenarios"""
    
    print("=" * 80)
    print("Testing GET /api/documents - Search & Filter Endpoint")
    print("=" * 80)
    
    # Test 1: Get all documents (with pagination)
    print("\n1. Get all documents (page 1, 10 items per page)")
    response = requests.get(f'{BASE_URL}/api/documents', params={
        'user_id': 1,
        'page': 1,
        'per_page': 10
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total documents: {data['pagination']['total']}")
        print(f"Pages: {data['pagination']['pages']}")
        print(f"Documents returned: {len(data['documents'])}")
        for doc in data['documents'][:3]:  # Show first 3
            print(f"  - {doc['original_name']} ({doc['category']}) - {doc['created_at']}")
    print()
    
    # Test 2: Keyword search
    print("\n2. Keyword search: 'invoice'")
    response = requests.get(f'{BASE_URL}/api/documents', params={
        'user_id': 1,
        'q': 'invoice'
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found: {data['pagination']['total']} documents")
        for doc in data['documents'][:5]:
            print(f"  - {doc['original_name']} ({doc['category']}) - Tags: {', '.join(doc['tags'])}")
    print()
    
    # Test 3: Filter by category
    print("\n3. Filter by category: 'Finance'")
    response = requests.get(f'{BASE_URL}/api/documents', params={
        'user_id': 1,
        'category': 'Finance'
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Finance documents: {data['pagination']['total']}")
        for doc in data['documents'][:5]:
            print(f"  - {doc['original_name']} - {doc['created_at']}")
    print()
    
    # Test 4: Date range filter
    print("\n4. Date range filter: 2024-01-01 to 2024-12-31")
    response = requests.get(f'{BASE_URL}/api/documents', params={
        'user_id': 1,
        'start_date': '2024-01-01',
        'end_date': '2024-12-31'
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Documents in 2024: {data['pagination']['total']}")
    print()
    
    # Test 5: Combined filters
    print("\n5. Combined: keyword='budget' + category='Finance' + date range")
    response = requests.get(f'{BASE_URL}/api/documents', params={
        'user_id': 1,
        'q': 'budget',
        'category': 'Finance',
        'start_date': '2024-01-01',
        'end_date': '2024-12-31'
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Matching documents: {data['pagination']['total']}")
        for doc in data['documents']:
            print(f"  - {doc['original_name']} ({doc['category']})")
            print(f"    Tags: {', '.join(doc['tags'])}")
            print(f"    Preview: {doc['text_preview'][:100]}...")
    print()
    
    # Test 6: Tag search
    print("\n6. Search by tag: 'payment'")
    response = requests.get(f'{BASE_URL}/api/documents', params={
        'user_id': 1,
        'q': 'payment'
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Documents with 'payment' in tags or text: {data['pagination']['total']}")
        for doc in data['documents'][:5]:
            print(f"  - {doc['original_name']}")
            print(f"    Tags: {', '.join(doc['tags'])}")
    print()
    
    # Test 7: Pagination
    print("\n7. Pagination test: page 2, 5 items per page")
    response = requests.get(f'{BASE_URL}/api/documents', params={
        'user_id': 1,
        'page': 2,
        'per_page': 5
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Page {data['pagination']['page']} of {data['pagination']['pages']}")
        print(f"Has next: {data['pagination']['has_next']}")
        print(f"Has prev: {data['pagination']['has_prev']}")
        print(f"Documents on this page: {len(data['documents'])}")
    print()
    
    # Test 8: Error handling - invalid date format
    print("\n8. Error handling: invalid date format")
    response = requests.get(f'{BASE_URL}/api/documents', params={
        'user_id': 1,
        'start_date': '2024-13-45'  # Invalid date
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        print(f"Error response: {response.json()}")
    print()
    
    # Test 9: All categories
    print("\n9. Test each category filter")
    categories = ['Finance', 'HR', 'Procurement', 'Maintenance']
    for cat in categories:
        response = requests.get(f'{BASE_URL}/api/documents', params={
            'user_id': 1,
            'category': cat
        })
        if response.status_code == 200:
            total = response.json()['pagination']['total']
            print(f"  {cat}: {total} documents")
    print()
    
    print("=" * 80)
    print("Search API testing complete!")
    print("=" * 80)


if __name__ == '__main__':
    try:
        test_search_endpoint()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Flask server at http://localhost:5001")
        print("Please ensure the server is running: python flask_app.py")
    except Exception as e:
        print(f"Test error: {e}")
