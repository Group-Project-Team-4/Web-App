from flask import Blueprint

bp = Blueprint("cart", __name__)

@bp.route("/cart")
def index():
    return "<h1>Cart Page</h1>"
