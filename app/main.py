from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Originals Test Task",
        docs_url="/api/docs",
    )

    return app
    