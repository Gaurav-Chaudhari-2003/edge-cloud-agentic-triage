from app.agents.base import AgentState

class MedicalComplexityAgent:
    """
    Analyzes the query to determine its complexity, now based on the
    pre-classified intent for better separation of concerns.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "medical_complexity"
        state.execution_path.append("medical_complexity")

        content_to_analyze = (state.sanitized_content or state.content).lower()
        total_complexity = 0.0

        print("=" * 60)
        print("MEDICAL COMPLEXITY DEBUG")
        print(f"INTENT: {state.intent}")
        print(f"CONTENT: {repr(content_to_analyze)}")

        if state.intent == "emergency":
            total_complexity = 1.0
            print("  - Intent is 'emergency', setting complexity to 1.0")
        elif state.intent == "medical_symptom":
            symptom_scores = {
                "heart": 0.4, "stroke": 0.4, "breathing": 0.3, "bleeding": 0.3,
                "diabetes": 0.2, "fever": 0.1, "pain": 0.1, "vomiting": 0.1,
            }
            print("\n  - Checking for medical symptom keywords:")
            for keyword, score in symptom_scores.items():
                match = keyword in content_to_analyze
                if match:
                    total_complexity += score
                print(f"    - '{keyword}': {'MATCH' if match else 'no match'} (+{score if match else 0})")
        else:
            print("\n  - Intent is not medical, complexity remains 0.")

        # Cap the complexity at 1.0
        normalized_complexity = min(total_complexity, 1.0)
        
        print(f"\nFINAL CALCULATED COMPLEXITY: {normalized_complexity}")
        print("=" * 60)

        state.complexity = normalized_complexity
        return state
