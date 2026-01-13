"""
OCR service: Extract text from various document formats
"""
from typing import BinaryIO
from fastapi import UploadFile
from io import BytesIO
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
import docx


async def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF files"""
    reader = PdfReader(BytesIO(file_bytes))
    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(texts)


async def extract_text_from_image(file_bytes: bytes) -> str:
    """Extract text from image files using Tesseract OCR"""
    img = Image.open(BytesIO(file_bytes))
    # Support both English and Sinhala
    # Install with: brew install tesseract-lang (macOS) or apt-get install tesseract-ocr-sin (Ubuntu)
    try:
        text = pytesseract.image_to_string(img, lang='eng+sin')
    except Exception:
        # Fallback to English only if Sinhala is not installed
        text = pytesseract.image_to_string(img, lang='eng')
    return text


async def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from Word documents (.docx)"""
    doc = docx.Document(BytesIO(file_bytes))
    texts = []
    for paragraph in doc.paragraphs:
        texts.append(paragraph.text)
    return "\n".join(texts)


async def extract_text_from_any(upload_file: UploadFile) -> str:
    """
    Extract text from any supported document format
    Supports: PDF, images (PNG, JPG, TIFF, BMP), Word documents
    """
    content = await upload_file.read()
    filename = upload_file.filename.lower()
    content_type = upload_file.content_type or ""
    
    # PDF files
    if filename.endswith(".pdf") or content_type == "application/pdf":
        return await extract_text_from_pdf(content)
    
    # Word documents
    if filename.endswith(".docx") or "wordprocessingml" in content_type:
        return await extract_text_from_docx(content)
    
    # Image files
    image_extensions = [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"]
    if any(filename.endswith(ext) for ext in image_extensions) or content_type.startswith("image/"):
        return await extract_text_from_image(content)
    
    # Fallback: try PDF, then image, then Word
    try:
        return await extract_text_from_pdf(content)
    except Exception:
        try:
            return await extract_text_from_image(content)
        except Exception:
            try:
                return await extract_text_from_docx(content)
            except Exception:
                return ""
