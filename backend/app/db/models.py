from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, JSON, DateTime
from sqlalchemy.sql import func

Base = declarative_base()

class Request(Base):
    """
    Represents an incoming request before processing. This is now a lightweight
    record, as the detailed processing trail is captured in the AuditLog.
    """
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    input_type = Column(String)
    content = Column(Text)
    status = Column(String, default="QUEUED")
    # The final output is stored here after processing
    output = Column(JSON, nullable=True)


class AuditLog(Base):
    """
    A comprehensive log of a completed request, providing a full audit trail
    for traceability and analysis.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Key metadata for audit
    contains_pii = Column(Boolean)
    detected_entities = Column(JSON)
    intent = Column(String)
    complexity = Column(Float)
    urgency = Column(String)
    route = Column(String)
    model_used = Column(String)
    latency_ms = Column(Integer)
    status = Column(String) # e.g., "completed", "failed"
    
    # The final result for easy access
    final_result = Column(JSON)
    
    # The full execution path for explainability
    execution_path = Column(JSON)
