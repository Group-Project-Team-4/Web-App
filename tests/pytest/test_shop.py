from clothing_store.db import get_db


def test_shop(client, app):
    response = client.get("/shop")
    assert response.status_code == 200

    with app.app_context():
        assert (
            get_db()
            .execute(
                "SELECT * FROM product",
            )
            .fetchone()
            is not None
        )
