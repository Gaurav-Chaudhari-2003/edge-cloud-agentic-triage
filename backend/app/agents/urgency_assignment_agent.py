from app.agents.base import AgentState

class UrgencyAssignmentAgent:
    """
    Assigns an urgency level based on the classified intent and complexity score.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "urgency_assignment"

        if state.intent == "emergency":
            state.urgency = "emergency"
        elif state.complexity >= 0.7:
            state.urgency = "high"
        elif state.complexity >= 0.4:
            state.urgency = "medium"
        else:
            state.urgency = "low"
            
        return state
