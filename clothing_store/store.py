from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from clothing_store.auth import login_required
from clothing_store.db import get_db

bp = Blueprint("blog", __name__)

@bp.route("/")
    def index():
        return "<h1>It works!</h1>\
                The app is running, but this home page is WIP. If you are testing another page, navigate to it manually via the URL."
