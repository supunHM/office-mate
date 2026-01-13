"""
Statistics and dashboard routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta

from app import models
from app.database import get_db
from app.services.auth import get_current_active_user

router = APIRouter()


@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get dashboard statistics for current user"""
    
    # Document statistics
    total_documents = db.query(func.count(models.Document.id)).filter(
        models.Document.user_id == current_user.id
    ).scalar()
    
    # Documents by category
    docs_by_category = db.query(
        models.Document.category,
        func.count(models.Document.id).label('count')
    ).filter(
        models.Document.user_id == current_user.id
    ).group_by(models.Document.category).all()
    
    # Task statistics
    total_tasks = db.query(func.count(models.Task.id)).filter(
        models.Task.user_id == current_user.id
    ).scalar()
    
    completed_tasks = db.query(func.count(models.Task.id)).filter(
        models.Task.user_id == current_user.id,
        models.Task.status == "Done"
    ).scalar()
    
    pending_tasks = total_tasks - completed_tasks
    
    # Overdue tasks
    today = date.today()
    overdue_tasks = db.query(func.count(models.Task.id)).filter(
        models.Task.user_id == current_user.id,
        models.Task.status != "Done",
        models.Task.due_date < today
    ).scalar()
    
    # Upcoming tasks (next 7 days)
    next_week = today + timedelta(days=7)
    upcoming_tasks = db.query(func.count(models.Task.id)).filter(
        models.Task.user_id == current_user.id,
        models.Task.status != "Done",
        models.Task.due_date >= today,
        models.Task.due_date <= next_week
    ).scalar()
    
    # Tasks by priority
    tasks_by_priority = db.query(
        models.Task.priority,
        func.count(models.Task.id).label('count')
    ).filter(
        models.Task.user_id == current_user.id,
        models.Task.status != "Done"
    ).group_by(models.Task.priority).all()
    
    # Recent documents (last 7 days)
    week_ago = today - timedelta(days=7)
    recent_documents = db.query(func.count(models.Document.id)).filter(
        models.Document.user_id == current_user.id,
        models.Document.created_at >= week_ago
    ).scalar()
    
    return {
        "documents": {
            "total": total_documents,
            "recent": recent_documents,
            "by_category": [
                {"category": cat, "count": count}
                for cat, count in docs_by_category
            ]
        },
        "tasks": {
            "total": total_tasks,
            "completed": completed_tasks,
            "pending": pending_tasks,
            "overdue": overdue_tasks,
            "upcoming": upcoming_tasks,
            "by_priority": [
                {"priority": priority, "count": count}
                for priority, count in tasks_by_priority
            ]
        }
    }


@router.get("/stats/documents")
def get_document_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get detailed document statistics"""
    
    # Total size of all documents
    total_size = db.query(func.sum(models.Document.file_size)).filter(
        models.Document.user_id == current_user.id
    ).scalar() or 0
    
    # Average OCR confidence
    avg_confidence = db.query(func.avg(models.Document.ocr_confidence)).filter(
        models.Document.user_id == current_user.id
    ).scalar() or 0
    
    # Documents by file type
    docs_by_type = db.query(
        models.Document.file_type,
        func.count(models.Document.id).label('count')
    ).filter(
        models.Document.user_id == current_user.id
    ).group_by(models.Document.file_type).all()
    
    return {
        "total_size_bytes": int(total_size),
        "average_confidence": round(float(avg_confidence), 2),
        "by_file_type": [
            {"type": ftype or "unknown", "count": count}
            for ftype, count in docs_by_type
        ]
    }


@router.get("/stats/tasks")
def get_task_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get detailed task statistics"""
    
    # Completion rate
    total = db.query(func.count(models.Task.id)).filter(
        models.Task.user_id == current_user.id
    ).scalar()
    
    completed = db.query(func.count(models.Task.id)).filter(
        models.Task.user_id == current_user.id,
        models.Task.status == "Done"
    ).scalar()
    
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    # Tasks by status
    tasks_by_status = db.query(
        models.Task.status,
        func.count(models.Task.id).label('count')
    ).filter(
        models.Task.user_id == current_user.id
    ).group_by(models.Task.status).all()
    
    # Average completion time (for completed tasks)
    avg_completion_time = db.query(
        func.avg(
            func.julianday(models.Task.completed_at) - func.julianday(models.Task.created_at)
        )
    ).filter(
        models.Task.user_id == current_user.id,
        models.Task.status == "Done",
        models.Task.completed_at.isnot(None)
    ).scalar() or 0
    
    return {
        "total": total,
        "completed": completed,
        "completion_rate": round(completion_rate, 2),
        "by_status": [
            {"status": status, "count": count}
            for status, count in tasks_by_status
        ],
        "average_completion_days": round(float(avg_completion_time), 2)
    }
