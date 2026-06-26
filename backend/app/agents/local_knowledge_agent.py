import json
import os
import re
from app.services.llm_service import generate
from app.agents.base import AgentState

class LocalKnowledgeAgent:
    """
    Handles simple, non-medical queries using a deterministic JSON lookup based on keywords.
    If no direct match is found, it falls back to a lightweight LLM (TinyLlama).
    """

    def __init__(self):
        kb_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'hospital_kb.json')
        with open(kb_path, 'r') as f:
            self.knowledge_base = json.load(f)

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "local_knowledge"
        state.execution_path.append("local_knowledge")

        content_to_analyze = (state.sanitized_content or state.content).lower()
        
        found_in_kb = False
        for key, entry in self.knowledge_base.items():
            for keyword in entry["keywords"]:
                # Corrected regex with single backslash for word boundaries
                if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', content_to_analyze):
                    state.output = entry["answer"]
                    state.model_used = "KnowledgeBase"
                    found_in_kb = True
                    break
            if found_in_kb:
                break

        if not found_in_kb:
            prompt = f"""
You are a hospital administrative assistant. Your capabilities are strictly limited to providing general information about hospital services.
Analyze the user's question: "{content_to_analyze}"

If the question is about hospital timings, appointments, departments, billing, or insurance, provide a concise answer.
If the question is about a medical symptom, condition, or any other topic outside your capabilities, you MUST respond with only one sentence: "This request requires medical triage."
"""
            llm_output = generate(
                "tinyllama",
                prompt
            )
            state.output = llm_output
            state.model_used = "TinyLlama"

        return state
