from pathlib import Path

import pytest
from ruamel.yaml import YAML

import scripts.promote as promote


def write_values(path: Path, frontend_tag: str, backend_tag: str):
    yaml = YAML()

    data = {
        "frontend": {
            "image": {
                "repository": "ghcr.io/example/frontend",
                "tag": frontend_tag,
            }
        },
        "backend": {
            "image": {
                "repository": "ghcr.io/example/backend",
                "tag": backend_tag,
            }
        },
    }

    with path.open("w", encoding="utf-8") as file:
        yaml.dump(data, file)


def test_valid_promotion():
    promote.validate_promotion("dev", "staging")
    promote.validate_promotion("staging", "prod")


def test_invalid_promotion():
    with pytest.raises(promote.PromotionError):
        promote.validate_promotion("dev", "prod")


def test_image_reference():
    yaml = YAML()

    values = yaml.load(
        """
frontend:
  image:
    repository: ghcr.io/example/frontend
    tag: abc123
"""
    )

    repository, tag = promote.get_image_reference(
        values,
        "frontend",
    )

    assert repository == "ghcr.io/example/frontend"
    assert tag == "abc123"


def test_missing_image_tag():
    yaml = YAML()

    values = yaml.load(
        """
frontend:
  image:
    repository: ghcr.io/example/frontend
"""
    )

    with pytest.raises(promote.PromotionError):
        promote.get_image_reference(
            values,
            "frontend",
        )
