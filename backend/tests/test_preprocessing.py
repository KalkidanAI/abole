"""Tests for the image preprocessing service."""
import io
import numpy as np
import pytest
from PIL import Image
from app.services.preprocessing import preprocessing_service, TARGET_SIZE


def create_test_image(format="JPEG", size=(300, 300), mode="RGB"):
    img = Image.new(mode, size, color=(100, 150, 50) if mode == "RGB" else 100)
    buf = io.BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()


class TestPreprocessing:
    def test_load_valid_jpg(self):
        result, _ = preprocessing_service.process_image(create_test_image(format="JPEG"))
        assert result.shape == (1, 3, TARGET_SIZE[0], TARGET_SIZE[1])

    def test_load_valid_png(self):
        result, _ = preprocessing_service.process_image(create_test_image(format="PNG"))
        assert result.shape == (1, 3, 224, 224)

    def test_resize_to_224(self):
        result, _ = preprocessing_service.process_image(create_test_image(size=(500, 400)))
        assert result.shape == (1, 3, 224, 224)

    def test_normalization_range(self):
        result, _ = preprocessing_service.process_image(create_test_image())
        assert result.min() > -5.0 and result.max() < 5.0

    def test_warning_low_resolution(self):
        _, warnings = preprocessing_service.process_image(create_test_image(size=(100, 100)))
        assert any("resolution" in w.lower() for w in warnings)

    def test_no_warnings_normal_image(self):
        _, warnings = preprocessing_service.process_image(create_test_image(size=(500, 500)))
        assert len(warnings) == 0

    def test_invalid_format_rejected(self):
        from app.core.exceptions import InvalidImageError
        with pytest.raises(InvalidImageError):
            preprocessing_service.process_image(b"not an image")

    def test_rgba_converted_to_rgb(self):
        result, _ = preprocessing_service.process_image(create_test_image(format="PNG", mode="RGBA"))
        assert result.shape == (1, 3, 224, 224)

    def test_unusual_aspect_ratio_warning(self):
        _, warnings = preprocessing_service.process_image(create_test_image(size=(200, 1000)))
        assert any("aspect ratio" in w.lower() for w in warnings)
