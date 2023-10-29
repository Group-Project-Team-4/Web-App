from flask import Blueprint

bp = Blueprint("shop", __name__)

@bp.route("/shop")
def index():
    return "<h1>Shop Page</h1>"
