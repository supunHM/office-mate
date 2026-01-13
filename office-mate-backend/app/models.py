from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


# Association table for many-to-many relationship between Documents and Tags
document_tags = Table(
    "document_tags",
    Base.metadata,
    Column("document_id", Integer, ForeignKey("documents.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    preferred_language = Column(String, default="en")  # 'en' or 'si' for Sinhala
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    documents = relationship("Document", back_populates="owner", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")


class Tag(Base):
    """Tag model for document categorization"""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    name_si = Column(String, nullable=True)  # Sinhala translation
    color = Column(String, default="#3B82F6")  # Hex color for UI
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    documents = relationship("Document", secondary=document_tags, back_populates="tags")


class Document(Base):
    """Document model for uploaded files with OCR and classification"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Storage path
    file_size = Column(Integer, default=0)  # Size in bytes
    file_type = Column(String, nullable=True)  # MIME type
    category = Column(String, default="unknown")  # Finance, HR, Procurement, Maintenance
    content = Column(Text, default="")  # OCR extracted text
    content_si = Column(Text, default="")  # Sinhala text if detected
    ocr_confidence = Column(Integer, default=0)  # OCR confidence score
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="documents")
    tags = relationship("Tag", secondary=document_tags, back_populates="documents")
    tasks = relationship("Task", back_populates="document")


class Task(Base):
    """Task model for to-do list with document linking"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    title_si = Column(String, nullable=True)  # Sinhala title
    description = Column(Text, default="")
    description_si = Column(Text, default="")  # Sinhala description
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    priority = Column(String, default="Low")  # Low, Medium, High, Urgent
    due_date = Column(Date, nullable=True)
    status = Column(String, default="Todo")  # Todo, InProgress, Done
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="tasks")
    document = relationship("Document", back_populates="tasks")
