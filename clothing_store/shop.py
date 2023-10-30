from flask import Blueprint, render_template

from clothing_store.db import get_db

bp = Blueprint("shop", __name__)


@bp.route("/shop")
def index():
    db = get_db()
    products = db.execute(
        "SELECT id, name, price, category_id" " FROM product"
    ).fetchall()

    product_categories = db.execute(
        "SELECT id, name" " FROM product_category"
    ).fetchall()

    return render_template(
        "shop/index.html", products=products, product_categories=product_categories
    )
