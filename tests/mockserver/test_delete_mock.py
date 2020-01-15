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
