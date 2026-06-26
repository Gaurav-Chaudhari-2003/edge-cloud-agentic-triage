import time
from app.agents.base import AgentState
from app.agents.validation_agent import ValidationAgent
from app.agents.pii_detection_agent import PIIDetectionAgent
from app.agents.pii_sanitization_agent import PIISanitizationAgent
from app.agents.intent_classification_agent import IntentClassificationAgent
from app.agents.medical_complexity_agent import MedicalComplexityAgent
from app.agents.router_agent import RouterAgent
from app.agents.local_knowledge_agent import LocalKnowledgeAgent
from app.agents.medical_reasoning_agent import MedicalReasoningAgent
from app.agents.formatter_agent import FormatterAgent
from app.agents.audit_logger_agent import AuditLoggerAgent
from app.api.metrics import counter # Import the counter

# The pipeline is now defined as a configurable list of agent classes
PIPELINE = [
    ValidationAgent,
    PIIDetectionAgent,
    PIISanitizationAgent,
    IntentClassificationAgent,
    MedicalComplexityAgent,
    RouterAgent,
]

def run_pipeline(req):
    """
    Executes the full, refactored pipeline of agents for medical triage,
    concluding with an audit log of the entire process.
    """
    
    state = AgentState(
        request_id=req.id,
        content=req.content,
        input_type=req.input_type
    )
    state.execution_path.append("start")
    
    start_time = time.time()

    # Execute the main pipeline
    for agent_cls in PIPELINE:
        state = agent_cls().run(state)
        if state.validation_errors:
            state.route = "validation_failed"
            break
    
    # Increment the counter based on the final route
    # This is a much safer place to do this
    if state.route in counter:
        counter[state.route] += 1

    # Execute the routed agent if validation passed
    if not state.validation_errors:
        if state.route == "local_knowledge":
            state = LocalKnowledgeAgent().run(state)
        else:
            state = MedicalReasoningAgent().run(state)

    state.latency_ms = (time.time() - start_time) * 1000
    
    # Formatter creates the final response for the user
    final_output = FormatterAgent().run(state)
    
    # AuditLogger writes the comprehensive log to the database
    AuditLoggerAgent().run(state, final_output)
    
    state.execution_path.append("end")

    return final_output
