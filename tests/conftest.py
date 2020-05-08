import pytest
from mergedeep import merge
from starlette.testclient import TestClient

from pymockserver import database  # noqa


@pytest.fixture(scope="session")
def app():
    from pymockserver.main import app

    return app


@pytest.fixture(scope="session")
def client(app):
    """A test client for the app."""
    yield TestClient(app)


@pytest.fixture(scope="function")
def cleanup(app):
    yield
    database.db.clear()


@pytest.fixture(scope="function")
def base_data(app):
    json_data = {
        "httpRequest": {"method": "GET", "path": "/users",},
        "httpResponse": {"statusCode": 200, "remainingTimes": -1, "delay": 0,},
    }

    def fill_data(data):
        return merge({}, json_data, data)

    return fill_data


@pytest.fixture(scope="function")
def create_mock(client, base_data):
    def add_mock(data):
        mock_data = base_data(data)
        add_response = client.post("/mockserver", json=mock_data)

        assert add_response.status_code == 201
        assert add_response.json() == {"status": "ok"}

        return {
            "data": mock_data,
            "response": add_response,
        }

    return add_mock
