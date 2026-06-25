from fastapi import FastAPI

from app.api.triage import router

app=FastAPI()

app.include_router(router)
from app.api.status import router as status

app.include_router(status)

@app.get("/")
def health():

    return {
        "ok":True
    }