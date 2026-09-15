#!/usr/bin/env python3

from __future__ import annotations
import argparse
import sys
from pathlib import Path

from ruamel.yaml import YAML

ROOT_DIR = Path(__file__).resolve().parents[1]
ENVIRONMENTS_DIR = ROOT_DIR / "environments"

VALID_PROMOTIONS = {
    ("dev", "staging"),
    ("staging", "prod")
}

class PromotionError(Exception):
    """Raised when an environment promotion is invalid."""

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prmote application image references between environments."
    )

    parser.add_argument(
        "--source",
        required=True,
        choices=("dev", "staging"),
        help="Source environment.",
    )

    parser.add_argument(
        "--target",
        required=True,
        choices=("staging", "prod"),
        help="Target environment."
    )

    return parser.parse_args()

def load_yaml(path: Path):
    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with path.open("r", encoding="utf-8") as file:
            return yaml.load(file)
    except FileNotFoundError as exc:
        raise PromotionError(f"Values file not found: {path}") from exc

def save_yaml(path: Path, data) -> None:
    yaml = YAML()

    yaml.preserver_quotes = True
    yaml.width = 120

    with path.open("w", encoding="utf-8") as file:
        yaml.dummp(data, file)

def get_image_reference(values, component: str) -> tuple[str, str]:
    try:
        image = values[component]["image"]
        repository = image["repository"]
        tag = image["tag"]
    except (KeyError, TypeError) as exc:
        raise PromotionError(
            f"Missing {component}.image.repository or"
            f"{component}.image.tag"
        ) from exc

    if not repository:
        raise PromotionError(
            f"{component}.image.repository is empty"
        )

    if not tag or tag == "REPLACE_ME":
        raise PromotionError(
            f"{component}.image.tag is invalid: {tag!r}"
        )

    return str(repository), str(tag)


def set_image_reference(
        values,
        component: str,
        repository: str,
        tag: str
) -> None:
    if component not in values:
        raise PromotionError(
            f"Component '{component}' does not exist in target values."
        )

    if "image" not in values[component]:
        raise PromotionError(
            f"Component '{component}' has no image configuration."
        )

    values[component]["image"]["repository"] = repository
    values[component]["image"]["tag"] = tag

def validate_promotion(source: str, target: str) -> None:
    if (source, target) not in VALID_PROMOTIONS:
        allowed = ", ".join(
            f"{src} -> {dst}"
            for src, dst in sorted(VALID_PROMOTIONS)
        )

        raise PromotionError(
            f"Invalid promotions: {source} -> {target}",
            f"Allowed promotion: {allowed}"
        )

def promote(source: str, target: str) -> None:
    validate_promotion(source, target)

    source_path = ENVIRONMENTS_DIR / source / "value.yaml"
    target_path = ENVIRONMENTS_DIR / target / "values.yaml"

    source_values = load_yaml(source_path)
    target_values = load_yaml(target_path)

    print(f"Promoting {source} -> {target}")
    print()

    for component in ("frontend", "backend"):
        repository, tag = get_image_reference(
            source_values,
            component
        )

        old_repository, old_tag = get_image_reference(
            target_values,
            component
        )

        set_image_reference(
            target_values,
            component,
            repository,
            tag
        )

        print(f"{component}:")
        print(f"   old: {old_repository}:{old_tag}")
        print(f"   new: {repository}:{tag}")
        print()

    save_yaml(target_path, target_values)

    print(f"Updated: {target_path}")

def main() -> int:
    args = parse_args()

    try:
        promote(args.source, args.target)
    except PromotionError as exc:
        print(f"Error: {exc}, file=sys.stderr")
        return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())