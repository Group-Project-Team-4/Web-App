import pytest

from clothing_store.db import get_db

PRODUCT_ID = 3
USER_ID = 1


def add_item_to_cart(app):
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO cart_item (product_id, user_id, quantity) VALUES (?, ?, ?)",
            (PRODUCT_ID, USER_ID, 1),
        )
        db.commit()


def test_checkout(client, auth, app):
    # test user cannot navigate to checkout when not logged in
    response = client.get("/checkout")
    assert response.status_code == 401

    # test user is redirected to cart page when there are no items in the cart
    auth.login()
    response = client.get("/checkout")
    assert response.status_code == 302
    assert response.headers["Location"] == "/cart"

    # test user can navigate to checkout when logged in and has items in cart
    add_item_to_cart(app)

    response = client.get("/checkout")
    assert response.status_code == 200
    assert b"Checkout" in response.data


# parametrize this test to check each field
@pytest.mark.parametrize(
    ("data", "message"),
    (
        # test checkout responds with error message if request form values are missing
        ({}, b"Email was missing in request."),
        # test checkout responds with error message if a value is blank
        (
            {
                "email": "test@gmail.com",
                "name": "Bob",
                "address": "",
                "country": "usa",
                "credit-card": "1234 1234 1234 1234",
                "expiration-date": "02 / 28",
                "cvc": "123",
            },
            b"Address is required.",
        ),
    ),
)
def test_invalid_checkout(auth, client, data, message):
    # test user cannot checkout with invalid information
    auth.login()
    response = client.post("/checkout", data=data)
    assert response.status_code == 302
    assert message in response.data or b"Redirecting..." in response.data
