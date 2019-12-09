def test_read_health(client):
    response = client.get("/_meta/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
