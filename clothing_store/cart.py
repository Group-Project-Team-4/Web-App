from flask import (
    Blueprint,
    render_template,
    g,
    redirect,
    url_for,
    request,
    flash,
    abort,
)

from clothing_store.db import get_db

bp = Blueprint("cart", __name__)


def select_product(product_id):
    db = get_db()
    product = db.execute(
        "SELECT id, name, price, quantity FROM product WHERE id = ?", (
            product_id,)
    ).fetchone()
    return product


@bp.route("/cart", methods=("GET", "POST"))
def index():
    # redirect to login page if user is not logged in
    if g.user is None:
        return redirect(url_for("auth.login"), code=401)

    db = get_db()

    # get all items in the cart for the current user
    cart = db.execute(
        """
        SELECT cart_item.id, product_id, user_id, cart_item.quantity, name, price
        FROM cart_item
        JOIN product ON product_id = product.id
        WHERE user_id = ?
        """,
        (str(g.user["id"])),
    ).fetchall()

    # post method for adding items to cart
    if request.method == "POST":
        product_id = None
        quantity = None

        # validate product_id and quantity are provided in request
        try:
            product_id = request.form["product_id"]
        except KeyError:
            abort(400, "Product ID is required.")

        try:
            quantity = request.form["quantity"]
        except KeyError:
            abort(400, "Quantity is required.")

        # validate product_id (check if product_id exists in database)
        product = select_product(product_id)

        if product is None:
            abort(400, "Product does not exist.")

        # check if item already exists in cart
        is_in_cart = False
        cart_item_quantity = 0
        for item in cart:
            if item["product_id"] == int(product_id):
                is_in_cart = True
                cart_item_quantity = item["quantity"]
                break

        # if product quantity is exceeded, flash error and redirect to previous page
        if product["quantity"] < cart_item_quantity + 1:
            flash("Product quantity exceeded.")
            return redirect(request.referrer)

        if is_in_cart:
            # update quantity of item in cart
            db.execute(
                "UPDATE cart_item SET quantity = quantity + 1 WHERE product_id = ? AND user_id = ?",
                (product_id, str(g.user["id"])),
            )
            db.commit()
        else:
            # add item to cart if it does not exist
            db.execute(
                "INSERT INTO cart_item (product_id, user_id, quantity) VALUES (?, ?, ?)",
                (product_id, str(g.user["id"]), quantity),
            )
            db.commit()

        return redirect(url_for("cart.index"), code=302)

    # calculate total price of all items in the cart
    total_price = 0
    for item in cart:
        total_price += item["price"] * item["quantity"]

    # render the cart page
    formatted_total_price = "{:.2f}".format(total_price)
    return render_template("cart.html", cart=cart, total_price=formatted_total_price)
