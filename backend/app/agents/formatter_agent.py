from app.agents.base import AgentState

class FormatterAgent:
    """
    Formats the final output, creating a rich JSON response that provides
    a full, observable trace of the agent pipeline's execution.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "formatter"
        state.execution_path.append("formatter")

        # Handle the case where validation failed
        if state.validation_errors:
            return {
                "request_id": state.request_id,
                "status": "failed",
                "errors": state.validation_errors,
                "execution_path": state.execution_path,
                "latency_ms": state.latency_ms,
            }

        # Format the successful response
        return {
            "request_id": state.request_id,
            "status": "completed",
            "contains_pii": state.contains_pii,
            "detected_entities": state.detected_entities,
            "intent": state.intent,
            "complexity": round(state.complexity, 2),
            "urgency": state.urgency, # This will be implemented in a future step
            "route": state.route,
            "model_used": state.model_used,
            "latency_ms": round(state.latency_ms),
            "execution_path": state.execution_path,
            "result": state.output,
        }
