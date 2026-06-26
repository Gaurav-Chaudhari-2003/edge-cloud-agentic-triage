from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.metrics_service import get_dashboard_metrics

router = APIRouter()

@router.get("/metrics", tags=["Metrics"])
def get_metrics_dashboard(db: Session = Depends(get_db)):
    """
    Returns a comprehensive dashboard of metrics, providing measurable
    evidence of the system's performance and routing strategy.
    """
    return get_dashboard_metrics(db)
