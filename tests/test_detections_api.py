import io
import uuid
from datetime import datetime, timezone

from fastapi.testclient import TestClient
from PIL import Image

from shelfsight.api.dependencies import get_detection_service
from shelfsight.api.v1.schemas.detection_schema import (
    DetectionRunResponse,
    RunSummary,
    Status,
)
from shelfsight.main import app


class StubDetectionService:
    def create_run(self, detection_input):
        return DetectionRunResponse(
            run_id=uuid.uuid4(),
            filename=detection_input.filename,
            content_type=detection_input.content_type or "image/png",
            model_version="dummy-version",
            status=Status.completed,
            source=detection_input.source,
            detections=[],
            summary=RunSummary(total_detections=0, counts_by_label={}),
            image_width=detection_input.image_width,
            image_height=detection_input.image_height,
            image_uri=None,
            error=None,
            created_at=datetime.now(timezone.utc),
        )


def make_test_png_bytes() -> bytes:
    img = Image.new("RGB", (10, 10))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_post_detections_upload_returns_contract():
    # Override DI
    app.dependency_overrides[get_detection_service] = lambda: StubDetectionService()
    client = TestClient(app)

    png_bytes = make_test_png_bytes()

    files = {"file": ("test.png", png_bytes, "image/png")}

    resp = client.post("/v1/detections", files=files)
    assert resp.status_code == 200

    data = resp.json()
    assert "run_id" in data
    assert data["status"] == "completed"
    assert data["source"] == "upload"
    assert isinstance(data["detections"], list)
    assert "summary" in data
    assert data["image_width"] == 10
    assert data["image_height"] == 10

    # Cleanup override so it doesn't leak into other tests
    app.dependency_overrides.clear()
