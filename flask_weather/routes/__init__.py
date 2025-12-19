"""Routes module for Flask Weather App"""

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Home page"""
    return render_template("base.html", title="天氣應用")


@main_bp.route("/api/weather")
def get_weather():
    """Get weather data (API endpoint)"""
    return {"status": "ok", "message": "天氣 API 端點"}
