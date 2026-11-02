"""Disease information retrieval service."""
import json
import logging
from pathlib import Path
from typing import Dict, List

from app.config import settings
from app.core.exceptions import DiseaseInfoNotFoundError
from app.schemas.prediction import DiseaseInfo

logger = logging.getLogger(__name__)


class DiseaseInfoService:
    def __init__(self):
        self.data: Dict = {}
        self.disclaimer: str = ""
        self._loaded = False

    def load(self) -> None:
        info_path = Path(settings.DISEASE_INFO_PATH)
        if info_path.exists():
            with open(info_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            self.disclaimer = self.data.get(
                "disclaimer",
                "This is AI-assisted analysis, not a confirmed diagnosis. Consult a qualified agronomist.",
            )
            self._loaded = True
            logger.info(f"Disease info loaded from {info_path}")
        else:
            logger.warning(f"Disease info file not found at {info_path}")
            self.disclaimer = "This is AI-assisted analysis, not a confirmed diagnosis. Consult a qualified agronomist."

    def get_info(self, class_name: str) -> DiseaseInfo:
        if not self._loaded:
            self.load()

        classes = self.data.get("classes", {})
        info = classes.get(class_name)

        if info is None:
            raise DiseaseInfoNotFoundError(f"Disease information not found for class: {class_name}")

        return DiseaseInfo(
            name=info["name"],
            scientific_name=info["scientific_name"],
            description=info["description"],
            symptoms=info["symptoms"],
            management_practices=info["management_practices"],
            ethiopian_context=info.get("ethiopian_context"),
            citations=info["citations"],
        )

    def get_disclaimer(self) -> str:
        if not self._loaded:
            self.load()
        return self.disclaimer

    @property
    def available_classes(self) -> List[str]:
        if not self._loaded:
            self.load()
        return list(self.data.get("classes", {}).keys())


disease_info_service = DiseaseInfoService()
