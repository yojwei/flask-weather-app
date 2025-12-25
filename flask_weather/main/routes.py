from flask import render_template
from flask_weather.weather.forms import SearchForm
from . import main_bp


@main_bp.route("/")
def index():
    """Home page"""
    form = SearchForm()
    return render_template("index.html", form=form)


@main_bp.route("/api/weather", methods=["GET"])
def weather_api_root():
    """天氣 API 端點"""
    return {"status": "ok", "message": "天氣 API 端點"}
