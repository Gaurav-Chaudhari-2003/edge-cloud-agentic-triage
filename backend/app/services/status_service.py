from app.db.models import Request

def update_status(
    db,
    request_id,
    status,
    agent=None
):

    req=(
        db.query(Request)
        .filter(
            Request.id==request_id
        )
        .first()
    )

    req.status=status

    req.current_agent=agent

    db.commit()

    return req