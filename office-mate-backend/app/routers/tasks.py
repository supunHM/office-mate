"""
Task routes: CRUD operations for tasks with document linking
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, timedelta

from app import models, schemas
from app.database import get_db
from app.services.auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Create a new task"""
    # Verify document belongs to user if document_id is provided
    if task_in.document_id:
        doc = db.query(models.Document).filter(
            models.Document.id == task_in.document_id,
            models.Document.user_id == current_user.id
        ).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
    
    task = models.Task(**task_in.dict(), user_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=List[schemas.TaskRead])
def list_tasks(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    overdue: Optional[bool] = Query(None),
    upcoming_days: Optional[int] = Query(None),
    document_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """List tasks for current user with various filters"""
    q = db.query(models.Task).filter(models.Task.user_id == current_user.id)
    today = date.today()
    
    if status:
        q = q.filter(models.Task.status == status)
    
    if priority:
        q = q.filter(models.Task.priority == priority)
    
    if overdue:
        q = q.filter(models.Task.status != "Done").filter(models.Task.due_date < today)
    
    if upcoming_days is not None:
        end = today + timedelta(days=upcoming_days)
        q = q.filter(models.Task.due_date >= today).filter(models.Task.due_date <= end)
    
    if document_id:
        q = q.filter(models.Task.document_id == document_id)
    
    return q.order_by(models.Task.due_date.asc()).all()


@router.get("/{task_id}", response_model=schemas.TaskRead)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get a specific task"""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=schemas.TaskRead)
def update_task(
    task_id: int,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Update a task"""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Handle status change to Done
    update_data = task_in.dict(exclude_unset=True)
    if "status" in update_data:
        if update_data["status"] == "Done" and task.status != "Done":
            task.completed_at = datetime.utcnow()
        elif update_data["status"] != "Done" and task.status == "Done":
            task.completed_at = None
    
    # Verify document belongs to user if document_id is being updated
    if task_in.document_id:
        doc = db.query(models.Document).filter(
            models.Document.id == task_in.document_id,
            models.Document.user_id == current_user.id
        ).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
    
    for key, value in update_data.items():
        setattr(task, key, value)
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Delete a task"""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
