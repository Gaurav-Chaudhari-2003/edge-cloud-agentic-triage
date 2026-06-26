import time
from app.agents.base import AgentState
from app.agents.validation_agent import ValidationAgent
from app.agents.ocr_agent import OCRAgent
from app.agents.pii_detection_agent import PIIDetectionAgent
from app.agents.pii_sanitization_agent import PIISanitizationAgent
from app.agents.intent_classification_agent import IntentClassificationAgent
from app.agents.medical_complexity_agent import MedicalComplexityAgent
from app.agents.router_agent import RouterAgent
from app.agents.local_knowledge_agent import LocalKnowledgeAgent
from app.agents.medical_reasoning_agent import MedicalReasoningAgent
from app.agents.formatter_agent import FormatterAgent
from app.agents.audit_logger_agent import AuditLoggerAgent
from app.api.metrics import counter

PIPELINE = [
    ValidationAgent, OCRAgent, PIIDetectionAgent, PIISanitizationAgent,
    IntentClassificationAgent, MedicalComplexityAgent, RouterAgent,
]

def run_pipeline(req):
    state = AgentState(request_id=req.id, content=req.content, input_type=req.input_type)
    total_start_time = time.time()

    def run_agent(agent_cls, current_state):
        agent_start_time = time.time()
        new_state = agent_cls().run(current_state)
        agent_duration = round((time.time() - agent_start_time) * 1000)
        
        new_state.execution_path.append({
            "name": new_state.current_agent or agent_cls.__name__.replace('Agent', '').lower(),
            "status": "completed",
            "duration_ms": agent_duration,
        })
        return new_state

    for agent_cls in PIPELINE:
        state = run_agent(agent_cls, state)
        if state.validation_errors:
            state.route = "validation_failed"
            break

    if state.route in counter:
        counter[state.route] += 1

    if not state.validation_errors:
        routed_agent = LocalKnowledgeAgent if state.route == "local_knowledge" else MedicalReasoningAgent
        state = run_agent(routed_agent, state)

    state.latency_ms = round((time.time() - total_start_time) * 1000)
    
    final_output = FormatterAgent().run(state)
    run_agent(AuditLoggerAgent, state) # Also trace the audit logger

    return final_output
