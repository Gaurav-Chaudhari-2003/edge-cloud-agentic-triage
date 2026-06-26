from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models import Request
from app.services.result_service import get_result_from_audit

router = APIRouter()

@router.get("/result/{request_id}", tags=["Result"])
def get_result(request_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the final result of a completed request.
    This endpoint checks the request status first, then fetches the detailed
    result from the audit log if the request is complete.
    """
    # First, check the status of the main request
    req = db.query(Request).filter(Request.id == request_id).first()

    if not req:
        raise HTTPException(status_code=404, detail="Request not found.")

    if req.status != "COMPLETED":
        return {"status": req.status, "message": "Result is not yet available."}

    # If completed, fetch the rich details from the audit log
    audit_log = get_result_from_audit(db, request_id)

    if not audit_log:
        raise HTTPException(status_code=404, detail="Result audit log not found, though request was marked as completed.")

    return audit_log.final_result
