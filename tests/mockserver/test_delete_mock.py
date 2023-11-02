import pytest


@pytest.mark.usefixtures("cleanup")
def test_should_delete_only_one_mock(client, create_mock):
    first_path = "/users"
    second_path = "/users2"

    create_mock(
        {
            "httpRequest": {
                "path": first_path,
            },
        }
    )
    mock = create_mock(
        {
            "httpRequest": {
                "path": second_path,
            },
        }
    )

    del_response = client.request("DELETE", "/mockserver", json=mock.get("data").get("httpRequest"))
    assert del_response.status_code == 200

    mock_response = client.get(first_path)
    assert mock_response.status_code == 200

    mock_response = client.get(second_path)
    assert mock_response.status_code == 404


@pytest.mark.usefixtures("cleanup")
def test_should_delete_only_mock_without_qs(client, create_mock):
    path = "/users"
    query_params = {"name": ["John"]}

    create_mock(
        {
            "httpRequest": {
                "path": path,
                "queryStringParameters": query_params,
            },
        }
    )
    mock = create_mock(
        {
            "httpRequest": {
                "path": path,
            },
        }
    )

    del_response = client.request("DELETE", "/mockserver", json=mock.get("data").get("httpRequest"))
    assert del_response.status_code == 200

    mock_response = client.get(path, params=query_params)
    assert mock_response.status_code == 200

    mock_response = client.get(path)
    assert mock_response.status_code == 404


@pytest.mark.usefixtures("cleanup")
def test_should_delete_only_mock_with_qs(client, create_mock):
    path = "/users"
    query_params = {"name": ["John"]}

    mock = create_mock(
        {
            "httpRequest": {
                "path": path,
                "queryStringParameters": query_params,
            },
        }
    )
    create_mock(
        {
            "httpRequest": {
                "path": path,
            },
        }
    )

    del_response = client.request("DELETE", "/mockserver", json=mock.get("data").get("httpRequest"))
    assert del_response.status_code == 200

    mock_response = client.get(path)
    assert mock_response.status_code == 200

    mock_response = client.get(path, params=query_params)
    assert mock_response.status_code == 404


@pytest.mark.usefixtures("cleanup")
def test_should_delete_only_mock_with_get_method(client, create_mock):
    path = "/users"

    create_mock(
        {
            "httpRequest": {
                "path": path,
                "method": "POST",
            },
        }
    )
    create_mock(
        {
            "httpRequest": {
                "path": path,
                "method": "PATCH",
            },
        }
    )
    create_mock(
        {
            "httpRequest": {
                "path": path,
                "method": "PUT",
            },
        }
    )
    mock = create_mock(
        {
            "httpRequest": {
                "path": path,
            },
        }
    )

    del_response = client.request("DELETE", "/mockserver", json=mock.get("data").get("httpRequest"))
    assert del_response.status_code == 200

    mock_response = client.post(path)
    assert mock_response.status_code == 200

    mock_response = client.patch(path)
    assert mock_response.status_code == 200

    mock_response = client.put(path)
    assert mock_response.status_code == 200

    mock_response = client.get(path)
    assert mock_response.status_code == 404


@pytest.mark.usefixtures("cleanup")
def test_should_not_delete_anything(client, create_mock):
    first_path = "/users"
    second_path = "/users2"

    mock = create_mock(
        {
            "httpRequest": {
                "path": first_path,
            },
        }
    )

    mock["data"]["httpRequest"]["path"] = second_path
    del_response = client.request("DELETE", "/mockserver", json=mock.get("data").get("httpRequest"))
    assert del_response.status_code == 200

    mock_response = client.get(first_path)
    assert mock_response.status_code == 200


@pytest.mark.usefixtures("cleanup")
def test_should_delete_everything(client, create_mock):
    first_path = "/users"
    second_path = "/users2"

    create_mock(
        {
            "httpRequest": {
                "path": first_path,
            },
        }
    )
    create_mock(
        {
            "httpRequest": {
                "path": second_path,
            },
        }
    )

    purge_response = client.request("DELETE", "/mockserver/reset")
    assert purge_response.status_code == 200

    mock_response = client.get(first_path)
    assert mock_response.status_code == 404

    mock_response = client.get(second_path)
    assert mock_response.status_code == 404

    get_response = client.get("/mockserver")
    assert get_response.json() == {}
