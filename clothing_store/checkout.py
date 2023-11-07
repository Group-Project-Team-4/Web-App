from flask import Blueprint, render_template, g, redirect, url_for, request, flash

from clothing_store.db import get_db

bp = Blueprint("checkout", __name__)


@bp.route("/checkout", methods=("GET", "POST"))
def index():
    # redirect to login page if user is not logged in
    if g.user is None:
        return redirect(url_for("auth.login"), code=401)

    db = get_db()

    if request.method == "POST":
        # dictionary of all input fields where the first element is the name of the field and the second element is the value
        input_fields = {
            "email": None,
            "name": None,
            "address": None,
            "country": None,

            "credit-card": None,
            "expiration-date": None,
            "cvc": None,
        }

        # loop through all input fields and validate they are in the request
        for key, value in input_fields.items():
            try:
                input_fields[key] = request.form[key]

                # check if any fields are empty strings
                if input_fields[key] == "" or not input_fields[key]:
                    error_message = f"{key} is required.".replace("-", " ").capitalize()
                    flash(error_message)
                    return redirect(request.referrer)
            except KeyError:
                error_message = f"{key} was missing in request.".replace("-", " ").capitalize()
                flash(error_message)
                return redirect(request.referrer)

        # TODO: redirect to checkout success page
        return redirect(url_for("checkout.success"))

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

    # check if cart is empty
    if len(cart) == 0:
        return redirect(url_for("cart.index"))

    # calculate total price of all items in the cart
    total_price = 0
    for item in cart:
        total_price += item["price"] * item["quantity"]

    formatted_total_price = "{:.2f}".format(total_price)
    return render_template("checkout/index.html", total_price=formatted_total_price)


@bp.route("/checkout/success")
def success():
    # redirect to login page if user is not logged in
    if g.user is None:
        return redirect(url_for("auth.login"), code=401)

    return render_template("checkout/success.html")
