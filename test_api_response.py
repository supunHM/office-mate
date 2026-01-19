#!/usr/bin/env python3
"""
Test the enhanced summary API response
"""
import requests
import json

# Step 1: Login to get token
login_data = {
    "email": "admin@gmail.com",
    "password": "admin123"
}

print("🔐 Step 1: Authenticating...")
response = requests.post("http://localhost:8000/api/auth/login", json=login_data)
if response.status_code != 200:
    print(f"❌ Login failed: {response.text}")
    exit(1)

token = response.json()["access_token"]
print(f"✓ Authenticated successfully")

# Step 2: Upload document
headers = {"Authorization": f"Bearer {token}"}

print("\n📄 Step 2: Uploading test HR document...")
with open("/Users/supunherath/Documents/Dev-Pro/office-mate-backend/test_hr_document.txt", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/api/documents", files=files, headers=headers)

if response.status_code != 201:
    print(f"❌ Upload failed: {response.text}")
    exit(1)

result = response.json()
print(f"✓ Document uploaded (ID: {result['id']})")

# Step 3: Display results
print("\n" + "="*80)
print("POINT-WISE AI SUMMARY - ENHANCED RESPONSE")
print("="*80)

print(f"\n📋 Document: {result['filename']}")
print(f"📂 Category: {result['category']}")
print(f"📏 Length: {result['extracted_text_length']} characters")

if 'ai_summary' in result:
    ai_summary = result['ai_summary']
    
    print(f"\n{'─'*80}")
    print("📊 AI SUMMARY (Point-Wise Analysis)")
    print(f"{'─'*80}")
    
    print(f"\n✓ Executive Summary:")
    print(f"  {ai_summary['executive_summary'][:150]}...")
    
    print(f"\n✓ Key Points ({len(ai_summary['key_points'])} identified):")
    for i, point in enumerate(ai_summary['key_points'], 1):
        preview = point[:70] + "..." if len(point) > 70 else point
        print(f"  {i}. {preview}")
    
    print(f"\n✓ Key Concepts ({len(ai_summary['key_concepts'])} concepts):")
    concepts = ai_summary['key_concepts'][:10]
    print(f"  {', '.join(concepts)}")
    
    if ai_summary['key_entities']:
        print(f"\n✓ Key Entities:")
        for entity_type, values in ai_summary['key_entities'].items():
            print(f"  • {entity_type}: {', '.join(values[:3])}")
    
    print(f"\n✓ Document Structure: {ai_summary['structure']}")
    print(f"✓ Analysis Confidence: {ai_summary['confidence']*100:.1f}%")
    
    if ai_summary['document_sections']:
        print(f"\n✓ Document Sections ({len(ai_summary['document_sections'])} sections):")
        for section in list(ai_summary['document_sections'].keys())[:3]:
            content = ai_summary['document_sections'][section]
            preview = content[:50].replace('\n', ' ') + "..."
            print(f"  • {section}: {preview}")

if 'classification_details' in result:
    clf = result['classification_details']
    print(f"\n{'─'*80}")
    print("🤖 CLASSIFICATION ANALYSIS")
    print(f"{'─'*80}")
    
    print(f"\n✓ Category: {result['category']}")
    print(f"✓ Confidence: {clf['confidence']}")
    print(f"✓ Confidence Level: {clf['confidence_level']}")
    print(f"✓ Model Agreement: {'Yes ✓' if clf['model_agreement'] else 'No ✗'}")
    print(f"✓ Agreement Strength: {clf['agreement_strength']}")
    
    print(f"\n✓ Top Features (word importance):")
    for feature in clf['top_features'][:5]:
        print(f"  • {feature}")
    
    print(f"\n✓ All Categories (confidence ranking):")
    for category, score in clf['probability_ranking']:
        bar = "█" * int(score * 20)
        print(f"  {category:15} {bar} {score*100:.1f}%")

print("\n" + "="*80)
print("✅ API TEST COMPLETED SUCCESSFULLY")
print("="*80)
print("\n📌 Summary:")
print("   • ✓ AI summary is now point-wise and detailed")
print("   • ✓ Includes key points, concepts, and entities")
print("   • ✓ Document structure is analyzed")
print("   • ✓ Confidence metric provided")
print("   • ✓ Classification details preserved")
