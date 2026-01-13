from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date


# ============= User Schemas =============
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    preferred_language: Optional[str] = "en"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    preferred_language: Optional[str] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


# ============= Tag Schemas =============
class TagBase(BaseModel):
    name: str
    name_si: Optional[str] = None
    color: Optional[str] = "#3B82F6"


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = None
    name_si: Optional[str] = None
    color: Optional[str] = None


class TagRead(TagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============= Document Schemas =============
class DocumentBase(BaseModel):
    filename: str
    category: Optional[str] = "unknown"


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    filename: Optional[str] = None
    category: Optional[str] = None


class DocumentRead(DocumentBase):
    id: int
    file_path: str
    file_size: int
    file_type: Optional[str] = None
    content: str
    content_si: Optional[str] = ""
    ocr_confidence: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    tags: List[TagRead] = []

    class Config:
        from_attributes = True


class DocumentListRead(BaseModel):
    """Simplified schema for document listing (without full content)"""
    id: int
    filename: str
    category: str
    file_size: int
    file_type: Optional[str] = None
    user_id: int
    created_at: datetime
    tags: List[TagRead] = []

    class Config:
        from_attributes = True


# ============= Task Schemas =============
class TaskBase(BaseModel):
    title: str
    title_si: Optional[str] = None
    description: Optional[str] = ""
    description_si: Optional[str] = ""
    document_id: Optional[int] = None
    priority: Optional[str] = "Low"
    due_date: Optional[date] = None
    status: Optional[str] = "Todo"


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    title_si: Optional[str] = None
    description: Optional[str] = None
    description_si: Optional[str] = None
    document_id: Optional[int] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None


class TaskRead(TaskBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True
