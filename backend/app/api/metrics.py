from fastapi import APIRouter

router = APIRouter()

# The counter now uses the new, more descriptive route names
counter = {
    "local_knowledge": 0,
    "medical_reasoning": 0,
    "validation_failed": 0, # Also good to track how many requests fail validation
}

@router.get("/metrics", tags=["Metrics"])
def get_metrics():
    """
    Returns a simple in-memory counter for the number of requests per route.
    """
    return counter
