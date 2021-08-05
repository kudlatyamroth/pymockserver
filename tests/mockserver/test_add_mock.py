import pytest


@pytest.mark.usefixtures("cleanup")
def test_minimal_request_to_add_mock(client):
    http_request = {
        "path": "/users",
    }
    http_response = {
        "body": {
            "users": ["John Doe", "John Dave"],
        },
    }
    add_response = client.post(
        "/mockserver",
        json={
            "httpRequest": http_request,
            "httpResponse": http_response,
        },
    )

    assert add_response.status_code == 201
    assert add_response.json() == {"status": "ok"}

    mock_response = client.get(http_request.get("path"))
    assert mock_response.status_code == 200
    assert mock_response.json() == http_response.get("body")


@pytest.mark.usefixtures("cleanup")
def test_largest_request_to_add_mock(client):
    http_request = {
        "method": "POST",
        "path": "/users",
        "queryStringParameters": {
            "name": ["John"],
        },
        "headers": {
            "x-header": "secure",
        },
        "body": {
            "users": ["John Doe"],
        },
        "match_body_mode": "partially",
    }
    http_response = {
        "statusCode": 201,
        "headers": {
            "x-user": "John Doe",
        },
        "body": {
            "users": ["John Doe", "John Dave"],
        },
        "remainingTimes": -1,
        "delay": 0,
    }
    add_response = client.post(
        "/mockserver",
        json={
            "httpRequest": http_request,
            "httpResponse": http_response,
        },
    )

    assert add_response.status_code == 201
    assert add_response.json() == {"status": "ok"}

    mock_response = client.post(
        url=http_request.get("path"),
        params={"name": "John"},
        json={"users": ["John Doe"]},
        headers={"x-header": "secure"},
    )
    assert mock_response.status_code == 201
    assert mock_response.json() == http_response.get("body")


@pytest.mark.parametrize(
    "body",
    [
        [
            {
                "users": ["John Doe", "John Dave"],
            }
        ],
        {
            "users": ["John Doe", "John Dave"],
        },
        ["users"],
        "a:300",
        "",
        None,
        True,
        False,
        1,
        0,
        300,
        -300,
    ],
)
@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH"])
@pytest.mark.usefixtures("cleanup")
def test_request_body_could_be_anything(client, body, method):
    methods = [
        "POST",
        "PUT",
        "PATCH",
    ]
    path = "/users"
    http_request = {
        "method": method,
        "path": path,
        "body": body,
    }

    add_response = client.post(
        "/mockserver",
        json={
            "httpRequest": http_request,
            "httpResponse": {},
        },
    )
    assert add_response.status_code == 201
    assert add_response.json() == {"status": "ok"}

    methods.remove(method)
    for fail_method in methods:
        mock_response = client.request(fail_method, url=path, json=body)
        assert mock_response.status_code == 404

    mock_response = client.request(method, url=path, json=body)
    assert mock_response.status_code == 200


@pytest.mark.parametrize(
    "body",
    [
        [
            {
                "users": ["John Doe", "John Dave"],
            }
        ],
        {
            "users": ["John Doe", "John Dave"],
        },
        ["users"],
        "a:300",
        "",
        None,
        True,
        False,
        1,
        0,
        300,
        -300,
    ],
)
@pytest.mark.usefixtures("cleanup")
def test_response_body_could_be_anything(client, body):
    http_request = {
        "path": "/users",
    }
    http_response = {
        "body": body,
    }

    add_response = client.post(
        "/mockserver",
        json={
            "httpRequest": http_request,
            "httpResponse": http_response,
        },
    )
    assert add_response.status_code == 201
    assert add_response.json() == {"status": "ok"}

    mock_response = client.get(http_request.get("path"))
    assert mock_response.status_code == 200
    assert mock_response.json() == body


@pytest.mark.usefixtures("cleanup")
def test_missing_path_not_add_mocks(client):
    http_request = {
        "method": "GET",
    }
    http_response = {
        "body": {
            "users": ["John Doe", "John Dave"],
        },
    }

    add_response = client.post(
        "/mockserver",
        json={
            "httpRequest": http_request,
            "httpResponse": http_response,
        },
    )
    assert add_response.status_code == 422

    get_response = client.get("/mockserver")
    assert get_response.json() == {}


@pytest.mark.usefixtures("cleanup")
def test_wrong_format_of_qs_not_add_mocks(client):
    http_request = {
        "path": "/users",
        "queryStringParameters": {
            "name": "John",
        },
    }
    http_response = {
        "body": {
            "users": ["John Doe", "John Dave"],
        },
    }

    add_response = client.post(
        "/mockserver",
        json={
            "httpRequest": http_request,
            "httpResponse": http_response,
        },
    )
    assert add_response.status_code == 422

    get_response = client.get("/mockserver")
    assert get_response.json() == {}


@pytest.mark.parametrize(
    "status",
    [
        "",
        None,
        "a",
        -100,
        69,
        600,
    ],
)
@pytest.mark.usefixtures("cleanup")
def test_wrong_value_of_status_code(client, status):
    http_request = {
        "path": "/users",
    }
    http_response = {
        "body": "test",
        "statusCode": status,
    }

    add_response = client.post(
        "/mockserver",
        json={
            "httpRequest": http_request,
            "httpResponse": http_response,
        },
    )
    assert add_response.status_code == 422

    get_response = client.get("/mockserver")
    assert get_response.json() == {}


@pytest.mark.parametrize(
    "headers",
    [
        {"x-user": ["test"]},
        {"x-user": {100: 100}},
    ],
)
@pytest.mark.usefixtures("cleanup")
def test_wrong_value_of_response_headers(client, headers):
    http_request = {
        "path": "/users",
    }
    http_response = {
        "body": "test",
        "headers": headers,
    }

    add_response = client.post(
        "/mockserver",
        json={
            "httpRequest": http_request,
            "httpResponse": http_response,
        },
    )
    assert add_response.status_code == 422

    get_response = client.get("/mockserver")
    assert get_response.json() == {}


@pytest.mark.parametrize(
    "times",
    [
        "",
        None,
        "a",
        -100,
    ],
)
@pytest.mark.usefixtures("cleanup")
def test_wrong_value_of_remaining_times(client, times):
    http_request = {
        "path": "/users",
    }
    http_response = {
        "body": "test",
        "remainingTimes": times,
    }

    add_response = client.post(
        "/mockserver",
        json={
            "httpRequest": http_request,
            "httpResponse": http_response,
        },
    )
    assert add_response.status_code == 422

    get_response = client.get("/mockserver")
    assert get_response.json() == {}


@pytest.mark.parametrize(
    "delay",
    [
        "",
        None,
        "a",
        -100,
    ],
)
@pytest.mark.usefixtures("cleanup")
def test_wrong_value_of_response_delay(client, delay):
    http_request = {
        "path": "/users",
    }
    http_response = {
        "body": "test",
        "delay": delay,
    }

    add_response = client.post(
        "/mockserver",
        json={
            "httpRequest": http_request,
            "httpResponse": http_response,
        },
    )
    assert add_response.status_code == 422

    get_response = client.get("/mockserver")
    assert get_response.json() == {}
