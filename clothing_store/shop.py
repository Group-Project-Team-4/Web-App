from flask import Blueprint, render_template

bp = Blueprint("shop", __name__)

@bp.route("/shop")
def index():
    return render_template("shop/index.html")
