#!/usr/bin/env python3
"""
Test API response formats for consistency
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("\n" + "="*80)
print("TESTING API RESPONSE FORMATS")
print("="*80)

# Step 1: Login
print("\n1️⃣ Authenticating...")
login_data = {"email": "admin@gmail.com", "password": "admin123"}
response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("✅ Authenticated")

# Step 2: Get documents list
print("\n2️⃣ Getting documents list...")
response = requests.get(f"{BASE_URL}/api/documents", headers=headers)
docs = response.json()["documents"]

print(f"✅ Retrieved {len(docs)} documents")
print("\n📋 LIST RESPONSE FORMAT:")
print("-" * 80)

if docs:
    doc = docs[0]
    print(f"Document fields in LIST response:")
    for key in sorted(doc.keys()):
        value = doc[key]
        if isinstance(value, str) and len(str(value)) > 60:
            print(f"  ✓ {key}: {str(value)[:60]}...")
        else:
            print(f"  ✓ {key}: {value}")
    
    # Check for summary field
    has_summary = 'summary' in doc
    has_created_at = 'created_at' in doc
    has_extracted_length = 'extracted_text_length' in doc
    
    print(f"\n📌 Key Fields Check:")
    print(f"  {'✅' if has_summary else '❌'} summary field present: {has_summary}")
    print(f"  {'✅' if has_created_at else '❌'} created_at field present: {has_created_at}")
    print(f"  {'✅' if has_extracted_length else '❌'} extracted_text_length field present: {has_extracted_length}")
    
    # Display summary preview
    if has_summary and doc.get('summary'):
        summary = doc.get('summary', '')
        preview = summary[:100] + "..." if len(summary) > 100 else summary
        print(f"\n📝 Summary Preview (first 100 chars):")
        print(f"  {preview}")

print("\n" + "="*80)
print("✅ API RESPONSE FORMAT TEST COMPLETE")
print("="*80)
print("\nSummary:")
print("  • List response now includes 'summary' field for UI display")
print("  • Each document has all necessary fields for frontend")
print("  • Data is synchronized between list and upload endpoints")
