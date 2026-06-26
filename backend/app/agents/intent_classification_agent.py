from app.agents.base import AgentState

class IntentClassificationAgent:
    """
    Classifies the user's intent based on keyword matching.
    This version uses simple substring matching for robustness and includes
    detailed debugging prints.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "intent_classification"
        state.execution_path.append("intent_classification")

        content_to_analyze = (state.sanitized_content or state.content).lower()
        detected_intent = "other"

        intent_keywords = {
            "emergency": ["chest pain", "breathing", "severe bleed", "unconscious", "accident"],
            "appointment": ["appointment", "book", "schedule", "meet a doctor"],
            "insurance": ["insurance", "claim", "policy", "coverage", "billing"],
            "medical_symptom": ["fever", "cough", "headache", "pain", "vomit", "dizzy", "nausea", "symptom"],
            "hospital_faq": ["hours", "timing", "address", "contact", "departments", "visiting"],
        }

        print("=" * 60)
        print("INTENT CLASSIFICATION DEBUG")
        print(f"CONTENT: {repr(content_to_analyze)}")

        for intent, keywords in intent_keywords.items():
            print(f"\nChecking intent: {intent}")
            for keyword in keywords:
                match = keyword in content_to_analyze
                print(f"  - '{keyword}': {'MATCH' if match else 'no match'}")
                if match:
                    detected_intent = intent
                    break
            if detected_intent != "other":
                break
        
        print(f"\nFINAL DETECTED INTENT: {detected_intent}")
        print("=" * 60)

        state.intent = detected_intent
        return state
