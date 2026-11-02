"""Tests for the ONNX inference service."""
import numpy as np
import pytest
from app.services.inference import inference_service, softmax


class TestSoftmax:
    def test_softmax_sums_to_one(self):
        result = softmax(np.array([[1.0, 2.0, 3.0, 4.0, 5.0]]))
        assert np.isclose(result.sum(), 1.0)

    def test_softmax_shape_preserved(self):
        result = softmax(np.random.randn(10, 5))
        assert result.shape == (10, 5)
        assert np.allclose(result.sum(axis=-1), 1.0)


class TestInferenceService:
    def test_predict_output_shape(self):
        _, _, all_probs, _ = inference_service.predict(np.random.randn(1, 3, 224, 224).astype(np.float32))
        assert len(all_probs) == 5

    def test_confidence_range(self):
        _, confidence, _, _ = inference_service.predict(np.random.randn(1, 3, 224, 224).astype(np.float32))
        assert 0.0 <= confidence <= 1.0

    def test_probabilities_sum_to_one(self):
        _, _, all_probs, _ = inference_service.predict(np.random.randn(1, 3, 224, 224).astype(np.float32))
        assert np.isclose(sum(p for _, p in all_probs), 1.0, atol=1e-5)

    def test_predicted_class_is_valid(self):
        valid = {"Cercospora", "Healthy", "Leaf Rust", "Miner", "Phoma"}
        cls, _, _, _ = inference_service.predict(np.random.randn(1, 3, 224, 224).astype(np.float32))
        assert cls in valid

    def test_probabilities_sorted(self):
        _, _, all_probs, _ = inference_service.predict(np.random.randn(1, 3, 224, 224).astype(np.float32))
        probs = [p for _, p in all_probs]
        assert probs == sorted(probs, reverse=True)

    def test_demo_mode_deterministic(self):
        arr = np.ones((1, 3, 224, 224), dtype=np.float32) * 0.5
        _, _, p1, _ = inference_service.predict(arr)
        _, _, p2, _ = inference_service.predict(arr)
        assert pytest.approx([p for _, p in p1], rel=1e-4) == [p for _, p in p2]
