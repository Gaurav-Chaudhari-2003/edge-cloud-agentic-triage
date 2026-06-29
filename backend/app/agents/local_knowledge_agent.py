import json
import os
from app.services.llm_service import generate
from app.agents.base import AgentState

class LocalKnowledgeAgent:
    """
    Handles simple, non-medical queries using a deterministic JSON lookup.
    If no direct match is found, it falls back to a lightweight LLM (TinyLlama)
    with a robust, structured prompt.
    """

    def __init__(self):
        kb_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'hospital_kb.json')
        with open(kb_path, 'r') as f:
            self.knowledge_base = json.load(f)

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "local_knowledge"
        
        # The IntentClassificationAgent has already done the hard work.
        # We can directly use the classified intent to look up the answer.
        if state.intent in self.knowledge_base:
            state.output = self.knowledge_base[state.intent]["answer"]
            state.model_used = "KnowledgeBase"
        else:
            # Fallback to TinyLlama ONLY if the intent is 'other' or not in our KB
            prompt = f"""
You are a hospital assistant. The user asked: "{state.sanitized_content or state.content}"
This is not a medical question. Provide a brief, helpful administrative response.
If you cannot help, say: "Please contact our help desk for assistance."
"""
            llm_output = generate("tinyllama", prompt)
            state.output = llm_output
            state.model_used = "TinyLlama"

        return state
