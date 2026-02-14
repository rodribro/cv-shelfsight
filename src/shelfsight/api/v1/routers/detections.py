from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image

from shelfsight.services.detection import DetectionService

router = APIRouter(prefix="/detections", tags=["detections"])

MAX_BYTES = 50 * 1024 * 1024  # 50 MB limit
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}


def validate_image_upload(data: bytes, content_type: str) -> None:

    if not data:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="File size exceeds 50 MB limit.")

    if content_type and content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Invalid file type. JPEG/PNG only")

    try:
        img = Image.open(BytesIO(data))
        img.verify()

    except Exception as err:
        raise HTTPException(
            status_code=415,
            detail="Corrupted or unreadable image.",
        ) from err


@router.post("/", summary="Run model inference", description="Inference endpoint")
async def upload(file: UploadFile = File(...)):

    data = await file.read()
    await file.close()

    content_type = file.content_type or ""

    validate_image_upload(data, content_type)

    detection_service = DetectionService(model=None)
    run_id, detections, total_detections, products = detection_service.create_run(data)

    return {
        "run_id": run_id,
        "status": "completed",
        "source": "upload",
        "detections": detections,
        "summary": {"total_detections": total_detections, "products": products},
    }
