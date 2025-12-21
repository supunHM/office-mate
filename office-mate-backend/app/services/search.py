from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional
from datetime import date

from app import models


def search_documents(db: Session, query: Optional[str] = None, category: Optional[str] = None,
                     date_from: Optional[date] = None, date_to: Optional[date] = None):
    q = db.query(models.Document)
    if query:
        like = f"%{query}%"
        q = q.filter(or_(models.Document.content.ilike(like), models.Document.filename.ilike(like), models.Document.tags.ilike(like)))
    if category:
        q = q.filter(models.Document.category == category)
    if date_from and date_to:
        q = q.filter(models.Document.created_at >= date_from).filter(models.Document.created_at <= date_to)
    elif date_from:
        q = q.filter(models.Document.created_at >= date_from)
    elif date_to:
        q = q.filter(models.Document.created_at <= date_to)
    return q.all()
