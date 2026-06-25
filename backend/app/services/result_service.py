from sqlalchemy.orm import Session
from app.db.models import Request


def get_result(
    db: Session,
    request_id: int
):
    return (
        db.query(Request)
        .filter(
            Request.id == request_id
        )
        .first()
    )