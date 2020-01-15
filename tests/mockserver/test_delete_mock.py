import pytest


@pytest.mark.usefixtures("cleanup")
def test_should_delete_only_one_mock(client, create_mock):
    first_path = "/users"
    second_path = "/users2"

    create_mock(
        {"httpRequest": {"path": first_path,},}
    )
    mock = create_mock({"httpRequest": {"path": second_path,},})

    del_response = client.delete("/mockserver", json=mock.get("data").get("httpRequest"))
    assert del_response.status_code == 200

    mock_response = client.get(first_path)
    assert mock_response.status_code == 200

    mock_response = client.get(second_path)
    assert mock_response.status_code == 404


@pytest.mark.usefixtures("cleanup")
def test_should_not_delete_anything(client, create_mock):
    first_path = "/users"
    second_path = "/users2"

    mock = create_mock({"httpRequest": {"path": first_path,},})

    mock["data"]["httpRequest"]["path"] = second_path
    del_response = client.delete("/mockserver", json=mock.get("data").get("httpRequest"))
    assert del_response.status_code == 200

    mock_response = client.get(first_path)
    assert mock_response.status_code == 200


@pytest.mark.usefixtures("cleanup")
def test_should_delete_everything(client, create_mock):
    first_path = "/users"
    second_path = "/users2"

    create_mock(
        {"httpRequest": {"path": first_path,},}
    )
    create_mock(
        {"httpRequest": {"path": second_path,},}
    )

    purge_response = client.delete("/mockserver/reset")
    assert purge_response.status_code == 200

    mock_response = client.get(first_path)
    assert mock_response.status_code == 404

    mock_response = client.get(second_path)
    assert mock_response.status_code == 404

    get_response = client.get("/mockserver")
    assert get_response.json() == {}
