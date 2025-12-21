from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    category = Column(String, default="unknown")
    tags = Column(String, default="")
    content = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="document")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    priority = Column(String, default="Low")
    due_date = Column(Date, nullable=True)
    status = Column(String, default="Todo")
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="tasks")
