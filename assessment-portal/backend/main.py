from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.exceptions.handlers import (
    register_exception_handlers
)


app = FastAPI(
    title="Assessment Portal API",
    version="1.0.0"
)

register_exception_handlers(
    app
)

app.include_router(
    auth_router
)


@app.get("/")
def home():

    return {
        "message":
        "Assessment Portal API Running"
    }