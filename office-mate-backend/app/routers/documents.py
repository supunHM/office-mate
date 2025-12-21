from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app import models, schemas
from app.database import get_db
from app.services.ocr import extract_text_from_any
from app.services.classifier import predict_category
from app.services.search import search_documents

router = APIRouter()


@router.post("/", response_model=schemas.DocumentRead)
async def create_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await extract_text_from_any(file)

    category = "unknown"
    try:
        category = predict_category(content)
    except Exception:
        category = "unknown"

    # simple tags: top frequent words
    words = [w.lower() for w in content.split() if len(w) > 3]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    tags = ",".join([k for k, _ in sorted(freq.items(), key=lambda x: -x[1])][:5])

    doc = models.Document(filename=file.filename, content=content or "", category=category, tags=tags)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.get("/", response_model=List[schemas.DocumentRead])
def list_documents(
    query: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    docs = search_documents(db, query=query, category=category, date_from=date_from, date_to=date_to)
    return docs


@router.get("/{document_id}", response_model=schemas.DocumentRead)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc
