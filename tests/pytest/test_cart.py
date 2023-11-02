
def test_cart(client, app):
    # test cart page responds with 401 if user is not logged in
    response = client.get("/cart")
    assert response.status_code == 401
