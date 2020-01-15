import sys
from pathlib import Path

import pytest
from starlette.testclient import TestClient

base_path = Path(__file__).parents[1].joinpath("pymockserver")
sys.path.append(str(base_path))

import mocks_manager  # noqa


@pytest.fixture(scope="session")
def app():
    from main import app

    return app


@pytest.fixture(scope="session")
def client(app):
    """A test client for the app."""
    yield TestClient(app)


@pytest.fixture(scope="function")
def cleanup(app):
    yield
    mocks_manager.mocks = {}
