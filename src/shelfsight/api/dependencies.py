from functools import lru_cache

from shelfsight.services.detection_service import DetectionService


@lru_cache(maxsize=1)
def get_detection_service() -> DetectionService:
    # load model and pass into DetectionService
    return DetectionService(model=None)
