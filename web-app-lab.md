# Web Application Tests Lab

## Introduction
This lab tests the web application through Flasks test client, it will simulate requests to the application and return response data.

It will also be using `pytest` and `coverage` to test code and measure coverage.

## Set up
Follow the installation instructions in the [Web App readme](https://github.com/Group-Project-Team-4/Web-App#installation). This includes:
- Creating and activating the virtual environment
- Installing required libraries:
```shell
pip3 install -r requirements.txt
```
- Installing the clothing store application:
```shell
pip install -e .
```

## Running the tests
To run all tests together and view the results run the following command:

```shell
pytest tests/pytest
```


## Tutorial
This tutorial will go through the basics of creating tests by replicating the `test_checkout.py` file.

To start, create a file named `test_tutorial.py` in the `tests/pytest/` directory and open it in your text editor.

### Imports
First `pytest` needs to be imported for later use. Then, to interact with the applications database, `clothing_store.db` needs to be imported.

```python
import pytest
from clothing_store.db import get_db
```


### Adding an item to cart
In order to access the checkout page the user needs to have a product in the cart.

First, some constants need to be defined for adding a product to a users cart. Then define a function to insert an item into the `cart_item` table in the database.

```python
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
```

This `add_item_to_cart` function uses a `pytest` fixture called `app`, which is a setup function that each function in `pytest` can use. To see all the fixtures see the `tests/pytest/conftest.py` file and to learn more about fixtures see the `pytest` [documentation](https://docs.pytest.org/en/6.2.x/fixture.html).

### Test navigating to checkout
The important things to test on the checkout page are:
1. The user *can not* navigate to checkout when they are not logged in
2. The user *can not* navigate to checkout when there are no items in the cart
3. The user *can* navigate to checkout when they are both logged in and there is one or more items in the cart

The way to achieve these requirements in code is as follows:

```python
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
```

Each of these sections tests a response status code correlating to the outcome that is expected. For example, an unauthenticated request should result in a status code of `401 Unauthorized`. For more information on HTTP response status codes see the [MDN documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).

### Test invalid checkout
Often, testing invalid inputs can be tedious because many inputs need to be tested. To solve this `pytest` provides a way to parameterize the tests. This means one function can be written and it will be passed a series of parameters defined above the function.

```python
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
```

In this code we first use pytests `@pytest.mark.parametrize` decorator to pass in a series of arguments to the `test_invalid_checkout` test. 

The first argument in the decorator is a tuple with the name of the arguments we want to pass to the test. In this case, `data` and `message` are the names, `data` will used as the body of the `POST` request and `message` is the message that is expected from the response.

The next argument is a tuple of tuples containing the values of each argument when running the test. 

The `test_invalid_checkout` test will run twice. First it will run with a blank body which should result in a "Email was missing in request." message. Next, it will run with a blank address which should result in a "Address is required." message.

To learn more about parameterizing see the [pytest documentation](https://docs.pytest.org/en/7.1.x/how-to/parametrize.html).

### Running the test
Finally, to test the file you created run the following command:

```shell
pytest tests/pytest/test_tutorial.py
```
