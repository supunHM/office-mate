"""
Migration script to update task status and priority values
from PascalCase to lowercase format

Run this once after deploying the new task API code.

Usage:
    python migrate_task_values.py
"""
from flask import Flask
from flask_models import db, Task

# Create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///office_mate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)


def migrate_task_values():
    """Migrate status and priority values to lowercase"""
    with app.app_context():
        print("Starting task values migration...")
        
        # Count tasks that need migration
        status_to_migrate = Task.query.filter(
            Task.status.in_(['Todo', 'InProgress', 'Done'])
        ).count()
        
        priority_to_migrate = Task.query.filter(
            Task.priority.in_(['Low', 'Medium', 'High', 'Urgent'])
        ).count()
        
        print(f"Found {status_to_migrate} tasks with old status values")
        print(f"Found {priority_to_migrate} tasks with old priority values")
        
        if status_to_migrate == 0 and priority_to_migrate == 0:
            print("No migration needed. All tasks are already using lowercase values.")
            return
        
        # Migrate status values
        status_migrations = {
            'Todo': 'pending',
            'InProgress': 'in_progress',
            'Done': 'completed'
        }
        
        for old_value, new_value in status_migrations.items():
            count = Task.query.filter_by(status=old_value).update({'status': new_value})
            if count > 0:
                print(f"Migrated {count} tasks: status '{old_value}' → '{new_value}'")
        
        # Migrate priority values
        priority_migrations = {
            'Low': 'low',
            'Medium': 'medium',
            'High': 'high',
            'Urgent': 'urgent'
        }
        
        for old_value, new_value in priority_migrations.items():
            count = Task.query.filter_by(priority=old_value).update({'priority': new_value})
            if count > 0:
                print(f"Migrated {count} tasks: priority '{old_value}' → '{new_value}'")
        
        # Commit changes
        db.session.commit()
        print("\nMigration completed successfully!")
        
        # Verify migration
        remaining_old_status = Task.query.filter(
            Task.status.in_(['Todo', 'InProgress', 'Done'])
        ).count()
        
        remaining_old_priority = Task.query.filter(
            Task.priority.in_(['Low', 'Medium', 'High', 'Urgent'])
        ).count()
        
        if remaining_old_status > 0 or remaining_old_priority > 0:
            print(f"WARNING: {remaining_old_status} tasks still have old status values")
            print(f"WARNING: {remaining_old_priority} tasks still have old priority values")
        else:
            print("Verification passed: All tasks migrated successfully!")


if __name__ == '__main__':
    try:
        migrate_task_values()
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        import traceback
        traceback.print_exc()
