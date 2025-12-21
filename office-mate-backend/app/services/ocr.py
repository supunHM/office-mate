from typing import BinaryIO
from fastapi import UploadFile
from io import BytesIO
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader


async def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(texts)


async def extract_text_from_image(file_bytes: bytes) -> str:
    img = Image.open(BytesIO(file_bytes))
    text = pytesseract.image_to_string(img)
    return text


async def extract_text_from_any(upload_file: UploadFile) -> str:
    content = await upload_file.read()
    filename = upload_file.filename.lower()
    if filename.endswith(".pdf") or upload_file.content_type == "application/pdf":
        return await extract_text_from_pdf(content)
    # treat other common image types
    if any(filename.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]):
        return await extract_text_from_image(content)
    # fallback: try pdf then image
    try:
        return await extract_text_from_pdf(content)
    except Exception:
        try:
            return await extract_text_from_image(content)
        except Exception:
            return ""
