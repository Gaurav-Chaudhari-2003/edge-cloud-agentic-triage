import time
from app.agents.base import AgentState
from app.agents.validation_agent import ValidationAgent
from app.agents.ocr_agent import OCRAgent
from app.agents.pii_detection_agent import PIIDetectionAgent
from app.agents.pii_sanitization_agent import PIISanitizationAgent
from app.agents.intent_classification_agent import IntentClassificationAgent
from app.agents.medical_complexity_agent import MedicalComplexityAgent
from app.agents.urgency_assignment_agent import UrgencyAssignmentAgent # Import new agent
from app.agents.router_agent import RouterAgent
from app.agents.local_knowledge_agent import LocalKnowledgeAgent
from app.agents.medical_reasoning_agent import MedicalReasoningAgent
from app.agents.formatter_agent import FormatterAgent
from app.agents.audit_logger_agent import AuditLoggerAgent

# The pipeline is now defined as a configurable list of agent classes
PIPELINE = [
    ValidationAgent, OCRAgent, PIIDetectionAgent, PIISanitizationAgent,
    IntentClassificationAgent, MedicalComplexityAgent, UrgencyAssignmentAgent, RouterAgent,
]

def run_pipeline(req):
    """
    Executes the full, refactored pipeline of agents for medical triage.
    """
    state = AgentState(request_id=req.id, content=req.content, input_type=req.input_type)
    
    def run_agent(agent_cls, current_state):
        agent_start_time = time.time()
        instance = agent_cls()
        new_state = instance.run(current_state)
        agent_duration = round((time.time() - agent_start_time) * 1000)
        
        # Use the agent's class name for a consistent trace name
        trace_name = agent_cls.__name__.replace('Agent', '').lower()
        new_state.execution_path.append({
            "name": trace_name,
            "status": "completed",
            "duration_ms": agent_duration,
        })
        return new_state

    # Execute the main pipeline
    for agent_cls in PIPELINE:
        state = run_agent(agent_cls, state)
        if state.validation_errors:
            state.route = "validation_failed"
            break

    # Set the human review flag
    if state.complexity >= 0.8 or state.intent == "emergency":
        state.requires_human_review = True

    # Execute the routed agent if validation passed
    if not state.validation_errors:
        routed_agent = LocalKnowledgeAgent if state.route == "local_knowledge" else MedicalReasoningAgent
        state = run_agent(routed_agent, state)

    # Formatter and AuditLogger are the final steps
    final_output = FormatterAgent().run(state)
    run_agent(AuditLoggerAgent, state)

    return final_output
