import json
from pathlib import Path

import yaml

from pymockserver.logger import logger
from pymockserver.managers import set_mocks
from pymockserver.models import MockedData
from pymockserver.utils import request_hash

FIXTURES_DIR = Path("/etc/fixtures")


def load_fixtures():
    if not FIXTURES_DIR.is_dir() or not any(FIXTURES_DIR.iterdir()):
        return

    for fixture_file in FIXTURES_DIR.iterdir():
        if not check_file_extension(fixture_file):
            continue
        load_fixture_file(fixture_file)


def check_file_extension(fixture_file: Path) -> bool:
    if fixture_file.suffix not in [".json", ".yaml"]:
        logger.warn("Wrong fixture file extension. Only json and yaml are handled.")
        return False
    return True


def load_fixture_file(fixture_file: Path):
    file_ext = fixture_file.suffix
    if file_ext == ".yaml":
        load_yaml_fixture(fixture_file)
    if file_ext == ".json":
        load_json_fixture(fixture_file)


def load_yaml_fixture(fixture_file: Path):
    with fixture_file.open(encoding="utf8") as file:
        fixtures = yaml.load(file, Loader=yaml.FullLoader)

    add_fixtures(fixtures)


def load_json_fixture(fixture_file: Path):
    with fixture_file.open(encoding="utf8") as file:
        fixtures = json.load(file)

    add_fixtures(fixtures)


def add_fixtures(fixtures):
    for fixture in fixtures:
        payload = MockedData.parse_obj(fixture)
        req_hash = request_hash(payload.httpRequest)

        set_mocks(req_hash, payload)
