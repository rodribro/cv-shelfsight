import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):
    completed = "completed"
    queued = "queued"
    failed = "failed"


class Source(str, Enum):
    upload = "upload"
    s3 = "s3"


class RunSummary(BaseModel):
    total_detections: int
    counts_by_label: dict[str, int]


class BoundingBox(BaseModel):
    x_min: int
    y_min: int
    x_max: int
    y_max: int


class Detection(BaseModel):
    label: str
    confidence: float
    bounding_box: BoundingBox  # x_min, y_min, x_max, y_max


class DetectionInput(BaseModel):
    image_bytes: bytes
    filename: str | None
    content_type: str | None
    source: Source
    image_height: int
    image_width: int


class DetectionRunResponse(BaseModel):
    run_id: uuid.UUID
    filename: str | None
    content_type: str | None
    model_version: str | None
    status: Status
    source: Source
    detections: list[Detection]
    summary: RunSummary
    image_width: int
    image_height: int
    image_uri: str | None
    error: str | None
    created_at: datetime
