from flask import Blueprint, render_template, request

from clothing_store.db import get_db

bp = Blueprint("shop", __name__)


@bp.route("/shop")
def index():
    # Get the category_id from the request parameters
    category_id = request.args.get("category", default="All", type=str)

    db = get_db()

    # Get all products if category_id is "All", otherwise get products in the specified category
    products = None
    if category_id != "All":
        products = db.execute(
            "SELECT id, name, price, category_id" " FROM product WHERE category_id = ?",
            (category_id),
        ).fetchall()
    else:
        products = db.execute(
            "SELECT id, name, price, category_id" " FROM product"
        ).fetchall()

    # Get all product categories
    product_categories = db.execute(
        "SELECT id, name" " FROM product_category"
    ).fetchall()

    return render_template(
        "shop/index.html", products=products, product_categories=product_categories
    )


@bp.route("/shop/<int:product_id>")
def product(product_id):
    db = get_db()

    # Get the product with the specified id
    product = db.execute(
        "SELECT id, name, price, description, category_id" " FROM product WHERE id = ?", (str(product_id))
    ).fetchone()

    return render_template("shop/product.html", product=product)
