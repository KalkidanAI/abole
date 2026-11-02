"""Tests for the FastAPI endpoints."""
import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from app.main import app
from app.config import settings

client = TestClient(app)


def make_img(fmt="JPEG", size=(300, 300)):
    img = Image.new("RGB", size, (100, 150, 50))
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()

HEADERS = {"X-API-Key": settings.API_KEY}


class TestHealth:
    def test_health_200(self):
        assert client.get("/health").status_code == 200

    def test_health_no_auth(self):
        assert client.get("/health", headers={}).status_code == 200


class TestPredictAuth:
    def test_no_key_401(self):
        r = client.post("/predict", files={"file": ("t.jpg", make_img(), "image/jpeg")})
        assert r.status_code == 401

    def test_bad_key_401(self):
        r = client.post("/predict", files={"file": ("t.jpg", make_img(), "image/jpeg")}, headers={"X-API-Key": "bad"})
        assert r.status_code == 401

    def test_valid_key_200(self):
        r = client.post("/predict", files={"file": ("t.jpg", make_img(), "image/jpeg")}, headers=HEADERS)
        assert r.status_code == 200


class TestPredictResponse:
    def test_response_structure(self):
        r = client.post("/predict", files={"file": ("t.jpg", make_img(), "image/jpeg")}, headers=HEADERS)
        d = r.json()
        for k in ["predicted_class", "confidence", "all_probabilities", "disease_info", "warnings", "disclaimer", "is_demo_prediction"]:
            assert k in d

    def test_five_classes(self):
        d = client.post("/predict", files={"file": ("t.jpg", make_img(), "image/jpeg")}, headers=HEADERS).json()
        assert len(d["all_probabilities"]) == 5

    def test_low_res_warning(self):
        d = client.post("/predict", files={"file": ("t.jpg", make_img(size=(100, 100)), "image/jpeg")}, headers=HEADERS).json()
        assert len(d["warnings"]) > 0

    def test_disclaimer(self):
        d = client.post("/predict", files={"file": ("t.jpg", make_img(), "image/jpeg")}, headers=HEADERS).json()
        assert "AI-assisted" in d["disclaimer"]


class TestPredictErrors:
    def test_invalid_image_422(self):
        r = client.post("/predict", files={"file": ("t.txt", b"not image", "text/plain")}, headers=HEADERS)
        assert r.status_code == 422
