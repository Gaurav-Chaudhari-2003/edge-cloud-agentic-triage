from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models import Request

router = APIRouter()

@router.get("/status/{request_id}", tags=["Status"])
def get_status(request_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the current status of a request.
    If the request is completed, it also returns the final output.
    """
    req = db.query(Request).filter(Request.id == request_id).first()

    if not req:
        raise HTTPException(status_code=404, detail="Request not found.")

    response = {"status": req.status}

    # If the task is completed, include the final output in the response
    if req.status == "COMPLETED":
        response["output"] = req.output

    return response
