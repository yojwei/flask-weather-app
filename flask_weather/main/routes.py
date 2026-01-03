from flask import render_template, session, flash, redirect, request, url_for
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


@main_bp.route("/set_units/<unit>")
def set_units(unit):
    if unit in ["metric", "imperial"]:
        session["units"] = unit
        flash(f"已切換至 {'攝氏 (°C)' if unit == 'metric' else '華氏 (°F)'}", "success")
    return redirect(request.referrer or url_for("main.index"))
