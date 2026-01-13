"""
Tags routes: CRUD operations for tags
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db
from app.services.auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=schemas.TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_in: schemas.TagCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Create a new tag"""
    # Check if tag already exists
    existing_tag = db.query(models.Tag).filter(models.Tag.name == tag_in.name).first()
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag with this name already exists"
        )
    
    tag = models.Tag(**tag_in.dict())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.get("/", response_model=List[schemas.TagRead])
def list_tags(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """List all tags"""
    tags = db.query(models.Tag).all()
    return tags


@router.get("/{tag_id}", response_model=schemas.TagRead)
def get_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get a specific tag"""
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.put("/{tag_id}", response_model=schemas.TagRead)
def update_tag(
    tag_id: int,
    tag_update: schemas.TagUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Update a tag"""
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # Check if new name conflicts with existing tag
    if tag_update.name and tag_update.name != tag.name:
        existing = db.query(models.Tag).filter(models.Tag.name == tag_update.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag with this name already exists"
            )
    
    for key, value in tag_update.dict(exclude_unset=True).items():
        setattr(tag, key, value)
    
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Delete a tag"""
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted successfully"}
