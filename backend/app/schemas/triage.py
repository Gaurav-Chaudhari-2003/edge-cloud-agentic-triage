from pydantic import BaseModel

class TriageRequest(
    BaseModel
):
    type:str
    content:str


class TriageResponse(
    BaseModel
):
    request_id:int
    status:str