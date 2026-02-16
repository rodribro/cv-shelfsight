from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from shelfsight.api.dependencies import get_detection_service
from shelfsight.api.v1.schemas.detection_schema import DetectionInput, Source
from shelfsight.services.detection_service import DetectionService, InvalidImageError
from shelfsight.services.image_utils import validate_and_get_image_info

router = APIRouter(prefix="/detections", tags=["detections"])

MAX_BYTES = 50 * 1024 * 1024  # 50 MB limit
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}


@router.post("/", summary="Run model inference", description="Inference endpoint")
async def upload(
    file: UploadFile = File(...),
    detection_service: DetectionService = Depends(get_detection_service),
):

    image_bytes = await file.read()
    await file.close()
    content_type = file.content_type or ""

    try:
        image_info = validate_and_get_image_info(
            image_bytes,
            max_bytes=MAX_BYTES,
            allowed_content_types=ALLOWED_CONTENT_TYPES,
            content_type=file.content_type,
        )
    except InvalidImageError as e:
        msg = str(e)

        status_code = 415
        if "exceeds" in msg:
            status_code = 413

        raise HTTPException(status_code=status_code, detail=msg) from e

    detection_service = DetectionService(model=None)
    detection_input = DetectionInput(
        image_bytes=image_bytes,
        filename=file.filename,
        content_type=content_type,
        source=Source.upload,
        image_height=image_info.height,
        image_width=image_info.width,
    )
    detection = detection_service.create_run(detection_input)

    return detection
