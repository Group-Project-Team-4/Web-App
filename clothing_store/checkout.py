from flask import Blueprint, render_template

bp = Blueprint("checkout", __name__)

@bp.route("/checkout")
def index():
    return render_template("checkout.html")
