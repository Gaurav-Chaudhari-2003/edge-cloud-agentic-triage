from app.agents.base import AgentState
from app.db.models import AuditLog
from app.core.database import SessionLocal
from app.agents.formatter_agent import FormatterAgent

class AuditLoggerAgent:
    """
    Logs the final state of a request to the database for audit and traceability.
    This is the final agent in the pipeline.
    """

    def run(self, state: AgentState):
        state.current_agent = "audit_logger"
        
        # We need the final output for the log, so we can call the formatter here
        # This is safe because the formatter is a pure function of the state
        final_output = FormatterAgent().run(state)

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
