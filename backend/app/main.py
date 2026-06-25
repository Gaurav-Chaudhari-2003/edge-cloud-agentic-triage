from fastapi import FastAPI

from app.api.triage import router
from app.api.status import router as status
from app.api.result import router as result

app = FastAPI()

app.include_router(router)
app.include_router(status)
app.include_router(result)


@app.get("/")
def health():

    return {
        "ok": True
    }