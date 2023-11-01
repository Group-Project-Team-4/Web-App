from clothing_store.db import get_db


def test_shop(client, app):
    response = client.get("/shop/1")
    assert response.status_code == 200

    assert b"T-Shirt" in response.data
    assert b"A comfortable shirt." in response.data
    assert b"19.99" in response.data
