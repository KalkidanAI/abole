"""ONNX inference service for coffee leaf disease detection."""
import json
import logging
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

from app.config import settings

logger = logging.getLogger(__name__)

DEFAULT_CLASS_NAMES = ["Cercospora", "Healthy", "Leaf Rust", "Miner", "Phoma"]


def softmax(logits: np.ndarray, axis: int = -1) -> np.ndarray:
    shifted = logits - np.max(logits, axis=axis, keepdims=True)
    exp_vals = np.exp(shifted)
    return exp_vals / np.sum(exp_vals, axis=axis, keepdims=True)


class InferenceService:
    def __init__(self):
        self.session = None
        self.input_name = "input"
        self.output_name = "output"
        self.class_names: List[str] = DEFAULT_CLASS_NAMES
        self.model_loaded = False
        self.is_demo = False

    def load_model(self) -> None:
        model_path = Path(settings.MODEL_PATH)

        if model_path.exists():
            try:
                import onnxruntime as ort

                self.session = ort.InferenceSession(
                    str(model_path), providers=["CPUExecutionProvider"]
                )
                self.input_name = self.session.get_inputs()[0].name
                self.output_name = self.session.get_outputs()[0].name
                self.model_loaded = True
                self.is_demo = False
                logger.info(f"ONNX model loaded from {model_path}")

                label_path = Path(settings.LABEL_MAPPING_PATH)
                if label_path.exists():
                    with open(label_path) as f:
                        mapping = json.load(f)
                    self.class_names = [mapping[str(i)] for i in range(len(mapping))]
                    logger.info(f"Loaded label mapping: {self.class_names}")
                return
            except Exception as e:
                logger.warning(f"Failed to load ONNX model: {e}. Falling back to demo mode.")

        if settings.DEMO_MODE:
            self.model_loaded = False
            self.is_demo = True
            logger.warning("Running in DEMO MODE - no ONNX model found. Predictions will be placeholder.")
        else:
            from app.core.exceptions import ModelNotAvailableError
            raise ModelNotAvailableError(
                "No ONNX model found and demo mode is disabled. "
                "Place the trained model at: " + str(model_path)
            )

    def predict(self, input_array: np.ndarray) -> Tuple[str, float, List[Tuple[str, float]], bool]:
        if self.model_loaded and self.session is not None:
            outputs = self.session.run([self.output_name], {self.input_name: input_array})
            logits = outputs[0]
            probs = softmax(logits, axis=-1)[0]
        else:
            np.random.seed(int(np.sum(input_array) * 1000) % (2**32))
            logits = np.random.randn(len(self.class_names)).astype(np.float32) * 2
            probs = softmax(logits)[0]

        sorted_indices = np.argsort(probs)[::-1]
        all_probs = [(self.class_names[i], float(probs[i])) for i in sorted_indices]
        predicted_class = self.class_names[sorted_indices[0]]
        confidence = float(probs[sorted_indices[0]])

        return predicted_class, confidence, all_probs, self.is_demo


inference_service = InferenceService()
