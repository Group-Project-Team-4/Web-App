from flask import Blueprint, render_template, g, redirect, url_for

from clothing_store.db import get_db

bp = Blueprint("cart", __name__)


@bp.route("/cart")
def index():
    # redirect to login page if user is not logged in
    if g.user is None:
        return redirect(url_for("auth.login"), code=401)

    db = get_db()

    # get all items in the cart for the current user
    cart = db.execute(
        """
        SELECT cart_item.id, product_id, user_id, quantity, name, price
        FROM cart_item
        JOIN product ON product_id = product.id
        WHERE user_id = ?
        """,
        (str(g.user["id"])),
    ).fetchall()

    # calculate total price of all items in the cart
    total_price = 0
    for item in cart:
        total_price += item["price"] * item["quantity"]

    # render the cart page
    formatted_total_price = "{:.2f}".format(total_price)
    return render_template("cart.html", cart=cart, total_price=formatted_total_price)
