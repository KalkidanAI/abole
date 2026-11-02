"""Tests for the disease information service."""
import pytest
from app.services.disease_info import disease_info_service
from app.core.exceptions import DiseaseInfoNotFoundError


class TestDiseaseInfo:
    def test_all_five_classes_present(self):
        disease_info_service.load()
        classes = disease_info_service.available_classes
        assert "Cercospora" in classes
        assert "Healthy" in classes
        assert "Leaf Rust" in classes
        assert "Miner" in classes
        assert "Phoma" in classes
        assert len(classes) == 5

    def test_cercospora_fields(self):
        info = disease_info_service.get_info("Cercospora")
        assert info.name == "Cercospora"
        assert info.scientific_name != ""
        assert len(info.symptoms) > 0
        assert len(info.management_practices) > 0
        assert len(info.citations) > 0

    def test_leaf_rust_fields(self):
        info = disease_info_service.get_info("Leaf Rust")
        assert info.scientific_name == "Hemileia vastatrix"

    def test_ethiopian_context_present(self):
        for cls in disease_info_service.available_classes:
            assert disease_info_service.get_info(cls).ethiopian_context is not None

    def test_disclaimer_present(self):
        d = disease_info_service.get_disclaimer()
        assert "AI-assisted" in d

    def test_unknown_class_raises(self):
        with pytest.raises(DiseaseInfoNotFoundError):
            disease_info_service.get_info("UnknownDisease")
