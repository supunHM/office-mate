"""
Database Migration Script for Search Optimization
Adds indexes to existing database for better search performance
Run this after updating flask_models.py to apply new indexes
"""
from flask import Flask
from flask_models import db, Document, Tag, document_tags
import os

def create_indexes():
    """Create indexes for search optimization"""
    print("Creating database indexes for search optimization...")
    
    # Get database connection
    with db.engine.connect() as conn:
        # Check if indexes already exist
        result = conn.execute(db.text("SELECT name FROM sqlite_master WHERE type='index';"))
        existing_indexes = [row[0] for row in result]
        
        print(f"\nExisting indexes: {len(existing_indexes)}")
        for idx in existing_indexes:
            if idx and not idx.startswith('sqlite_'):  # Skip SQLite internal indexes
                print(f"  - {idx}")
        
        # Create composite index for user + created_at (if not exists)
        if 'idx_user_created' not in existing_indexes:
            print("\nCreating idx_user_created (user_id, created_at)...")
            conn.execute(db.text(
                "CREATE INDEX IF NOT EXISTS idx_user_created ON documents (user_id, created_at);"
            ))
            conn.commit()
            print("  ✓ Created")
        else:
            print("\nidx_user_created already exists")
        
        # Create composite index for user + category (if not exists)
        if 'idx_user_category' not in existing_indexes:
            print("\nCreating idx_user_category (user_id, category)...")
            conn.execute(db.text(
                "CREATE INDEX IF NOT EXISTS idx_user_category ON documents (user_id, category);"
            ))
            conn.commit()
            print("  ✓ Created")
        else:
            print("\nidx_user_category already exists")
        
        # Create index on user_id (if not exists)
        if 'ix_documents_user_id' not in existing_indexes:
            print("\nCreating ix_documents_user_id (user_id)...")
            conn.execute(db.text(
                "CREATE INDEX IF NOT EXISTS ix_documents_user_id ON documents (user_id);"
            ))
            conn.commit()
            print("  ✓ Created")
        else:
            print("\nix_documents_user_id already exists")
        
        # Verify all indexes were created
        result = conn.execute(db.text("SELECT name FROM sqlite_master WHERE type='index';"))
        final_indexes = [row[0] for row in result]
        
        print(f"\nFinal index count: {len(final_indexes)}")
        print("\nAll document-related indexes:")
        for idx in sorted(final_indexes):
            if idx and not idx.startswith('sqlite_'):
                print(f"  - {idx}")
    
    print("\n✓ Index creation complete!")
    print("\nTo verify indexes are being used, run:")
    print("  EXPLAIN QUERY PLAN SELECT * FROM documents WHERE user_id=1 ORDER BY created_at DESC;")


def analyze_database():
    """Analyze database for optimization"""
    print("\n" + "="*80)
    print("Database Analysis")
    print("="*80)
    
    with db.engine.connect() as conn:
        # Count documents
        result = conn.execute(db.text("SELECT COUNT(*) FROM documents;"))
        doc_count = result.scalar()
        print(f"\nTotal documents: {doc_count}")
        
        # Count by category
        result = conn.execute(db.text(
            "SELECT category, COUNT(*) as count FROM documents GROUP BY category;"
        ))
        print("\nDocuments by category:")
        for row in result:
            print(f"  {row[0]}: {row[1]}")
        
        # Count tags
        result = conn.execute(db.text("SELECT COUNT(*) FROM tags;"))
        tag_count = result.scalar()
        print(f"\nTotal tags: {tag_count}")
        
        # Most common tags
        result = conn.execute(db.text("""
            SELECT t.name, COUNT(*) as count 
            FROM tags t 
            JOIN document_tags dt ON t.id = dt.tag_id 
            GROUP BY t.id 
            ORDER BY count DESC 
            LIMIT 10;
        """))
        print("\nTop 10 most used tags:")
        for row in result:
            print(f"  {row[0]}: {row[1]} documents")
        
        # Date range
        result = conn.execute(db.text(
            "SELECT MIN(created_at), MAX(created_at) FROM documents;"
        ))
        date_range = result.fetchone()
        if date_range[0]:
            print(f"\nDate range: {date_range[0]} to {date_range[1]}")
    
    print("\n" + "="*80)


def main():
    """Main migration function"""
    print("="*80)
    print("Database Migration for Search Optimization")
    print("="*80)
    
    # Setup Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///office_mate.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        # Check if database exists
        if not os.path.exists('office_mate.db'):
            print("\nWarning: Database file 'office_mate.db' not found.")
            print("Creating database with indexes...")
            db.create_all()
            print("✓ Database created with all indexes")
        else:
            print("\nDatabase found. Updating indexes...")
            create_indexes()
            analyze_database()
    
    print("\nMigration complete!")
    print("\nNext steps:")
    print("1. Test the search API: python test_search_api.py")
    print("2. Monitor query performance in production")
    print("3. Run ANALYZE periodically for SQLite optimization")


if __name__ == '__main__':
    main()
