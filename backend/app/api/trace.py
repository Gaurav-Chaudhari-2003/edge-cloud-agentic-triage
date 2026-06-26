from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.trace_service import get_trace_for_request

router = APIRouter()

@router.get("/trace/{request_id}", tags=["Observability"])
def get_trace(request_id: int, db: Session = Depends(get_db)):
    """
    Returns the complete execution trace for a given request ID.
    This provides a detailed, step-by-step view of the agent pipeline.
    """
    trace_log = get_trace_for_request(db, request_id)

    if not trace_log:
        raise HTTPException(status_code=404, detail="Trace not found for the given request ID.")

    return {
        "request_id": trace_log.request_id,
        "pipeline": trace_log.execution_path,
        "route": trace_log.route,
        "model_used": trace_log.model_used,
        "latency_ms": trace_log.latency_ms,
    }
