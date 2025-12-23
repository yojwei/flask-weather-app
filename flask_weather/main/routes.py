from flask import render_template
from . import main_bp


@main_bp.route("/")
def index():
    """Home page"""
    return render_template("index.html")
