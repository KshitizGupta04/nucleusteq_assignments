from fastapi import FastAPI

from app.api.v1.auth import router as auth_router

from app.api.v1.category import (
    router as category_router
)

from app.exceptions.handlers import (
    register_exception_handlers
)

from app.api.v1.quiz import (
    router as quiz_router
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

app.include_router(
    category_router
)

app.include_router(
    quiz_router
)


@app.get("/")
def home():

    return {
        "message":
        "Assessment Portal API Running"
    }