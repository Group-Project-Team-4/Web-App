import pytest

from clothing_store.db import get_db


def test_cart(client, app, auth):
    # test cart page responds with 401 if user is not logged in
    assert client.get("/cart").status_code == 401

    # test cart page responds with 200 if user is logged in
    auth.login()
    assert client.get("/cart").status_code == 200


# id of product being tested
PRODUCT_ID = 3
USER_ID = 1

def test_add_to_cart(client, app, auth):
    # test add to cart responds with 401 if user is not logged in
    assert client.post("/cart").status_code == 401

    # # test add to cart responds with 302 and redirects to cart page if user is logged in
    auth.login()
    response = client.post("/cart", data={"product_id": PRODUCT_ID, "quantity": 1})
    print(response)
    assert response.status_code == 302
    assert response.headers["Location"] == "/cart"

    # test add to cart adds item to cart_item table
    with app.app_context():
        assert (
            get_db()
            .execute(
                f"SELECT * FROM cart_item WHERE user_id = '{USER_ID}' AND product_id = '{PRODUCT_ID}'",
            )
            .fetchone()
            is not None
        )

    # # test add to cart increases quantity if product is already in cart
    response = client.post("/cart", data={"product_id": PRODUCT_ID, "quantity": 1})
    assert response.status_code == 302
    assert response.headers["Location"] == "/cart"
    with app.app_context():
        assert (
            get_db()
            .execute(
                f"SELECT * FROM cart_item WHERE user_id = '{USER_ID}' AND product_id = '{PRODUCT_ID}'",
            )
            .fetchone()["quantity"]
            == 2
        )

    # test cart quantity doesn't exceed quantity in stock when adding to cart
    auth.login()
    response = client.post("/cart", data={"product_id": PRODUCT_ID, "quantity": 100})
    assert response.status_code == 302
    with app.app_context():
        assert (
            get_db()
            .execute(
                f"SELECT * FROM cart_item WHERE user_id = '{USER_ID}' AND product_id = '{PRODUCT_ID}'",
            )
            .fetchone()["quantity"]
            == 2
        )


# tests invalid input for add to cart
@pytest.mark.parametrize(
    ("data", "message"),
    (
        # test add to cart responds with error message if product_id is not provided
        ({"quantity": 1}, b"Product ID is required."),
        # test add to cart responds with error message if quantity is not provided
        ({"product_id": PRODUCT_ID}, b"Quantity is required."),
        # test add to cart responds with 404 if product does not exist
        ({"product_id": 100, "quantity": 1}, b"Product does not exist."),
    ),
)
def test_add_to_cart_validate_input(client, auth, data, message):
    auth.login()
    response = client.post("/cart", data=data)
    assert response.status_code == 400
    assert message in response.data
