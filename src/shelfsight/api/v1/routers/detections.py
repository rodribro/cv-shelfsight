from fastapi import APIRouter, File, HTTPException, UploadFile
from io import BytesIO
from PIL import Image

router = APIRouter(prefix="/detections", tags=["detections"])

MAX_BYTES = 50 * 1024 * 1024  # 50 MB limit
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}

def validate_image_upload(data: bytes, content_type: str) -> None:

    if not data:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")
    
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="File size exceeds the 50 MB limit.")
    
    if content_type and content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Invalid file type. Only JPEG and PNG are allowed.")        
    
    try:
        img = Image.open(BytesIO(data))
        img.verify()

    except Exception:
        raise HTTPException(
            status_code=415,
            detail="Corrupted or unreadable image.",
        )

@router.post("/", summary="Upload image and get detections", description="Upload an image and receive detected products and their details.")
async def upload(file: UploadFile = File(...)):

    data = await file.read()
    content_type = file.content_type or ""

    validate_image_upload(data, content_type)
    
    
    # when implemented: run inference on the uploaded image and generate detections
    # detections = run_inference(image)

    return {
            "run_id": 12345,
            "status": "completed",
            "source": "upload",
            "detections": [],
            "summary": {
                "total_detections": 0,
                "products": {}
                }
    }