"""Routes module for Flask Weather App"""

from flask import render_template


def register_routes(app):
    """Register routes with the Flask app"""

    @app.route("/")
    def index():
        """Home page"""
        return "這是首頁"

    @app.route("/search")
    def search_page():
        """Search page"""
        return "這是搜尋頁面"
