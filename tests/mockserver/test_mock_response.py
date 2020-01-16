import timeit

import pytest


@pytest.mark.parametrize("status", [101, 203, 301, 400, 505,])
@pytest.mark.usefixtures("cleanup")
def test_should_response_with_given_status_code(client, create_mock, status):
    path = "/users"

    create_mock(
        {"httpRequest": {"path": path,}, "httpResponse": {"statusCode": status,},}
    )

    mock_response = client.get(path)
    assert mock_response.status_code == status


@pytest.mark.usefixtures("cleanup")
def test_should_response_with_given_headers(client, create_mock):
    path = "/users"

    create_mock(
        {"httpRequest": {"path": path,}, "httpResponse": {"headers": {"x-status": "100"},},}
    )

    mock_response = client.get(path)
    assert mock_response.headers.get("x-status") == "100"


@pytest.mark.usefixtures("cleanup")
def test_should_response_only_given_times(client, create_mock):
    path = "/users"

    create_mock(
        {"httpRequest": {"path": path,}, "httpResponse": {"remainingTimes": 1,},}
    )

    mock_response = client.get(path)
    assert mock_response.status_code == 200

    mock_response = client.get(path)
    assert mock_response.status_code == 404


@pytest.mark.usefixtures("cleanup")
def test_should_response_with_first_mock_and_then_next(client, create_mock):
    path = "/users"

    create_mock(
        {"httpRequest": {"path": path,}, "httpResponse": {"remainingTimes": 1, "body": "John"},}
    )
    create_mock(
        {"httpRequest": {"path": path,}, "httpResponse": {"remainingTimes": 1, "body": "Jane"},}
    )

    mock_response = client.get(path)
    assert mock_response.status_code == 200
    assert mock_response.json() == "John"

    mock_response = client.get(path)
    assert mock_response.status_code == 200
    assert mock_response.json() == "Jane"

    mock_response = client.get(path)
    assert mock_response.status_code == 404


@pytest.mark.usefixtures("cleanup")
def test_should_delay_response(client, create_mock):
    path = "/users"

    create_mock(
        {"httpRequest": {"path": path,}, "httpResponse": {"delay": 500,},}
    )

    def get_response():
        mock_response = client.get(path)
        assert mock_response.status_code == 200

    exec_time = timeit.timeit(get_response, number=1) * 1000
    assert exec_time >= 500


@pytest.mark.parametrize("method", ["POST", "GET", "PUT", "PATCH", "DELETE",])
@pytest.mark.usefixtures("cleanup")
def test_should_response_only_on_mocked_method(client, create_mock, method):
    methods = [
        "POST",
        "GET",
        "PUT",
        "PATCH",
        "DELETE",
    ]
    path = "/users"

    create_mock(
        {"httpRequest": {"method": method, "path": path,},}
    )

    methods.remove(method)
    for fail_method in methods:
        mock_response = client.request(fail_method, url=path)
        assert mock_response.status_code == 404

    mock_response = client.request(method, url=path)
    assert mock_response.status_code == 200
