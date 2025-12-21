from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, timedelta

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.TaskRead)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = models.Task(**task_in.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=List[schemas.TaskRead])
def list_tasks(
    status: Optional[str] = Query(None),
    overdue: Optional[bool] = Query(None),
    upcoming_days: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(models.Task)
    today = date.today()
    if status:
        q = q.filter(models.Task.status == status)
    if overdue:
        q = q.filter(models.Task.status != "Done").filter(models.Task.due_date < today)
    if upcoming_days is not None:
        end = today + timedelta(days=upcoming_days)
        q = q.filter(models.Task.due_date >= today).filter(models.Task.due_date <= end)
    return q.all()


@router.patch("/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for k, v in task_in.dict(exclude_unset=True).items():
        setattr(task, k, v)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"ok": True}
