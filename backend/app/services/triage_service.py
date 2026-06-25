from sqlalchemy.orm import Session

from app.db.models import Request
from app.schemas.triage import TriageRequest


def create_request(
    db: Session,
    payload: TriageRequest
):
    req = Request(
        input_type=payload.type,
        content=payload.content
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req