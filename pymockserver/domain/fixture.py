import json
from pathlib import Path
from typing import Any

import yaml

from pymockserver.domain.request import request_hash
from pymockserver.models.manager import add_mock
from pymockserver.models.type import CreatePayload
from pymockserver.tools.logger import logger

FIXTURES_DIR = Path("/etc/fixtures")


def load_fixtures() -> None:
    if not FIXTURES_DIR.is_dir() or not any(FIXTURES_DIR.iterdir()):
        return

    for fixture_file in FIXTURES_DIR.iterdir():
        if not check_file_extension(fixture_file):
            continue
        load_fixture_file(fixture_file)


def check_file_extension(fixture_file: Path) -> bool:
    if fixture_file.suffix not in [".json", ".yaml"]:
        logger.warning("Wrong fixture file extension. Only json and yaml are handled.")
        return False
    return True


def load_fixture_file(fixture_file: Path) -> None:
    file_ext = fixture_file.suffix
    if file_ext == ".yaml":
        load_yaml_fixture(fixture_file)
    if file_ext == ".json":
        load_json_fixture(fixture_file)


def load_yaml_fixture(fixture_file: Path) -> None:
    with fixture_file.open(encoding="utf8") as file:
        fixtures = yaml.load(file, Loader=yaml.FullLoader)

    add_fixtures(fixtures)


def load_json_fixture(fixture_file: Path) -> None:
    with fixture_file.open(encoding="utf8") as file:
        fixtures = json.load(file)

    add_fixtures(fixtures)


def add_fixtures(fixtures: Any) -> None:
    for fixture in fixtures:
        payload = CreatePayload.model_validate(fixture)
        req_hash = request_hash(payload.httpRequest)

        add_mock(req_hash=req_hash, payload=payload)
