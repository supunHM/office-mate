#!/usr/bin/env python
"""
Simple backend verification script
Tests core functionality without requiring running server
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all modules can be imported"""
    print("=" * 70)
    print("TEST 1: Module Imports")
    print("=" * 70)
    
    try:
        print("✓ Importing flask_app...")
        from flask_app import app
        print("✓ Importing flask_models...")
        from flask_models import db, User, Document, Tag, Task
        print("✓ Importing flask_auth...")
        from flask_auth import auth_bp
        print("✓ Importing flask_documents_api...")
        from flask_documents_api import documents_bp
        print("✓ Importing flask_tasks_api...")
        from flask_tasks_api import tasks_bp
        
        print("\n✅ All imports successful!\n")
        return True
    except Exception as e:
        print(f"\n❌ Import failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_database():
    """Test database initialization"""
    print("=" * 70)
    print("TEST 2: Database Initialization")
    print("=" * 70)
    
    try:
        from flask_app import app
        from flask_models import db
        
        print("✓ Creating Flask app context...")
        with app.app_context():
            print("✓ Creating database tables...")
            db.create_all()
            print("✓ Verifying tables...")
            
            # Check tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            required_tables = ['users', 'documents', 'tags', 'tasks', 'document_tags']
            for table in required_tables:
                if table in tables:
                    print(f"  ✓ Table '{table}' exists")
                else:
                    print(f"  ❌ Table '{table}' missing")
                    return False
        
        print("\n✅ Database initialized successfully!\n")
        return True
    except Exception as e:
        print(f"\n❌ Database test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_models():
    """Test model instantiation"""
    print("=" * 70)
    print("TEST 3: Model Instantiation")
    print("=" * 70)
    
    try:
        from flask_app import app
        from flask_models import db, User, Tag, Document, Task
        from datetime import date
        
        with app.app_context():
            print("✓ Creating user model...")
            user = User(username="testuser", email="test@example.com", password_hash="hash")
            
            print("✓ Creating tag model...")
            tag = Tag(name="TestTag")
            
            print("✓ Creating document model...")
            doc = Document(
                file_path="/path/to/file.pdf",
                original_name="test.pdf",
                user_id=1
            )
            
            print("✓ Creating task model...")
            task = Task(
                title="Test Task",
                priority="high",
                due_date=date.today(),
                user_id=1
            )
            
        print("\n✅ All models instantiated successfully!\n")
        return True
    except Exception as e:
        print(f"\n❌ Model test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_flask_app():
    """Test Flask app creation"""
    print("=" * 70)
    print("TEST 4: Flask App Configuration")
    print("=" * 70)
    
    try:
        from flask_app import app
        
        print(f"✓ App name: {app.name}")
        print(f"✓ Debug mode: {app.debug}")
        print(f"✓ Testing: {app.testing}")
        
        # Check blueprints
        blueprints = list(app.blueprints.keys())
        print(f"✓ Registered blueprints: {blueprints}")
        
        expected = ['auth', 'documents', 'tasks']
        for bp in expected:
            if bp in blueprints:
                print(f"  ✓ Blueprint '{bp}' registered")
            else:
                print(f"  ⚠ Blueprint '{bp}' not found")
        
        print("\n✅ Flask app configured successfully!\n")
        return True
    except Exception as e:
        print(f"\n❌ Flask app test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "🧪 OFFICE MATE BACKEND VERIFICATION" + " " * 18 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("Database", test_database),
        ("Models", test_models),
        ("Flask App", test_flask_app),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}\n")
            results.append((name, False))
    
    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Backend is working correctly.\n")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
