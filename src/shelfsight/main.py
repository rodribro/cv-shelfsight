from fastapi import FastAPI

from shelfsight.api.router import api_router

app = FastAPI(
    title="ShelfSight API",
    description="API for ShelfSight, a CV application for shelf monitoring.",
    version="1.0.0",
)

app.include_router(api_router, prefix="/v1")
