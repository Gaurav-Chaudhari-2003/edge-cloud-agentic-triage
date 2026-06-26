from dataclasses import dataclass, field
from typing import List

@dataclass
class AgentState:
    # Existing fields (preserved for backward compatibility)
    request_id: int
    content: str
    input_type: str
    route: str = None
    complexity: float = 0
    confidence: float = 0
    output: str = None
    current_agent: str = None
    latency_ms: int = 0
    estimated_cost: int = 0 # This will be replaced by a better metric later
    escalated: bool = False

    # New fields for healthcare privacy workflow
    sanitized_content: str = ""
    contains_pii: bool = False
    detected_entities: List[str] = field(default_factory=list)
    intent: str = "unknown"
    urgency: str = "low"
    validation_errors: List[str] = field(default_factory=list)
    model_used: str = ""
    execution_path: List[str] = field(default_factory=list)