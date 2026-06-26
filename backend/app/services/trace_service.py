from sqlalchemy.orm import Session
from app.db.models import AuditLog

def get_trace_for_request(db: Session, request_id: int):
    """
    Retrieves the audit log for a specific request ID from the database.
    """
    return db.query(AuditLog).filter(AuditLog.request_id == request_id).first()
