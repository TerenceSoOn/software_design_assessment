"""
Upload Router - Handle file uploads.
"""
import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from app.config import settings

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/image")
async def upload_image(request: Request, file: UploadFile = File(...)):
    """
    Upload an image file.
    Returns the URL of the uploaded file.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
    # Use the request's base URL to construct the full URL
    base_url = str(request.base_url).rstrip('/')
    return {"url": f"{base_url}/static/uploads/{filename}"}
