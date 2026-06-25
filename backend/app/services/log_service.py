from sqlalchemy.orm import Session
from app.db.models import AgentLog


def log_agent_step(
    db: Session,
    request_id: int,
    agent: str,
    duration_ms: int,
    decision: str
):
    log = AgentLog(
        request_id=request_id,
        agent=agent,
        duration_ms=duration_ms,
        decision=decision
    )
    db.add(log)
    db.commit()