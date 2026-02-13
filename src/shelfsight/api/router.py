from fastapi import APIRouter

from shelfsight.api.v1.routers import health

api_router = APIRouter()
api_router.include_router(health.router)
