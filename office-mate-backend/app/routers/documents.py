"""
Document routes: upload, list, search, and manage documents
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import os
import shutil

from app import models, schemas
from app.database import get_db
from app.services.ocr import extract_text_from_any
from app.services.classifier import predict_category
from app.services.search import search_documents
from app.services.auth import get_current_active_user
from app.config import UPLOAD_DIR, MAX_UPLOAD_SIZE

router = APIRouter()


@router.post("/", response_model=schemas.DocumentRead, status_code=status.HTTP_201_CREATED)
async def create_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Upload and process a document (OCR + classification)"""
    # Check file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {MAX_UPLOAD_SIZE} bytes"
        )
    
    # Extract text using OCR
    content = await extract_text_from_any(file)
    
    # Predict category using ML classifier
    category = "unknown"
    try:
        category = predict_category(content)
    except Exception:
        category = "unknown"
    
    # Save file to disk
    user_upload_dir = UPLOAD_DIR / str(current_user.id)
    user_upload_dir.mkdir(exist_ok=True)
    
    file_path = user_upload_dir / file.filename
    # Handle duplicate filenames
    counter = 1
    while file_path.exists():
        name, ext = os.path.splitext(file.filename)
        file_path = user_upload_dir / f"{name}_{counter}{ext}"
        counter += 1
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create document record
    doc = models.Document(
        filename=file.filename,
        file_path=str(file_path),
        file_size=file_size,
        file_type=file.content_type,
        content=content or "",
        category=category,
        ocr_confidence=0,  # TODO: Calculate actual confidence
        user_id=current_user.id
    )
    
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.get("/", response_model=List[schemas.DocumentListRead])
def list_documents(
    query: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """List and search documents for current user"""
    docs = search_documents(
        db,
        user_id=current_user.id,
        query=query,
        category=category,
        date_from=date_from,
        date_to=date_to
    )
    return docs


@router.get("/{document_id}", response_model=schemas.DocumentRead)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get a specific document"""
    doc = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.put("/{document_id}", response_model=schemas.DocumentRead)
def update_document(
    document_id: int,
    doc_update: schemas.DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Update document metadata"""
    doc = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    for key, value in doc_update.dict(exclude_unset=True).items():
        setattr(doc, key, value)
    
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Delete a document"""
    doc = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file from disk
    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)
    
    db.delete(doc)
    db.commit()
    return {"message": "Document deleted successfully"}


@router.post("/{document_id}/tags/{tag_id}")
def add_tag_to_document(
    document_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Add a tag to a document"""
    doc = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    if tag not in doc.tags:
        doc.tags.append(tag)
        db.commit()
    
    return {"message": "Tag added to document"}


@router.delete("/{document_id}/tags/{tag_id}")
def remove_tag_from_document(
    document_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Remove a tag from a document"""
    doc = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    if tag in doc.tags:
        doc.tags.remove(tag)
        db.commit()
    
    return {"message": "Tag removed from document"}
