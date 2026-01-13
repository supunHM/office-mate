"""
Test script for Flask Document Upload API
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_health_check():
    """Test health check endpoint"""
    print("\n1. Testing health check...")
    response = requests.get(BASE_URL)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200

def test_upload_document(file_path):
    """Test document upload"""
    print(f"\n2. Testing document upload: {file_path}...")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'user_id': 1}
            
            response = requests.post(
                f'{BASE_URL}/api/documents',
                files=files,
                data=data
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 201:
                result = response.json()
                print(f"   Document ID: {result['id']}")
                print(f"   Category: {result['category']}")
                print(f"   Tags: {', '.join(result['tags'])}")
                print(f"   Summary: {result['summary'][:100]}...")
                return result['id']
            else:
                print(f"   Error: {response.json()}")
                return None
    except FileNotFoundError:
        print(f"   ⚠️  File not found: {file_path}")
        print(f"   Skipping test...")
        return None

def test_get_documents():
    """Test get all documents"""
    print("\n3. Testing get all documents...")
    response = requests.get(f'{BASE_URL}/api/documents', params={'user_id': 1})
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        documents = response.json()
        print(f"   Total documents: {len(documents)}")
        for doc in documents[:3]:  # Show first 3
            print(f"   - {doc['original_name']} ({doc['category']})")

def test_get_single_document(doc_id):
    """Test get single document"""
    if not doc_id:
        print("\n4. Skipping single document test (no document ID)")
        return
    
    print(f"\n4. Testing get document ID {doc_id}...")
    response = requests.get(f'{BASE_URL}/api/documents/{doc_id}')
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        doc = response.json()
        print(f"   Filename: {doc['original_name']}")
        print(f"   Category: {doc['category']}")
        print(f"   Tags: {', '.join(doc['tags'])}")
        print(f"   Text length: {len(doc['text'])} characters")

def test_invalid_upload():
    """Test invalid file upload"""
    print("\n5. Testing invalid upload (no file)...")
    response = requests.post(f'{BASE_URL}/api/documents', data={'user_id': 1})
    
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 400

if __name__ == '__main__':
    print("=" * 60)
    print("Flask Document Upload API - Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: Health check
        test_health_check()
        
        # Test 2: Upload document
        # You can replace these with actual test files
        test_files = [
            'test_invoice.pdf',
            'test_image.jpg',
            'test_document.docx'
        ]
        
        doc_id = None
        for file_path in test_files:
            result_id = test_upload_document(file_path)
            if result_id and not doc_id:
                doc_id = result_id
        
        # Test 3: Get all documents
        test_get_documents()
        
        # Test 4: Get single document
        test_get_single_document(doc_id)
        
        # Test 5: Invalid upload
        test_invalid_upload()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to Flask server")
        print("   Make sure the server is running: python flask_app.py")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
