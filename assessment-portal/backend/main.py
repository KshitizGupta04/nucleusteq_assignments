from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth import router as auth_router

from app.api.v1.category import (
    router as category_router
)

from app.api.v1.quiz import (
    router as quiz_router
)

from app.api.v1.question import (
    router as question_router
)

from app.api.v1.attempt import (
    router as attempt_router
)

from app.exceptions.handlers import (
    register_exception_handlers
)

from app.api.v1.result import (
    router as result_router
)


app = FastAPI(
    title="Assessment Portal API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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

app.include_router(
    question_router
)

app.include_router(
    attempt_router
)

app.include_router(
    result_router
)


@app.get("/")
def home():

    return {
        "message":
        "Assessment Portal API Running"
    }