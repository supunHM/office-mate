"""
Flask Tasks API Blueprint
Provides endpoints for task management with filtering and authentication
Follows report requirements: task tracking linked to documents with priorities, due dates, and status
"""
from flask import Blueprint, request, jsonify
from flask_models import db, Task, Document
from flask_auth import get_current_user
from datetime import datetime, timedelta

tasks_bp = Blueprint('tasks', __name__)

# Map frontend status values to database values
# Frontend uses lowercase: pending, in_progress, completed
# For consistency, we'll accept both and store as lowercase
STATUS_MAP = {
    'pending': 'pending',
    'in_progress': 'in_progress',
    'completed': 'completed',
    # Legacy support
    'Todo': 'pending',
    'InProgress': 'in_progress',
    'Done': 'completed'
}

# Map frontend priority values to database values
# Frontend uses lowercase: low, medium, high
PRIORITY_MAP = {
    'low': 'low',
    'medium': 'medium',
    'high': 'high',
    'urgent': 'urgent',
    # Legacy support
    'Low': 'low',
    'Medium': 'medium',
    'High': 'high',
    'Urgent': 'urgent'
}


def get_upcoming_tasks_for_user(user_id, days=3):
    """
    Helper function to get upcoming tasks for a user within the next N days
    REPORT REQUIREMENT: Show upcoming deadlines (2-3 days ahead) for better task visibility
    
    Args:
        user_id: ID of the user
        days: Number of days to look ahead (default: 3 for report requirement)
    
    Returns:
        List of tasks due within the next N days, excluding completed tasks
    """
    today = datetime.now().date()
    end_date = today + timedelta(days=days)
    
    # Query tasks due within date range, not completed, ordered by due date
    # REPORT REQUIREMENT: Filter out completed tasks to show only actionable items
    tasks = Task.query.filter(
        Task.user_id == user_id,
        Task.due_date >= today,
        Task.due_date <= end_date,
        Task.status != 'completed'
    ).order_by(Task.due_date.asc(), Task.priority.desc()).all()
    
    return tasks


@tasks_bp.route('/api/tasks', methods=['POST'])
def create_task():
    """
    Create a new task
    REPORT REQUIREMENT: Allow users to create tasks with title, description, priority, due_date, status
    and link them to documents (linked_document_id)
    
    Required fields:
    - title: Task title (string, required)
    
    Optional fields:
    - description: Task description (string)
    - priority: low, medium, high, urgent (default: medium)
    - due_date: Due date in YYYY-MM-DD format
    - status: pending, in_progress, completed (default: pending)
    - document_id: Link to a document (integer) - REPORT REQUIREMENT: link tasks to documents
    
    Returns:
    - 201: Task created successfully
    - 400: Validation error
    - 401: Authentication required
    - 404: Document not found
    """
    # Get authenticated user - REPORT REQUIREMENT: tasks are created_by a user
    user_id = get_current_user()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Get request data
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate required fields - REPORT REQUIREMENT: title is mandatory
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    # Get optional fields with defaults
    description = data.get('description', '').strip()
    priority = data.get('priority', 'medium').lower()
    status = data.get('status', 'pending').lower()
    document_id = data.get('document_id') or data.get('documentId')  # Support both naming conventions
    
    # Normalize and validate priority - REPORT REQUIREMENT: support priority levels
    if priority in PRIORITY_MAP:
        priority = PRIORITY_MAP[priority]
    else:
        return jsonify({'error': f'Priority must be one of: low, medium, high, urgent'}), 400
    
    # Normalize and validate status - REPORT REQUIREMENT: track status
    if status in STATUS_MAP:
        status = STATUS_MAP[status]
    else:
        return jsonify({'error': f'Status must be one of: pending, in_progress, completed'}), 400
    
    # Parse due_date if provided - REPORT REQUIREMENT: support due dates for deadline tracking
    due_date = None
    if data.get('due_date') or data.get('dueDate'):
        due_date_str = data.get('due_date') or data.get('dueDate')
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid due_date format. Use YYYY-MM-DD'}), 400
    
    # Verify document exists and belongs to user (if document_id provided)
    # REPORT REQUIREMENT: Tasks can be linked to specific documents
    if document_id:
        try:
            document_id = int(document_id)
            document = Document.query.filter_by(id=document_id, user_id=user_id).first()
            if not document:
                return jsonify({'error': 'Document not found or access denied'}), 404
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid document_id'}), 400
    
    # Create task
    try:
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            status=status,
            document_id=document_id,
            user_id=user_id  # REPORT REQUIREMENT: created_by field
        )
        
        db.session.add(task)
        db.session.commit()
        
        # Prepare response with document info if linked
        response_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            'status': task.status,
            'document_id': task.document_id,
            'created_at': task.created_at.isoformat(),
            'message': 'Task created successfully'
        }
        
        # Include linked document name if exists
        if task.document_id and task.document:
            response_data['document'] = {
                'id': task.document.id,
                'original_name': task.document.original_name
            }
        
        return jsonify(response_data), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating task: {str(e)}")
        return jsonify({'error': 'Failed to create task'}), 500


