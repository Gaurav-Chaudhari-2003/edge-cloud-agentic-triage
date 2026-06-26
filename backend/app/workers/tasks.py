from app.workers.celery_app import celery
from app.core.database import SessionLocal
from app.db.models import Request
from app.services.orchestrator import run_pipeline

@celery.task
def process_request(request_id: int):
    """
    The main Celery task. Its responsibilities are to:
    1. Set the request status to PROCESSING.
    2. Execute the agent pipeline.
    3. Save the final result and set the status to COMPLETED.
    """
    db = SessionLocal()
    try:
        # 1. Fetch the request and set status to PROCESSING
        req = db.query(Request).filter(Request.id == request_id).first()
        if not req:
            return

        req.status = "PROCESSING"
        db.commit()

        # 2. Execute the agent pipeline
        final_output = run_pipeline(req)

        # 3. Save the final result and set status to COMPLETED
        req.output = final_output
        req.status = "COMPLETED"
        db.commit()

    finally:
        db.close()
