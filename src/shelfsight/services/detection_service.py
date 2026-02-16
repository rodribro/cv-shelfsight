import uuid
from datetime import datetime, timezone
from io import BytesIO

from PIL import Image

from shelfsight.api.v1.schemas.detection_schema import (
    Detection,
    DetectionInput,
    DetectionRunResponse,
    RunSummary,
    Status,
)


class DetectionService:
    def __init__(self, model):
        self.model = model  # Placeholder for actual model loading
        self.model_version = "1.0"  # Placeholder for actual model versioning

    def create_run(self, detection_input: DetectionInput) -> DetectionRunResponse:

        height, width = calculate_image_dimensions(detection_input.image_bytes)

        detections = []
        counts_by_label = count_label_detections(detections)

        return DetectionRunResponse(
            run_id=uuid.uuid4(),
            filename=detection_input.filename,
            content_type=detection_input.content_type,
            model_version=self.model_version,
            status=Status.completed,
            source=detection_input.source,
            detections=detections,
            summary=RunSummary(
                total_detections=len(detections),
                counts_by_label=counts_by_label,
            ),
            image_width=width,
            image_height=height,
            image_uri=None,
            error=None,
            created_at=datetime.now(timezone.utc),
        )


def calculate_image_dimensions(image_bytes: bytes) -> tuple[int, int]:
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            return img.height, img.width
    except Exception as err:
        raise InvalidImageError(
            "Unable to determine image dimensions. Invalid image data."
        ) from err


def count_label_detections(detections: list[Detection]) -> dict[str, int]:
    counts = {}
    for det in detections:
        counts[det.label] = counts.get(det.label, 0) + 1
    return counts


class InvalidImageError(Exception):

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"InvalidImageError: {self.message}"
