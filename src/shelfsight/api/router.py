from fastapi import APIRouter

from shelfsight.api.v1.routers import detections, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(detections.router)
