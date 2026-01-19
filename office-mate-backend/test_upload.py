#!/usr/bin/env python
"""Test document upload to verify database schema is working"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

# 1. Login to get token
print("1. Logging in...")
login_response = requests.post(
    f"{BASE_URL}/api/login",
    json={"username": "admin", "password": "admin123"}
)

if login_response.status_code != 200:
    print(f"✗ Login failed: {login_response.text}")
    exit(1)

token = login_response.json().get("access_token")
print(f"✓ Token received: {token[:20]}...")

headers = {"Authorization": f"Bearer {token}"}

# 2. Check existing documents
print("\n2. Checking existing documents...")
docs_response = requests.get(f"{BASE_URL}/api/documents", headers=headers)
print(f"   Status: {docs_response.status_code}")
if docs_response.status_code == 200:
    docs = docs_response.json()
    print(f"   Found {len(docs)} documents")
    for doc in docs[:2]:
        print(f"   - {doc.get('filename', 'N/A')}: {doc.get('category', 'N/A')}")

# 3. Test database insertion directly
print("\n3. Testing database insertion...")
try:
    from flask_models import db, Document
    from flask_app import app
    import os
    os.chdir('/Users/supunherath/Documents/Dev-Pro/office-mate-backend')
    
    with app.app_context():
        # Create a test document
        test_doc = Document(
            file_path='test_path.txt',
            original_name='test.txt',
            text='This is test content',
            category='Finance',
            user_id=1,
            summary='Test summary',
            ai_summary_json={'test': 'data', 'confidence': 0.95}
        )
        db.session.add(test_doc)
        db.session.commit()
        print(f"✓ Test document created with ID {test_doc.id}")
        
        # Verify it was saved
        retrieved = db.session.query(Document).filter_by(id=test_doc.id).first()
        if retrieved:
            print(f"✓ Document retrieved: {retrieved.original_name}")
            print(f"  - Summary: {retrieved.summary[:50]}...")
            print(f"  - AI Summary JSON keys: {list(retrieved.ai_summary_json.keys())}")
        
        # Clean up test document
        db.session.delete(test_doc)
        db.session.commit()
        print("✓ Test document deleted")
        
except Exception as e:
    print(f"✗ Database test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n✓ All tests completed!")
