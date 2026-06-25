from fastapi import *
from sqlalchemy.orm import Session

from app.schemas.triage import *
from app.services.triage_service import *

from app.core.database import get_db
from app.workers.tasks import (
process_request
)

router=APIRouter()

@router.post(
"/triage"
)

def triage(
payload:TriageRequest,
db:Session=Depends(
get_db
)
):

    req=create_request(
        db,
        payload
    )

    print("sending task")

    process_request.delay(
        req.id
    )

    return {
        "request_id":req.id,
        "status":req.status
    }