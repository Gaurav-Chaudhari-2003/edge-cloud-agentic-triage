from fastapi import FastAPI

from app.api.triage import router
from app.api.status import router as status
from app.api.result import router as result
from app.api.metrics import router as metrics
from app.api.trace import router as trace_router

app = FastAPI()

app.include_router(router, tags=["Triage"])
app.include_router(status, tags=["Status"])
app.include_router(result, tags=["Result"])
app.include_router(metrics, tags=["Metrics"])
app.include_router(trace_router, tags=["Observability"]) # New trace endpoint


@app.get("/")
def health():

    return {
        "ok": True
    }
