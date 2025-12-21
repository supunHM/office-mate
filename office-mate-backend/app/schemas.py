from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


class DocumentBase(BaseModel):
    filename: str
    content: Optional[str] = ""
    category: Optional[str] = "unknown"
    tags: Optional[str] = ""


class DocumentCreate(DocumentBase):
    pass


class DocumentRead(DocumentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = ""
    document_id: Optional[int] = None
    priority: Optional[str] = "Low"
    due_date: Optional[date] = None
    status: Optional[str] = "Todo"


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[str]
    due_date: Optional[date]
    status: Optional[str]


class TaskRead(TaskBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