@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    Get all tasks for the authenticated user with optional filters
    REPORT REQUIREMENT: List and filter tasks by status, due_date range, and linked_document_id
    
    Query parameters:
    - status: Filter by status (pending, in_progress, completed)
    - due_from: Filter tasks due from this date (YYYY-MM-DD)
    - due_to: Filter tasks due until this date (YYYY-MM-DD)
    - document_id: Filter tasks linked to specific document - REPORT REQUIREMENT
    - page: Page number (default: 1)
    - per_page: Items per page (default: 50, max: 100)
    
    Returns:
    - 200: List of tasks with pagination
    - 401: Authentication required
    """
    # Get authenticated user
    user_id = get_current_user()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Start with base query - REPORT REQUIREMENT: Only show user's own tasks
    query = Task.query.filter_by(user_id=user_id)
    
    # Apply status filter - REPORT REQUIREMENT: Filter by task status
    status = request.args.get('status')
    if status:
        status = status.lower()
        if status in STATUS_MAP:
            normalized_status = STATUS_MAP[status]
            query = query.filter_by(status=normalized_status)
        else:
            return jsonify({'error': f'Invalid status. Must be one of: pending, in_progress, completed'}), 400
    
    # Filter by document_id - REPORT REQUIREMENT: View tasks linked to specific document
    document_id = request.args.get('document_id') or request.args.get('documentId')
    if document_id:
        try:
            document_id = int(document_id)
            query = query.filter_by(document_id=document_id)
        except ValueError:
            return jsonify({'error': 'Invalid document_id'}), 400
    
    # Filter by due date range - REPORT REQUIREMENT: Support deadline tracking
    due_from = request.args.get('due_from')
    if due_from:
        try:
            due_from_date = datetime.strptime(due_from, '%Y-%m-%d').date()
            query = query.filter(Task.due_date >= due_from_date)
        except ValueError:
            return jsonify({'error': 'Invalid due_from format. Use YYYY-MM-DD'}), 400
    
    due_to = request.args.get('due_to')
    if due_to:
        try:
            due_to_date = datetime.strptime(due_to, '%Y-%m-%d').date()
            query = query.filter(Task.due_date <= due_to_date)
        except ValueError:
            return jsonify({'error': 'Invalid due_to format. Use YYYY-MM-DD'}), 400
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 100)
    
    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 50
    
    # Order by due date (nulls last), then by created date
    # REPORT REQUIREMENT: Prioritize tasks with deadlines
    query = query.order_by(Task.due_date.asc().nullslast(), Task.created_at.desc())
    
    # Execute query with pagination
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Format results
    tasks = []
    for task in paginated.items:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            'status': task.status,
            'document_id': task.document_id,
            'created_at': task.created_at.isoformat()
        }
        
        # Include document info if linked - REPORT REQUIREMENT: Show which document task is linked to
        if task.document_id and task.document:
            task_data['document'] = {
                'id': task.document.id,
                'original_name': task.document.original_name,
                'category': task.document.category
            }
        
        tasks.append(task_data)
    
    response = {
        'tasks': tasks,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': paginated.total,
            'pages': paginated.pages,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev
        }
    }
    
    return jsonify(response), 200


@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    """
    Update an existing task
    REPORT REQUIREMENT: Allow updating task status and details
    
    Path parameters:
    - task_id: ID of the task to update
    
    Body (all optional):
    - title: New title
    - description: New description
    - priority: New priority (low, medium, high, urgent)
    - due_date or dueDate: New due date (YYYY-MM-DD)
    - status: New status (pending, in_progress, completed)
    - document_id or documentId: Link to new document or null to unlink
    
    Returns:
    - 200: Task updated successfully
    - 400: Validation error
    - 401: Authentication required
    - 404: Task not found
    """
    # Get authenticated user
    user_id = get_current_user()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Find task - REPORT REQUIREMENT: Only allow user to update their own tasks
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Get update data
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Update title
        if 'title' in data:
            title = data['title'].strip()
            if not title:
                return jsonify({'error': 'Title cannot be empty'}), 400
            task.title = title
        
        # Update description
        if 'description' in data:
            task.description = data['description'].strip()
        
        # Update priority - REPORT REQUIREMENT: Support priority changes
        if 'priority' in data:
            priority = data['priority'].lower()
            if priority in PRIORITY_MAP:
                task.priority = PRIORITY_MAP[priority]
            else:
                return jsonify({'error': f'Priority must be one of: low, medium, high, urgent'}), 400
        
        # Update status - REPORT REQUIREMENT: Track task status updates
        if 'status' in data:
            status = data['status'].lower()
            if status in STATUS_MAP:
                task.status = STATUS_MAP[status]
            else:
                return jsonify({'error': f'Status must be one of: pending, in_progress, completed'}), 400
        
        # Update due_date - REPORT REQUIREMENT: Support deadline changes
        due_date_field = 'due_date' if 'due_date' in data else 'dueDate' if 'dueDate' in data else None
        if due_date_field:
            if data[due_date_field] is None:
                task.due_date = None
            else:
                try:
                    task.due_date = datetime.strptime(data[due_date_field], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'error': 'Invalid due_date format. Use YYYY-MM-DD'}), 400
        
        # Update document_id - REPORT REQUIREMENT: Allow relinking tasks to documents
        document_field = 'document_id' if 'document_id' in data else 'documentId' if 'documentId' in data else None
        if document_field:
            if data[document_field] is None or data[document_field] == '':
                task.document_id = None
            else:
                try:
                    document_id = int(data[document_field])
                    # Verify document exists and belongs to user
                    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
                    if not document:
                        return jsonify({'error': 'Document not found or access denied'}), 404
                    task.document_id = document_id
                except (ValueError, TypeError):
                    return jsonify({'error': 'Invalid document_id'}), 400
        
        db.session.commit()
        
        # Prepare response with linked document info
        response_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            'status': task.status,
            'document_id': task.document_id,
            'created_at': task.created_at.isoformat(),
            'message': 'Task updated successfully'
        }
        
        # Include document info if linked
        if task.document_id and task.document:
            response_data['document'] = {
                'id': task.document.id,
                'original_name': task.document.original_name
            }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating task: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to update task'}), 500


@tasks_bp.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Get a single task by ID
    
    Path parameters:
    - task_id: ID of the task
    
    Returns:
    - 200: Task details
    - 401: Authentication required
    - 404: Task not found
    """
    # Get authenticated user
    user_id = get_current_user()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Find task
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Format response
    task_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'priority': task.priority,
        'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
        'status': task.status,
        'document_id': task.document_id,
        'created_at': task.created_at.isoformat()
    }
    
    # Include document info if linked
    if task.document_id and task.document:
        task_data['document'] = {
            'id': task.document.id,
            'original_name': task.document.original_name,
            'category': task.document.category,
            'created_at': task.document.created_at.isoformat()
        }
    
    return jsonify(task_data), 200


