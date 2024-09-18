from fastapi import FastAPI

from app.api.v1.task import router as task_router
from app.api.v1.user import router as user_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Originals Test Task",
        docs_url="/api/docs",
    )
    app.include_router(user_router)
    app.include_router(task_router)

    return app
