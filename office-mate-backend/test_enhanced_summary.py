#!/usr/bin/env python3
"""
Test the enhanced summary generator
"""
import sys
sys.path.insert(0, '/Users/supunherath/Documents/Dev-Pro/office-mate-backend')

from enhanced_summary import SummaryGenerator

test_text = """
Finance Module Specification

Executive Summary
The Finance Module is a specialized component designed to manage financial documents, transactions, invoices, and receipts for office administration.

Key Features:
1. Automated Classification of financial documents
2. Secure storage with encryption
3. Audit compliance and reporting
4. Intelligent task management for financial workflows

Technical Details:
The module uses advanced machine learning algorithms for automatic document categorization. It integrates seamlessly with the main database system for real-time processing and provides comprehensive analytics.

Implementation Timeline:
Phase 1: Core module development (Q1 2026)
Phase 2: Integration testing (Q2 2026)
Phase 3: Deployment (Q3 2026)

Conclusion:
This Finance Module provides comprehensive financial document management capabilities for modern office administration.
"""

print("\n" + "="*80)
print("ENHANCED SUMMARY GENERATOR - TEST RESULTS")
print("="*80)

try:
    gen = SummaryGenerator()
    result = gen.generate_point_wise_summary(test_text, 'Finance')
    
    print(f"\n✓ Executive Summary:")
    print(f"   {result['executive_summary']}")
    
    print(f"\n✓ Key Points ({len(result['key_points'])} found):")
    for i, point in enumerate(result['key_points'], 1):
        preview = point[:80] + "..." if len(point) > 80 else point
        print(f"   {i}. {preview}")
    
    print(f"\n✓ Key Concepts ({len(result['key_concepts'])} identified):")
    for concept in result['key_concepts'][:8]:
        print(f"   • {concept}")
    
    print(f"\n✓ Document Sections ({len(result['sections'])} found):")
    for section, content in list(result['sections'].items())[:5]:
        preview = content[:60].replace('\n', ' ') + "..."
        print(f"   • {section}: {preview}")
    
    print(f"\n✓ Key Entities Found:")
    if result['key_entities']:
        for entity_type, values in result['key_entities'].items():
            print(f"   • {entity_type}: {', '.join(values[:3])}")
    else:
        print("   No named entities detected")
    
    print(f"\n✓ Analysis Confidence: {result['confidence']*100:.1f}%")
    print(f"✓ Document Structure: {result['structure']}")
    
    print("\n" + "="*80)
    print("TEST COMPLETED SUCCESSFULLY ✓")
    print("="*80)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
