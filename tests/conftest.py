import sys
from pathlib import Path

import pytest
from starlette.testclient import TestClient


base_path = Path(__file__).parents[1].joinpath("src")
sys.path.append(str(base_path))


@pytest.fixture(scope="session")
def app():
    from main import app

    return app


@pytest.fixture(scope="session")
def client(app):
    """A test client for the app."""
    yield TestClient(app)
