from fastapi import *
from sqlalchemy.orm import *

from app.core.database import *

from app.db.models import *

router=APIRouter()


@router.get(
"/status/{id}"
)

def status(
id:int,
db:Session=
Depends(
get_db
)
):

    req=(
        db.query(Request)
        .filter(
            Request.id==id
        )
        .first()
    )

    return {

        "status":
        req.status,

        "agent":
        req.current_agent
    }