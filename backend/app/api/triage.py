import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.schemas.triage import TriageRequest
from app.services.triage_service import create_request
from app.core.database import get_db
from app.workers.tasks import process_request

router = APIRouter()

UPLOADS_DIR = "uploads"
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png"]

@router.on_event("startup")
def on_startup():
    # Create the uploads directory on startup if it doesn't exist
    os.makedirs(UPLOADS_DIR, exist_ok=True)

@router.post("/triage", tags=["Triage"])
def triage(
    # The endpoint now accepts either a file or a text payload
    file: UploadFile = File(None),
    content: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Accepts a triage request. It can be either a text query or an image file.
    - For text: provide 'content' in the form data.
    - For images: provide 'file' as a file upload (image/jpeg or image/png).
    """
    if file:
        # --- Image Upload Logic ---
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid file type. Only {', '.join(ALLOWED_MIME_TYPES)} are allowed.")
        
        input_type = "image"
        # Save the uploaded file to a temporary location
        file_path = os.path.join(UPLOADS_DIR, file.filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        finally:
            file.file.close() # Ensure the file is closed
        
        # The content for the agent pipeline will be the path to the file
        request_content = file_path

    elif content:
        # --- Text Input Logic (unchanged) ---
        input_type = "text"
        request_content = content
    else:
        raise HTTPException(status_code=400, detail="Either 'file' for image upload or 'content' for text input must be provided.")

    # Create the request payload for the database
    payload = TriageRequest(type=input_type, content=request_content)
    
    req = create_request(db, payload)

    print("Sending task to Celery worker...")
    process_request.delay(req.id)

    return {
        "request_id": req.id,
        "status": req.status
    }
