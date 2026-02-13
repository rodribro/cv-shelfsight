from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/", summary="Health Check", description="Check API health")
async def health_check():
    return {"status": "ok", "message": "ShelfSight API is healthy."}
