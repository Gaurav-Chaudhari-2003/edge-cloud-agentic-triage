from app.agents.base import AgentState

class RouterAgent:
    """
    Routes the request to the appropriate downstream agent based on business logic.
    It uses the intent and complexity scores calculated by upstream agents.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "router"
        state.execution_path.append("router")

        # High complexity overrides all other routing rules
        if state.complexity > 0.8:
            state.route = "medical_reasoning"
        else:
            # Route based on the classified intent
            intent_to_route_map = {
                "hospital_faq": "local_knowledge",
                "appointment": "local_knowledge",
                "insurance": "local_knowledge",
                "medical_symptom": "medical_reasoning",
                "emergency": "medical_reasoning",
            }
            # Get the route from the map, or default to 'local_knowledge' for 'other' intent
            state.route = intent_to_route_map.get(state.intent, "local_knowledge")

        print("=" * 60)
        print("ROUTER DEBUG")
        print(f"INTENT: {state.intent}")
        print(f"COMPLEXITY: {state.complexity}")
        print(f"FINAL ROUTE: {state.route}")
        print("=" * 60)

        return state
