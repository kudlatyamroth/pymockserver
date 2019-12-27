def test_add_mock(client):
    http_request = {
        "method": "GET",
        "path": "/users",
        "queryStringParameters": {"name": ["John"],},
    }
    http_response = {
        "statusCode": 200,
        "headers": {"x-user": "John Doe",},
        "body": {"users": ["John Doe", "John Dave"],},
        "remainingTimes": -1,
        "delay": 0,
    }
    add_response = client.post("/mockserver", json={"httpRequest": http_request, "httpResponse": http_response,})

    assert add_response.status_code == 201
    assert add_response.json() == {"status": "ok"}

    get_response = client.get(http_request.get("path"))
    assert get_response.status_code == 404

    mock_response = client.get(http_request.get("path"), params={"name": "John"})
    assert mock_response.status_code == 200
    assert mock_response.json() == http_response.get("body")
