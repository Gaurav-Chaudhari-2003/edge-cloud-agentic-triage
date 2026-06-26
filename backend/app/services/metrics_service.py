from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.db.models import Request, AuditLog

def get_dashboard_metrics(db: Session):
    """
    Calculates a comprehensive set of metrics for the dashboard.
    """
    total_requests = db.query(Request).count()
    
    text_requests = db.query(Request).filter(Request.input_type == 'text').count()
    image_requests = db.query(Request).filter(Request.input_type == 'image').count()
    
    knowledge_base_routes = db.query(AuditLog).filter(AuditLog.route == 'local_knowledge').count()
    medical_reasoning_routes = db.query(AuditLog).filter(AuditLog.route == 'medical_reasoning').count()
    
    pii_detected = db.query(AuditLog).filter(AuditLog.contains_pii == True).count()
    
    average_latency_ms = db.query(func.avg(AuditLog.latency_ms)).scalar()
    
    # Calculate average OCR latency by looking into the JSON execution_path
    # This is a more advanced query and might be slow on very large datasets
    # For this project, it's a great demonstration of the power of structured logs
    ocr_latencies = []
    logs_with_ocr = db.query(AuditLog.execution_path).filter(AuditLog.execution_path.isnot(None)).all()
    for log in logs_with_ocr:
        for step in log.execution_path:
            if isinstance(step, dict) and step.get("name") == "ocr":
                ocr_latencies.append(step.get("duration_ms", 0))

    average_ocr_latency_ms = sum(ocr_latencies) / len(ocr_latencies) if ocr_latencies else 0

    return {
        "total_requests": total_requests,
        "text_requests": text_requests,
        "image_requests": image_requests,
        "knowledge_base_routes": knowledge_base_routes,
        "medical_reasoning_routes": medical_reasoning_routes,
        "pii_detected": pii_detected,
        "average_latency_ms": round(average_latency_ms) if average_latency_ms else 0,
        "average_ocr_latency_ms": round(average_ocr_latency_ms) if average_ocr_latency_ms else 0,
    }