@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task
    
    Path parameters:
    - task_id: ID of the task to delete
    
    Returns:
    - 200: Task deleted successfully
    - 401: Authentication required
    - 404: Task not found
    """
    # Get authenticated user
    user_id = get_current_user()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Find task
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting task: {str(e)}")
        return jsonify({'error': 'Failed to delete task'}), 500


@tasks_bp.route('/api/tasks/upcoming', methods=['GET'])
def get_upcoming_tasks():
    """
    Get upcoming tasks for the authenticated user (next 2-3 days)
    REPORT REQUIREMENT: Provide reminders/notifications for upcoming deadlines
    This endpoint supports the dashboard "upcoming tasks" widget
    
    Query parameters:
    - days: Number of days to look ahead (default: 3, max: 30)
    
    Returns:
    - 200: List of upcoming tasks (excludes completed tasks)
    - 401: Authentication required
    
    Example response:
    {
        "tasks": [
            {
                "id": 1,
                "title": "Review contract",
                "description": "Review and approve vendor contract",
                "priority": "high",
                "due_date": "2026-01-15",
                "status": "pending",
                "document_id": 5,
                "created_at": "2026-01-14T10:30:00",
                "days_until_due": 1,
                "is_overdue": false,
                "document": {
                    "id": 5,
                    "original_name": "vendor_contract.pdf",
                    "category": "Finance"
                }
            }
        ],
        "count": 1,
        "period_days": 3
    }
    """
    # Get authenticated user
    user_id = get_current_user()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Get days parameter (default 3 for report requirement, max 30)
    # REPORT REQUIREMENT: Show tasks with due_date in the next 2-3 days
    days = request.args.get('days', 3, type=int)
    days = max(1, min(days, 30))  # Clamp between 1 and 30
    
    # Get upcoming tasks using helper function
    tasks = get_upcoming_tasks_for_user(user_id, days)
    
    # Format results
    today = datetime.now().date()
    result_tasks = []
    
    for task in tasks:
        # Calculate days until due - REPORT REQUIREMENT: Deadline visibility
        days_until_due = (task.due_date - today).days
        is_overdue = days_until_due < 0
        
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'due_date': task.due_date.strftime('%Y-%m-%d'),
            'status': task.status,
            'document_id': task.document_id,
            'created_at': task.created_at.isoformat(),
            'days_until_due': days_until_due,
            'is_overdue': is_overdue
        }
        
        # Include document info if linked - REPORT REQUIREMENT: Show task-document link
        if task.document_id and task.document:
            task_data['document'] = {
                'id': task.document.id,
                'original_name': task.document.original_name,
                'category': task.document.category
            }
        
        result_tasks.append(task_data)
    
    response = {
        'tasks': result_tasks,
        'count': len(result_tasks),
        'period_days': days
    }
    
    return jsonify(response), 200
