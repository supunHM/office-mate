"""
Migration script to add indexes to tasks table
Run this after updating the Task model
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask_app import app, db
from flask_models import Task

def migrate_task_indexes():
    """Add indexes to tasks table for better query performance"""
    with app.app_context():
        print("Adding indexes to tasks table...")
        
        try:
            # Get database connection
            with db.engine.connect() as conn:
                # Check if indexes already exist
                result = conn.execute(db.text(
                    "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='tasks'"
                ))
                existing_indexes = {row[0] for row in result}
                
                print(f"Existing indexes: {existing_indexes}")
                
                # Create indexes if they don't exist
                indexes_to_create = [
                    ("idx_task_user_status", "CREATE INDEX IF NOT EXISTS idx_task_user_status ON tasks(user_id, status)"),
                    ("idx_task_user_due", "CREATE INDEX IF NOT EXISTS idx_task_user_due ON tasks(user_id, due_date)"),
                    ("ix_tasks_status", "CREATE INDEX IF NOT EXISTS ix_tasks_status ON tasks(status)"),
                    ("ix_tasks_due_date", "CREATE INDEX IF NOT EXISTS ix_tasks_due_date ON tasks(due_date)"),
                    ("ix_tasks_created_at", "CREATE INDEX IF NOT EXISTS ix_tasks_created_at ON tasks(created_at)"),
                    ("ix_tasks_document_id", "CREATE INDEX IF NOT EXISTS ix_tasks_document_id ON tasks(document_id)"),
                    ("ix_tasks_user_id", "CREATE INDEX IF NOT EXISTS ix_tasks_user_id ON tasks(user_id)"),
                ]
                
                for index_name, sql in indexes_to_create:
                    if index_name not in existing_indexes:
                        print(f"Creating index: {index_name}")
                        conn.execute(db.text(sql))
                        conn.commit()
                    else:
                        print(f"Index already exists: {index_name}")
                
                print("\n✓ Task indexes migration completed successfully")
                
        except Exception as e:
            print(f"\n✗ Error during migration: {str(e)}")
            return False
    
    return True


if __name__ == '__main__':
    success = migrate_task_indexes()
    sys.exit(0 if success else 1)
