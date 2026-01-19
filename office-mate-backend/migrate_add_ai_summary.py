"""
Database migration script to add summary and ai_summary_json columns to documents table
"""
import sqlite3
import os

def migrate_db():
    """Add summary and ai_summary_json columns to documents table"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'office_mate.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(documents)")
        columns = {row[1] for row in cursor.fetchall()}
        
        if 'summary' in columns and 'ai_summary_json' in columns:
            print("✓ Columns 'summary' and 'ai_summary_json' already exist")
            conn.close()
            return True
        
        # Add missing columns
        if 'summary' not in columns:
            print("Adding 'summary' column...")
            cursor.execute("ALTER TABLE documents ADD COLUMN summary TEXT DEFAULT ''")
            print("✓ 'summary' column added")
        
        if 'ai_summary_json' not in columns:
            print("Adding 'ai_summary_json' column...")
            cursor.execute("ALTER TABLE documents ADD COLUMN ai_summary_json JSON DEFAULT '{}'")
            print("✓ 'ai_summary_json' column added")
        
        conn.commit()
        print("\n✓ Database migration completed successfully!")
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    migrate_db()
