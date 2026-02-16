from io import BytesIO

from PIL import Image


class InvalidImageError(Exception):
    pass


class ImageInfo:
    def __init__(self, width: int, height: int, format: str | None):
        self.width = width
        self.height = height
        self.format = format


def validate_and_get_image_info(
    image_bytes: bytes,
    *,
    max_bytes: int,
    allowed_content_types: set[str],
    content_type: str | None,
) -> ImageInfo:
    if not image_bytes:
        raise InvalidImageError("Empty file uploaded.")

    if len(image_bytes) > max_bytes:
        raise InvalidImageError(f"File size exceeds the {max_bytes // (1024 * 1024)} MB limit.")

    if content_type and content_type not in allowed_content_types:
        raise InvalidImageError("Invalid file type. Only JPEG and PNG are allowed.")

    try:
        with Image.open(BytesIO(image_bytes)) as img:
            img.verify()
            width, height = img.size
            fmt = img.format
    except Exception as e:
        raise InvalidImageError("Corrupted or unreadable image.") from e

    return ImageInfo(width=width, height=height, format=fmt)
