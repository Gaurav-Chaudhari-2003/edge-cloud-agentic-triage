from app.agents.base import AgentState
from app.db.models import AuditLog
from app.core.database import SessionLocal

class AuditLoggerAgent:
    """
    Logs the final state of a request to the database for audit and traceability.
    This is the final agent in the pipeline.
    """

    def run(self, state: AgentState, final_output: dict):
        state.current_agent = "audit_logger"
        state.execution_path.append("audit_logger")

        db = SessionLocal()
        try:
            log_entry = AuditLog(
                request_id=state.request_id,
                contains_pii=state.contains_pii,
                detected_entities=state.detected_entities,
                intent=state.intent,
                complexity=state.complexity,
                urgency=state.urgency,
                route=state.route,
                model_used=state.model_used,
                latency_ms=state.latency_ms,
                status=final_output.get("status", "unknown"),
                final_result=final_output,
                execution_path=state.execution_path,
            )
            db.add(log_entry)
            db.commit()
        finally:
            db.close()
            
        return state
